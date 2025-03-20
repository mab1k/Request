import pytest
import requests
import json

# тест на создание пользователя и проверку успешного создания
def test_create_user():
    user = {
        "name": "Ronn",
        "age": "32",
        "mail": "magicRon@mal.com".strip(),
        "password": "123".strip()
    }

    url = "http://localhost:5000/users/"
    r = requests.post(url, json=user)
    print(r.json())
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == 201

# тест на получение пользователя по id
def test_get_user_by_id():
    example_user = {"name": "Ron", "age": "39", "mail": "magicRon@mal.com", "password": "123"}
    url = "http://localhost:5000/users/Ron"
    r = requests.get(url)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    user = r.json()
    assert example_user == user