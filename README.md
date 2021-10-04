# Architektūra

Keletas svarstytų pasirinkimų:
1. hash paduotą link'ą ir nukirst iki norimo ilgio. Bet taip atsekamumas yra.
2. linkui pridėt timestatmp ir tada hash. Bet reikės saugoti visa tai db, ir jei kas gautų priėjimą prie db viską atsekt galėtų.
3. Dabartinis variantas - generuojam string'ą norimo ilgio; hash'inam su salt iš django secret key; saugom db į indeksuotą lentelę.

# Instalation commands

required linux libraries:
``python3.9  python3-pip``

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