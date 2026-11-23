# alihashemi-ai.github.io

Personal academic website of Ali Hashemi, Ph.D. — built with [Hugo](https://gohugo.io/).

## Local development

```bash
hugo server -D
```

Visit `http://localhost:1313/`.

## Structure

- `content/` — page front matter (Home, Publications, CV, Contact, Projects)
- `data/` — structured content: `experience.yaml`, `education.yaml`, `awards.yaml`,
  `skills.yaml`, `talks.yaml`, `news.yaml`, `publications.yaml`, `projects.yaml`.
  Edit these to update the site — no template changes needed for routine content
  updates.
- `layouts/` — custom sidebar-profile theme (no external theme dependency)
- `static/files/Ali_Hashemi_CV.pdf` — downloadable CV, linked from the sidebar
- `static/images/profile.jpg` — the sidebar portrait
- `static/js/scrollcraft.js` — a small vanilla-JS scroll engine (MIT, from
  [nateherkai/scroll-craft](https://github.com/nateherkai/scroll-craft)), used only
  for its `data-sc-in` (fade-up on scroll entry) and `data-sc-tilt` (pointer tilt
  on project cards) attributes. See the comment block at the top of the file for
  the full attribute reference if you want to use more of it.

## Deployment

Pushing to `main` triggers `.github/workflows/hugo.yml`, which builds the site with
Hugo and deploys it to GitHub Pages via GitHub Actions.

**One-time setup:** in the repo settings, under **Settings → Pages**, set
**Source** to **GitHub Actions**.
