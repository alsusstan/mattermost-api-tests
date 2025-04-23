import requests
import time

BASE_URL = "http://localhost:8065/api/v4"
ADMIN_TOKEN = "9z7xtn7b4jgttd9jh888j6pkph"  # токен админа

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}

def test_create_channel_success():
    """Тест успешного создания нового канала"""
    try:
        url = f"{BASE_URL}/channels"
        timestamp = int(time.time())
        unique_name = f"autotest-channel-{timestamp}"

        data = {
            "team_id": "pr4hewpb17f48rca9gihy5b4oa",
            "name": unique_name,
            "display_name": f"Autotest Channel {timestamp}",
            "type": "O"
        }

        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            response_json = response.json()
            print(f"Успешно создан канал: {response_json['name']}")
            assert response_json["name"] == unique_name
        else:
            print(f"Ошибка создания канала. Код: {response.status_code}, Ответ: {response.text}")
            assert False, f"Ожидался код 201, получен {response.status_code}"

    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка при создании канала: {str(e)}")
        raise

def test_create_channel_duplicate_name():
    """Тест обработки дублирования имени канала"""
    try:
        url = f"{BASE_URL}/channels"
        data = {
            "team_id": "pr4hewpb17f48rca9gihy5b4oa",
            "name": "autotest-channel",
            "display_name": "Duplicate Autotest Channel",
            "type": "O"
        }

        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 400:
            print("Правильно обработано дублирование имени канала")
        else:
            print(f"Неожиданный ответ при дублировании. Код: {response.status_code}, Ответ: {response.text}")
            assert False, f"Ожидался код 400, получен {response.status_code}"

    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка при проверке дублирования: {str(e)}")
        raise

