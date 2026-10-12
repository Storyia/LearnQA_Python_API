import requests


def test_homework_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")

    print(response.headers)

    header_value = response.headers.get("x-secret-homework-header")

    assert header_value == "Some secret value"
