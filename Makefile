# ForgeIEC Website - Build & Deploy
# Hugo static site → forgeiec.io (eigener Server via rsync)

HUGO        ?= hugo
DEPLOY_HOST ?= forgeiec.io
DEPLOY_USER ?= root
DEPLOY_PATH ?= /var/www/forgeiec.io/public/
DEPLOY_SSH  ?= $(DEPLOY_USER)@$(DEPLOY_HOST)

.DEFAULT_GOAL := help
.PHONY: help build check serve deploy clean sync-schemas screenshots-missing screenshots-list entwurf

# Studio-Repo Root, in dem die Quell-XSDs liegen. Wird beim
# sync-schemas-Target aus dem Submodule-Verzeichnis raus auf
# documentation/schemas/ resolved.
STUDIO_SCHEMAS_DIR ?= ../schemas

# Default target: show usage
help:
	@echo "ForgeIEC Website (Hugo) — verfuegbare Targets:"
	@echo ""
	@echo "  make help     Zeigt diese Hilfe (Default-Target)"
	@echo "  make build    Baut die statische Site nach public/ (mit Minify)"
	@echo "  make check    Pruef-Build ohne und mit Drafts nach $(CHECK_DIR) (muss still sein)"
	@echo "  make entwurf  Listet alle ENTWURF-Marker (offene Punkte fuer den Eigentuemer)"
	@echo "  make serve    Lokaler Dev-Server mit Live-Reload"
	@echo "                  (lauscht auf 0.0.0.0, Drafts inkludiert)"
	@echo "  make deploy   Build + rsync nach $(DEPLOY_SSH):$(DEPLOY_PATH)"
	@echo "  make sync-schemas   XSDs aus ../schemas/ in static/schemas/ syncen"
	@echo "  make clean    Loescht public/ und resources/_gen/"
	@echo "  make screenshots-missing  Listet Screenshot-Stubs (<program>/<name>)"
	@echo "  make screenshots-list     Vorhandene Screenshots mit Version, veraltete markiert"
	@echo ""
	@echo "Variablen (per make VAR=value oder Environment ueberschreibbar):"
	@echo "  HUGO          $(HUGO)"
	@echo "  DEPLOY_HOST   $(DEPLOY_HOST)"
	@echo "  DEPLOY_USER   $(DEPLOY_USER)"
	@echo "  DEPLOY_PATH   $(DEPLOY_PATH)"

# Build static site into public/
build:
	HUGO_ENV=production $(HUGO) --minify

# Check build: must print nothing. Without drafts (what main publishes)
# and with drafts (Impressum, Datenschutz, CLA). Output outside /tmp.
CHECK_DIR ?= $(HOME)/.cache/forgeiec-build/check
check:
	$(HUGO) --quiet --minify --cleanDestinationDir -d $(CHECK_DIR)/public
	$(HUGO) --quiet --minify --cleanDestinationDir --buildDrafts -d $(CHECK_DIR)/drafts

# Open points for the owner (HTML comments "ENTWURF: ...").
entwurf:
	@grep -rn 'ENTWURF' content layouts

# Local development server with live reload
serve:
	$(HUGO) server -D --bind 0.0.0.0

# Deploy to own server via rsync
deploy: build
	@echo "Deploying to $(DEPLOY_SSH):$(DEPLOY_PATH) ..."
	rsync -avz --delete public/ $(DEPLOY_SSH):$(DEPLOY_PATH)
	@echo "Deployed to https://$(DEPLOY_HOST)/"

# Remove generated files
clean:
	rm -rf public/ resources/_gen/

# Sync the canonical XSD-Quellen aus documentation/schemas/ ins
# static/schemas/ Verzeichnis dieser Website. Studio-Repo ist die
# single source of truth fuer die Schema-Files; Website re-published
# sie 1:1 unter https://forgeiec.io/schemas/.
#
# Aufruf:    make sync-schemas
# Override:  make sync-schemas STUDIO_SCHEMAS_DIR=/path/to/schemas
sync-schemas:
	@echo "Syncing schemas from $(STUDIO_SCHEMAS_DIR)/ -> static/schemas/"
	@mkdir -p static/schemas
	@# Drop any stale .xsd that no longer exists upstream (the per-NS
	@# split in 2026-05-21 dropped the monolithic forgeiec-v2.xsd).
	@for stale in static/schemas/*.xsd; do \
	  [ -f "$$stale" ] || continue; \
	  base=$$(basename "$$stale"); \
	  if [ ! -f "$(STUDIO_SCHEMAS_DIR)/$$base" ]; then \
	    rm -f "$$stale"; \
	    echo "  rm stale $$base"; \
	  fi; \
	done
	@# Pull the current upstream set
	@for f in tc6_0201.xsd \
	          forgeiec-v2-variable.xsd \
	          forgeiec-v2-task.xsd \
	          forgeiec-v2-bus-config.xsd \
	          forgeiec-v2-comments.xsd \
	          forgeiec-v2-sanitize-map.xsd \
	          forgeiec-v2-hearth.xsd \
	          README.md; do \
	  if [ -f "$(STUDIO_SCHEMAS_DIR)/$$f" ]; then \
	    cp "$(STUDIO_SCHEMAS_DIR)/$$f" static/schemas/$$f; \
	    echo "  cp $$f"; \
	  else \
	    echo "  WARN: $$f missing in $(STUDIO_SCHEMAS_DIR)/"; \
	  fi; \
	done
	@echo "Sync done. Review with: git diff static/schemas/"

# ---- Screenshots (static/img/screenshots/README.md) ----
SHOTS_DIR := static/img/screenshots

# Build into a temp dir and list every placeholder (data-stub attribute,
# survives --minify) as <program>/<name>.
screenshots-missing:
	@tmp=$$(mktemp -d); \
	$(HUGO) --quiet -d "$$tmp" >/dev/null || { rm -rf "$$tmp"; exit 1; }; \
	grep -rhoE 'data-stub="[^"]+"' "$$tmp" | sed -E 's/data-stub="([^"]+)"/\1/' | sort -u; \
	rm -rf "$$tmp"

# List existing screenshots with their version; flag a file as outdated
# when the program's current version (versions.txt) is newer than the
# newest screenshot of that program/name.
screenshots-list:
	@find $(SHOTS_DIR) -mindepth 2 -maxdepth 2 -type f \( -name '*.png' -o -name '*.webp' \) \
	  | sed -nE 's|^$(SHOTS_DIR)/([^/]+)/(.+)-([0-9]+\.[0-9]+\.[0-9]+)\.(png\|webp)$$|\1 \2 \3|p' \
	  | sort -k1,1 -k2,2 -k3,3V \
	  | awk 'NR==FNR { if ($$0 !~ /^#/ && NF >= 2) cur[$$1] = $$2; next } \
	         { key = $$1 "/" $$2; ver[key] = $$3; prog[key] = $$1 } \
	         END { n = 0; for (k in ver) { n++; c = cur[prog[k]]; flag = ""; \
	               if (c != "") { cmd = "printf \"%s\\n%s\\n\" " ver[k] " " c " | sort -V | tail -1"; \
	                 cmd | getline top; close(cmd); if (top != ver[k]) flag = "  outdated (current " c ")"; } \
	               printf "%-32s %s%s\n", k, ver[k], flag } \
	               if (n == 0) print "(no screenshots yet)" }' $(SHOTS_DIR)/versions.txt -
