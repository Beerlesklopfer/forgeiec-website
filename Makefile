# ForgeIEC Website - Build & Deploy
# Hugo static site → forgeiec.io (eigener Server via rsync)

HUGO        ?= hugo
DEPLOY_HOST ?= forgeiec.io
DEPLOY_USER ?= root
DEPLOY_PATH ?= /var/www/forgeiec.io/public/
DEPLOY_SSH  ?= $(DEPLOY_USER)@$(DEPLOY_HOST)

.DEFAULT_GOAL := help
.PHONY: help build serve deploy clean sync-schemas

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
	@echo "  make serve    Lokaler Dev-Server mit Live-Reload"
	@echo "                  (lauscht auf 0.0.0.0, Drafts inkludiert)"
	@echo "  make deploy   Build + rsync nach $(DEPLOY_SSH):$(DEPLOY_PATH)"
	@echo "  make sync-schemas   XSDs aus ../schemas/ in static/schemas/ syncen"
	@echo "  make clean    Loescht public/ und resources/_gen/"
	@echo ""
	@echo "Variablen (per make VAR=value oder Environment ueberschreibbar):"
	@echo "  HUGO          $(HUGO)"
	@echo "  DEPLOY_HOST   $(DEPLOY_HOST)"
	@echo "  DEPLOY_USER   $(DEPLOY_USER)"
	@echo "  DEPLOY_PATH   $(DEPLOY_PATH)"

# Build static site into public/
build:
	$(HUGO) --minify

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
	          README.md; do \
	  if [ -f "$(STUDIO_SCHEMAS_DIR)/$$f" ]; then \
	    cp "$(STUDIO_SCHEMAS_DIR)/$$f" static/schemas/$$f; \
	    echo "  cp $$f"; \
	  else \
	    echo "  WARN: $$f missing in $(STUDIO_SCHEMAS_DIR)/"; \
	  fi; \
	done
	@echo "Sync done. Review with: git diff static/schemas/"
