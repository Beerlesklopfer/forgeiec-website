# ForgeIEC Website - Build & Deploy
# Hugo static site → forgeiec.io (eigener Server via rsync)

HUGO        ?= hugo
DEPLOY_HOST ?= forgeiec.io
DEPLOY_USER ?= root
DEPLOY_PATH ?= /var/www/forgeiec.io/public/
DEPLOY_SSH  ?= $(DEPLOY_USER)@$(DEPLOY_HOST)

.DEFAULT_GOAL := help
.PHONY: help build serve deploy clean

# Default target: show usage
help:
	@echo "ForgeIEC Website (Hugo) — verfuegbare Targets:"
	@echo ""
	@echo "  make help     Zeigt diese Hilfe (Default-Target)"
	@echo "  make build    Baut die statische Site nach public/ (mit Minify)"
	@echo "  make serve    Lokaler Dev-Server mit Live-Reload"
	@echo "                  (lauscht auf 0.0.0.0, Drafts inkludiert)"
	@echo "  make deploy   Build + rsync nach $(DEPLOY_SSH):$(DEPLOY_PATH)"
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
