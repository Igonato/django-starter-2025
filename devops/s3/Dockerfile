# S3-compatible service https://garagehq.deuxfleurs.fr/
FROM dxflrs/garage:v2.0.0-beta1 AS garage

FROM alpine:3.21.3

RUN apk add --no-cache bash

ENV RUST_BACKTRACE=1
ENV RUST_LOG=garage=error

COPY --from=garage /garage /usr/local/bin/garage

RUN chmod +x /usr/local/bin/garage

COPY devops/wait-for-it.sh /wait-for-it.sh
COPY devops/s3/garage-dev-config.toml /etc/garage.toml
COPY devops/s3/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh /wait-for-it.sh

ENTRYPOINT ["/entrypoint.sh"]
