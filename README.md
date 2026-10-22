# forgeiec.io — website

Hugo site for <https://forgeiec.io>. German (`content/de`, default) and
English (`content/en`) are built; the content directories of ar, es, fr,
ja, tr and zh stay in the repository but are not configured in
`hugo.toml` and therefore not built.

**Publishing:** every push to `main` is built and deployed by
`.forgejo/workflows/deploy.yml` (rsync to `root@forgeiec.io`). Merging to
`main` publishes the site. Before that, work through
[RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md).

## Build

Requirements: Hugo extended (tested with 0.168), `make`. No Node, no CDN:
the site loads no third-party scripts, styles, fonts or images.

```sh
make build        # HUGO_ENV=production hugo --minify  -> public/
make serve        # dev server with live reload, drafts included (0.0.0.0)
make clean        # remove public/ and resources/_gen/
make sync-schemas # copy the XSDs from ../schemas/ to static/schemas/
make help         # all targets and variables
```

A check build that must print nothing (no warnings):

```sh
make check   # hugo --quiet --minify, without and with --buildDrafts, to ~/.cache/forgeiec-build/check
```

`make deploy` (build + rsync from your machine) exists for emergencies;
the normal path is the deploy workflow on `main`.

## Layout of the repository

| Path | Content |
|---|---|
| `hugo.toml` | languages, menus, `ctaHref` (target of the pilot button) |
| `content/de`, `content/en` | pages; `translationKey` links the two languages |
| `layouts/` | templates of the redesign (`_default/baseof.html`, `partials/`, `shortcodes/`) |
| `assets/css/forge.css`, `assets/css/parts/*.css` | design system, concatenated and fingerprinted into one file |
| `static/css/contact.css`, `static/js/contact.js` | contact form (loaded only by the `contact-form` shortcode) |
| `static/img/screenshots/` | program screenshots, see below |
| `contact-service/` | backend of the contact form (Python stdlib, systemd, nginx) |

## Drafts

Pages with `draft: true` are not built and not linked: the footer links
and the cookie notice use `partials/page-link.html` / `site.GetPage`, so
they appear only once the page is published. Current drafts:

- `content/{de,en}/impressum.md`
- `content/{de,en}/datenschutz.md` (English URL `/en/privacy/`)
- `content/{de,en}/cla.md`

Preview them with `make serve` or `hugo --buildDrafts`. Publish a page by
deleting its `draft: true` line (after the steps in the release checklist).

## Open points in the text (ENTWURF markers)

Open questions for the owner are HTML comments starting with `ENTWURF:`
(invisible on the site). List them with:

```sh
grep -rn 'ENTWURF' content layouts     # or: make entwurf
```

Only the built languages: `grep -rn 'ENTWURF' content/de content/en layouts`.

## Screenshots

Screenshots are referenced with a shortcode; as long as the file does not
exist the page shows a marked placeholder ("Screenshot folgt").

```
{{</* screenshot program="rivet" name="gateway-setup" alt="…" caption="…" */>}}
```

File scheme: `static/img/screenshots/<program>/<name>-<version>.png`
(or `.webp`), e.g. `studio/editor-st-0.2.0.png`; the newest version is
used. Current program versions: `static/img/screenshots/versions.txt`.
The list of screens, capture rules and the shortcode lines for every page
are in [static/img/screenshots/README.md](static/img/screenshots/README.md).

```sh
make screenshots-missing   # placeholders still on the site, as <program>/<name>
make screenshots-list      # existing files with version, outdated ones flagged
```

## Contact form

The pages `/de/kontakt/` and `/en/contact/` embed `{{</* contact-form */>}}`.
The pilot buttons link to `?type=pilot`, which preselects the subject
(`pilot`, `licence`, `partnership`, `job`, `other` are accepted). The form
posts to `/api/contact/` on the same host; nginx forwards that to the
`forgeiec-contact` service. Without the service the form shows an error
with the e-mail address as fallback.

Install, configuration, nginx block and tests:
[contact-service/README.md](contact-service/README.md). The tests run
offline against a fake SMTP server:

```sh
cd contact-service && python3 -m unittest -v
```
