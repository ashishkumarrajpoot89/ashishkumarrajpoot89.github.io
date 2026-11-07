"""
Freeze the Flask app into static HTML for GitHub Pages.

Run:  FREEZE=1 python freeze.py        (PowerShell: $env:FREEZE=1; python freeze.py)
Output goes to the ./build directory, which GitHub Pages serves.

Note: the contact form uses Formspree in the static build (set FORMSPREE_ENDPOINT).
Server-only routes (/contact/submit) are skipped since static hosting can't run them.
"""
import os

os.environ.setdefault("FREEZE", "1")

from flask_frozen import Freezer
from app import app, PROJECTS, SITE_URL

# Base URL path on GitHub Pages. For a project page the site lives at
# https://<user>.github.io/<repo>/, so assets must be prefixed with /<repo>.
# Override with SITE_BASE env var; defaults to /portfolio.
app.config["FREEZER_DESTINATION"] = os.path.join(os.path.dirname(__file__), "build")
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True
# The /about, /skills, ... routes return redirects (to #anchors) and
# /contact/submit is POST-only. Ignore redirects so freezing doesn't fail.
app.config["FREEZER_REDIRECT_POLICY"] = "ignore"
# Only freeze the real pages we list; don't auto-crawl every endpoint.
app.config["FREEZER_IGNORE_404_NOT_FOUND"] = True

freezer = Freezer(app, with_no_argument_rules=False, log_url_for=False)


@freezer.register_generator
def home():
    yield {}


@freezer.register_generator
def project_detail():
    for p in PROJECTS:
        yield {"slug": p["slug"]}


def write_seo_files(dest):
    """Write robots.txt and sitemap.xml at the build root."""
    base = SITE_URL.rstrip("/")
    urls = [base + "/"] + [f"{base}/projects/{p['slug']}/" for p in PROJECTS]
    entries = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    with open(os.path.join(dest, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + "\n</urlset>\n")
    with open(os.path.join(dest, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n")


if __name__ == "__main__":
    freezer.freeze()
    write_seo_files(app.config["FREEZER_DESTINATION"])
    # GitHub Pages: add .nojekyll so it serves files/folders starting with _ as-is.
    open(os.path.join(app.config["FREEZER_DESTINATION"], ".nojekyll"), "w").close()
    print("Static site written to ./build")
