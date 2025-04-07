# Облачное хранилище My Cloud

Развернутое на сервере REG.RU [приложение](http://193.227.241.176:5000/).

## Запуск приложения на локальном диске

1. Создаём директорию для backend части проекта
2. Клонируем в неё репозиторий:
   ```
   git clone https://github.com/poi1nt/backend_diplom.git
   ```
3. Открываем папку `backend_diplom` в любой IDE и запускаем встроенный терминал
4. Создаём виртуальное окружение:
   ```
   python -m venv env
   ```
5. Активируем его:
   ```
   env/Scripts/activate
   ```
6. Устанавливаем зависимости:
   ```
   pip install -r requirements.txt
   ```
7. В папке `backend` создаём файл `.env` в соответствии с шаблоном:
      ```
      SECRET_KEY=
      DEBUG=
      ALLOWED_HOSTS=(list)

      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=db_cloud
      DB_USER=user
      DB_PASSWORD=password

      ADMIN_USERNAME=
      ADMIN_FIRSTNAME=
      ADMIN_LASTNAME=
      ADMIN_EMAIL=
      ADMIN_PASSWORD=

      BASE_STORAGE=
      ```
8. Создаём базу данных с учётом настроек указанных в файле `.env`:
   `createdb -U <DB_USER> <DB_NAME>` Пароль: `<DB_PASSWORD>`
9.  Применяем миграции:
   ```
   python manage.py migrate
   ```
10. Создаём суперпользователя с указанными в файле `.env` данными:
   ```
   python manage.py create_superuser
   ```
11. Запускаем сервер:
   ```
   python manage.py runserver
   ```
12. Создаём директорию для frontend части проекта
13. Клонируем в неё репозиторий:
   ```
   git clone https://github.com/poi1nt/frontend_diplom.git
   ```
14. Открываем папку `frontend_diplom` в любой IDE и запускаем встроенный терминал
15. В файле `.env` указываем базовый URL сервера:
   ```
   VITE_SERVER_URL=http://localhost:8000/api
   ```
16. Устанавливаем необходимые зависимости:
   ```
   npm install
   ```
17. Запускаем приложение:
   ```
   npm run dev
   ```

## Развёртывание приложения на облачном сервере

1. Генерируем SSH-ключ, если его ещё нет
2. Копируем публичный SSH-ключ
3. Создаем на сайте [reg.ru](https://cloud.reg.ru) облачный сервер:
   - образ - `Ubuntu 22.04 LTS`
   - vCPU и тип диска - `Стандартный`
   - тариф - `Std C1-M1-D10`
   - регион размещения - `Москва`

   Добавляем наш публичный SSH-ключ, задав ему название.

   Указываем название сервера.

   Нажимаем кнопку `Заказать сервер`

   Получаем по электронной почте данные для подключения к серверу через SSH.
4. Запускаем терминал и подключаемся к серверу, использую полученные данные:
   ```
   ssh root@<ip адрес сервера>
   ```
   Вводим пароль
5. Создаем нового пользователя:
   ```
   adduser <имя пользователя>
   ```
6. Добавляем созданного пользователя в группу `sudo`:
   ```
   usermod <имя пользователя> -aG sudo
   ```
7. Выходим из-под пользователя `root`:
   ```
   logout
   ```
8. Подключаемся к серверу под новым пользователем:
   ```
   ssh <имя пользователя>@<ip адрес сервера>
   ```
9. Обновим список доступных репозиториев для пакетного менеджера `apt`:
   ```
   sudo apt update
   ```
10. Обновим пакеты до последних версий:
   ```
   sudo apt upgrage
   ```
11. Проверяем, что установлен `git`:
   ```
   git --version
   ```
12. Устанавливаем необходимые пакеты:
   ```
   sudo apt install python3-venv python3-pip postgresql nginx
   ```
13. Заходим в терминал `psql` под пользователем `postgres`:
   ```
   sudo -u postgres psql
   ```
14. Создаём базу данных:
   ```
   create database db_cloud;
   ```
15. Задаём пароль для пользователя `postgres`:
   ```
   alter user postgres with password 'postgres';
   ```
16. Выходим из терминала `psql`:
   ```
   \q
   ```
17. Клонируем репозиторий с `backend` частью:
   ```
   git clone https://github.com/poi1nt/backend_diplom.git
   ```
18. Переходим в папку `backend_diplom`:
   ```
   cd /backend_diplom
   ```
19. Устанавливаем виртуальное окружение:
   ```
   python3 -m venv env
   ```
20. Активируем его:
   ```
   source env/bin/activate
   ```
21. Устанавливаем необходимые зависимости:
   ```
   pip install -r requirements.txt
   ```
22. В папке `backend` создаём файл `.env`
   ```
   nano .env
   ```

   в соответствии с шаблоном:
      ```
      SECRET_KEY=
      DEBUG=
      ALLOWED_HOSTS=(list)

      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=db_cloud
      DB_USER=user
      DB_PASSWORD=password

      ADMIN_USERNAME=
      ADMIN_FIRSTNAME=
      ADMIN_LASTNAME=
      ADMIN_EMAIL=
      ADMIN_PASSWORD=

      BASE_STORAGE=
      ```
23. Применяем миграции:
   ```
   python manage.py migrate
   ```
24. Создаём суперпользователя:
   ```
   python manage.py createsuperuser
   ```
25. Собираем весь статичный контент в одну папку на сервере:
   ```
   python manage.py collectstatic
   ```
26. Запускаем сервер:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```
27. Проверяем работу `gunicorn`:
   ```
   gunicorn backend.wsgi -b 0.0.0.0:8000
   ```
28. Создаём сервис `gunicorn.service`:
   ```
   sudo nano /etc/systemd/system/gunicorn.service
   ```
   с содержимым

      ```
      [Unit]
      Description=gunicorn service
      After=network.target

      [Service]
      User=<имя пользователя>
      Group=www-data
      WorkingDirectory=/home/<имя пользователя>/backend_diplom
      ExecStart=/home/<имя пользователя>/backend_diplom/env/bin/gunicorn \
               --access-logfile - \
               --workers=3 \
               --bind unix:/home/<имя пользователя>/backend_diplom/backend/project.sock \
               backend.wsgi:application

      [Install]
      WantedBy=multi-user.target
      ```
29. Запускаем сервис `gunicorn`:
   ```
   sudo systemctl start gunicorn
   ```
   ```
   sudo systemctl enable gunicorn
   ```
30. Проверяем его статус:
   ```
   sudo systemctl status gunicorn
   ```
31. Убеждаемся, что файл `project.sock` присутствует в папке проекта `~/backend_diplom/backend/`:
   ```
   cd
   ```
   ```
   ls backend_diplom/backend/
   ```
32. Клонируем репозиторий с `frontend` частью:
   ```
   git clone https://github.com/poi1nt/frontend_diplom.git
   ```
33. Переходим в папку `frontend_diplom`:
   ```
   cd /frontend_diplom
   ```
34. Создаём файл `.env`
   ```
   nano .env
   ```
    и прописываем в нем:
   ```
   VITE_SERVER_URL=/api
   ```
35. Устанавливаем необходимые зависимости:
   ```
   npm install
   ```
36. Создаём рабочую версию приложения:
   ```
   npm run build
   ```
   *Если на этапе сборки терминал зависает, необходимо на этап сборки увеличить размер памяти RAM на сервере [REG.RU](https://cloud.reg.ru/panel/) до 4 ГБ*
      ### Инструкция по замене тарифа на сервере:
      1)  В браузере заходим на [облачное хранилище](https://cloud.reg.ru/panel/);
      2)  Выбираем созданный ранее сервер;
      3)  Нажимаем кнопку **••• Ещё** и выбираем **Изменить тариф**;
      4)  В сплывающем окне выбираем **Своя конфигурация**;
      5)  Ниже меняем **Размер памяти RAM** до 4 ГБ.
   *После успешной сборки можно вернуть параметры сервера к исходным настройкам (тариф - `Std C1-M1-D10`)*
37. Убеждаемся, что создалась папка `dist`:
   ```
   cd
   ```
   ```
   ls frontend_diplom/
   ```
   И проверяем наличие файлов в ней:
   ```
   ls frontend_diplom/dist/
   ```
   Должно быть:
   ```
   assets
   index.html
   vite.svg
   ```
38. Создаём модуль `nginx`:
   ```
   sudo nano /etc/nginx/sites-available/my_cloud
   ```
   со следующим содержимым

      ```
      server {
         listen 80;
         server_name <ip адрес сервера>;

         # FRONTEND (Vite build)
         root /home/<имя пользователя>/frontend_diplom/dist;
         index index.html;

         location / {
             try_files $uri /index.html;
         }

         # BACKEND API
         location /api/ {
             include proxy_params;
             proxy_pass http://unix:/home/<имя пользователя>/backend_diplom/backend/project.sock;
         }

         # Django STATIC
         location /static/ {
             root /home/<имя пользователя>/backend_diplom;
         }
      }     
      ```
39. Создаём символическую ссылку:
   ```
   sudo ln -s /etc/nginx/sites-available/my_cloud /etc/nginx/sites-enabled
   ```
40. Добавляем пользователя `www-data` в группу текущего пользователя:
   ```
   sudo usermod -aG <имя пользователя> www-data
   ```
41. Диагностируем `nginx` на предмет ошибок в синтаксисе:
   ```
   sudo nginx -t
   ```
42. Перезапускаем веб-сервер:
   ```
   sudo systemctl restart nginx
   ```
43. Проверяем статус `nginx`:
   ```
   sudo systemctl status nginx
   ```
44. Проверяем доступ к сайту:
   ```
   http://<ip адрес сервера>
   ```
