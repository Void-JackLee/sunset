# caddy build
FROM caddy:2.11.4-builder AS caddy-builder
LABEL authors="jackli"

WORKDIR /build

ENV GOPROXY=https://goproxy.cn,direct

RUN xcaddy build \
           --with github.com/caddy-dns/alidns \
           --with github.com/caddyserver/replace-response

# vue builder
FROM node:20-alpine AS web-builder

WORKDIR /build

COPY web/ .

RUN yarn
RUN yarn build

# deploy
FROM caddy:2.11.4
LABEL authors="jackli"

WORKDIR /data

COPY --from=caddy-builder /build /usr/bin/
COPY --from=web-builder /build/dist /root/html

ENTRYPOINT ["caddy", "run"]
