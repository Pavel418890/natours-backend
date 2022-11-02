# Natours Backend

*Ссылка на репозиторий UI части приложения*

[Natours Frontend](https://github.com/Pavel418890/natours-frontend.git)

## Содержание

* [Краткое описание проекта.](#summary)

* [Используемые технологии.](#used-tech)

* [Установка локально.](#local-installation-instruction)

* [API документация.](#api-docs)

* [Планы по развитию проекта.](#plans)


<h3><a id="summary">Краткое описание проекта</a></h3>

Natours Backend - серверная часть web-приложения тур-агенства, которое решает 
задачи по созданию, продаже и организации туров.

<h3><a id="used-tech">Используемые технологии</a></h3>

|Название                                        | Описание                                                                       |
|------------------------------------------------|--------------------------------------------------------------------------------|
| Python 3.10                                    | Язык программирования                                                          |
| Django/Django Rest Framework                   | Web-Фреймворк                                                                  |
| Postgres                                       | База данных                                                                    |
| Docker/Docker-compose                          | Платформа для разработки, доставки и запуска приложения                        |
| Gunicorn + Nginx                               | WSGI + Reverse Proxy `prod`                                                    |
| Celery + RabbitMQ + Redis                      | Инструменты для управления очередями и работы отложенными/асинхронными задачами|
| Flower + RabbitMQ Management UI                | Мониторинг работы воркеров                                                     |
| Stripe                                         | Сервис для оплаты                                                              |
| Sentry                                         | Логирование `prod`                                                             |
| Google Cloud Platform/Google Kubernetes Engine | Хостинг и деплой `prod`                                                        |

<h3><a id="local-installation-instruction">Установка локально</a></h3>

*Необходимые условия:*

- [docker / docker compose v2](https://www.docker.com/products/docker-desktop/)

- [git-cli](https://git-scm.com/downloads)

- [stripe-cli ( `optional `)](https://stripe.com/docs/stripe-cli)

### Клонирование репозиториев.

```shell
git clone git@github.com:pavel418890/natours-backend.git
```

```shell
git clone git@github.com:pavel418890/natours-frontend.git
```

### Запуск frontend dev mode.

<sub>Переход в директорию</sub>

```shell
cd natours-frontend
```

<sub>Запуск frontend app</sub>

```shell
docker compose up -d
```

### Настройка переменных окружения


* *путь до переменных окружения`<path-to-natours-backend-project>/environments/.env.dev`*

* *путь до переменных окружения DB `<path-to-natours-backend-project>/environments/.env.db.dev`*


* Заполнить пароль для БД

    `DATABASE_PASSWORD=<{{любой пароль}}>`
        
    `POSTGRES_PASSWORD={{DATABASE_PASSWORD}}`


    <details><summary>`Optional` Для тестирования оплаты локально:</summary>

    - Написать мне в телеграмм `@pavel418890` или на почту `pavel418890@gmail.com` 
для получения УЗ и `{{приватного ключа}}` от stripe аккаунта.

    - Установить stripe [stripe-cli](https://stripe.com/docs/stripe-cli).

    * <sub>Аутентификация stripe-cli.</sub>

    ```shell
    stripe login

    ```
    * <sub>Запуск вебхука</sub>

    ```shell
    stripe listen --forward-to localhost:8888/v1/bookings/tour-booking/

    > OUTPUT:
    Ready! Your webhook signing secret is '{{WEBHOOK_SIGNING_SECRET}}' (^C to quit)
    ```

    * <sub>Вставка переменных окружения</sub>

        `STRIPE_WEBHOOK_SECRET_KEY=<{{WEBHOOK_SIGNING_SECRET}}>`

        `STRIPE_PRIVATE_KEY=<{{приватный ключ}}>`
</details>

### Запуск сервера natours-backend

* <sub>Переходим в директорию проекта</sub>

    ```shell
    cd <path-to-natours-backend-project>
    ```

* <sub>Запуск backend приложения</sub>

    ```shell
    docker compose up -d 
    ```
 
<h3><a id="api-docs">API документация</a><h3> 

https://documenter.getpostman.com/view/11170718/UVsPQQrd

<h3><a id="plans">Планы по развитию проекта</a></h3>

1. Написать unit тесты.
1. Настройка CI/CD через Jenkins или Gitlab
1. Чаты. Обмен сообщениями через websoket
1. Разработка пространства для админа/гида
1. Добавить систему фильтров
1. Перенести хранение static и media файлов в Google Storage или  S3. На данный момент файлы хранятся в nfs

