## Homework docker


## Часть 1
### Копируем репозиторий лабораторной

```bash
vboxuser@Linuxoid:~/satodim/workspace/workspace/projects$ git clone https://github.com/tp-lessons/lab_docker lab_docker_homework/
Cloning into 'lab_docker_homework'...
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 16 (delta 1), reused 13 (delta 1), pack-reused 0 (from 0)
Receiving objects: 100% (16/16), 5.01 KiB | 5.01 MiB/s, done.
Resolving deltas: 100% (1/1), done.
```
### теперь создадим Dockerfile
```sh
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
```
### Собираем Docker образ 
```sh
sudo docker build -t lab-web-app .
```

```sh
[+] Building 48.8s (11/11) FINISHED                              docker:default
 => [internal] load build definition from Dockerfile                       0.1s
 => => transferring dockerfile: 621B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim         1.4s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [1/6] FROM docker.io/library/python:3.9-slim@sha256:2d97f6910b16bd338  0.1s
 => => resolve docker.io/library/python:3.9-slim@sha256:2d97f6910b16bd338  0.1s
 => [internal] load build context                                          0.1s
 => => transferring context: 1.76kB                                        0.0s
 => CACHED [2/6] WORKDIR /app                                              0.0s
 => [3/6] RUN apt-get update && apt-get install -y     gcc     default-l  21.8s
 => [4/6] COPY app/requirements.txt .                                      0.2s 
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt               8.3s 
 => [6/6] COPY app/ .                                                      0.1s 
 => exporting to image                                                    16.6s 
 => => exporting layers                                                   12.1s 
 => => exporting manifest sha256:bcca4c6f387fb765092797f9c9107f1d3a9b7bc7  0.0s 
 => => exporting config sha256:ee8d1e26b9dc482339d34a15b863442aa750ce20c3  0.0s 
 => => exporting attestation manifest sha256:8011fe3d0e791c12dcc81f15bdf9  0.0s 
 => => exporting manifest list sha256:555294a9dcc516f101d97e4ef08b0c4352d  0.0s
 => => naming to docker.io/library/lab-web-app:latest                      0.0s
 => => unpacking to docker.io/library/lab-web-app:latest                   4.3s
```
### Запускаем контейнер 
```sh
vboxuser@Linuxoid:~/satodim/workspace/workspace/projects/lab_docker_homework$ sudo docker run -d --name my-app -p 5000:5000 lab-web-app
77abc4607a6dbde26761822cd01d51a87de7d39acaad8e1806c5d2c7484676cf
```
### Копируем файл README в контейнер
```sh
sudo docker cp README.md my-app:/home/
Successfully copied 4.44kB (transferred 6.14kB) to my-app:/home/
```
### Подключаемся к контейнеру в интерактивном режие
```sh
sudo docker exec -it my-app /bin/bash
root@77abc4607a6d:/app# ls -la /home/
total 16
drwxr-xr-x 1 root root 4096 May 10 12:06 .
drwxr-xr-x 1 root root 4096 May 10 12:06 ..
-rw-rw-r-- 1 1000 1000 4442 May 10 12:01 README.md
```

### и проверяем, все ли выполнилось

```sh
root@77abc4607a6d:/app# cat /home/README.md
## Лабораторная работа по работе с docker
Работа посвящена изучению технологии работы с контейнерами

## Задачи

- [ ] 1. Ознакомиться со ссылками учебного материала
- [ ] 2. Выполнить инструкцию учебного материала
- [ ] 3. Составить отчет и отправить ссылку преподавателю 

## Задание лабораторной работы

$ export GITHUB_USERNAME=<имя_пользователя>
$ export GIST_TOKEN=<сохраненный_токен>
$ alias edit=<nano|vi|vim|subl>

$ git clone https://github.com/${GITHUB_USERNAME}/lab06 projects/lab_docker
$ cd projects/lab_docker
$ git remote remove origin
$ git remote add origin https://github.com/${GITHUB_USERNAME}/lab_docker

# Debian
$ sudo apt-get update
$ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

$ cat >> main.py <<EOF
print("Hello, Docker!")
EOF


$ cat >> requirements.txt <<EOF
flask
requests
EOF

$ cat >> Dockerfile <<EOF
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
EOF



$ docker build -t lab-docker .
$ docker run --rm -it lab-docker


### Docker compose


$ cat >> docker-compose.yml <<EOF
version: '3.8'

services:
  app:
    build: . 
    container_name: lab_docker
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DB_HOST=$DB_HOST
      - DB_USER=$DB_USER
      - DB_PASSWORD=$DB_PASSWORD
      - DB_NAME=$DB_NAME

  # Сервис базы данных MySQL
  db:
    image: mysql:8.0
    container_name: mysql_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: $DB_ROOT_PASSWORD
      MYSQL_DATABASE: $DB_NAME
      MYSQL_USER: $DB_USER
      MYSQL_PASSWORD: $DB_PASSWORD
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db_data:
EOF


$ docker compose up --build


## Ссылки

### Docker compose

- [Install the Docker Compose plugin](https://docs.docker.com/compose/install/linux/)

### Dockerfile

- [Как запаковать простое приложение в Docker: на пальцах](https://habr.com/ru/companies/slurm/articles/930822/)

## Домашнее задание

В репозитории приведен код web-приложения, которое сохраняет в БД введенную информацию о задаче - ее имя.

## Часть I. Docker

1. Добавьте в код Dockerfile, который позволит запустить web-приложение с исходным кодом в каталоге app/ через docker.
2. Выполните запуск контейнера с этим приложением.
3. Скопируйте из консоли в каталог /home/ контейнера файл README.md.
4. Подключитесь к терминалу контейнера с приложением в интерактивном режиме. Проверьте, что скопированный файл находится в нужном каталоге.
5. Выйдите из интерактивного режима.
6. Остановите контейнер с приложением.


## Часть II. Docker compose
1. Создайте файл docker-compose.yml таким образом, чтобы совместно с описанным в части 1 контейнером работала бы база данных mysql. Файл инициализации БД в каталоге db/init.sql. Также пропишите порт подключения к приложению. Например 5000.
2. Запустите связку web-приложение - БД.
3. Проверьте подключение к приложению через браузер. Сделайте снимок экрана.
4. Проверьте работу приложения через браузер.

root@77abc4607a6d:/app# ls -la /app/
total 28
drwxr-xr-x 1 root root 4096 May 10 12:06 .
drwxr-xr-x 1 root root 4096 May 10 12:06 ..
drwxr-xr-x 2 root root 4096 May 10 12:06 __pycache__
-rw-rw-r-- 1 root root  453 May 10 12:01 app.py
-rw-rw-r-- 1 root root  778 May 10 12:01 models.py
-rw-rw-r-- 1 root root   29 May 10 12:01 requirements.txt
drwxrwxr-x 2 root root 4096 May 10 12:01 templates
root@77abc4607a6d:/app# cat /app/app.py
from flask import Flask, render_template
from models import ItemModel

app = Flask(__name__)
model = ItemModel()

@app.route('/')
def index():
    # Контроллер запрашивает данные у модели
    items = model.get_all_items()
    # И передает их в представление (шаблон)
    return render_template('index.html', items=items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
root@77abc4607a6d:/app# exit
exit
```

### Останавливаем контейнер
```sh
sudo docker stop my-app
sudo docker rm my-app
```

## Часть 2

### Создаем docker-compose.yml
```sh
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_USER=satodim
      - DB_PASS=mypass
      - DB_NAME=mydatabase
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: satodim
      MYSQL_PASSWORD: mypass
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-usatodim", "-pmypass"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db_data:
```
### Запускаем docker-compose
```sh
sudo docker compose up --build
```
```bash
sudo docker compose up --build
[+] Building 1.9s (13/13) FINISHED                                              
 => [internal] load local bake definitions                                 0.0s
 => => reading from stdin 606B                                             0.0s
 => [internal] load build definition from Dockerfile                       0.0s
 => => transferring dockerfile: 621B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim         0.8s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [1/6] FROM docker.io/library/python:3.9-slim@sha256:2d97f6910b16bd338  0.1s
 => => resolve docker.io/library/python:3.9-slim@sha256:2d97f6910b16bd338  0.1s
 => [internal] load build context                                          0.1s
 => => transferring context: 1.81kB                                        0.1s
 => CACHED [2/6] WORKDIR /app                                              0.0s
 => CACHED [3/6] RUN apt-get update && apt-get install -y     gcc     def  0.0s
 => CACHED [4/6] COPY app/requirements.txt .                               0.0s
 => CACHED [5/6] RUN pip install --no-cache-dir -r requirements.txt        0.0s
 => [6/6] COPY app/ .                                                      0.2s
 => exporting to image                                                     0.3s
 => => exporting layers                                                    0.1s
 => => exporting manifest sha256:4d1aadc5fd4f9c03b32723524d61de16f54e6119  0.0s
 => => exporting config sha256:75c9f57f4d22dbc54e4b00a43a81fd3d5ab0dc6540  0.0s
 => => exporting attestation manifest sha256:1c22e05ad936adce74a4a9624591  0.0s
 => => exporting manifest list sha256:df3997c9b4b4d44f39b5ba7d8a87599f11c  0.0s
 => => naming to docker.io/library/lab_docker_homework-app:latest          0.0s
 => => unpacking to docker.io/library/lab_docker_homework-app:latest       0.0s
 => resolving provenance for metadata file                                 0.0s
[+] up 5/5
 ✔ Image lab_docker_homework-app       Built                                2.0s
 ✔ Network lab_docker_homework_default Created                              0.1s
 ✔ Volume lab_docker_homework_db_data  Created                              0.0s
 ✔ Container lab_docker_homework-db-1  Created                              0.2s
 ✔ Container lab_docker_homework-app-1 Created                              0.2s
Attaching to app-1, db-1
Container lab_docker_homework-db-1 Waiting 
db-1  | 2026-05-10 12:39:50+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.0.46-1.el9 started.
db-1  | 2026-05-10 12:39:50+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
db-1  | 2026-05-10 12:39:50+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.0.46-1.el9 started.
db-1  | 2026-05-10 12:39:51+00:00 [Note] [Entrypoint]: Initializing database files
db-1  | 2026-05-10T12:39:51.078973Z 0 [Warning] [MY-011068] [Server] The syntax '--skip-host-cache' is deprecated and will be removed in a future release. Please use SET GLOBAL host_cache_size=0 instead.
db-1  | 2026-05-10T12:39:51.079068Z 0 [System] [MY-013169] [Server] /usr/sbin/mysqld (mysqld 8.0.46) initializing of server in progress as process 78
db-1  | 2026-05-10T12:39:51.087280Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db-1  | 2026-05-10T12:39:51.981719Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db-1  | 2026-05-10T12:39:53.935977Z 6 [Warning] [MY-010453] [Server] root@localhost is created with an empty password ! Please consider switching off the --initialize-insecure option.
db-1  | 2026-05-10 12:39:58+00:00 [Note] [Entrypoint]: Database files initialized
db-1  | 2026-05-10 12:39:58+00:00 [Note] [Entrypoint]: Starting temporary server
db-1  | 2026-05-10T12:39:58.653651Z 0 [Warning] [MY-011068] [Server] The syntax '--skip-host-cache' is deprecated and will be removed in a future release. Please use SET GLOBAL host_cache_size=0 instead.
db-1  | 2026-05-10T12:39:58.655240Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.0.46) starting as process 120
db-1  | 2026-05-10T12:39:58.689735Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db-1  | 2026-05-10T12:39:58.994546Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db-1  | 2026-05-10T12:39:59.324650Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db-1  | 2026-05-10T12:39:59.325451Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db-1  | 2026-05-10T12:39:59.331634Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db-1  | 2026-05-10T12:39:59.359820Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Socket: /var/run/mysqld/mysqlx.sock
db-1  | 2026-05-10T12:39:59.360399Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.46'  socket: '/var/run/mysqld/mysqld.sock'  port: 0  MySQL Community Server - GPL.
db-1  | 2026-05-10 12:39:59+00:00 [Note] [Entrypoint]: Temporary server started.
db-1  | '/var/lib/mysql/mysql.sock' -> '/var/run/mysqld/mysqld.sock'
db-1  | Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
db-1  | Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
db-1  | Warning: Unable to load '/usr/share/zoneinfo/leapseconds' as time zone. Skipping it.
Container lab_docker_homework-db-1 Healthy 
db-1  | Warning: Unable to load '/usr/share/zoneinfo/tzdata.zi' as time zone. Skipping it.
db-1  | Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
db-1  | Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
db-1  | 2026-05-10 12:40:02+00:00 [Note] [Entrypoint]: Creating database mydatabase
db-1  | 2026-05-10 12:40:02+00:00 [Note] [Entrypoint]: Creating user satodim
db-1  | 2026-05-10 12:40:02+00:00 [Note] [Entrypoint]: Giving user satodim access to schema mydatabase
db-1  | 
db-1  | 2026-05-10 12:40:02+00:00 [Note] [Entrypoint]: /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init.sql
db-1  | 
db-1  | 
db-1  | 2026-05-10 12:40:02+00:00 [Note] [Entrypoint]: Stopping temporary server
db-1  | 2026-05-10T12:40:02.239803Z 15 [System] [MY-013172] [Server] Received SHUTDOWN from user root. Shutting down mysqld (Version: 8.0.46).
app-1  |  * Serving Flask app 'app'
app-1  |  * Debug mode: off
app-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
app-1  |  * Running on all addresses (0.0.0.0)
app-1  |  * Running on http://127.0.0.1:5000
app-1  |  * Running on http://172.19.0.3:5000
app-1  | Press CTRL+C to quit
db-1   | 2026-05-10T12:40:04.424918Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.0.46)  MySQL Community Server - GPL.
db-1   | 2026-05-10 12:40:05+00:00 [Note] [Entrypoint]: Temporary server stopped
db-1   | 
db-1   | 2026-05-10 12:40:05+00:00 [Note] [Entrypoint]: MySQL init process done. Ready for start up.
db-1   | 
db-1   | 2026-05-10T12:40:05.536835Z 0 [Warning] [MY-011068] [Server] The syntax '--skip-host-cache' is deprecated and will be removed in a future release. Please use SET GLOBAL host_cache_size=0 instead.
db-1   | 2026-05-10T12:40:05.538465Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.0.46) starting as process 1
db-1   | 2026-05-10T12:40:05.553583Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
db-1   | 2026-05-10T12:40:05.848939Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
db-1   | 2026-05-10T12:40:06.065696Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
db-1   | 2026-05-10T12:40:06.065730Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
db-1   | 2026-05-10T12:40:06.072640Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
db-1   | 2026-05-10T12:40:06.098186Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
db-1   | 2026-05-10T12:40:06.099623Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.46'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
app-1  | 172.19.0.1 - - [10/May/2026 12:40:21] "GET / HTTP/1.1" 200 -
```
## Проверка в консоли
```sh
vboxuser@Linuxoid:~/satodim/workspace/workspace/projects/lab_docker_homework$ sudo docker exec -it lab_docker_homework-db-1 mysql -usatodim -pmypass mydatabase -e "SELECT * FROM items;"
mysql: [Warning] Using a password on the command line interface can be insecure.
+----+-----------+
| id | name      |
+----+-----------+
|  1 | Example 1 |
|  2 | Example 2 |
+----+-----------+

```
## Проверка в браузере по адресу http://localhost:5000

```sh
Список из Базы Данных

    Example 1
    Example 2

```
## Остановка приложения
```sh
sudo docker compose down
```

```sh
vboxuser@Linuxoid:~/satodim/workspace/workspace/projects/lab_docker_homework$ sudo docker compose down
[sudo] password for vboxuser: 
[+] down 3/3
 ✔ Container lab_docker_homework-app-1 Removed                             10.3s
 ✔ Container lab_docker_homework-db-1  Removed                              1.6s
 ✔ Network lab_docker_homework_default Removed                              0.vvvv
```
