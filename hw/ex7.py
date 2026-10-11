import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1 Запрос без параметра method
response = requests.get(url)
print("1 Запрос без параметра method:")
print(response.text)

# 2 Запрос методом, которого нет в списке
response = requests.head(url, data={"method": "HEAD"})
print("2 HEAD-запрос:")
print(response.status_code)
print(response.text)

# 3 Запрос с правильным значением method
response = requests.get(url, params={"method": "GET"})
print("3 Правильный GET-запрос:")
print(response.text)

# 4 Проверка всех сочетаний
methods = ["GET", "POST", "PUT", "DELETE"]
print("4 Проверка всех сочетаний:")

for request_method in methods:
    for method_value in methods:

        if request_method == "GET":
            response = requests.get(
                url,
                params={"method": method_value}
            )
        elif request_method == "POST":
            response = requests.post(
                url,
                data={"method": method_value}
            )
        elif request_method == "PUT":
            response = requests.put(
                url,
                data={"method": method_value}
            )
        else:
            response = requests.delete(
                url,
                data={"method": method_value}
            )

        print(
            f"HTTP method: {request_method}, "
            f"method param: {method_value}, "
            f"response: {response.text}"
        )
