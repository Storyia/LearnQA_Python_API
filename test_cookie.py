import requests


def test_homework_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")

    print(response.cookies)

    cookie_value = response.cookies.get("HomeWork")

    assert cookie_value == "hw_value"
