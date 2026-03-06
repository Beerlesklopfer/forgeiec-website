# ForgeIEC Website - Build & Deploy
# Hugo static site → forgeiec.io (eigener Server via rsync)

HUGO        ?= hugo
DEPLOY_HOST ?= forgeiec.io
DEPLOY_USER ?= root
DEPLOY_PATH ?= /var/www/forgeiec.io/public/
DEPLOY_SSH  ?= $(DEPLOY_USER)@$(DEPLOY_HOST)

.PHONY: build serve deploy clean

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
