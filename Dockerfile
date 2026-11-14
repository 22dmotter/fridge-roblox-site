FROM python:3.12-slim-bookworm AS build

WORKDIR /site

RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY . .

ARG SITE_BASE=https://22dmotter.github.io/fridge-roblox-site/
ENV SITE_BASE=${SITE_BASE}

RUN python -m pip install --no-cache-dir Pillow \
    && python _build/build.py \
    && mkdir -p /out \
    && cp /site/*.html /site/sitemap.xml /site/robots.txt /site/ads.txt /site/favicon.ico /out/ \
    && cp -a /site/assets /out/assets

FROM nginx:alpine AS runtime

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /out/ /usr/share/nginx/html/

EXPOSE 80
