import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Проверка несуществующего token
response = requests.get(url, params={"token": "wrong_token"})
data = response.json()

print("Неверный токен:", data)
assert data["error"] == "No job linked to this token"

# 1 Создаем задачу
response = requests.get(url)
data = response.json()

token = data["token"]
seconds = data["seconds"]
print("создали задачу")
print("токен:", token)
print("ожидание:", seconds)

# 2 Проверяем до готовности
response = requests.get(url, params={"token": token})
data = response.json()

print("статус до ожидания:", data)
assert data["status"] == "Job is NOT ready"

# 3 Ждем
time.sleep(seconds)

# 4 Проверяем после готовности
response = requests.get(url, params={"token": token})
data = response.json()

print("статус после ожидания:", data)
assert data["status"] == "Job is ready"
assert "result" in data
