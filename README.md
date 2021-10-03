# Instalation commands

required linux libraries:
``python3.9  python3.9-dev python3-pip``

Installation:

```python3 -m venv ENV_PATH 

cd ENV_PATH 

source bin/activate

cd PROJECT_PATH

python3 -m pip install -r requirements.txt
```

Django install and run:

```
python3 manage.py migrate

python3 manage.py runserver
```