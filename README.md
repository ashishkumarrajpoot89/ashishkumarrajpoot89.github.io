# Ashish Kumar Rajpoot — Portfolio

A single-page data-professional portfolio built with **Python + Flask**, themed in Combo 09
(Vulcanico orange `#FF4103` on Noturno navy `#001621`). It runs as a live Flask app or can be
exported to static HTML for GitHub Pages.

**Live:** https://ashishkumarrajpoot89.github.io/

## Sections
Home (hero + stats) · About · Skills · Projects (+ detail pages) · Experience · Education ·
Resume (download/view) · Contact · custom 404.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000  (debug auto-reload on).

## Edit content
All text (profile, skills, projects, experience, education, learning) lives in the data
dictionaries at the top of **`app.py`** — edit there and the whole site updates.

## Regenerate assets
- **Resume PDF** (one page, from resume content):
  ```bash
  pip install reportlab
  python generate_resume_pdf.py        # -> static/resume.pdf
  ```
  Prefer your own PDF? Just drop it in as `static/resume.pdf`.
- **Social share image** (1200x630 OG card):
  ```bash
  pip install pillow
  python generate_og_image.py          # -> static/img/og-image.png
  ```

## Build static site (GitHub Pages)

```bash
# PowerShell:  $env:FREEZE=1; python freeze.py
FREEZE=1 python freeze.py              # -> ./build
```
The contact form posts to Formspree in the static build; set your endpoint via the
`FORMSPREE_ENDPOINT` env var (or a repo secret of the same name for CI). If it is empty or
unset, the contact section shows email / LinkedIn / GitHub buttons instead of the form.
`freeze.py` also writes `robots.txt` and `sitemap.xml` into `./build`.

## Deployment
- **GitHub Pages** (static): pushing to `main` triggers `.github/workflows/deploy-pages.yml`,
  which runs `freeze.py` and publishes `./build`. Pages source = GitHub Actions.
- **Render / Railway** (live Flask app): uses `Procfile` (`gunicorn app:app`) and `render.yaml`.

## Project structure
```
portfolio/
├── app.py                  # Flask app + all site content
├── freeze.py               # Frozen-Flask static export
├── generate_resume_pdf.py  # builds static/resume.pdf
├── generate_og_image.py    # builds static/img/og-image.png
├── requirements.txt
├── Procfile / render.yaml  # live-host config
├── .github/workflows/      # GitHub Pages auto-deploy
├── templates/              # base + index + project_detail + 404 + partials
└── static/                 # css, js, img, resume.pdf
```
