FROM caddy:2.11.4-builder AS builder
LABEL authors="jackli"

WORKDIR /build

ENV GOPROXY=https://goproxy.cn,direct

RUN xcaddy build \
           --with github.com/caddy-dns/alidns \
           --with github.com/caddyserver/replace-response

FROM caddy:2.11.4
LABEL authors="jackli"

WORKDIR /data

COPY --from=builder /build /usr/bin/

ENTRYPOINT ["caddy", "run"]
