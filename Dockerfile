FROM python:3.6-alpine as package

COPY . /srv/
RUN set -x \
    && cd srv \
    && mkdir .tmp \
    && python3 setup.py sdist \
    && mv .build/ /deploy/

FROM registry.itpc.ru/devops/docker/baseimages/python:1.0

ARG env=production
ENV ENVIORNMENT ${env}
ENV APP_TARGET /app/project

COPY --from=package /deploy/ /usr/src/app

RUN set -x \
    && apk add --no-cache \
    libstdc++ \
    make \
    unixodbc \
    freetds \
    freetds-dev \
    && apk add --no-cache --virtual .build-deps \
    build-base \
    unixodbc-dev \
    && cd /usr/src/app \
    && tar -xzf *.tar.gz \
    && rm -rf *tar.gz \
    && cd * \
    && python setup.py install \
    --root=${APP_TARGET} \
    --home=. \
    --install-purelib=. \
    --install-platlib=. \
    --install-lib=. \
    --install-scripts=. \
    && apk del .build-only \
    && cd ${APP_TARGET} \
    && rm -rf /usr/src/app

COPY ./odbc /etc
VOLUME /app/data
EXPOSE 8080

ENTRYPOINT ["/usr/bin/make"]
CMD ["serve"]
