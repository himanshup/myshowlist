# myshowlist Server

This readme is a work in progress.

## Running locally

```
git clone https://github.com/himanshup/myshowlist.git
cd myshowlist
pip3 install -r requirements.txt
```

Install postgres and create and configure a database. In myshowlist/settings.py, change the NAME/USER/PASSWORD values to yours.  

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

Create new migrations, apply the migrations to the database, and then run the server.

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

