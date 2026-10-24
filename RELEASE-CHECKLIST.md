# Release checklist — forgeiec.io

Steps for the owner before the redesign goes live. Work top to bottom;
the last step publishes.

> **Merging to `main` publishes the site.** `.forgejo/workflows/deploy.yml`
> runs on every push to `main`, builds with `hugo --minify` and copies
> `public/` by `rsync --delete` to `root@forgeiec.io:/var/www/forgeiec.io/public/`.
> There is no staging step in between.

Open points in the text are HTML comments starting with `ENTWURF:`.
Overview: `grep -rn 'ENTWURF' content/de content/en layouts`.

## 1. Legal pages

- [ ] **Impressum** — fill every `[Angabe des Eigentümers …]` field.
  Files: `content/de/impressum.md` (authoritative), `content/en/impressum.md`.
  Markers: `ENTWURF: Alle Felder in eckigen Klammern füllt der Eigentümer` (de),
  `ENTWURF: All bracketed fields are to be filled by the owner` (en).
- [ ] **Datenschutz / Privacy** — fill controller, hosting, log retention,
  mail provider, deletion period, supervisory authority, date.
  Files: `content/de/datenschutz.md` (authoritative), `content/en/datenschutz.md` (URL `/en/privacy/`).
  Markers: `ENTWURF: Datenschutzerklärung — Felder in eckigen Klammern …`,
  `ENTWURF: Rechtsprüfung nötig: TDDDG §25 und DSGVO Art. 6` (section *Cookies und lokale Speicherung*),
  `ENTWURF: Abschnitt aus contact-service/DATENSCHUTZ-ABSCHNITT.md übernommen …` (section *Kontaktformular*,
  including the open question whether the form's checkbox is consent or acknowledgement).

## 2. Legal review

- [ ] **CLA** — `content/de/cla.md`, `content/en/cla.md` (English is authoritative).
  Both carry the visible callout "Entwurf — rechtlich prüfen" / "Draft — legal review required";
  remove it after the review. Related marker in `content/{de,en}/entwickler/mitmachen.md`:
  `ENTWURF: Die CLA ist noch nicht anwaltlich geprüft …` (the link there appears once the CLA is published).
- [ ] **Licence FAQ on the home page** — `content/de/_index.md` and `content/en/_index.md`
  (front matter `faq.items`), marker `ENTWURF: Lizenz-FAQ (faq.items) muss … von einem Anwalt gelesen werden`;
  template marker in `layouts/index.html` (`ENTWURF: Lizenz-FAQ ist ein Entwurf`).
- [ ] **Privacy texts** — all of `content/{de,en}/datenschutz.md` (see step 1),
  including the contact-form section and the no-consent-banner reasoning (§ 25 TDDDG).
- [ ] **Trademark notice** — `content/{de,en}/markenrechtshinweis.md`,
  marker `ENTWURF: Der folgende Satz (nicht-kommerziell, ehrenamtlich) widerspricht den Eigentümer-Fakten …`.

## 3. Contact service (server)

- [ ] Install `forgeiec-contact` on the web server as described in
  `contact-service/README.md`, section *Install (once, as root on the web server)*:
  code, `/etc/forgeiec-contact/env`, systemd unit `contact-service/forgeiec-contact.service`.
- [ ] Add the nginx parts from `contact-service/nginx-contact.conf`: the zone line
  to `/etc/nginx/conf.d/forgeiec-contact-zone.conf`, the `location /api/contact/`
  block into the HTTPS `server {}` of forgeiec.io; `nginx -t`, reload.
- [ ] **Secrets** in `/etc/forgeiec-contact/env` (root, 0600): `CONTACT_SECRET`
  (at least 32 characters: `python3 -c "import secrets; print(secrets.token_urlsafe(48))"`),
  `CONTACT_MAIL_FROM`; for a remote relay also `CONTACT_SMTP_USER` and
  `CONTACT_SMTP_PASSWORD` or `CONTACT_SMTP_PASSWORD_FILE`. Template: `contact-service/env.example`.
- [ ] Check the local MTA (README, *Local MTA check list*: SPF/DKIM for the sender address)
  and send one test message (README, *Test with curl*; this sends one real mail).

## 4. Content from the owner

- [ ] **Developer page: CV and role** — `content/de/entwickler/_index.md`
  (`ENTWURF: Werdegang/Lebenslauf-Link fehlt`, `ENTWURF: Zielrolle und Form (Festanstellung/freiberuflich) fehlen`)
  and `content/en/entwickler/_index.md` (`ENTWURF: CV / career link missing`, `ENTWURF: target role and form … missing`).
- [ ] **Windows download address** — `content/de/download/_index.md` and
  `content/en/download/_index.md`, section *Windows*: currently "installer on request";
  replace with the download URL once a public build exists.
  RPM table in the same files: `ENTWURF: RPM-Tabelle nach Audit W-09 …` — verify against rpm.forgeiec.io.
- [ ] **Fork year** — `content/de/news/die-forgeiec-geschichte.md` and
  `content/en/news/die-forgeiec-geschichte.md`, marker `ENTWURF: Jahr des Forks offen`
  (git shows own work from February 2026, the owner says 2018; no year without evidence).
- [ ] **IL statement, Annex B** — read Annex B of IEC 61131-3:2025 before the IL/AWL
  sentence is quoted as a statement about the standard. Files: `content/{de,en}/plattform/forge-studio.md`,
  `content/{de,en}/help/il/index.md` (marker `ENTWURF: Annex B der Norm einsehen …`);
  the same wording is in `content/{de,en}/roadmap.md`.
- [ ] Other owner decisions (each marked `ENTWURF:`): Rivet target group, gateway hardware and
  pilot offer (`content/{de,en}/rivet.md`); Rivet/Hearth version numbers and CODESYS import
  (`content/{de,en}/roadmap.md`); Modbus RTU delivery (`content/{de,en}/plattform/tongs.md`);
  Spark (`content/de/plattform/verbund.md`); rusty plan (`content/{de,en}/partner/index.md`, news posts);
  wording of "Arbeit mit KI-Werkzeugen" (`content/{de,en}/entwickler/engineering-praxis.md`).
- [ ] Screenshots: `make screenshots-missing` lists the placeholders still shown
  ("Screenshot folgt"); scheme and capture rules in `static/img/screenshots/README.md`.

## 5. Publish the drafts

- [ ] Delete the line `draft: true` in `content/{de,en}/impressum.md`,
  `content/{de,en}/datenschutz.md` and `content/{de,en}/cla.md` — only after steps 1 and 2.
  The footer links (Impressum, Datenschutz, CLA), the cookie notice in the footer and the
  privacy link in the contact form appear automatically once the pages are published.
- [ ] Remove the "Entwurf"/"Draft" callouts at the top of these pages.
- [ ] Check: `hugo --quiet --minify -d ~/.cache/forgeiec-build/check` prints nothing; open
  `/de/impressum/`, `/de/datenschutz/`, `/en/privacy/`, `/de/cla/` and the privacy link on `/de/kontakt/`.

## 6. Go live

- [ ] Merge the release branch (`website-release`) into `main` and push.
  **This publishes:** the deploy workflow builds and rsyncs to `root@forgeiec.io`
  (`/var/www/forgeiec.io/public/`, with `--delete`).
- [ ] Afterwards: open https://forgeiec.io/de/ and /en/, send one message through the form and
  check that the header button "Pilotprojekt anfragen" opens the form with the subject preselected.
