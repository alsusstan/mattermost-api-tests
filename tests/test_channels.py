import requests
import time
import random

BASE_URL = "http://localhost:8065/api/v4"
ADMIN_TOKEN = "9z7xtn7b4jgttd9jh888j6pkph"  # токен админа

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}

def test_create_channel_success():
    """Проверка успешного создания канала"""
    url = f"{BASE_URL}/channels"
    
    try:
        # Генерируем уникальное имя канала
        timestamp = int(time.time())
        unique_name = f"autotest-channel-{int(time.time())}-{random.randint(1000,9999)}"
        
        data = {
            "team_id": "pr4hewpb17f48rca9gihy5b4oa",
            "name": unique_name,
            "display_name": f"Autotest Channel {timestamp}",
            "type": "O"  # O = public, P = private
        }

        response = requests.post(url, headers=headers, json=data)
        
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
        response_json = response.json()
        assert response_json["name"] == unique_name, f"Имя канала не совпадает: ожидалось {unique_name}"
        print(f"Канал {unique_name} успешно создан")
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при создании канала: {e}")
        raise

def test_create_channel_duplicate_name():
    """Проверка создания канала с дублирующимся именем"""
    url = f"{BASE_URL}/channels"
    
    try:
        data = {
            "team_id": "pr4hewpb17f48rca9gihy5b4oa",
            "name": "autotest-channel",  # уже существует!
            "display_name": "Duplicate Autotest Channel",
            "type": "O"
        }

        response = requests.post(url, headers=headers, json=data)
        
        assert response.status_code == 400, (
            f"Ожидался код 400 при дублировании имени канала, получен {response.status_code}"
        )
        print("Тест с дублирующимся именем канала: пройден")
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при попытке создать канал: {e}")
        raise
