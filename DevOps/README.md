Создание и запуск образа nginx:

`docker build -t test-nginx-image nginx\`

`docker run --name test-nginx-cnt -p 8080:80 -d test-nginx-image`

Создание и запуск образа postgresql:

`docker build -t test-postgres-image postgresql\`

`docker run --name test-postgres-cnt -e POSTGRES_PASSWORD=postgres -d test-postgres-image`