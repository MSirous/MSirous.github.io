# Mahsa Research Workbench

Source for [msirous.github.io](https://msirous.github.io/), built with Quarto and Jupyter.

## Content workflow

- `projects/` contains research case studies.
- `lab/` contains Quarto documents and Jupyter notebooks.
- `publish: false` in document front matter keeps drafts out of listings.
- Notebook outputs can be frozen so expensive computations are not repeated on every site build.

## Local preview

```bash
quarto preview
```

## Production build

```bash
quarto render
```

Every push to `main` executes the notebooks, validates local links, and deploys the rendered site to GitHub Pages.
