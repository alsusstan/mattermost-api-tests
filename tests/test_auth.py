import requests

BASE_URL = "http://localhost:8065/api/v4"

def test_successful_login():
    """Проверка успешной аутентификации"""
    url = f"{BASE_URL}/users/login"
    data = {
        "login_id": "testqa",
        "password": "TestPass123!"
    }

    try:
        response = requests.post(url, json=data)
        assert response.status_code == 200, f"Ожидался код 200, а получен {response.status_code}"
        assert "Token" in response.headers, "Токен отсутствует в заголовках ответа"
        print("Успешная аутентификация: пройдена")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        raise

def test_invalid_password():
    """Проверка аутентификации с неверным паролем"""
    url = f"{BASE_URL}/users/login"
    data = {
        "login_id": "testqa",
        "password": "WrongPassword123!"
    }

    try:
        response = requests.post(url, json=data)
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        assert "Token" not in response.headers, "Токен не должен присутствовать в ответе при ошибке"
        print("Тест с неверным паролем: пройден")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        raise

def test_blocked_user_login():
    """Проверка входа заблокированного пользователя"""
    url = f"{BASE_URL}/users/login"
    data = {
        "login_id": "blockedqa2025",
        "password": "Blocked#Test42"
    }

    try:
        response = requests.post(url, json=data)
        assert response.status_code == 401, f"Ожидался код 401, а получен {response.status_code}"
        assert "Token" not in response.headers, "Токен не должен присутствовать в ответе при ошибке"
        print("Тест с заблокированным пользователем: пройден")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        raise

def test_inactive_user_login():
    """Проверка входа неактивного пользователя"""
    url = f"{BASE_URL}/users/login" 
    data = {
        "login_id": "inactiveqa2025",
        "password": "Inactive#Test56"
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 404:
            print("Внимание: получен код 404 (возможный баг)")
        assert response.status_code in [401, 403], (
            f"Ожидался код 401 или 403, получен {response.status_code}"
        )
        assert "Token" not in response.headers, "Токен не должен присутствовать в ответе при ошибке"
        print("Тест с неактивным пользователем: завершен")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        raise

def test_auth_server_unavailable():
    """Проверка недоступности сервера аутентификации"""
    url = "http://localhost:9999/api/v4/users/login"
    data = {
        "login_id": "testqa",
        "password": "TestPass123!"
    }

    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"Неожиданно получили ответ: {response.status_code}")
        assert False, "Сервер не должен быть доступен"
    except requests.exceptions.ConnectionError:
        print("Тест недоступности сервера: пройден (ожидаемое исключение)")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        raise
