# myshowlist Server

This is the Django API for myshowlist - a web app for tracking shows. This readme is a work in progress.

## Running locally

```
git clone https://github.com/himanshup/myshowlist.git
cd myshowlist
pip3 install -r requirements.txt
```

Install [PostgreSQL](https://www.postgresql.org/) and create and configure a database.   

In `/myshowlist/settings.py`, change NAME, USER, and PASSWORD values to yours:

```
DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': '<name>',
          'USER': '<user>',
          'PASSWORD': '',
          'HOST': 'localhost',
          'PORT': '5432'
      }
  }
```

You also might need to generate your own secret key and put it in a .env file:

```
SECRET_KEY='<key>'
```  

Start PostgreSQL, create/apply migrations to the database, and then run the server.

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

