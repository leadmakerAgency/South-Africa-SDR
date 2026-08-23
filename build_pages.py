#!/usr/bin/env python3
"""Generate all South Africa SDR website pages as self-contained HTML files."""

import os
import json
from pathlib import Path

ROOT = Path(__file__).parent
CONTACT_CTA = "/contact/"
LOGO = "/images/brand/lockup-horizontal.svg"
LOGO_REV = "/images/brand/lockup-horizontal-rev.svg"

with open(ROOT / "styles.css", encoding="utf-8") as f:
    BASE_CSS = f.read()

with open(ROOT / "script.js", encoding="utf-8") as f:
    BASE_JS = f.read()

EXTRA_CSS = """
/* Inner page — split hero (matches home) */
.page-hero { padding: calc(var(--header-offset) + 28px) 0 100px; }
.page-hero-grid { display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 56px; align-items: center; }
.page-hero-grid.hero-copy-only { grid-template-columns: 1fr; max-width: 760px; }
.page-hero-visual { position: relative; }
.photo-frame { position: relative; border-radius: 18px; overflow: hidden; box-shadow: var(--shadow-float); border: 3px solid rgba(250,248,242,0.12); }
.photo-frame img { width: 100%; height: auto; aspect-ratio: 4/3; object-fit: cover; display: block; }
.photo-accent { position: absolute; bottom: -16px; left: -16px; width: 80px; height: 80px; border-radius: 16px; background: var(--gold); opacity: 0.35; z-index: -1; }
.photo-frame-offset { transform: rotate(-1.5deg); }
.split-section { display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; }
.split-section.reverse .split-media { order: 2; }
.split-section.reverse .split-copy { order: 1; }
.split-media img { width: 100%; border-radius: 16px; box-shadow: var(--shadow-soft); aspect-ratio: 4/3; object-fit: cover; }
.deliverable-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }
.deliverable-card { background: #fff; border: 0.5px solid rgba(2,64,61,0.1); border-radius: var(--radius-card); padding: 28px 24px; box-shadow: 0 8px 24px rgba(30,38,34,0.05); transition: transform 0.25s, box-shadow 0.25s; }
.deliverable-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-soft); }
.deliverable-icon { width: 48px; height: 48px; border-radius: 12px; background: rgba(218,168,102,0.14); color: #B8945A; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; }
.deliverable-icon svg { width: 24px; height: 24px; }
.deliverable-card h3 { font-size: 18px; margin-bottom: 8px; }
.deliverable-card p { font-size: 14.5px; color: rgba(30,38,34,0.72); line-height: 1.55; }
.visual-panel { background: linear-gradient(145deg, var(--green) 0%, #012B28 100%); border-radius: 18px; padding: 36px 32px; color: var(--cream); position: relative; overflow: hidden; }
.visual-panel::before { content: ""; position: absolute; top: -40px; right: -40px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(218,168,102,0.2) 0%, transparent 70%); pointer-events: none; }
.visual-panel h3 { color: var(--cream); font-size: 22px; margin-bottom: 16px; position: relative; }
.visual-panel p { color: rgba(250,248,242,0.82); font-size: 15px; line-height: 1.6; position: relative; }
.visual-stat-row { display: flex; gap: 28px; margin-top: 28px; position: relative; }
.visual-stat-row span { display: flex; flex-direction: column; }
.visual-stat-row strong { font-family: var(--font-serif); font-size: 28px; color: var(--gold); }
.visual-stat-row small { font-size: 12px; color: rgba(250,248,242,0.6); margin-top: 2px; }
.faq-layout { display: grid; grid-template-columns: 0.85fr 1.15fr; gap: 56px; align-items: start; }
.faq-side { position: sticky; top: calc(var(--header-offset) + 24px); }
.faq-side-img { border-radius: 16px; overflow: hidden; box-shadow: var(--shadow-soft); margin-top: 24px; }
.faq-side-img img { width: 100%; aspect-ratio: 4/5; object-fit: cover; }
.faq-category { margin-bottom: 48px; }
.faq-category-head { display: flex; align-items: center; gap: 14px; margin-bottom: 20px; }
.faq-cat-icon { width: 40px; height: 40px; border-radius: 10px; background: rgba(218,168,102,0.14); color: #B8945A; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.faq-cat-icon svg { width: 20px; height: 20px; }
.about-values { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin-top: 48px; }
.value-card { text-align: center; padding: 32px 24px; background: #fff; border-radius: var(--radius-card); border: 0.5px solid rgba(2,64,61,0.1); }
.value-card .deliverable-icon { margin: 0 auto 16px; }
.compare-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.compare-choice { padding: 36px 32px; border-radius: var(--radius-card); }
.compare-choice.alt { background: #fff; border: 0.5px solid rgba(2,64,61,0.12); box-shadow: 0 8px 24px rgba(30,38,34,0.05); }
.compare-choice.sa { background: var(--green); color: var(--cream); }
.compare-choice.sa h3 { color: var(--cream); }
.compare-choice.sa p { color: rgba(250,248,242,0.85); }
.compare-choice h3 { font-size: 22px; margin-bottom: 14px; }
.compare-choice p { font-size: 16px; line-height: 1.65; color: rgba(30,38,34,0.78); }
.book-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 56px; align-items: start; max-width: var(--container); margin: 0 auto; padding: 48px 28px 80px; text-align: left; }
.book-visual img { border-radius: 16px; box-shadow: var(--shadow-soft); width: 100%; aspect-ratio: 3/4; object-fit: cover; }
.article-hero-img { width: 100%; max-height: 440px; object-fit: cover; border-radius: 18px; margin-bottom: 40px; box-shadow: var(--shadow-soft); }
.article-meta-bar { display: flex; flex-wrap: wrap; gap: 16px 32px; padding: 20px 0; border-top: 1px solid rgba(2,64,61,0.1); border-bottom: 1px solid rgba(2,64,61,0.1); margin-bottom: 36px; font-size: 14px; color: rgba(30,38,34,0.6); }
.prose { font-size: 17px; line-height: 1.7; color: rgba(30,38,34,0.82); }
.prose p { margin-bottom: 18px; }
.prose p:last-child { margin-bottom: 0; }
.prose h3 { margin: 28px 0 12px; font-size: 22px; }
.prose ul { margin: 0 0 18px 20px; }
.prose li { margin-bottom: 8px; }
.prose-green p { color: rgba(250,248,242,0.86); }
.content-split { display: grid; grid-template-columns: 1fr 1fr; gap: 56px; align-items: start; }
.content-narrow { max-width: 720px; }
.content-wide { max-width: 900px; margin: 0 auto; }
.check-list { list-style: none; margin: 0; padding: 0; }
.check-list li { position: relative; padding-left: 28px; margin-bottom: 12px; font-size: 16px; }
.check-list li::before { content: ""; position: absolute; left: 0; top: 0.45em; width: 16px; height: 16px; border-radius: 50%; background: rgba(63,142,118,0.2); border: 2px solid var(--green-support); }
.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.feature-mini { background: #fff; border: 0.5px solid rgba(2,64,61,0.12); border-radius: var(--radius-card); padding: 28px 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.05); }
.feature-mini h3 { font-size: 19px; margin-bottom: 10px; }
.feature-mini p { font-size: 15px; color: rgba(30,38,34,0.75); }
.faq-list { display: flex; flex-direction: column; gap: 12px; max-width: 800px; }
.faq-item { background: #fff; border: 0.5px solid rgba(2,64,61,0.12); border-radius: 12px; overflow: hidden; }
.faq-q { width: 100%; display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 20px 24px; font-family: var(--font-serif); font-size: 18px; font-weight: 600; color: var(--green); background: none; border: none; cursor: pointer; text-align: left; }
.faq-q .faq-icon { flex-shrink: 0; width: 24px; height: 24px; border-radius: 50%; background: rgba(218,168,102,0.15); color: #B8945A; display: flex; align-items: center; justify-content: center; font-size: 18px; line-height: 1; transition: transform 0.25s; }
.faq-item.open .faq-icon { transform: rotate(45deg); }
.faq-a { max-height: 0; overflow: hidden; transition: max-height 0.35s ease; }
.faq-a-inner { padding: 0 24px 20px; font-size: 16px; line-height: 1.65; color: rgba(30,38,34,0.78); }
.faq-item.open .faq-a { max-height: 400px; }
.compare-table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 -4px; padding: 4px; }
.compare-table { width: 100%; min-width: 560px; border-collapse: collapse; background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 8px 28px rgba(30,38,34,0.06); }
.compare-table th, .compare-table td { padding: 16px 20px; text-align: left; border-bottom: 1px solid rgba(2,64,61,0.08); font-size: 15px; }
.compare-table th { background: var(--green); color: var(--cream); font-family: var(--font-serif); font-weight: 600; font-size: 16px; }
.compare-table tr:last-child td { border-bottom: none; }
.compare-table td:first-child { font-weight: 500; color: var(--green); background: rgba(250,248,242,0.5); }
.compare-table .good { color: var(--green-support); font-weight: 600; }
.compare-table .neutral { color: rgba(30,38,34,0.65); }
.cta-band-green { background: var(--green); text-align: center; padding: 80px 0; position: relative; overflow: hidden; }
.cta-band-green h2 { color: var(--cream); margin-bottom: 28px; max-width: 640px; margin-left: auto; margin-right: auto; }
.cta-band-green .cta-glow { position: absolute; top: -120px; right: -80px; width: 500px; height: 500px; background: radial-gradient(circle, rgba(218,168,102,0.18) 0%, transparent 65%); pointer-events: none; }
.hub-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 22px; }
.hub-card { display: block; background: #fff; border: 0.5px solid rgba(2,64,61,0.12); border-radius: 16px; padding: 32px 28px; transition: transform 0.25s, box-shadow 0.25s; }
.hub-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-soft); }
.hub-card h3 { margin-bottom: 10px; }
.hub-card p { font-size: 15px; color: rgba(30,38,34,0.72); margin-bottom: 16px; }
.blog-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px; }
.blog-card { display: flex; flex-direction: column; background: #fff; border-radius: 16px; overflow: hidden; border: 0.5px solid rgba(2,64,61,0.1); transition: transform 0.25s, box-shadow 0.25s; }
.blog-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-soft); }
.blog-card-img { aspect-ratio: 16/10; background: var(--footer-caramel); overflow: hidden; }
.blog-card-img img { width: 100%; height: 100%; object-fit: cover; }
.blog-card-body { padding: 22px 24px 26px; flex: 1; display: flex; flex-direction: column; }
.blog-meta { font-size: 12px; font-weight: 500; letter-spacing: 0.4px; text-transform: uppercase; color: #B8945A; margin-bottom: 10px; }
.blog-card h3 { font-size: 19px; margin-bottom: 10px; }
.blog-card p { font-size: 14.5px; color: rgba(30,38,34,0.7); flex: 1; }
.article-header { max-width: 720px; margin-bottom: 40px; }
.article-body { max-width: 720px; }
.article-body h2 { margin: 36px 0 14px; font-size: 26px; }
.article-body p { margin-bottom: 18px; font-size: 17px; line-height: 1.7; color: rgba(30,38,34,0.82); }
.contact-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: start; }
.form-group { margin-bottom: 18px; }
.form-group label { display: block; font-size: 14px; font-weight: 500; color: var(--green); margin-bottom: 6px; }
.form-group input, .form-group textarea, .form-group select {
  width: 100%; font-family: var(--font-sans); font-size: 16px; padding: 12px 14px;
  border: 1px solid rgba(2,64,61,0.2); border-radius: 9px; background: #fff; color: var(--ink);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.form-group input:focus, .form-group textarea:focus, .form-group select:focus {
  outline: none; border-color: var(--gold); box-shadow: 0 0 0 3px rgba(218,168,102,0.2);
}
.form-group textarea { min-height: 120px; resize: vertical; }
.form-error { font-size: 13px; color: var(--clay); margin-top: 4px; display: none; }
.form-group.invalid .form-error { display: block; }
.form-group.invalid input, .form-group.invalid textarea { border-color: var(--clay); }
.contact-info { background: var(--green); border-radius: 16px; padding: 32px 28px; color: var(--cream); }
.contact-info h3 { color: var(--cream); margin-bottom: 20px; font-size: 20px; }
.contact-info-item { display: flex; gap: 12px; margin-bottom: 16px; font-size: 15px; color: rgba(250,248,242,0.85); }
.contact-info-item svg { width: 20px; height: 20px; flex-shrink: 0; color: var(--gold); }
.book-page { min-height: 100vh; background: var(--cream); }
.book-header { padding: 20px 28px; display: flex; align-items: center; justify-content: space-between; }
.book-header .logo-img { height: 32px; }
.book-main { max-width: 680px; margin: 0 auto; padding: 40px 28px 80px; text-align: center; }
.book-main h1 { margin-bottom: 14px; }
.book-main .hero-subhead { color: rgba(30,38,34,0.75); margin: 0 auto 32px; max-width: 520px; }
.book-ticks { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px 28px; margin-bottom: 40px; list-style: none; }
.book-ticks li { font-size: 14.5px; font-weight: 500; color: var(--green); padding-left: 22px; position: relative; }
.book-ticks li::before { content: ""; position: absolute; left: 0; top: 0.35em; width: 14px; height: 14px; background: rgba(63,142,118,0.2); border-radius: 50%; border: 2px solid var(--green-support); }
.success-page { min-height: 80vh; display: flex; align-items: center; justify-content: center; padding: 120px 28px 80px; text-align: center; }
.success-inner { max-width: 520px; }
.success-icon { width: 72px; height: 72px; border-radius: 50%; background: rgba(63,142,118,0.15); color: var(--green-support); display: flex; align-items: center; justify-content: center; margin: 0 auto 28px; font-size: 32px; }
.success-inner h1 { margin-bottom: 14px; }
.success-inner p { color: rgba(30,38,34,0.75); margin-bottom: 28px; }
.legal-content { max-width: 760px; }
.legal-content h2 { margin: 36px 0 14px; font-size: 24px; }
.legal-content h3 { margin: 24px 0 10px; font-size: 19px; }
.legal-content p, .legal-content li { font-size: 16px; line-height: 1.7; color: rgba(30,38,34,0.8); }
.legal-content ul { margin: 0 0 18px 24px; }
.error-page { min-height: 80vh; display: flex; align-items: center; text-align: center; padding: 120px 28px 80px; }
.error-code { font-family: var(--font-serif); font-size: clamp(80px, 15vw, 140px); font-weight: 600; color: var(--gold); line-height: 1; margin-bottom: 12px; }
.error-links { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 28px; }
.btn-outline-green { background: transparent; border: 1px solid var(--green); color: var(--green); }
.btn-outline-green:hover { background: var(--green); color: var(--cream); }
.pricing-box { background: rgba(250,248,242,0.06); border: 1px solid rgba(250,248,242,0.14); border-radius: 16px; padding: 36px 32px; max-width: 640px; }
.pricing-box p { font-size: 17px; color: rgba(250,248,242,0.86); }
.case-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 32px 0; }
.case-metric { text-align: center; padding: 24px 16px; background: #fff; border-radius: 12px; border: 0.5px solid rgba(2,64,61,0.1); }
.case-metric strong { display: block; font-family: var(--font-serif); font-size: 32px; color: var(--gold); margin-bottom: 4px; }
.case-metric span { font-size: 13px; color: rgba(30,38,34,0.6); }
.nav-link.active { color: var(--green); background: #F3F4F6; }
@media (max-width: 1080px) {
  .page-hero-grid, .split-section, .contact-layout, .feature-grid, .faq-layout, .book-layout, .compare-cards, .deliverable-grid { grid-template-columns: 1fr; }
  .split-section.reverse .split-media, .split-section.reverse .split-copy { order: unset; }
  .blog-grid { grid-template-columns: repeat(2, 1fr); }
  .hub-grid { grid-template-columns: 1fr; }
  .faq-side { position: static; }
  .about-values { grid-template-columns: 1fr; }
}
@media (max-width: 760px) {
  .feature-grid, .blog-grid, .case-metrics, .deliverable-grid { grid-template-columns: 1fr; }
  .page-hero { padding: calc(var(--header-offset) + 20px) 0 72px; }
  .faq-q { font-size: 16px; padding: 16px 18px; }
  .faq-a-inner { padding: 0 18px 16px; }
  .footer-nav-grid { grid-template-columns: 1fr 1fr; }
  .book-layout { padding: 32px 20px 60px; }
}
.footer-nav-grid { grid-template-columns: repeat(4, minmax(120px, 1fr)); }
"""

EXTRA_JS = """
/* FAQ accordion */
document.querySelectorAll('.faq-q').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var item = btn.closest('.faq-item');
    var open = item.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
});

/* Form validation */
var contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    var valid = true;
    contactForm.querySelectorAll('[required]').forEach(function(field) {
      var group = field.closest('.form-group');
      if (!field.value.trim()) {
        group.classList.add('invalid');
        valid = false;
      } else {
        group.classList.remove('invalid');
      }
    });
    var email = contactForm.querySelector('[type="email"]');
    if (email && email.value && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email.value)) {
      email.closest('.form-group').classList.add('invalid');
      valid = false;
    }
    if (valid) {
      var depth = contactForm.getAttribute('data-depth') || '';
      window.location.href = depth + 'success/contact-received/index.html';
    }
  });
  contactForm.querySelectorAll('input, textarea').forEach(function(field) {
    field.addEventListener('input', function() {
      field.closest('.form-group').classList.remove('invalid');
    });
  });
}

/* Newsletter */
var subForm = document.getElementById('subscribeForm');
if (subForm) {
  subForm.addEventListener('submit', function(e) {
    e.preventDefault();
    var email = subForm.querySelector('[type="email"]');
    if (email && email.value.trim()) {
      var depth = subForm.getAttribute('data-depth') || '';
      window.location.href = depth + 'success/subscribed/index.html';
    }
  });
}
"""


def rel(depth: int, path: str) -> str:
    """Build relative path from page at given depth."""
    if path.startswith("http"):
        return path
    prefix = "../" * depth if depth else ""
    if path == "/":
        return prefix + ("index.html" if depth else "index.html")
    clean = path.strip("/")
    if clean.endswith(".html"):
        return prefix + clean
    return prefix + clean + "/index.html"


def header_html(depth: int, minimal: bool = False) -> str:
    if minimal:
        return f"""<header class="book-header">
  <a href="{rel(depth, '/')}" class="logo" aria-label="South Africa SDR, home">
    <img src="{LOGO}" alt="South Africa SDR" class="logo-img" width="220" height="40" />
  </a>
  <a href="{CONTACT_CTA}" class="btn btn-primary" style="padding:10px 20px;font-size:14px;">Book a call</a>
</header>"""

    return f"""<header class="site-header" id="siteHeader">
  <div class="header-shell">
    <div class="header-pill">
      <a href="{rel(depth, '/')}" class="logo" aria-label="South Africa SDR, home">
        <img src="{LOGO}" alt="South Africa SDR — Western Sales Talent" class="logo-img" width="220" height="40" fetchpriority="high" />
      </a>
      <nav class="main-nav" id="mainNav" aria-label="Main">
        <ul class="nav-list">
          <li><a href="{rel(depth, '/why-south-africa/')}" class="nav-link">Why South Africa</a></li>
          <li class="has-dropdown">
            <button class="nav-link nav-toggle" aria-expanded="false" aria-haspopup="true">Services
              <svg class="chev" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <div class="dropdown">
              <a href="{rel(depth, '/services/sdr/')}">SDR Services</a>
              <a href="{rel(depth, '/services/appointment-setting/')}">Appointment Setting</a>
              <a href="{rel(depth, '/services/customer-service/')}">Customer Service</a>
              <a href="{rel(depth, '/services/technical-support/')}">Technical Support</a>
            </div>
          </li>
          <li class="has-dropdown">
            <button class="nav-link nav-toggle" aria-expanded="false" aria-haspopup="true">Industries
              <svg class="chev" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <div class="dropdown dropdown-wide">
              <div class="dropdown-cols">
                {industry_dropdown_links(depth)}
              </div>
            </div>
          </li>
          <li><a href="{rel(depth, '/about/')}" class="nav-link">About</a></li>
          <li class="has-dropdown">
            <button class="nav-link nav-toggle" aria-expanded="false" aria-haspopup="true">Resources
              <svg class="chev" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </button>
            <div class="dropdown">
              <a href="{rel(depth, '/blog/')}">Blog / Insights</a>
              <a href="{rel(depth, '/case-studies/')}">Case Studies</a>
              <a href="{rel(depth, '/faq/')}">FAQ</a>
              <div class="dropdown-group-label">Compare</div>
              <a href="{rel(depth, '/compare/south-africa-vs-philippines/')}">South Africa vs Philippines</a>
              <a href="{rel(depth, '/compare/south-africa-vs-india/')}">South Africa vs India</a>
              <a href="{rel(depth, '/compare/south-africa-vs-latin-america/')}">South Africa vs Latin America</a>
              <a href="{rel(depth, '/compare/south-africa-vs-eastern-europe/')}">South Africa vs Eastern Europe</a>
              <a href="{rel(depth, '/compare/in-house-vs-outsourced/')}">In-house vs Outsourced</a>
            </div>
          </li>
        </ul>
      </nav>
      <div class="header-actions">
        <a href="{CONTACT_CTA}" class="btn-header-cta">
          <svg class="btn-header-icon" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M8 2v6l3.5 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="8" cy="8" r="6.25" stroke="currentColor" stroke-width="1.6"/></svg>
          Book a call
        </a>
        <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu"><span></span><span></span><span></span></button>
      </div>
    </div>
    <div class="mobile-menu" id="mobileMenu">
      <nav aria-label="Mobile">
        <a class="mm-link" href="{rel(depth, '/why-south-africa/')}">Why South Africa</a>
        <button class="mm-link mm-accordion" aria-expanded="false">Services <svg class="chev" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
        <div class="mm-panel">
          <a href="{rel(depth, '/services/sdr/')}">SDR Services</a>
          <a href="{rel(depth, '/services/appointment-setting/')}">Appointment Setting</a>
          <a href="{rel(depth, '/services/customer-service/')}">Customer Service</a>
          <a href="{rel(depth, '/services/technical-support/')}">Technical Support</a>
        </div>
        <button class="mm-link mm-accordion" aria-expanded="false">Industries <svg class="chev" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
        <div class="mm-panel">
          {industry_mobile_links(depth)}
        </div>
        <a class="mm-link" href="{rel(depth, '/about/')}">About</a>
        <button class="mm-link mm-accordion" aria-expanded="false">Resources <svg class="chev" viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
        <div class="mm-panel">
          <a href="{rel(depth, '/blog/')}">Blog / Insights</a>
          <a href="{rel(depth, '/case-studies/')}">Case Studies</a>
          <a href="{rel(depth, '/faq/')}">FAQ</a>
          <a href="{rel(depth, '/compare/south-africa-vs-philippines/')}">Compare locations</a>
        </div>
        <a href="{CONTACT_CTA}" class="btn btn-primary mm-cta">
          <svg class="btn-header-icon" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M8 2v6l3.5 2" stroke="currentColor" stroke-width="1.6"/><circle cx="8" cy="8" r="6.25" stroke="currentColor" stroke-width="1.6"/></svg>
          Book a call
        </a>
      </nav>
    </div>
  </div>
</header>"""


def footer_html(depth: int) -> str:
    return f"""<footer class="site-footer">
  <div class="container footer-container">
    <div class="footer-header">
      <a href="{rel(depth, '/')}" class="footer-logo" aria-label="South Africa SDR, home">
        <img src="{LOGO}" alt="South Africa SDR" class="footer-logo-img" width="200" height="36" loading="lazy" />
      </a>
      <p class="footer-tagline">Western sales talent that actually delivers.</p>
    </div>
    <div class="footer-divider" aria-hidden="true"></div>
    <div class="footer-main">
      <div class="footer-nav-grid">
        <div class="footer-col">
          <h4>Services</h4>
          <ul class="footer-links">
            <li><a href="{rel(depth, '/services/sdr/')}">SDR Services</a></li>
            <li><a href="{rel(depth, '/services/appointment-setting/')}">Appointment Setting</a></li>
            <li><a href="{rel(depth, '/services/customer-service/')}">Customer Service</a></li>
            <li><a href="{rel(depth, '/services/technical-support/')}">Technical Support</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Industries</h4>
          <ul class="footer-links">
            {industry_footer_links(depth)}
          </ul>
        </div>
        <div class="footer-col">
          <h4>Compare</h4>
          <ul class="footer-links">
            <li><a href="{rel(depth, '/compare/south-africa-vs-philippines/')}">vs Philippines</a></li>
            <li><a href="{rel(depth, '/compare/south-africa-vs-india/')}">vs India</a></li>
            <li><a href="{rel(depth, '/compare/in-house-vs-outsourced/')}">In-house vs Outsourced</a></li>
          </ul>
        </div>
        <div class="footer-col footer-contact-col">
          <h4>Company</h4>
          <ul class="footer-links">
            <li><a href="{rel(depth, '/about/')}">About</a></li>
            <li><a href="{rel(depth, '/contact/')}">Contact</a></li>
            <li><a href="{rel(depth, '/blog/')}">Blog</a></li>
            <li><a href="{rel(depth, '/case-studies/')}">Case Studies</a></li>
            <li><a href="{rel(depth, '/faq/')}">FAQ</a></li>
          </ul>
        </div>
      </div>
      <aside class="footer-aside">
        <a href="{CONTACT_CTA}" class="btn btn-primary" style="margin-bottom:16px;">Book a call</a>
        <div class="footer-social">
          <a href="https://www.linkedin.com/" class="footer-social-link" aria-label="LinkedIn" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 4.126 0 2.062 2.062 0 0 1-2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>
          <a href="https://www.youtube.com/" class="footer-social-link" aria-label="YouTube" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.5 31.5 0 0 0 0 12a31.5 31.5 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.5 31.5 0 0 0 24 12a31.5 31.5 0 0 0-.5-5.8zM9.7 15.5V8.5L15.8 12l-6.1 3.5z"/></svg></a>
        </div>
      </aside>
    </div>
    <div class="footer-bottom">
      <p class="footer-copy">© 2026 South Africa SDR. All rights reserved.</p>
      <nav class="footer-legal" aria-label="Legal">
        <a href="{rel(depth, '/privacy/')}">Privacy Policy</a>
        <a href="{rel(depth, '/terms/')}">Terms of Service</a>
        <a href="{rel(depth, '/cookies/')}">Cookies</a>
      </nav>
    </div>
  </div>
</footer>"""


def testimonials_section() -> str:
    return """<section class="section-green section testimonials-section">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow-pill pill-on-green">Testimonials</span>
      <h2>Client testimonials, in their own words</h2>
      <p class="section-sub section-sub-on-green">Complete reviews, not clipped to a single line, from the teams we have built pipeline for.</p>
    </div>
    <p class="testimonials-attribution reveal">
      Shared from <a href="https://leadmaker.agency" target="_blank" rel="noopener noreferrer">LeadMaker</a>, our parent company and the outbound team behind South Africa SDR.
    </p>
    <div class="testimonials-marquee reveal" data-testimonials-carousel aria-label="Client testimonials">
      <div class="tc-viewport">
        <div class="tc-track"></div>
      </div>
    </div>
  </div>
</section>"""


def cta_band(depth: int, headline: str) -> str:
    return testimonials_section() + f"""<section class="cta-band-green section">
  <div class="cta-glow" aria-hidden="true"></div>
  <div class="container reveal">
    <h2>{headline}</h2>
    <a href="{CONTACT_CTA}" class="btn btn-primary btn-lg">Book a call</a>
  </div>
</section>"""


def page_closing(depth: int, headline: str = "Ready to build your pipeline with South African SDRs?") -> str:
    return cta_band(depth, headline)


def page_hero(eyebrow: str, h1: str, subhead: str = "", buttons: str = "", image_url: str = "", image_alt: str = "", single_col: bool = False) -> str:
    visual = ""
    if image_url:
        visual = f"""<div class="page-hero-visual reveal">
      <div class="photo-frame photo-frame-offset">
        <img src="{image_url}" alt="{image_alt}" loading="eager" width="800" height="520" />
        <div class="photo-accent" aria-hidden="true"></div>
      </div>
    </div>"""
    grid_cls = "hero-inner page-hero-grid" + (" hero-copy-only" if single_col or not image_url else "")
    btns = f'<div class="hero-buttons">{buttons}</div>' if buttons else ""
    return f"""<section class="page-hero section-green hero">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="hero-dots" aria-hidden="true"></div>
  <div class="container {grid_cls}">
    <div class="hero-copy reveal">
      <span class="eyebrow-pill pill-on-green">{eyebrow}</span>
      <h1>{h1}</h1>
      {f'<p class="hero-subhead">{subhead}</p>' if subhead else ''}
      {btns}
    </div>
    {visual}
  </div>
</section>"""


def section_head(eyebrow: str, title: str, sub: str = "", on_green: bool = False) -> str:
    pill = "eyebrow-pill pill-on-green" if on_green else "eyebrow-pill"
    sub_html = f'<p class="section-sub">{sub}</p>' if sub else ""
    return f"""<div class="section-head reveal">
      <span class="{pill}">{eyebrow}</span>
      <h2>{title}</h2>
      {sub_html}
    </div>"""


ICON_SVG = {
    "target": '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none"><path d="M6.5 4h3l1.2 4.2-2 1.2a13 13 0 0 0 5.1 5.1l1.2-2 4.2 1.2v3a2 2 0 0 1-2 2C10.4 18.7 5.3 13.6 5.3 6.5A2 2 0 0 1 6.5 4Z" stroke="currentColor" stroke-width="1.8"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none"><path d="M4 19V5M4 19h16M9 15V9M14 15V7M19 15v-3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none"><circle cx="9" cy="8" r="3.5" stroke="currentColor" stroke-width="1.8"/><path d="M2 19c0-3.3 3.1-5 7-5s7 1.7 7 5M17 8.5a2.5 2.5 0 1 1 0 5M22 19c0-2.2-2-3.5-4.5-3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="M3 12h18M12 3c2.5 2.8 4 6.2 4 9s-1.5 6.2-4 9M12 3c-2.5 2.8-4 6.2-4 9s1.5 6.2 4 9" stroke="currentColor" stroke-width="1.8"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none"><path d="M12 3l8 3v6c0 5-3.5 8.5-8 9-4.5-.5-8-4-8-9V6l8-3Z" stroke="currentColor" stroke-width="1.8"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none"><path d="M5 18l2.5-3H18a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h1v4Z" stroke="currentColor" stroke-width="1.8"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3.5 2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "money": '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v10M9.5 9.5c0-1 1-1.5 2.5-1.5s2.5.5 2.5 1.5-1 1.5-2.5 1.5-2.5.5-2.5 1.5 1 1.5 2.5 1.5 2.5-.5 2.5-1.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
}


def deliverable_grid(items: list) -> str:
    cards = []
    for icon, title, desc in items:
        cards.append(f"""<article class="deliverable-card reveal">
      <div class="deliverable-icon" aria-hidden="true">{ICON_SVG.get(icon, ICON_SVG["target"])}</div>
      <h3>{title}</h3>
      <p>{desc}</p>
    </article>""")
    return f'<div class="deliverable-grid">{"".join(cards)}</div>'


SERVICE_IMAGES = {
    "sdr": ("https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", "Sales development team reviewing outbound pipeline"),
    "appointment-setting": ("https://images.pexels.com/photos/1181717/pexels-photo-1181717.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", "Professional scheduling a client meeting"),
    "customer-service": ("https://images.pexels.com/photos/8867442/pexels-photo-8867442.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", "Customer service representative assisting a client"),
    "technical-support": ("https://images.pexels.com/photos/442150/pexels-photo-442150.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", "Technical support specialist at a workstation"),
}

SERVICE_DELIVERABLES = {
    "sdr": [
        ("target", "Prospecting & research", "Account research, list building, and ICP-matched outreach lists."),
        ("phone", "Multi-channel outreach", "Email, phone, and LinkedIn sequences in your voice."),
        ("calendar", "Meeting booking", "Qualified discovery calls booked directly to your calendar."),
        ("chart", "Pipeline reporting", "Activity metrics, reply rates, and pipeline health updates."),
        ("users", "Lead qualification", "Inbound and outbound leads qualified before handoff."),
        ("shield", "CRM hygiene", "Clean data, follow-ups, and notes your closers can trust."),
    ],
    "appointment-setting": [
        ("calendar", "Lead qualification", "Every meeting vetted against your criteria before booking."),
        ("globe", "Timezone coordination", "Scheduling across UK, EU, and US hours without friction."),
        ("phone", "Confirmations & follow-up", "Reminders, no-show recovery, and rescheduling handled."),
    ],
    "customer-service": [
        ("chat", "Multi-channel support", "Email, chat, and phone handled in your brand voice."),
        ("users", "Account follow-up", "Proactive check-ins that keep customers retained."),
        ("shield", "Escalation handling", "Issues resolved or routed with clear context."),
    ],
    "technical-support": [
        ("shield", "Tier 1 & 2 support", "Product troubleshooting that protects the relationship."),
        ("chart", "Ticket triage", "Prioritisation, documentation, and clean handoffs to engineering."),
        ("chat", "Customer-facing help", "Clear, patient explanations that build trust."),
    ],
}

FAQ_CAT_ICONS = {"About South Africa": "globe", "About pricing": "money", "About how it works": "clock", "About the reps": "users"}


def faq_html(items: list) -> str:
    out = ['<div class="faq-list">']
    for q, a in items:
        out.append(f"""<div class="faq-item">
  <button class="faq-q" aria-expanded="false">{q}<span class="faq-icon" aria-hidden="true">+</span></button>
  <div class="faq-a"><div class="faq-a-inner">{a}</div></div>
</div>""")
    out.append('</div>')
    return '\n'.join(out)


def faq_schema(items: list) -> str:
    entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, indent=2)


def calendly_placeholder() -> str:
    return """<div class="calendly-placeholder" role="presentation">
  <div class="cal-head"><span class="cal-dot"></span><span class="cal-dot"></span><span class="cal-dot"></span><span class="cal-title">Pick a time, 20 minutes</span></div>
  <div class="cal-body">
    <div class="cal-days"><span>Mon<br><b>13</b></span><span class="cal-active">Tue<br><b>14</b></span><span>Wed<br><b>15</b></span><span>Thu<br><b>16</b></span><span>Fri<br><b>17</b></span></div>
    <div class="cal-slots"><span>09:00</span><span class="slot-active">10:30</span><span>13:00</span><span>15:30</span></div>
    <p class="cal-note">Calendly embed loads here on the live site.</p>
  </div>
</div>"""


def wrap_page(title: str, description: str, depth: int, body: str, schema: str = "", noindex: bool = False, minimal_header: bool = False, extra_head: str = "", plain: bool = False) -> str:
    robots = '<meta name="robots" content="noindex, nofollow">' if noindex else ""
    favicon = """<link rel="icon" href="/images/brand/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/images/brand/favicon.svg">"""
    fonts = """<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600&family=Montserrat:wght@600;700&display=swap" rel="stylesheet">"""
    hdr = header_html(depth, minimal=minimal_header)
    ftr = "" if minimal_header else footer_html(depth)
    sch = f'<script type="application/ld+json">\n{schema}\n</script>' if schema else ""
    # Pages without a green hero (book, success, 404) keep a solid, readable navbar
    is_plain = plain or minimal_header
    body_cls = " ".join(c for c in ("book-page" if minimal_header else "", "page-plain" if is_plain else "") if c)
    body_attr = f' class="{body_cls}"' if body_cls else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#02403D">
  <title>{title}</title>
  <meta name="description" content="{description}">
  {robots}
  {favicon}
  {fonts}
  {extra_head}
  <style>
{BASE_CSS}
{EXTRA_CSS}
  </style>
  <link rel="stylesheet" href="/redesign.css">
</head>
<body{body_attr}>
{hdr}
{body}
{ftr}
{sch}
  <script>
{BASE_JS}
{EXTRA_JS}
  </script>
</body>
</html>"""


def write_page(path: str, content: str):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")
    print(f"  wrote {path}")


# --- Industry data ---
INDUSTRIES = [
    ("saas", "SaaS", "SaaS Companies", "Fill your SaaS pipeline with South African SDRs who know the buyer and the sales motion.",
     "SaaS sales cycles are long, competitive, and buyer-educated. Prospects have seen every cold email template. Breaking through means sounding credible on the product category, understanding the buyer's stack, and booking meetings with decision-makers who are already evaluating alternatives.",
     "Our South African SDRs research accounts deeply, personalise outreach around product use cases, and speak the language of SaaS metrics: ARR, churn, expansion, and time-to-value. They target VP Sales, RevOps, and founders with messaging that respects the buyer's intelligence.",
     "https://images.pexels.com/photos/12899167/pexels-photo-12899167.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("financial-services", "Financial Services", "Financial Services", "Compliant, professional outbound for financial services, powered by South African SDRs.",
     "Financial services outbound demands precision. Regulated language, senior buyers, and long trust cycles mean generic prospecting fails fast. Your reps need to understand compliance boundaries while still creating urgency.",
     "South African SDRs bring Western business norms and clear, neutral English that resonates with UK, EU, and US buyers. We train reps on your compliance guardrails, ideal customer profiles, and the titles that matter: CFOs, compliance officers, and portfolio managers.",
     "https://images.pexels.com/photos/6801643/pexels-photo-6801643.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("real-estate", "Real Estate", "Real Estate", "South African SDRs for real estate lead generation and investor outreach.",
     "Real estate prospecting is relationship-driven but volume-dependent. Whether you sell commercial space, property tech, or investment opportunities, your team needs consistent outreach without sacrificing professionalism.",
     "Our reps handle list building, investor outreach, and appointment setting for brokers, proptech firms, and agencies. They work your hours, follow your scripts, and book qualified conversations with buyers and sellers who match your criteria.",
     "https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("insurance", "Insurance", "Insurance", "Professional appointment setting for insurance brokers and insurtech teams.",
     "Insurance buyers are cautious and comparison-heavy. SDRs must build trust quickly, qualify rigorously, and respect regulatory messaging while still driving pipeline.",
     "South African reps deliver warm, professional conversations that feel domestic to UK and US prospects. We focus on policy renewals, cross-sell opportunities, and new business meetings booked directly to your producers' calendars.",
     "https://images.pexels.com/photos/5668859/pexels-photo-5668859.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("healthcare", "Healthcare", "Healthcare", "Outbound SDRs for healthcare, medtech, and health services companies.",
     "Healthcare sales requires sensitivity, accuracy, and respect for busy clinical and administrative buyers. Generic B2B playbooks do not translate.",
     "We train SDRs on your clinical vocabulary, buyer personas (practice managers, CMOs, procurement), and compliance requirements. The result is qualified meetings with decision-makers who are ready to evaluate your solution.",
     "https://images.pexels.com/photos/6129507/pexels-photo-6129507.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("recruitment", "Recruitment", "Recruitment", "Pipeline generation for recruitment agencies and staffing firms.",
     "Recruitment is a high-velocity sales motion. Your SDRs need to move fast, speak credibly to HR leaders and hiring managers, and book meetings that convert to retained or contingency placements.",
     "South African SDRs understand Western hiring norms and communicate with the professionalism your clients expect. They prospect hiring managers, build candidate pipeline support, and keep your consultants' calendars full.",
     "https://images.pexels.com/photos/3777946/pexels-photo-3777946.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("professional-services", "Professional Services", "Professional Services", "SDRs for consultancies, legal, accounting, and advisory firms.",
     "Professional services firms sell expertise and trust. Outbound must feel consultative, not transactional. Partners will not attend poorly qualified meetings.",
     "Our reps research prospects thoroughly, reference relevant industry challenges, and book meetings with budget holders who understand the value of expert advice. Messaging is tailored to partners, COOs, and department heads.",
     "https://images.pexels.com/photos/3184296/pexels-photo-3184296.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("technology-it", "Technology & IT", "Technology & IT", "South African SDRs for IT services, MSPs, and technology providers.",
     "Technology buyers are technical, sceptical, and time-poor. Your SDRs need to speak to infrastructure, security, and digital transformation without overpromising.",
     "We match reps who can discuss cloud migration, managed services, and enterprise IT with credibility. They target CTOs, IT directors, and procurement with messaging grounded in business outcomes.",
     "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("marketing-agencies", "Marketing Agencies", "Marketing Agencies", "Outbound SDRs for agencies selling retainers and project work.",
     "Agencies need a steady flow of new business conversations without pulling strategists off client work. Outbound must demonstrate creativity and commercial awareness.",
     "South African SDRs prospect marketing directors and founders, positioning your agency's case studies and capabilities. They book discovery calls that give your new business team a qualified head start.",
     "https://images.pexels.com/photos/6476589/pexels-photo-6476589.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("logistics", "Logistics", "Logistics", "SDRs for logistics, freight, and supply chain companies.",
     "Logistics sales is operational and relationship-driven. Buyers care about reliability, coverage, and cost. Your outreach must demonstrate industry knowledge from the first touch.",
     "Our reps target supply chain managers, operations directors, and procurement teams with messaging that speaks to routes, SLAs, and capacity. They build pipeline for freight forwarders, 3PLs, and logistics tech providers.",
     "https://images.pexels.com/photos/4483610/pexels-photo-4483610.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("manufacturing", "Manufacturing", "Manufacturing", "B2B outbound for manufacturing and industrial companies.",
     "Manufacturing buyers evaluate suppliers on quality, lead times, and total cost. SDRs must understand production cycles, certifications, and the long evaluation timelines common in industrial sales.",
     "South African reps prospect plant managers, procurement officers, and engineering leads with technically informed outreach. They book meetings that move opportunities into your sales engineers' pipelines.",
     "https://images.pexels.com/photos/1108101/pexels-photo-1108101.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
    ("cybersecurity", "Cybersecurity", "Cybersecurity", "SDRs for cybersecurity vendors and MSSPs.",
     "Cybersecurity buyers are flooded with outreach. Standing out requires credible threat language, regulatory awareness, and respect for the seriousness of the category.",
     "Our SDRs are trained on your product positioning, compliance frameworks (SOC 2, ISO 27001, GDPR), and the CISO personas you target. They book qualified discovery calls with security leaders who have real budget and urgency.",
     "https://images.pexels.com/photos/5380678/pexels-photo-5380678.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"),
]


def _industry_label(name: str) -> str:
    return name.replace("&", "&amp;")


def industry_dropdown_links(depth: int) -> str:
    return "\n                ".join(
        f'<a href="{rel(depth, f"/industries/{slug}/")}">{_industry_label(name)}</a>'
        for slug, name, *_ in INDUSTRIES
    )


def industry_mobile_links(depth: int) -> str:
    return "\n          ".join(
        f'<a href="{rel(depth, f"/industries/{slug}/")}">{_industry_label(name)}</a>'
        for slug, name, *_ in INDUSTRIES
    )


def industry_footer_links(depth: int) -> str:
    return "\n            ".join(
        f'<li><a href="{rel(depth, f"/industries/{slug}/")}">{_industry_label(name)}</a></li>'
        for slug, name, *_ in INDUSTRIES
    )


COMPARISONS = [
    ("south-africa-vs-philippines", "Philippines", "the Philippines",
     "The Philippines is one of the world's largest BPO markets with deep talent pools and competitive pricing. English is widely spoken, though accents and idioms differ from Western norms. Timezone overlap is strong for US West Coast and Australia.",
     "South Africa offers first-language English with a neutral accent, GMT+2 overlap with UK and EU, and Western business culture at a moderate cost premium over the Philippines."),
    ("south-africa-vs-india", "India", "India",
     "India offers exceptional scale, competitive pricing, and a vast educated workforce. English is an official language, though accents and communication styles vary. Timezone works well for US and UK overlap with some scheduling flexibility.",
     "South Africa provides clearer, neutral English, stronger cultural alignment with Western buyers, and GMT+2 timezone overlap ideal for UK and EU markets."),
    ("south-africa-vs-latin-america", "Latin America", "Latin America",
     "Latin America offers strong US timezone alignment, growing tech talent, and cultural affinity with North American markets. Spanish and Portuguese are common, though English proficiency is rising in major hubs.",
     "South Africa delivers first-language English, UK/EU timezone overlap, and Western business norms. Ideal when your buyers are primarily English-speaking in the UK, Europe, or US East Coast."),
    ("south-africa-vs-eastern-europe", "Eastern Europe", "Eastern Europe",
     "Eastern Europe has a strong tech and sales talent pool, competitive rates within Europe, and excellent timezone overlap with Western Europe. English proficiency is generally high in professional roles.",
     "South Africa offers lower cost than most Eastern European markets, first-language English, and strong overlap with UK hours. A compelling option for UK and US companies prioritising cost and communication clarity."),
    ("in-house-vs-outsourced", "In-house hiring", "building in-house",
     "In-house SDRs give you direct control, cultural immersion, and immediate access. But hiring is slow, expensive, and risky: recruitment fees, ramp time, turnover, and management overhead add up quickly.",
     "Outsourcing to South Africa gives you a dedicated rep at 55 to 65 percent lower cost, ramped in weeks, with recruitment and training handled for you. You keep control of playbook and tools."),
]


def steps_section() -> str:
    return """<section class="section-green section steps"><div class="container"><div class="section-head reveal"><span class="eyebrow-pill pill-on-green">How it works</span><h2>From kickoff to booked meetings in weeks, not months</h2></div>
<ol class="steps-grid"><li class="step reveal"><span class="step-num">1</span><h3>Discovery</h3><p>We learn your offer, your market and your ideal customer.</p></li>
<li class="step reveal"><span class="step-num">2</span><h3>We recruit and train</h3><p>We source, vet and train a dedicated SDR to your playbook.</p></li>
<li class="step reveal"><span class="step-num">3</span><h3>Your rep ramps</h3><p>They plug into your tools and start outreach fast.</p></li>
<li class="step reveal"><span class="step-num">4</span><h3>Pipeline flows</h3><p>Booked meetings land in your calendar, week after week.</p></li></ol></div></section>"""


def why_sa_teaser(depth: int) -> str:
    return f"""<section class="section-cream section"><div class="container">
{section_head("Why South Africa", "Western sales talent, without the Western price tag")}
<div class="pillar-grid reveal">
<article class="card pillar-card"><div class="pillar-icon" aria-hidden="true">{ICON_SVG["money"]}</div><h3>55-65% lower cost</h3><p>A South African SDR costs a fraction of a Western hire with comparable output.</p></article>
<article class="card pillar-card"><div class="pillar-icon" aria-hidden="true">{ICON_SVG["chat"]}</div><h3>First language English</h3><p>Clear, neutral English that UK and US prospects find familiar.</p></article>
<article class="card pillar-card"><div class="pillar-icon" aria-hidden="true">{ICON_SVG["clock"]}</div><h3>GMT+2 timezone</h3><p>Full UK and EU overlap, plus US East Coast mornings.</p></article>
</div>
<p style="margin-top:32px;text-align:center;"><a href="{rel(depth, '/why-south-africa/')}" class="text-link" style="color:var(--green);border-color:rgba(2,64,61,0.3);">Read the full case for South Africa <span class="arrow">→</span></a></p>
</div></section>"""


def service_page(slug, title, meta_desc, eyebrow, h1, subhead, what_heading, faqs, cta, depth=2):
    img, alt = SERVICE_IMAGES.get(slug, SERVICE_IMAGES["sdr"])
    deliverables = deliverable_grid(SERVICE_DELIVERABLES.get(slug, SERVICE_DELIVERABLES["sdr"]))
    faq_block = faq_html(faqs)
    body = f"""<main>
{page_hero(eyebrow, h1, subhead, f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a><a href="#pricing" class="btn btn-secondary">See pricing</a>', img, alt)}
<section class="section-cream section"><div class="container">
{section_head("What we do", what_heading)}
{deliverables}
</div></section>
{steps_section()}
{why_sa_teaser(depth)}
<section class="section-green section" id="pricing"><div class="container">
{section_head("Pricing", "Simple, predictable pricing", on_green=True)}
<div class="split-section reveal">
<div class="pricing-box" style="max-width:none;"><p>Pricing depends on rep count and scope. We offer flat monthly per-rep pricing with no long lock in. <a href="{CONTACT_CTA}" style="color:var(--gold);font-weight:500;">Book a call</a> for a quote tailored to your team.</p></div>
<div class="visual-panel"><h3>What you get</h3><p>A dedicated rep, recruitment, training, and ongoing support. No shared pools, no hidden fees.</p>
<div class="visual-stat-row"><span><strong>3 wks</strong><small>to ramp</small></span><span><strong>62%</strong><small>avg saving</small></span><span><strong>1:1</strong><small>dedicated rep</small></span></div></div>
</div></div></section>
<section class="section-cream section"><div class="container">
{section_head("FAQ", "Common questions")}
{faq_block}
</div></section>
{cta_band(depth, cta)}
</main>"""
    return wrap_page(f"{title} | South Africa SDR", meta_desc, depth, body, faq_schema(faqs))


def industry_page(slug, name, meta_title, meta_desc, challenge, solution, img, depth=2):
    faqs = [
        (f"Why use South African SDRs for {name}?", f"South African reps offer first-language English, Western business culture, and GMT+2 timezone overlap, at 55 to 65 percent lower cost than domestic hires."),
        (f"What titles do you target in {name}?", "We tailor prospecting to your ideal customer profile and the decision-makers that matter in your vertical."),
        (f"How quickly can a rep start?", "A trained rep can be ramping within about three weeks."),
    ]
    body = f"""<main>
{page_hero(name, f"SDRs for {name}", meta_desc, f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>', img, f"{name} professionals at work")}
<section class="section-cream section"><div class="container">
<div class="split-section reveal">
<div class="split-copy">
{section_head("The challenge", f"The {name.lower()} outbound challenge")}
<div class="prose"><p>{challenge}</p></div>
</div>
<div class="split-media"><img src="{img}" alt="{name} team at work" loading="lazy" width="800" height="520" /></div>
</div></div></section>
<section class="section-green section"><div class="container">
<div class="split-section reverse reveal">
<div class="split-copy">
{section_head("Our approach", f"How our SA reps solve it", on_green=True)}
<div class="prose prose-green"><p>{solution}</p></div>
</div>
<div class="split-media"><img src="https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop" alt="South African SDR on a sales call" loading="lazy" width="800" height="520" style="border: 3px solid rgba(250,248,242,0.1);" /></div>
</div></div></section>
<section class="section-cream section"><div class="container">
{section_head("Results", "Proof in pipeline", "Placeholder metrics until verified client data is available.")}
<div class="case-metrics reveal"><div class="case-metric"><strong>27</strong><span>meetings booked / month</span></div><div class="case-metric"><strong>9.4%</strong><span>avg reply rate</span></div><div class="case-metric"><strong>62%</strong><span>cost saved</span></div></div>
</div></section>
<section class="section-cream section" style="padding-top:0;"><div class="container">
{section_head("Services", "Relevant services")}
<div class="hub-grid reveal"><a href="{rel(depth, '/services/sdr/')}" class="hub-card"><h3>SDR Services</h3><p>Outbound prospecting and pipeline generation.</p><span class="card-link">Explore <span class="arrow">→</span></span></a>
<a href="{rel(depth, '/services/appointment-setting/')}" class="hub-card"><h3>Appointment Setting</h3><p>Qualified meetings booked to your calendar.</p><span class="card-link">Explore <span class="arrow">→</span></span></a></div>
</div></section>
<section class="section-cream section"><div class="container">
{section_head("FAQ", f"{name} FAQ")}
{faq_html(faqs)}
</div></section>
{cta_band(depth, f"Ready to build {name.lower()} pipeline?")}
</main>"""
    return wrap_page(f"SDRs for {meta_title} | South Africa SDR", meta_desc, depth, body, faq_schema(faqs))


def comparison_page(slug, name, name_the, alt_desc, sa_desc, depth=2):
    is_inhouse = slug == "in-house-vs-outsourced"
    col1 = "In-house" if is_inhouse else name
    col2 = "South Africa" if is_inhouse else "South Africa"
    hero_title = f"Choosing between South Africa and {name} for your SDR team" if not is_inhouse else "In-house vs outsourced SDR: which is right?"
    comp_img = "https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"
    faqs = [
        (f"When is {name_the} the better choice?", alt_desc[:200] + "..."),
        ("When is South Africa the better choice?", sa_desc[:200] + "..."),
        ("Can I switch later?", "Yes. We design engagements with flexibility so you can scale up, scale down, or adjust as your needs change."),
    ]
    body = f"""<main>
{page_hero("Honest comparison", hero_title, "A straight comparison on cost, English, timezone and fit, so you pick the right option for your market.", f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>', comp_img, "Team comparing outsourcing options")}
<section class="section-cream section"><div class="container">
{section_head("Compare", "Side by side")}
<div class="compare-table-wrap reveal"><table class="compare-table"><thead><tr><th>Factor</th><th>{col1}</th><th>{col2}</th></tr></thead><tbody>
<tr><td>Cost</td><td class="neutral">{"Higher (full employment cost)" if is_inhouse else "Generally lower"}</td><td class="good">55-65% less than Western hire</td></tr>
<tr><td>English</td><td class="good">Native</td><td class="good">First language, neutral accent</td></tr>
<tr><td>Timezone</td><td class="good">Your local hours</td><td class="good">GMT+2, UK/EU overlap</td></tr>
<tr><td>Scale speed</td><td class="neutral">Slow (recruit + ramp)</td><td class="good">Weeks, not months</td></tr>
<tr><td>Cultural fit</td><td class="good">Fully embedded</td><td class="good">Western business norms</td></tr>
</tbody></table></div>
</div></section>
<section class="section-cream section" style="padding-top:0;"><div class="container">
<div class="compare-cards reveal">
<div class="compare-choice alt"><h3>When {name_the} is the better choice</h3><p>{alt_desc}</p></div>
<div class="compare-choice sa"><h3>When South Africa is the better choice</h3><p>{sa_desc}</p></div>
</div></div></section>
<section class="section-cream section" style="padding-top:0;"><div class="container">
{section_head("Decide", "How to decide")}
<div class="prose reveal"><p>Match your choice to your buyer market, timezone needs, and budget. We run operations in multiple regions and will recommend the best fit, even if it is not South Africa. <a href="{CONTACT_CTA}" style="color:var(--green);font-weight:500;">Book a call</a> and we will walk through your specific situation.</p></div>
</div></section>
<section class="section-cream section"><div class="container">
{section_head("FAQ", "Comparison FAQ")}
{faq_html(faqs)}
</div></section>
{cta_band(depth, "Not sure which option fits? Let's talk.")}
</main>"""
    title = f"South Africa vs {name} for SDRs: An Honest Comparison | South Africa SDR" if not is_inhouse else "In-House vs Outsourced SDR: Which Is Right? | SA SDR"
    desc = f"Deciding between South Africa and {name} for your SDR team? A straight comparison on cost, English, timezone and fit." if not is_inhouse else "Build or buy your SDR team? Compare cost, speed, risk and control."
    return wrap_page(title, desc, depth, body, faq_schema(faqs))


def build_all():
    pages = []

    # WHY SOUTH AFRICA
    depth = 1
    why_faqs = [
        ("How much does a South African SDR cost?", "Typically 55 to 65 percent less than a US or UK hire. Exact pricing depends on rep count and scope."),
        ("Is the accent an issue for US buyers?", "No. South African English is clear and neutral, and reads as familiar to both UK and US ears."),
        ("What hours will my rep work?", "Your hours. GMT+2 covers the full UK and EU day and US mornings."),
        ("How fast can they start?", "A trained rep can be ramping within about three weeks."),
        ("How do you vet reps?", "We source, assess communication skills, run role-play exercises, and train each rep on your playbook before they go live."),
        ("Is South Africa right for every company?", "It is a strong fit for UK, EU, and US outbound. If you need 24/7 coverage at the lowest possible cost, another region may suit better."),
    ]
    why_img = "https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop"
    body = f"""<main>
{page_hero("The case for South Africa", "Why South Africa is the smartest place to build your SDR team", "Lower cost than the West, first language English, a timezone that overlaps your working day, and a business culture your prospects recognise. Here is the full picture.", f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>', why_img, "Professional team collaborating in a modern office")}
<section class="section-cream section"><div class="container"><div class="split-section reveal">
<div class="split-copy">{section_head("Cost", "The cost case")}<div class="prose"><p>A South African SDR typically costs 55 to 65 percent less than an equivalent hire in the US, UK or Australia. That is not a quality trade off, it is a currency and cost of living gap. The same money buys you more reps, more coverage and more pipeline.</p></div></div>
<div class="split-media"><img src="https://images.pexels.com/photos/4386321/pexels-photo-4386321.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop" alt="Financial planning and cost analysis" loading="lazy" /></div>
</div></div></section>
<section class="section-green section"><div class="container"><div class="split-section reverse reveal">
<div class="split-copy">{section_head("English", "The English case", on_green=True)}<div class="prose prose-green"><p>South Africa ranks first in Africa for English proficiency and sits high on the global index. English is a first language for a large, educated professional workforce. The accent reads as clear and neutral to UK and US ears, closer to home than most offshore options.</p></div></div>
<div class="split-media"><img src="https://images.pexels.com/photos/1181717/pexels-photo-1181717.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop" alt="Professional on a client call" loading="lazy" style="border:3px solid rgba(250,248,242,0.1);" /></div>
</div></div></section>
<section class="section-cream section"><div class="container"><div class="split-section reveal">
<div class="split-copy">{section_head("Timezone", "The timezone case")}<div class="prose"><p>At GMT+2, South Africa overlaps the entire UK and European working day and covers US East Coast mornings. Your rep works when your prospects work. No overnight shifts, no next day lag on replies.</p></div></div>
<div class="why-sa-stats" style="display:grid;grid-template-columns:1fr 1fr;gap:16px;"><div class="stat-block" style="background:#fff;border-color:rgba(2,64,61,0.1);"><span class="stat-figure" style="color:var(--gold);">GMT+2</span><span class="stat-label" style="color:rgba(30,38,34,0.6);">UK &amp; EU overlap</span></div><div class="stat-block" style="background:#fff;border-color:rgba(2,64,61,0.1);"><span class="stat-figure" style="color:var(--gold);">US AM</span><span class="stat-label" style="color:rgba(30,38,34,0.6);">East Coast coverage</span></div></div>
</div></div></section>
<section class="section-green section"><div class="container"><div class="split-section reveal">
<div class="split-copy">{section_head("Culture", "The cultural fit case", on_green=True)}<div class="prose prose-green"><p>South African business culture is Western in its norms, its written English and its professional expectations. Your rep will feel like part of the team, not a distant outsourced function.</p></div></div>
<div class="visual-panel" style="margin:0;"><h3>Western business norms</h3><p>Professional communication, directness, and accountability that your buyers already expect.</p><div class="visual-stat-row"><span><strong>#1</strong><small>in Africa for English</small></span><span><strong>55-65%</strong><small>cost saving</small></span></div></div>
</div></div></section>
<section class="section-cream section"><div class="container">
{section_head("Honest take", "Is South Africa right for you?")}
<div class="prose reveal"><p>South Africa is a strong fit if you sell into the UK, Europe or the US and want a Western style rep at a lower cost. If you need 24/7 coverage or very high volume at the lowest possible price, another region may suit better, and we will say so.</p><p><a href="{rel(depth, '/compare/south-africa-vs-philippines/')}" class="text-link" style="color:var(--green);border-color:rgba(2,64,61,0.3);">See our comparisons <span class="arrow">→</span></a></p></div>
</div></section>
<section class="section-cream section"><div class="container">
{section_head("FAQ", "Common questions")}
{faq_html(why_faqs)}
</div></section>
{cta_band(depth, "See the difference a South African SDR makes")}
</main>"""
    write_page("why-south-africa/index.html", wrap_page("Why Hire SDRs From South Africa? The Full Case | South Africa SDR", "Lower cost, first language English, GMT+2 timezone overlap and Western business culture. Here is why companies build their SDR teams in South Africa.", depth, body, faq_schema(why_faqs)))
    pages.append("why-south-africa/index.html")

    # SDR SERVICES
    sdr_faqs = [
        ("What does an outsourced SDR do?", "Prospecting, list building, multi-channel outreach, lead qualification, meeting booking, CRM hygiene, and activity reporting."),
        ("Is the rep dedicated to my accounts?", "Yes. Your rep works only your accounts, not a shared pool."),
        ("What tools do they use?", "Yours. They plug into your CRM, dialler, and sequencer."),
        ("How quickly can they start?", "A trained rep can be ramping within about three weeks."),
        ("How much does it cost?", "Typically 55 to 65 percent less than a US or UK hire. Book a call for a tailored quote."),
    ]
    sdr_what = "What your SDR handles"
    write_page("services/sdr/index.html", service_page("sdr", "SDR Services", "Dedicated South African SDRs who prospect, qualify and book meetings to your playbook. A fraction of the cost of a domestic hire.", "SDR Services", "Outsourced SDRs who fill your pipeline", "Dedicated South African sales development reps who prospect, qualify and book meetings for your team. Trained to your playbook, working your hours, at a fraction of a domestic hire.", sdr_what, sdr_faqs, "Let's build your pipeline."))
    pages.append("services/sdr/index.html")

    # APPOINTMENT SETTING
    appt_faqs = [
        ("What is the difference between SDR and appointment setting?", "Appointment setters focus solely on booking qualified meetings. SDRs handle broader pipeline generation including prospecting and qualification."),
        ("Do you qualify leads before booking?", "Yes. Every meeting is qualified against your criteria before it lands on your calendar."),
        ("Can they work across time zones?", "Yes. We coordinate scheduling across UK, EU, and US time zones."),
    ]
    appt_what = "What your appointment setter handles"
    write_page("services/appointment-setting/index.html", service_page("appointment-setting", "Appointment Setting", "Qualified sales meetings booked straight to your calendar by trained South African appointment setters.", "Appointment Setting", "Qualified meetings, booked to your calendar", "South African appointment setters focused on one outcome: qualified meetings booked directly to your calendar. Your hours, your CRM, your criteria.", appt_what, appt_faqs, "Fill your calendar with qualified meetings."))
    pages.append("services/appointment-setting/index.html")

    # CUSTOMER SERVICE
    cs_faqs = [
        ("What channels do you support?", "Email, chat, and phone support, tailored to your customer base."),
        ("Can reps handle escalations?", "Yes. We train reps on your escalation paths and tone of voice."),
    ]
    cs_what = "What your CS rep handles"
    write_page("services/customer-service/index.html", service_page("customer-service", "Customer Service", "Keep customers happy and revenue retained with South African customer service reps.", "Customer Service", "Customer service that protects revenue", "Dedicated South African reps who handle enquiries, resolve issues, and keep customers retained. First language English and Western business culture.", cs_what, cs_faqs, "Keep your customers happy."))
    pages.append("services/customer-service/index.html")

    # TECHNICAL SUPPORT
    ts_faqs = [
        ("What tier of support do you provide?", "Tier 1 and tier 2 product support, with clear escalation to your engineering team."),
        ("Do reps need technical backgrounds?", "We recruit for product aptitude and train on your specific product and documentation."),
    ]
    ts_what = "What your support rep handles"
    write_page("services/technical-support/index.html", service_page("technical-support", "Technical Support", "Protect the customer relationship with skilled South African technical support reps.", "Technical Support", "Technical support that protects the relationship", "Product-savvy South African support that resolves technical issues and protects the customer relationship. Clear English, your timezone, lower cost.", ts_what, ts_faqs, "Protect your customer relationships."))
    pages.append("services/technical-support/index.html")

    # SERVICES OVERVIEW
    d = 1
    svc_body = f"""<main>
{page_hero("Services", "Built around sales, backed by support", "Dedicated South African teams for outbound pipeline and the support functions that keep revenue moving.", f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>', "https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", "Sales and support teams at work")}
<section class="section-cream section"><div class="container">
{section_head("Our services", "Sales first, support behind it", "Each service is scoped to your playbook, tools, and market.")}
<div class="services-grid reveal">
<a href="{rel(d, '/services/sdr/')}" class="service-feature"><span class="service-feature-media"><img src="https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop" alt="SDR team" loading="lazy" /></span><span class="service-feature-body"><span class="service-tag">Sales</span><h3>SDR Services</h3><p class="service-outcome">Outbound reps who research, reach out, and build qualified pipeline.</p><span class="card-link">Explore <span class="arrow">→</span></span></span></a>
<a href="{rel(d, '/services/appointment-setting/')}" class="service-feature"><span class="service-feature-media"><img src="https://images.pexels.com/photos/1181717/pexels-photo-1181717.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop" alt="Appointment setting" loading="lazy" /></span><span class="service-feature-body"><span class="service-tag">Sales</span><h3>Appointment Setting</h3><p class="service-outcome">Qualified meetings booked directly to your calendar.</p><span class="card-link">Explore <span class="arrow">→</span></span></span></a>
<a href="{rel(d, '/services/customer-service/')}" class="service-feature"><span class="service-feature-media"><img src="https://images.pexels.com/photos/8867442/pexels-photo-8867442.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop" alt="Customer service" loading="lazy" /></span><span class="service-feature-body"><span class="service-tag service-tag-support">Support</span><h3>Customer Service</h3><p class="service-outcome">Keep customers happy and revenue retained.</p><span class="card-link">Explore <span class="arrow">→</span></span></span></a>
<a href="{rel(d, '/services/technical-support/')}" class="service-feature"><span class="service-feature-media"><img src="https://images.pexels.com/photos/442150/pexels-photo-442150.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop" alt="Technical support" loading="lazy" /></span><span class="service-feature-body"><span class="service-tag service-tag-support">Support</span><h3>Technical Support</h3><p class="service-outcome">Product support that protects the relationship.</p><span class="card-link">Explore <span class="arrow">→</span></span></span></a>
</div></div></section>
{cta_band(d, "Not sure which service fits? Book a fit call.")}
</main>"""
    write_page("services/index.html", wrap_page("Our Services | Sales, Support & More | South Africa SDR", "Outsourced SDRs, appointment setting, customer service and technical support from South Africa.", d, svc_body))
    pages.append("services/index.html")

    # INDUSTRIES OVERVIEW
    ind_cards = ""
    for slug, name, *_rest in INDUSTRIES:
        img = _rest[-1] if _rest else ""
        ind_cards += f'''<a href="{rel(d, f"/industries/{slug}/")}" class="industry-card">
<span class="industry-card-media"><img src="{img}" alt="{name}" loading="lazy" width="600" height="400" /></span>
<span class="industry-card-body"><span class="industry-card-title">{name}</span><span class="arrow" aria-hidden="true">→</span></span>
</a>\n'''
    ind_body = f"""<main>
{page_hero("Industries", "SDRs who already speak your industry", "We match reps and messaging to your market, from SaaS to logistics.", f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>', "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", "Diverse industries and markets")}
<section class="section-cream section"><div class="container">
{section_head("Industries", "Reps tuned to your vertical", "From SaaS to logistics, we match messaging and prospecting to your market.")}
<div class="industry-grid reveal">{ind_cards}</div>
</div></section>
{cta_band(d, "Ready to match an SDR to your industry?")}
</main>"""
    write_page("industries/index.html", wrap_page("SDRs by Industry | South Africa SDR", "Outsourced SDRs matched to your market, from SaaS to logistics.", d, ind_body))
    pages.append("industries/index.html")

    # INDUSTRY PAGES
    for slug, name, meta_title, meta_desc, challenge, solution, img in INDUSTRIES:
        path = f"industries/{slug}/index.html"
        write_page(path, industry_page(slug, name, meta_title, meta_desc, challenge, solution, img))
        pages.append(path)

    # COMPARISON PAGES
    for slug, name, name_the, alt_desc, sa_desc in COMPARISONS:
        path = f"compare/{slug}/index.html"
        write_page(path, comparison_page(slug, name, name_the, alt_desc, sa_desc))
        pages.append(path)

    # FAQ
    all_faqs = [
        ("Why hire SDRs from South Africa?", "Lower cost than the West, first language English, GMT+2 timezone overlap with the UK and EU, and a Western business culture."),
        ("Will the accent be an issue for US or UK prospects?", "No. South African English is clear and neutral, and reads as familiar to both UK and US ears."),
        ("What hours will my SDR work?", "Your hours. GMT+2 covers the full UK and EU day and US mornings."),
        ("How much does an outsourced SDR cost?", "Typically 55 to 65 percent less than a US or UK hire. Exact pricing depends on rep count and scope."),
        ("Is there a long contract?", "We keep commitments flexible. Book a call to discuss terms that work for your team."),
        ("How quickly can a rep start?", "A trained rep can be ramping within about three weeks."),
        ("Do I get a dedicated rep or a shared one?", "Dedicated. Your rep works only your accounts."),
        ("What tools do they use?", "Yours. They plug into your CRM, dialler and sequencer."),
        ("How do you vet and train SDRs?", "We source candidates, assess communication skills, run role-play exercises, and train each rep on your playbook before they go live."),
    ]
    faq_sections = [
        ("About South Africa", all_faqs[0:3]),
        ("About pricing", all_faqs[3:5]),
        ("About how it works", all_faqs[5:8]),
        ("About the reps", all_faqs[8:9]),
    ]
    faq_content = ""
    for sec_title, items in faq_sections:
        icon = FAQ_CAT_ICONS.get(sec_title, "chat")
        faq_content += f'''<div class="faq-category reveal">
<div class="faq-category-head"><span class="faq-cat-icon" aria-hidden="true">{ICON_SVG[icon]}</span><h3>{sec_title}</h3></div>
{faq_html(items)}</div>'''
    faq_body = f"""<main>
{page_hero("FAQ", "SDR outsourcing FAQ", "Straight answers on cost, accents, hours, ramp time and how we vet reps.", f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>', "https://images.pexels.com/photos/7688336/pexels-photo-7688336.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", "Team discussing sales strategy")}
<section class="section-cream section"><div class="container"><div class="faq-layout reveal">
<div class="faq-side">
{section_head("Answers", "Everything you need to know")}
<div class="visual-panel"><h3>Still unsure?</h3><p>Book a 20 minute call. We will walk through your market, goals, and whether South Africa is the right fit.</p><a href="{CONTACT_CTA}" class="btn btn-primary" style="margin-top:20px;display:inline-block;">Book a call</a></div>
<div class="faq-side-img"><img src="https://images.pexels.com/photos/3184296/pexels-photo-3184296.jpeg?auto=compress&cs=tinysrgb&w=600&h=750&fit=crop" alt="Professional consultation" loading="lazy" /></div>
</div>
<div>{faq_content}</div>
</div></div></section>
{cta_band(1, "Still have questions? Book a call.")}
</main>"""
    write_page("faq/index.html", wrap_page("SDR Outsourcing FAQ | South Africa SDR", "Common questions on hiring South African SDRs: cost, accents, hours, ramp time and how we vet reps.", 1, faq_body, faq_schema(all_faqs)))
    pages.append("faq/index.html")

    # BOOK
    book_body = f"""<main>
<div class="book-layout">
<div>
<h1>Book a 20 minute call</h1>
<p class="hero-subhead">Tell us about your sales goals and we will show you exactly how a South African SDR would work for you. No pressure, no hard sell.</p>
<ul class="book-ticks"><li>See real cost and pipeline numbers</li><li>Understand the process</li><li>Leave with a clear next step</li></ul>
{calendly_placeholder()}
</div>
<div class="book-visual">
<img src="https://images.pexels.com/photos/1181717/pexels-photo-1181717.jpeg?auto=compress&cs=tinysrgb&w=600&h=800&fit=crop" alt="Consultation call" loading="lazy" />
<div class="trust-strip" style="margin-top:24px;border-radius:12px;"><div class="container" style="padding:24px;"><p class="trust-label">Trusted by growing sales teams</p><div class="trust-logos"><span class="trust-logo">Fernbrook</span><span class="trust-logo">Latitude&amp;Co</span></div></div></div>
</div>
</div>
</main>"""
    write_page("book/index.html", wrap_page("Book a Call | South Africa SDR", "Book a 20 minute call to see exactly how a South African SDR would work for your team.", 1, book_body, minimal_header=True))
    pages.append("book/index.html")

    # CONTACT
    contact_body = f"""<main>
<section class="section-cream section" style="padding-top: calc(var(--header-offset) + 48px);"><div class="container contact-layout reveal">
<div class="card" style="padding:32px;">
{section_head("Message", "Send a message")}
<script src="https://www.cognitoforms.com/f/seamless.js" data-key="aUkYm0vkIEepZiVXFt6QrQ" data-form="184"></script>
</div>
<div>
{section_head("Book", "Or book a call")}
{calendly_placeholder()}
<div class="contact-info" style="margin-top:28px;">
<h3>Direct contact</h3>
<div class="contact-info-item"><svg viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M3 7l9 6 9-6" stroke="currentColor" stroke-width="1.6"/></svg><a href="mailto:hello@southafricasdr.com" style="color:inherit;">hello@southafricasdr.com</a></div>
<div class="contact-info-item"><svg viewBox="0 0 24 24" fill="none"><path d="M6.5 4h3l1.2 4.2-2 1.2a13 13 0 0 0 5.1 5.1l1.2-2 4.2 1.2v3a2 2 0 0 1-2 2C10.4 18.7 5.3 13.6 5.3 6.5A2 2 0 0 1 6.5 4Z" stroke="currentColor" stroke-width="1.6"/></svg><a href="tel:+27123456789" style="color:inherit;">+27 12 345 6789</a></div>
<div class="contact-info-item"><svg viewBox="0 0 24 24" fill="none"><path d="M12 21s6-5.2 6-10a6 6 0 1 0-12 0c0 4.8 6 10 6 10Z" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="11" r="2.2" stroke="currentColor" stroke-width="1.6"/></svg><span>Cape Town, South Africa (GMT+2)</span></div>
</div>
</div>
</div></section>
{page_closing(1)}
</main>"""
    write_page("contact/index.html", wrap_page("Contact Us | South Africa SDR", "Book a call or send a message. We reply within one business day.", 1, contact_body, plain=True))
    pages.append("contact/index.html")

    # ABOUT
    about_body = f"""<main>
{page_hero("About", "We build outsourced South African sales teams", "For companies in the US, UK and Australia who want pipeline without the Western price tag.", f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>', "https://images.pexels.com/photos/3184296/pexels-photo-3184296.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", "Team collaborating in a modern workspace")}
<section class="section-cream section"><div class="container">
<div class="split-section reveal">
<div class="split-copy">
{section_head("Our story", "Western sales talent, built in South Africa")}
<div class="prose"><p>South Africa SDR helps Western sales teams scale outbound with dedicated South African reps. We handle recruitment, training, and ongoing support so you get a rep who sounds right, works your hours, and costs a fraction of a domestic hire.</p><p>Our team combines sales operations experience with deep knowledge of the South African talent market. We have placed reps across SaaS, fintech, recruitment, professional services, and more.</p><p>We believe in honest recommendations. South Africa is not always the right answer, and we will tell you when another option fits better.</p></div>
</div>
<div class="why-sa-stats" style="display:grid;grid-template-columns:1fr;gap:16px;">
<div class="stat-block" style="background:#fff;border-color:rgba(2,64,61,0.1);"><span class="stat-figure" style="color:var(--gold);">55-65%</span><span class="stat-label" style="color:rgba(30,38,34,0.6);">average cost saving</span></div>
<div class="stat-block" style="background:#fff;border-color:rgba(2,64,61,0.1);"><span class="stat-figure" style="color:var(--gold);">3 weeks</span><span class="stat-label" style="color:rgba(30,38,34,0.6);">to a ramped rep</span></div>
</div>
</div>
<div class="about-values reveal">
<div class="value-card"><div class="deliverable-icon" aria-hidden="true">{ICON_SVG["shield"]}</div><h3>Honest advice</h3><p>We recommend the right region, even when it is not South Africa.</p></div>
<div class="value-card"><div class="deliverable-icon" aria-hidden="true">{ICON_SVG["users"]}</div><h3>Dedicated reps</h3><p>Your rep works only your accounts, never a shared pool.</p></div>
<div class="value-card"><div class="deliverable-icon" aria-hidden="true">{ICON_SVG["chart"]}</div><h3>Pipeline focus</h3><p>Everything we do is measured in meetings booked and pipeline built.</p></div>
</div>
</div></section>
{steps_section()}
{cta_band(1, "Ready to meet your next SDR?")}
</main>"""
    write_page("about/index.html", wrap_page("About Us | South Africa SDR", "We build outsourced South African sales teams for companies in the US, UK and Australia.", 1, about_body))
    pages.append("about/index.html")

    # CASE STUDIES HUB
    cases = [
        ("saas-pipeline-case-study", "B2B SaaS", "UK SaaS company books 27 meetings in month one", "A London-based SaaS startup replaced a stalled in-house hire with a South African SDR.", "27 meetings", "9.4% reply rate", "62% cost saved"),
        ("fintech-appointment-setting", "Fintech", "US fintech scales appointment setting", "A New York fintech needed US-morning coverage without the cost of a domestic team.", "34 meetings", "11% reply rate", "58% cost saved"),
    ]
    case_cards = ""
    for slug, ind, title, desc, *metrics in cases:
        case_cards += f'<a href="{rel(1, f"/case-studies/{slug}/")}" class="hub-card"><span class="blog-meta">{ind}</span><h3>{title}</h3><p>{desc}</p><span class="card-link">Read case study <span class="arrow">→</span></span></a>'
    cs_hub = f"""<main>
{page_hero("Case Studies", "Real results from South African SDR teams", "Meetings booked, pipeline built, cost saved. See the proof.", f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>', "https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", "Sales team celebrating results")}
<section class="section-cream section"><div class="container">
{section_head("Proof", "Client results")}
<div class="hub-grid reveal">{case_cards}</div>
<p class="prose" style="margin-top:32px;font-size:14px;color:rgba(30,38,34,0.55);">Placeholder case studies. Replace with verified client data when available.</p>
</div></section>
{cta_band(1, "Want results like these?")}
</main>"""
    write_page("case-studies/index.html", wrap_page("Case Studies | South Africa SDR", "Real results from South African SDR teams: meetings booked, pipeline built, cost saved.", 1, cs_hub))
    pages.append("case-studies/index.html")

    for slug, ind, title, desc, m1, m2, m3 in cases:
        cs_body = f"""<main>
{page_hero(ind, title, desc, f'<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>', "https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=800&h=520&fit=crop", title, True)}
<section class="section-cream section" style="padding-top:0;"><div class="container article-body reveal">
<div class="case-metrics"><div class="case-metric"><strong>{m1.split()[0]}</strong><span>{' '.join(m1.split()[1:])}</span></div><div class="case-metric"><strong>{m2.split()[0]}</strong><span>{' '.join(m2.split()[1:])}</span></div><div class="case-metric"><strong>{m3.split()[0]}</strong><span>{' '.join(m3.split()[1:])}</span></div></div>
<h2>The challenge</h2><p>{desc} They needed a rep who could ramp fast, work their hours, and book qualified meetings without the cost of a domestic hire.</p>
<h2>Our approach</h2><p>We recruited and trained a dedicated South African SDR on their playbook, ICP, and messaging. The rep plugged into their CRM and sequencer within the first week.</p>
<h2>Results</h2><p>Within the first month, the rep exceeded the pipeline output of their previous in-house hire. Placeholder data: replace with verified client metrics.</p>
<blockquote style="border-left:3px solid var(--gold);padding-left:20px;margin:28px 0;font-style:italic;color:rgba(30,38,34,0.8);">"Our rep booked more qualified meetings in her first month than our last in-house hire managed in a quarter." <cite style="display:block;margin-top:10px;font-style:normal;font-size:14px;color:rgba(30,38,34,0.55);">VP Sales, placeholder</cite></blockquote>
<p><a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a></p>
</div></div></section>
{page_closing(2, "Want results like these?")}
</main>"""
        path = f"case-studies/{slug}/index.html"
        write_page(path, wrap_page(f"{title} | South Africa SDR", desc, 2, cs_body))
        pages.append(path)

    # SUCCESS PAGES
    for path, title, msg in [
        ("success/booking-confirmed/index.html", "Booking confirmed", "Your call is booked. We look forward to speaking with you. Check your email for calendar details and a brief prep guide."),
        ("success/contact-received/index.html", "Message received", "Thanks for reaching out. We reply within one business day. In the meantime, feel free to book a call directly."),
        ("success/subscribed/index.html", "You are subscribed", "Thanks for subscribing. You will receive our latest insights on outbound and offshore SDR strategy."),
    ]:
        depth = path.count("/") - 1
        sbody = f"""<main class="success-page"><div class="success-inner reveal">
<div class="success-icon" aria-hidden="true">✓</div>
<h1>{title}</h1>
<p>{msg}</p>
<a href="{CONTACT_CTA}" class="btn btn-primary">Book a call</a>
<a href="{rel(depth, '/')}" class="btn btn-outline-green" style="margin-left:12px;">Back to home</a>
</div>
{page_closing(depth, "Ready to build your pipeline?")}
</main>"""
        write_page(path, wrap_page(f"{title} | South Africa SDR", msg, depth, sbody, noindex=True, plain=True))
        pages.append(path)

    # LEGAL PAGES
    legal_template = """<main>
{hero}
<section class="section-cream section"><div class="container"><div class="split-section reveal">
<div class="legal-content">{content}</div>
<div class="split-media"><img src="https://images.pexels.com/photos/7688336/pexels-photo-7688336.jpeg?auto=compress&cs=tinysrgb&w=600&h=750&fit=crop" alt="Professional workspace" loading="lazy" style="border-radius:16px;" /></div>
</div></div></section>
{closing}
</main>"""
    legal_pages = [
        ("privacy", "Privacy Policy", "<h2>Introduction</h2><p>South Africa SDR (\"we\", \"us\") respects your privacy. This policy explains how we collect, use, and protect personal information when you visit southafricasdr.com or contact us.</p><h2>Information we collect</h2><p>We collect information you provide via contact forms, call bookings, and email correspondence: name, work email, company, and message content.</p><h2>How we use your information</h2><p>We use your information to respond to enquiries, schedule calls, and provide our services. We do not sell your personal data.</p><h2>Data retention</h2><p>We retain contact data for as long as needed to fulfil the purposes above or as required by law.</p><h2>Your rights</h2><p>Under POPIA and GDPR, you may request access, correction, or deletion of your personal data. Contact hello@southafricasdr.com.</p><h2>Contact</h2><p>hello@southafricasdr.com, Cape Town, South Africa.</p>"),
        ("terms", "Terms of Service", "<h2>Agreement</h2><p>By using southafricasdr.com, you agree to these terms. If you do not agree, please do not use the site.</p><h2>Services</h2><p>South Africa SDR provides outsourced sales development and related services. Specific terms for engagements are agreed in separate service agreements.</p><h2>Website content</h2><p>Content on this site is for general information. We make reasonable efforts to ensure accuracy but do not guarantee completeness.</p><h2>Limitation of liability</h2><p>We are not liable for indirect or consequential damages arising from use of this website.</p><h2>Governing law</h2><p>These terms are governed by the laws of South Africa.</p><h2>Contact</h2><p>hello@southafricasdr.com</p>"),
        ("cookies", "Cookie Policy", "<h2>What are cookies</h2><p>Cookies are small text files stored on your device when you visit a website.</p><h2>How we use cookies</h2><p>We use essential cookies for site functionality. With your consent, we may use analytics and advertising cookies (GA4, Meta Pixel, LinkedIn) to understand traffic and improve marketing.</p><h2>Managing cookies</h2><p>You can control cookies through your browser settings. A cookie consent banner will allow you to accept or reject non-essential cookies.</p><h2>Contact</h2><p>Questions? Email hello@southafricasdr.com.</p>"),
    ]
    for slug, title, content in legal_pages:
        hero = page_hero("Legal", title, "", single_col=True)
        write_page(f"{slug}/index.html", wrap_page(f"{title} | South Africa SDR", f"{title} for South Africa SDR.", 1, legal_template.format(hero=hero, content=content, closing=page_closing(1))))
        pages.append(f"{slug}/index.html")

    # 404
    err_body = f"""<main class="error-page section-cream"><div class="container reveal">
<div class="error-code">404</div>
<h1>Page not found</h1>
<p class="prose" style="max-width:420px;margin:0 auto;">The page you are looking for does not exist or has been moved.</p>
<div class="error-links">
<a href="{rel(0, '/')}" class="btn btn-primary">Back to home</a>
<a href="{CONTACT_CTA}" class="btn btn-outline-green">Book a call</a>
<a href="{rel(0, '/faq/')}" class="btn btn-outline-green">FAQ</a>
</div>
{page_closing(0)}
</div></main>"""
    write_page("404.html", wrap_page("Page Not Found | South Africa SDR", "The page you are looking for does not exist.", 0, err_body, noindex=True, plain=True))
    pages.append("404.html")

    print(f"\nBuilt {len(pages)} pages.")
    return pages


if __name__ == "__main__":
    build_all()
