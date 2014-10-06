# StoryMaker Mezzanine Development

## 1. Setup project

```
$ pip install -r ./mezzanine/project_template/requirements.txt
(Note you must run pip install -r from this directory due to pip local directory dependency issues: https://github.com/pypa/pip/issues/328)
$ cp mezzanine/project_template/local_settings.py{.template,}
$ cp mezzanine/project_template/dev.db{.default,}
$ python setup.py develop
```

## 2. Create Superuser

```
python mezzanine/project_template/manage.py createsuperuser --settings=mezzanine.project_template.settings
```

## 3. Run server

```
$ python mezzanine/project_template/manage.py runserver
```
