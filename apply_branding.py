#!/usr/bin/env python3
"""Apply new South Africa SDR brand system across styles.css, build_pages.py, and HTML files."""

import re
from pathlib import Path

ROOT = Path(__file__).parent

FONTS_LINK = """<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600&family=Montserrat:wght@600;700&display=swap" rel="stylesheet">"""

FAVICON_LINKS = """<link rel="icon" href="/images/brand/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/images/brand/favicon.svg">"""

OLD_CDN_LOGO = "https://cdn.prod.website-files.com/6a550e6bc10b48cf2b0d2a00/6a5514db15499cf55b0299bd_logo.png"
LOGO_HORIZONTAL = "/images/brand/lockup-horizontal.svg"
LOGO_HORIZONTAL_REV = "/images/brand/lockup-horizontal-rev.svg"

# CSS variable block (new brand)
NEW_ROOT = """:root {
  /* Brand palette — South Africa SDR */
  --green: #02403D;           /* Deep green, primary */
  --forest: #012B28;          /* Darkest sections, footer */
  --green-darker: #012B28;
  --gold: #DAA866;            /* Accent */
  --gold-dark: #B8945A;
  --clay: #B8945A;            /* Legacy alias */
  --green-support: #3A7A72;
  --cream: #FAF8F2;
  --sand: #F1ECE1;
  --ink: #1E2622;
  --muted: #6B7168;
  --hairline: #E7E1D5;
  --white: #FFFFFF;
  --btn-ink: #02403D;

  --font-display: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-sans: "Hanken Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-serif: var(--font-display);

  --radius-btn: 9px;
  --radius-card: 14px;
  --shadow-soft: 0 10px 30px rgba(0, 0, 0, 0.12);
  --shadow-float: 0 30px 60px rgba(1, 43, 40, 0.35);

  --container: 1180px;
  --header-offset: 82px;

  --footer-caramel: #F1ECE1;
  --footer-brown: #B8945A;
}"""

CSS_REPLACEMENTS = [
    ("/* 1.2 Colour palette */", "/* Brand palette */"),
    ("/* South Africa SDR · Home page\n   Brand system from the Website Build Guide (June 2026)", "/* South Africa SDR\n   Brand system — Montserrat + Hanken Grotesk"),
    ("#1E4D40", "#02403D"),
    ("#173F34", "#012B28"),
    ("#E0A458", "#DAA866"),
    ("#C96F4A", "#B8945A"),
    ("#3F8E76", "#3A7A72"),
    ("#FBF7F0", "#FAF8F2"),
    ("#163A30", "#1E2622"),
    ("#1E3A2E", "#02403D"),
    ("#B27B33", "#B8945A"),
    ('"Fraunces", Georgia, serif', 'var(--font-display)'),
    ('"Inter", -apple-system', '"Hanken Grotesk", -apple-system'),
    ("rgba(22, 58, 48,", "rgba(30, 38, 34,"),
    ("rgba(22,58,48,", "rgba(30,38,34,"),
    ("rgba(30, 77, 64,", "rgba(2, 64, 61,"),
    ("rgba(30,77,64,", "rgba(2,64,61,"),
    ("rgba(224, 164, 88,", "rgba(218, 168, 102,"),
    ("rgba(224,164,88,", "rgba(218,168,102,"),
    ("rgba(251, 247, 240,", "rgba(250, 248, 242,"),
    ("rgba(251,247,240,", "rgba(250,248,242,"),
    ("rgba(10, 30, 24,", "rgba(1, 43, 40,"),
    ("rgba(63, 142, 118,", "rgba(58, 122, 114,"),
]

FOOTER_CSS = """
/* Footer — forest brand band */
.site-footer {
  background: var(--forest);
  border-top: none;
  padding: 48px 0 36px;
  color: rgba(250, 248, 242, 0.75);
}

.footer-tagline {
  font-size: 14px;
  line-height: 1.5;
  color: rgba(250, 248, 242, 0.55);
  text-align: right;
  max-width: 340px;
}

.footer-divider {
  height: 1px;
  background: rgba(250, 248, 242, 0.12);
  margin-bottom: 40px;
}

.footer-col h4 {
  font-family: var(--font-sans);
  font-size: 14px;
  font-weight: 600;
  color: var(--cream);
  margin-bottom: 18px;
  letter-spacing: -0.01em;
}

.footer-links a {
  font-size: 14px;
  line-height: 1.45;
  color: rgba(250, 248, 242, 0.58);
  transition: color 0.2s ease;
}

.footer-links a:hover { color: var(--gold); }

.footer-contact-item {
  color: rgba(250, 248, 242, 0.58);
}

a.footer-contact-item:hover { color: var(--gold); }

.footer-contact-icon {
  background: rgba(218, 168, 102, 0.15);
  color: var(--gold);
}

.footer-social-link {
  border: 1px solid rgba(250, 248, 242, 0.18);
  color: rgba(250, 248, 242, 0.75);
  background: transparent;
}

.footer-social-link:hover {
  color: var(--gold);
  border-color: rgba(218, 168, 102, 0.45);
  background: rgba(250, 248, 242, 0.06);
}

.footer-copy {
  font-size: 13px;
  color: rgba(250, 248, 242, 0.45);
}

.footer-legal a {
  font-size: 13px;
  color: rgba(250, 248, 242, 0.45);
  transition: color 0.2s ease;
}

.footer-legal a:hover { color: var(--gold); }

.footer-logo-img {
  height: 36px;
  width: auto;
  object-fit: contain;
}
"""

BTN_PRIMARY_CSS = """
.btn-primary {
  background: var(--green);
  color: var(--cream);
  box-shadow: 0 8px 22px rgba(2, 64, 61, 0.22);
}

.btn-primary:hover {
  background: var(--forest);
  color: var(--cream);
  transform: translateY(-2px);
  box-shadow: 0 12px 26px rgba(1, 43, 40, 0.28);
}
"""

SECTION_SAND_CSS = """
.section-sand { background: var(--sand); color: var(--ink); }
"""


def apply_css_replacements(css: str) -> str:
    for old, new in CSS_REPLACEMENTS:
        css = css.replace(old, new)
    return css


def replace_root_block(css: str) -> str:
    return re.sub(
        r":root\s*\{[^}]+\}",
        NEW_ROOT.strip(),
        css,
        count=1,
        flags=re.DOTALL,
    )


def patch_styles_css():
    path = ROOT / "styles.css"
    css = path.read_text(encoding="utf-8")
    css = replace_root_block(css)
    css = apply_css_replacements(css)

    # Headings use display font
    css = css.replace(
        "h1, h2, h3 {\n  font-family: var(--font-serif);",
        "h1, h2, h3 {\n  font-family: var(--font-display);",
    )

    # Trust strip
    css = css.replace(
        ".trust-strip {\n  background: #012B28;",
        ".trust-strip {\n  background: var(--forest);",
    )

    # Footer block replacement
    css = re.sub(
        r"/\* =+\s*\n\s*Footer[\s\S]*?\.footer-legal a:hover \{ color: var\(--green\); \}",
        FOOTER_CSS.strip(),
        css,
        count=1,
    )

    # Button primary
    css = re.sub(
        r"\.btn-primary \{[^}]+\}\s*\n\s*\.btn-primary:hover \{[^}]+\}",
        BTN_PRIMARY_CSS.strip(),
        css,
        count=1,
    )

    # Section sand after section-cream
    if ".section-sand" not in css:
        css = css.replace(
            ".section-cream { background: var(--cream); color: var(--ink); }",
            ".section-cream { background: var(--cream); color: var(--ink); }\n" + SECTION_SAND_CSS.strip(),
        )

    # Logo sizing for horizontal lockup
    css = css.replace(".logo-img {\n  width: auto;\n  height: 34px;", ".logo-img {\n  width: auto;\n  height: 38px;")
    css = css.replace(".site-header.scrolled .logo-img { height: 30px; }", ".site-header.scrolled .logo-img { height: 34px; }")
    css = css.replace(".footer-logo-img {\n  height: 32px;", ".footer-logo-img {\n  height: 36px;")

    path.write_text(css, encoding="utf-8")
    print("  updated styles.css")


def patch_build_pages():
    path = ROOT / "build_pages.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        'LOGO = "https://cdn.prod.website-files.com/6a550e6bc10b48cf2b0d2a00/6a5514db15499cf55b0299bd_logo.png"',
        f'LOGO = "{LOGO_HORIZONTAL}"\nLOGO_REV = "{LOGO_HORIZONTAL_REV}"',
    )
    text = text.replace(
        'class="logo-img" width="200" height="40"',
        'class="logo-img" width="220" height="40"',
    )
    text = text.replace(
        'class="footer-logo-img" width="180" height="36"',
        'class="footer-logo-img" width="200" height="36"',
    )
    text = text.replace(
        '<img src="{LOGO}" alt="South Africa SDR" class="footer-logo-img"',
        '<img src="{LOGO_REV}" alt="South Africa SDR" class="footer-logo-img"',
    )
    text = text.replace(
        'family=Fraunces:ital,opsz,wght,SOFT@0,9..144,400,100;0,9..144,600,100;1,9..144,400,100;1,9..144,600,100&family=Inter:wght@400;500;600',
        'family=Hanken+Grotesk:wght@400;500;600&family=Montserrat:wght@600;700',
    )
    text = apply_css_replacements(text)
    path.write_text(text, encoding="utf-8")
    print("  updated build_pages.py")


def patch_html_file(path: Path, depth: int = 0):
    text = path.read_text(encoding="utf-8")
    prefix = "../" * depth if depth else ""

    # Fonts
    text = re.sub(
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com">[\s\S]*?family=Inter[^"]*" rel="stylesheet">',
        FONTS_LINK,
        text,
        count=1,
    )

    # Favicon
    text = re.sub(
        r'<link rel="icon" href="[^"]*"[^>]*>\s*<link rel="apple-touch-icon" href="[^"]*">',
        FAVICON_LINKS.replace("/images/", f"{prefix}images/" if depth else "/images/"),
        text,
        count=1,
    )
    if 'rel="icon"' not in text and "<head>" in text:
        text = text.replace("<head>", f"<head>\n  {FAVICON_LINKS}", 1)

    # Logos in header/footer (keep depth-relative paths for nested pages)
    logo = f"{prefix}images/brand/lockup-horizontal.svg".lstrip("/") if depth else LOGO_HORIZONTAL
    logo_rev = f"{prefix}images/brand/lockup-horizontal-rev.svg".lstrip("/") if depth else LOGO_HORIZONTAL_REV
    if depth:
        logo = prefix + "images/brand/lockup-horizontal.svg"
        logo_rev = prefix + "images/brand/lockup-horizontal-rev.svg"

    text = text.replace(OLD_CDN_LOGO, logo)
    # Footer gets reversed logo — replace second occurrence in footer
    if 'class="footer-logo"' in text and logo_rev not in text:
        parts = text.split('class="footer-logo"', 1)
        if len(parts) == 2:
            rest = parts[1].split(logo, 1)
            if len(rest) == 2:
                text = parts[0] + 'class="footer-logo"' + rest[0] + logo_rev + rest[1]

    # Schema.org logo
    text = text.replace(
        f'"logo": "{OLD_CDN_LOGO}"',
        f'"logo": "https://southafricasdr.com/images/brand/lockup-horizontal.svg"',
    )
    text = text.replace(
        f'"logo": "{logo}"',
        f'"logo": "https://southafricasdr.com/images/brand/lockup-horizontal.svg"',
    )

    # Inline CSS in HTML files — replace :root and color tokens
    if "<style>" in text:
        def repl_style(m):
            block = apply_css_replacements(m.group(0))
            block = replace_root_block(block)
            return block

        # Only patch first large style block
        text = re.sub(r"<style>[\s\S]*?</style>", repl_style, text, count=1)

    path.write_text(text, encoding="utf-8")


def sync_index_html():
    """Sync index.html CSS from styles.css and patch logos/fonts."""
    index = ROOT / "index.html"
    styles = (ROOT / "styles.css").read_text(encoding="utf-8")
    extra = "\n.footer-nav-grid { grid-template-columns: repeat(4, minmax(120px, 1fr)); }\n"
    html = index.read_text(encoding="utf-8")

    # Replace inline style block
    html = re.sub(
        r"<style>[\s\S]*?</style>",
        f"<style>\n{styles}\n{extra}\n</style>",
        html,
        count=1,
    )

    # Fonts comment + link
    html = re.sub(
        r"<!-- Fonts:[^>]*-->\s*<link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\">[\s\S]*?display=swap\" rel=\"stylesheet\">",
        f"<!-- Fonts: Montserrat (headings) + Hanken Grotesk (body) -->\n  {FONTS_LINK}",
        html,
        count=1,
    )

    # Favicon
    html = re.sub(
        r"<!-- Favicons[^>]*-->\s*<link rel=\"icon\"[^>]*>\s*<link rel=\"apple-touch-icon\"[^>]*>",
        f"<!-- Favicons -->\n  {FAVICON_LINKS}",
        html,
        count=1,
    )

    # Logos
    html = html.replace(OLD_CDN_LOGO, LOGO_HORIZONTAL)
    # Footer logo — find footer-logo section
    html = re.sub(
        r'(class="footer-logo"[^>]*>[\s\S]*?src=")([^"]+)(")',
        rf'\1{LOGO_HORIZONTAL_REV}\3',
        html,
        count=1,
    )
    html = html.replace(
        '"logo": "https://cdn.prod.website-files.com/6a550e6bc10b48cf2b0d2a00/6a5514db15499cf55b0299bd_logo.png"',
        '"logo": "https://southafricasdr.com/images/brand/lockup-horizontal.svg"',
    )

    index.write_text(html, encoding="utf-8")
    print("  updated index.html")


def main():
    print("Applying brand updates...")
    patch_styles_css()
    patch_build_pages()

    # Regenerate inner pages
    import build_pages
    build_pages.build_all()

    sync_index_html()
    print("Branding applied successfully.")


if __name__ == "__main__":
    main()
