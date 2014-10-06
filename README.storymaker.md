# Storymaker Mezzanine Development

```
$ pip install -r ./mezzanine/project_template/requirements.txt
(Note you must run pip install -r from this directory due to pip local directory dependency issues: https://github.com/pypa/pip/issues/328)
$ cp mezzanine/project_template/local_settings.py{.template,}
$ cp mezzanine/project_template/dev.db{.default,}
$ python setup.py develop
$ python mezzanine/project_template/manage.py runserver
```
