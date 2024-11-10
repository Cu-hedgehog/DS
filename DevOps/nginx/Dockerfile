FROM alpine:latest
WORKDIR /etc/nginx
RUN apk update && apk add nginx
COPY nginx.conf /etc/nginx/nginx.conf
