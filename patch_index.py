from pathlib import Path

ROOT = Path(__file__).parent
CONTACT = "http://www.southafricasdr.com/contact"
css = (ROOT / "styles.css").read_text(encoding="utf-8")
js = (ROOT / "script.js").read_text(encoding="utf-8")
extra_css = """
.footer-nav-grid { grid-template-columns: repeat(4, minmax(120px, 1fr)); }
@media (max-width: 760px) { .footer-nav-grid { grid-template-columns: 1fr 1fr; } }
"""
html = (ROOT / "index.html").read_text(encoding="utf-8")
html = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>\n{css}\n{extra_css}\n</style>")
html = html.replace('<script src="script.js"></script>', f"<script>\n{js}\n</script>")
replacements = {
    'href="/"': 'href="index.html"',
    'href="/why-south-africa/"': 'href="why-south-africa/index.html"',
    'href="/about/"': 'href="about/index.html"',
    'href="/contact/"': 'href="contact/index.html"',
    'href="/book/"': f'href="{CONTACT}"',
    'href="/services/"': 'href="services/index.html"',
    'href="/services/sdr/"': 'href="services/sdr/index.html"',
    'href="/services/appointment-setting/"': 'href="services/appointment-setting/index.html"',
    'href="/services/customer-service/"': 'href="services/customer-service/index.html"',
    'href="/services/technical-support/"': 'href="services/technical-support/index.html"',
    'href="/industries/"': 'href="industries/index.html"',
    'href="/industries/saas/"': 'href="industries/saas/index.html"',
    'href="/industries/financial-services/"': 'href="industries/financial-services/index.html"',
    'href="/industries/real-estate/"': 'href="industries/real-estate/index.html"',
    'href="/industries/insurance/"': 'href="industries/insurance/index.html"',
    'href="/industries/healthcare/"': 'href="industries/healthcare/index.html"',
    'href="/industries/recruitment/"': 'href="industries/recruitment/index.html"',
    'href="/industries/professional-services/"': 'href="industries/professional-services/index.html"',
    'href="/industries/technology-it/"': 'href="industries/technology-it/index.html"',
    'href="/industries/marketing-agencies/"': 'href="industries/marketing-agencies/index.html"',
    'href="/industries/logistics/"': 'href="industries/logistics/index.html"',
    'href="/industries/manufacturing/"': 'href="industries/manufacturing/index.html"',
    'href="/industries/cybersecurity/"': 'href="industries/cybersecurity/index.html"',
    'href="/blog/"': 'href="blog/index.html"',
    'href="/case-studies/"': 'href="case-studies/index.html"',
    'href="/faq/"': 'href="faq/index.html"',
    'href="/compare/south-africa-vs-philippines/"': 'href="compare/south-africa-vs-philippines/index.html"',
    'href="/compare/south-africa-vs-india/"': 'href="compare/south-africa-vs-india/index.html"',
    'href="/compare/south-africa-vs-latin-america/"': 'href="compare/south-africa-vs-latin-america/index.html"',
    'href="/compare/south-africa-vs-eastern-europe/"': 'href="compare/south-africa-vs-eastern-europe/index.html"',
    'href="/compare/in-house-vs-outsourced/"': 'href="compare/in-house-vs-outsourced/index.html"',
    'href="/terms/"': 'href="terms/index.html"',
    'href="/privacy/"': 'href="privacy/index.html"',
    'href="/cookies/"': 'href="cookies/index.html"',
}
for old, new in replacements.items():
    html = html.replace(old, new)
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("index.html updated")
