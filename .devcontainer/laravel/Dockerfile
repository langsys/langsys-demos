FROM mcr.microsoft.com/devcontainers/php:1-8.3

# ext-intl gives the demo real ICU plurals and locale-formatted dates/numbers.
# Baked into the image so it runs as root at build and a failure breaks the
# build loudly instead of silently degrading the demo.
#
# Two base-image quirks handled here (both verified by building this image):
# - it does NOT include mlocati's install-php-extensions helper, so the
#   extension is built the plain way via docker-php-ext-install;
# - it ships a yarn apt source whose GPG key is stale, which fails every
#   `apt-get update` — the demo doesn't need yarn, so drop the source.
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends libicu-dev \
    && docker-php-ext-install intl \
    && rm -rf /var/lib/apt/lists/*
