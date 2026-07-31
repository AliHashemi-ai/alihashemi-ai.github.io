# alihashemi-ai.github.io

Personal academic website of Ali Hashemi, Ph.D. — built with [Hugo](https://gohugo.io/).

## Local development

```bash
hugo server -D
```

Visit `http://localhost:1313/`.

## Structure

- `content/` — page front matter (Home, Publications, CV, Contact)
- `data/` — structured content: `experience.yaml`, `education.yaml`, `awards.yaml`,
  `skills.yaml`, `talks.yaml`, `news.yaml`, `publications.yaml`. Edit these to update
  the site — no template changes needed for routine content updates.
- `layouts/` — custom minimal theme (no external theme dependency)
- `static/files/Ali_Hashemi_CV.pdf` — downloadable CV, linked from the CV page
- `static/images/` — replace the placeholder monogram avatar by adding a photo here
  and updating `layouts/index.html` to use an `<img>` instead of the `.avatar` initials

## Deployment

Pushing to `main` triggers `.github/workflows/hugo.yml`, which builds the site with
Hugo and deploys it to GitHub Pages via GitHub Actions.

**One-time setup:** in the repo settings, under **Settings → Pages**, set
**Source** to **GitHub Actions**.
