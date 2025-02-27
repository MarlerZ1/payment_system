# Введение
В данном документе будет описан способ запуска приложения для тестового задания.

Демонстрацию работы и запуск приложения можно найти по ссылкам: [тут](https://www.youtube.com/watch?v=jGamauMiNjw) или [тут](https://rutube.ru/video/private/c6384e3be0796eda1f60a55c45b271bf/?p=MB4ALNVdicqOa-I9s8RScQ)

Само тестовое задание представляет собой сервис покупок.
На сайте можно купить как целый заказ, состоящий из товаров, так и каждый товар по отдельности. К покупкам, что оформлены через заказы, применяются скидки и налоги. Оплата производится через Stripe.

Реализована система валюты по ТЗ: У каждого товара цена указана в определенной валюте. Реализовано ограничение Stripe: нельзя создать заказ (Order), если в нем присутствуют товары с разными валютами.

Заполнение платформы контентом производится через Django Admin панель. Чтобы в нее попасть, нужно дописать /admin к корневому адресу.


При создании или удалении налогов (TaxRate) или скидок (Discount) через Django Admin система автоматически синхронизует данные со stripe.

# Структура проекта следующая:
Корень 
- /item/{id}
- /buy/{id}
- /order/{id}
- /buy_order/{id}
- /admin

В корне приложения находится меню, в котором отображаются все товары и заказы. По нажатию на них можно перейти в соответствующий раздел (/item/{id} или /order/{id})

/item/{id} и /order/{id} - страницы просмотра конкретного товара/заказа. На каждой из них присутвует кнопка, позволяющая совершить покупку. Эта кнопка отправляет запрос к /buy/{id} или /buy_order/{id} соответственно. Эти контроллеры возвращают session id, который используется для формы оплаты.

# Запуск приложения
## Последовательность действий
- скачать проект;
- у файлf .env.template убрать .template;
- заполнить файл .env в соответствии с примером (пример в следующем разделе);
- запустить консоль в корневой папке приложения;
- ввести команду 'docker compose up';
- запустить еще одну консоль в той же папке;
- ввести в ней команду 'docker compose run django bash для того, чтобы "войти" в контейнер и вводить команды в его систему;
- в консоль ввести команду `python manage.py createsuperuser`, заполнить запрашиваемые поля;
- перейти по адресу http://127.0.0.1/admin/ ;
- создать необходимые для тестирования сущности;
- перейти в http://127.0.0.1/ для тестирования.

## Пример заполнения .env файла
STRIPE_PUBLIC_KEY и STRIPE_SECRET_KEY необходимо взять из профиля Stripe. Все указанные данные - случайные и не используются в реальном проекте.

```
SECRET_KEY = 'django-insecure-$fgt)(dfgfdfgfdfgfdfgfdfgfdfgfdfgfdfgfdfgfdfgfd'

ENGINE = 'django.db.backends.postgresql_psycopg2'
POSTGRES_DB = 'payment_system'
HOST = 'db'
PORT = '5432'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = '1234567890qwerty'

STRIPE_PUBLIC_KEY = 'pk_test_aaaaaaaaaaaaaaaaaaaaavvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvccccccccccccccccccccccccccccccccccccc'
STRIPE_SECRET_KEY = 'sk_test_aaaaaaaaaaaaaaaaaaaaaavvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvccccccccccccccccccccccccccccccc'

GUNICORN_WORKERS = '2'
```
