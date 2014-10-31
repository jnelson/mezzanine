# StoryMaker Mezzanine Development

## 1. Setup project

```
$ pip install -r ./mezzanine/project_template/requirements.txt
(Note you must run pip install -r from this directory due to pip local directory dependency issues: https://github.com/pypa/pip/issues/328)
$ pip install git+https://github.com/glassresistor/django-oauth2-provider.git
(Branch of provider that supports Django 1.7)
$ cp mezzanine/project_template/local_settings.py{.template,}
$ cp mezzanine/project_template/dev.db{.default,}
$ python setup.py develop
```

## 2. Create Superuser

```
python mezzanine/project_template/manage.py createsuperuser
```

## 3. Run server

```
$ python mezzanine/project_template/manage.py runserver
```

## Migrations

Whenever you alter the model run the following before committing:

```
$ python mezzanine/project_template/manage.py makemigrations
```

Then to apply those migrations to your local database:

```
$ python mezzanine/project_template/manage.py migrate

```

See [Django Docs]($ python mezzanine/project_template/manage.py makemigrations) for more info.
