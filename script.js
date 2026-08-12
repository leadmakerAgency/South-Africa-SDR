/* South Africa SDR · Home page interactions */

(function () {
  "use strict";

  var header = document.getElementById("siteHeader");
  var hamburger = document.getElementById("hamburger");

  /* Sticky header: add shadow once scrolled */
  function onScroll() {
    if (window.scrollY > 40) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  hamburger.addEventListener("click", function () {
    var open = header.classList.toggle("menu-open");
    hamburger.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
  });

  /* Mobile accordions */
  document.querySelectorAll(".mm-accordion").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var panel = btn.nextElementSibling;
      var open = panel.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  /* Close mobile menu when a link inside it is clicked */
  document.querySelectorAll(".mobile-menu a").forEach(function (link) {
    link.addEventListener("click", function () {
      header.classList.remove("menu-open");
      hamburger.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    });
  });

  /* ---------- Desktop dropdowns: click support (touch devices) ---------- */
  document.querySelectorAll(".has-dropdown > .nav-toggle").forEach(function (toggle) {
    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var li = toggle.parentElement;
      var wasOpen = li.classList.contains("open");
      document.querySelectorAll(".has-dropdown.open").forEach(function (openLi) {
        openLi.classList.remove("open");
        openLi.querySelector(".nav-toggle").setAttribute("aria-expanded", "false");
      });
      if (!wasOpen) {
        li.classList.add("open");
        toggle.setAttribute("aria-expanded", "true");
      }
    });
  });

  document.addEventListener("click", function () {
    document.querySelectorAll(".has-dropdown.open").forEach(function (li) {
      li.classList.remove("open");
      li.querySelector(".nav-toggle").setAttribute("aria-expanded", "false");
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll(".has-dropdown.open").forEach(function (li) {
        li.classList.remove("open");
        li.querySelector(".nav-toggle").setAttribute("aria-expanded", "false");
      });
      if (header.classList.contains("menu-open")) {
        header.classList.remove("menu-open");
        hamburger.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      }
    }
  });

  /* ---------- Scroll reveal ---------- */
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!reduceMotion && "IntersectionObserver" in window) {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );
    document.querySelectorAll(".reveal").forEach(function (el) {
      revealObserver.observe(el);
    });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) {
      el.classList.add("in");
    });
  }

  /* ---------- Metric band counters ---------- */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    var decimals = parseInt(el.getAttribute("data-decimals") || "0", 10);
    var duration = 1600;
    var start = null;

    function format(value) {
      var fixed = value.toFixed(decimals);
      if (decimals === 0 && value >= 1000) {
        fixed = Math.round(value).toLocaleString("en-US");
      }
      return fixed + suffix;
    }

    if (reduceMotion) {
      el.textContent = format(target);
      return;
    }

    function tick(ts) {
      if (!start) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = format(target * eased);
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  var counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window) {
    var countObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            countObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach(function (el) { countObserver.observe(el); });
  } else {
    counters.forEach(animateCount);
  }
})();
