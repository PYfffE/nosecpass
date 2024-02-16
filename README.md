# Startup

### ATTENTION! DO NOT USE APP DIRECTLY WITHOUT NGINX HTTPS PROXY

1. Create ssl certificates in nginx/certs

```bash
mkdir ./nginx/certs && \
 openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
 -keyout ./nginx/certs/nginx-selfsigned.key \
 -out ./nginx/certs/nginx-selfsigned.crt
 ```

2. Start docker containers
```
docker-compose up -d
```
