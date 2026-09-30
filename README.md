# Edwin's Projects — gilzone.github.io

A password-protected gallery of Edwin's HTML projects, hosted free on GitHub Pages.

## How it works

- `index.html` — password gate + project gallery. The gate compares the SHA-256 hash
  of the entered password against `PASS_HASH` in the page's script. Unlock state is
  kept in `sessionStorage`, so closing the tab/browser locks it again.
- `projects/<name>/index.html` — one folder per project. The sample project shows
  the structure; every project page links back to the gallery with `../../`.
- To change the site password: compute `sha256` of the new password and replace
  the `PASS_HASH` value in `index.html`.

## Adding a new project

1. Create `projects/<project-name>/` and put the project's files in it
   (its main page must be `index.html`).
2. In `index.html`, copy one of the `.proj` cards inside `.grid`, update the
   title, description, and `href` to `projects/<project-name>/`.
3. Commit and push — GitHub Pages redeploys automatically in about a minute.
