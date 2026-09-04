/**
 * South Africa SDR — first-party cookie consent manager
 * POPIA / GDPR / UK PECR compliant: opt-in, reject-all, granular controls.
 * Basic Google Consent Mode v2 — no third-party tags until consent granted.
 */
(function () {
  "use strict";

  var CFG = window.__SA_SDR_CONSENT__ || {};
  var STORAGE_KEY = CFG.storageKey || "sa_sdr_consent";
  var COOKIE_NAME = CFG.cookieName || "sa_sdr_consent";
  var COOKIE_MAX_AGE = (CFG.cookieMaxAgeDays || 395) * 86400;
  var CONSENT_VERSION = CFG.consentVersion || 1;

  var hasAnalyticsConfig = Boolean(CFG.gtmId || CFG.ga4Id);
  var hasMarketingConfig = Boolean(CFG.metaPixelId || CFG.linkedinPartnerId);

  function readCookie(name) {
    var match = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
    return match ? decodeURIComponent(match[1]) : null;
  }

  function writeCookie(name, value, maxAge) {
    var secure = location.protocol === "https:" ? "; Secure" : "";
    document.cookie =
      name +
      "=" +
      encodeURIComponent(value) +
      "; Path=/; Max-Age=" +
      maxAge +
      "; SameSite=Lax" +
      secure;
  }

  function loadStoredConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY) || readCookie(COOKIE_NAME);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (parsed.version !== CONSENT_VERSION) return null;
      return parsed;
    } catch (e) {
      return null;
    }
  }

  function saveConsent(consent) {
    var payload = {
      version: CONSENT_VERSION,
      essential: true,
      analytics: Boolean(consent.analytics),
      marketing: Boolean(consent.marketing),
      timestamp: new Date().toISOString(),
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch (e) {
      /* localStorage blocked */
    }
    writeCookie(COOKIE_NAME, JSON.stringify(payload), COOKIE_MAX_AGE);
    return payload;
  }

  function ensureGtagStub() {
    window.dataLayer = window.dataLayer || [];
    if (!window.gtag) {
      window.gtag = function () {
        window.dataLayer.push(arguments);
      };
    }
  }

  function setConsentMode(consent) {
    ensureGtagStub();
    window.gtag("consent", "update", {
      analytics_storage: consent.analytics ? "granted" : "denied",
      ad_storage: consent.marketing ? "granted" : "denied",
      ad_user_data: consent.marketing ? "granted" : "denied",
      ad_personalization: consent.marketing ? "granted" : "denied",
    });
  }

  function loadGtm(gtmId) {
    if (!gtmId || document.getElementById("sa-sdr-gtm")) return;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
    var script = document.createElement("script");
    script.id = "sa-sdr-gtm";
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(gtmId);
    document.head.appendChild(script);
  }

  function loadMetaPixel(pixelId) {
    if (!pixelId || window.fbq) return;
    var n = (window.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    });
    if (!window._fbq) window._fbq = n;
    n.push = n;
    n.loaded = true;
    n.version = "2.0";
    n.queue = [];
    var script = document.createElement("script");
    script.async = true;
    script.src = "https://connect.facebook.net/en_US/fbevents.js";
    document.head.appendChild(script);
    window.fbq("init", pixelId);
    window.fbq("track", "PageView");
  }

  function loadLinkedIn(partnerId) {
    if (!partnerId || window._linkedin_data_partner_ids) return;
    window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
    window._linkedin_data_partner_ids.push(partnerId);
    var script = document.createElement("script");
    script.async = true;
    script.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
    document.head.appendChild(script);
  }

  function applyConsent(consent) {
    setConsentMode(consent);
    if (consent.analytics && CFG.gtmId) loadGtm(CFG.gtmId);
    if (consent.marketing && CFG.metaPixelId) loadMetaPixel(CFG.metaPixelId);
    if (consent.marketing && CFG.linkedinPartnerId) loadLinkedIn(CFG.linkedinPartnerId);
    document.dispatchEvent(
      new CustomEvent("sa-sdr-consent-update", { detail: consent })
    );
  }

  function buildBanner() {
    if (document.getElementById("sa-sdr-consent-root")) return;

    var root = document.createElement("div");
    root.id = "sa-sdr-consent-root";
    root.className = "cc-root";
    root.hidden = true;

    var analyticsToggle = hasAnalyticsConfig
      ? '<label class="cc-toggle"><input type="checkbox" id="cc-analytics" /> Analytics</label>'
      : "";
    var marketingToggle = hasMarketingConfig
      ? '<label class="cc-toggle"><input type="checkbox" id="cc-marketing" /> Marketing</label>'
      : "";

    root.innerHTML =
      '<div class="cc-banner" id="sa-sdr-consent-banner" role="dialog" aria-labelledby="cc-title" aria-describedby="cc-desc" aria-modal="false">' +
      '<div class="cc-banner-inner">' +
      '<p class="cc-title" id="cc-title">Cookie preferences</p>' +
      '<p class="cc-desc" id="cc-desc">We use essential cookies to remember your choices. With your consent we may use analytics and marketing tools to understand traffic and improve campaigns. See our <a href="/cookies/">Cookie Policy</a> and <a href="/privacy/">Privacy Policy</a>.</p>' +
      '<div class="cc-actions">' +
      '<button type="button" class="cc-btn cc-btn-primary" data-cc="accept">Accept all</button>' +
      '<button type="button" class="cc-btn cc-btn-secondary" data-cc="reject">Reject non-essential</button>' +
      '<button type="button" class="cc-btn cc-btn-secondary" data-cc="customize">Customize</button>' +
      "</div>" +
      "</div>" +
      "</div>" +
      '<div class="cc-panel" id="sa-sdr-consent-panel" role="dialog" aria-labelledby="cc-panel-title" aria-modal="true" hidden>' +
      '<div class="cc-panel-inner">' +
      '<p class="cc-title" id="cc-panel-title">Manage cookie preferences</p>' +
      '<p class="cc-desc">Choose which optional cookies we may set. Essential cookies are always active.</p>' +
      '<div class="cc-toggles">' +
      '<label class="cc-toggle cc-toggle-locked"><input type="checkbox" checked disabled /> Essential (required)</label>' +
      analyticsToggle +
      marketingToggle +
      "</div>" +
      '<div class="cc-actions">' +
      '<button type="button" class="cc-btn cc-btn-primary" data-cc="save">Save preferences</button>' +
      '<button type="button" class="cc-btn cc-btn-secondary" data-cc="close-panel">Cancel</button>' +
      "</div>" +
      "</div>" +
      "</div>";

    document.body.appendChild(root);
    bindEvents(root);
  }

  function showBanner() {
    var root = document.getElementById("sa-sdr-consent-root");
    if (!root) return;
    root.hidden = false;
    var banner = document.getElementById("sa-sdr-consent-banner");
    var panel = document.getElementById("sa-sdr-consent-panel");
    if (banner) banner.hidden = false;
    if (panel) panel.hidden = true;
  }

  function showPanel() {
    var root = document.getElementById("sa-sdr-consent-root");
    if (!root) return;
    root.hidden = false;
    var banner = document.getElementById("sa-sdr-consent-banner");
    var panel = document.getElementById("sa-sdr-consent-panel");
    if (banner) banner.hidden = true;
    if (panel) panel.hidden = false;
    var stored = loadStoredConsent();
    var analyticsEl = document.getElementById("cc-analytics");
    var marketingEl = document.getElementById("cc-marketing");
    if (analyticsEl) analyticsEl.checked = stored ? stored.analytics : false;
    if (marketingEl) marketingEl.checked = stored ? stored.marketing : false;
  }

  function hideAll() {
    var root = document.getElementById("sa-sdr-consent-root");
    if (root) root.hidden = true;
  }

  function acceptAll() {
    var consent = saveConsent({ analytics: hasAnalyticsConfig, marketing: hasMarketingConfig });
    applyConsent(consent);
    hideAll();
  }

  function rejectAll() {
    var consent = saveConsent({ analytics: false, marketing: false });
    applyConsent(consent);
    hideAll();
  }

  function saveCustom() {
    var analyticsEl = document.getElementById("cc-analytics");
    var marketingEl = document.getElementById("cc-marketing");
    var consent = saveConsent({
      analytics: analyticsEl ? analyticsEl.checked : false,
      marketing: marketingEl ? marketingEl.checked : false,
    });
    applyConsent(consent);
    hideAll();
  }

  function bindEvents(root) {
    root.addEventListener("click", function (e) {
      var action = e.target && e.target.getAttribute("data-cc");
      if (!action) return;
      if (action === "accept") acceptAll();
      if (action === "reject") rejectAll();
      if (action === "customize") showPanel();
      if (action === "save") saveCustom();
      if (action === "close-panel") {
        var stored = loadStoredConsent();
        if (stored) hideAll();
        else showBanner();
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      var panel = document.getElementById("sa-sdr-consent-panel");
      if (panel && !panel.hidden) {
        var stored = loadStoredConsent();
        if (stored) hideAll();
        else showBanner();
      }
    });
  }

  function bindSettingsTriggers() {
    document.querySelectorAll("[data-cc-settings]").forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        buildBanner();
        showPanel();
      });
    });
  }

  function init() {
    ensureGtagStub();
    window.gtag("consent", "default", {
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      wait_for_update: 500,
    });

    buildBanner();
    bindSettingsTriggers();

    var stored = loadStoredConsent();
    if (stored) {
      applyConsent(stored);
      hideAll();
      return;
    }

    showBanner();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.SASDRConsent = {
    openSettings: function () {
      buildBanner();
      showPanel();
    },
    getConsent: loadStoredConsent,
  };
})();
