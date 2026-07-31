FROM mcr.microsoft.com/devcontainers/php:1-8.3

# ext-intl gives the demo real ICU plurals and locale-formatted dates/numbers.
# Baked into the image (not postCreateCommand) so it runs as root during the
# build and a failure breaks the build loudly instead of silently degrading
# the demo. Helper first; apt + docker-php-ext-install as the fallback.
RUN install-php-extensions intl \
    || (apt-get update \
        && apt-get install -y --no-install-recommends libicu-dev \
        && docker-php-ext-install intl \
        && rm -rf /var/lib/apt/lists/*)
