import requests

BASE_URL = "http://localhost:8065/api/v4"
ADMIN_TOKEN = "9z7xtn7b4jgttd9jh888j6pkph"
CHANNEL_ID = "yj3akdrseprxmqy9g3ti1ripyr"
USER_ID = "frsrfzp85jboddccb3fdmhbhqc"

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}

def test_connection():
    """Проверка соединения с сервером"""
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        assert response.status_code == 200, "Сервер недоступен или токен недействителен"
        print("Соединение с сервером установлено.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        raise

def test_channel_exists():
    """Проверка существования канала"""
    url = f"{BASE_URL}/channels/{CHANNEL_ID}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Канал {CHANNEL_ID} не найден, код {response.status_code}"
    print(f"Канал {CHANNEL_ID} существует.")

def test_user_exists():
    """Проверка существования пользователя"""
    url = f"{BASE_URL}/users/{USER_ID}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Пользователь {USER_ID} не найден, код {response.status_code}"
    print(f"Пользователь {USER_ID} существует.")

def test_add_user_to_channel():
    """Добавление пользователя в канал"""
    url = f"{BASE_URL}/channels/{CHANNEL_ID}/members"
    data = {"user_id": USER_ID}
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 400 and "already a channel member" in response.text:
        print(f"Пользователь {USER_ID} уже является участником канала {CHANNEL_ID}.")
    else:
        assert response.status_code == 201, f"Ошибка при добавлении пользователя: {response.status_code}, {response.text}"
        print(f"Пользователь {USER_ID} успешно добавлен в канал {CHANNEL_ID}.")

def test_remove_user_from_channel():
    """Удаление пользователя из канала"""
    url = f"{BASE_URL}/channels/{CHANNEL_ID}/members/{USER_ID}"
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 404 and "not a member" in response.text:
        print(f"Пользователь {USER_ID} не является участником канала {CHANNEL_ID}.")
    else:
        assert response.status_code == 200, f"Ошибка при удалении пользователя: {response.status_code}, {response.text}"
        print(f"Пользователь {USER_ID} успешно удалён из канала {CHANNEL_ID}.")
