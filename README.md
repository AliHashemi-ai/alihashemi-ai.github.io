# alihashemi-ai.github.io

Personal academic website of Ali Hashemi, Ph.D. — built with [Hugo](https://gohugo.io/).

## Local development

```bash
hugo server -D
```

Visit `http://localhost:1313/`.

## Structure

- A single scrolling page (`layouts/index.html`), built from the design in
  `site-template.html` (kept at the repo root as the design reference — see the
  comment at its top for the rules).
- `data/` — structured content: `experience.yaml`, `education.yaml`, `awards.yaml`,
  `news.yaml`, `publications.yaml`, `projects.yaml`, `talks.yaml`, `skills.yaml`.
  Edit these to update the site — no template changes needed for routine content
  updates.
- `static/css/site.css` — the template's stylesheet, copied in unchanged; only the
  two color-token blocks at the top should ever change.
- `static/files/Ali_Hashemi_CV.pdf` — downloadable CV, linked from the hero.

## Deployment

Pushing to `main` triggers `.github/workflows/hugo.yml`, which builds the site with
Hugo and deploys it to GitHub Pages via GitHub Actions.

**One-time setup:** in the repo settings, under **Settings → Pages**, set
**Source** to **GitHub Actions**.
