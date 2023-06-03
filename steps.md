# Steps to start similar app

1. create and activate virtualenv for python3

2. install Django 4.2

3. try instalation with

```
django-admin startproject mysite .
python manage.py migrate
python manage.py runserver
ctrl + D
```

4. Optional organize default APPS and allowed HOSTS

5. Trying first app with

```
python manage.py startapp blog
```

6. testing a Hello World view

```
---
blog/views.py
---
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the blog index.")

---
create a blog/urls.py
---
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]

---
update mysite/urls.py
---
ysite/urls.py¶
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("blog.urls")),
    path("admin/", admin.site.urls),
]

```

7. Database setup

a. install psycopg into environment

b. create database and user

```
sudo su postgres
psql
CREATE DATABASE <db_name>;
CREATE USER <db_user> WITH PASSWORD 'db_user_passw';
GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <db_user>;
\q
exit
```

c. testing setup

```
---
mysite/settings.py
---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pblog_db',
        'USER': 'admin_pblog',
        'PASSWORD': 'adminblog1234.',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

```

```
python3 manage.py migrate
python3 manage.py runserver
```
