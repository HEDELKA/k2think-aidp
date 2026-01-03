# 🔧 Troubleshooting Guide

## ❌ "RuntimeError: Authentication failed"

### Причины:
1. **Неверные credentials**
2. **K2Think сервис недоступен**
3. **Сетевая ошибка**
4. **Rate limiting**

### Решение:

**Шаг 1: Проверить credentials**
```python
# В Colab добавить новую ячейку:
import os
email = os.getenv("K2THINK_EMAIL")
password = os.getenv("K2THINK_PASSWORD")

print(f"Email: {email}")
print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
```

Если не видно - ввести заново в следующей ячейке:
```python
from getpass import getpass
os.environ['K2THINK_EMAIL'] = input("Email: ")
os.environ['K2THINK_PASSWORD'] = getpass("Password: ")
```

**Шаг 2: Проверить что credentials работают**
```python
# Зайти на https://www.k2think.ai
# Вручную залогиниться этой почтой/паролем
# Если не получается - исправить пароль
```

**Шаг 3: Проверить K2Think API напрямую**
```python
import requests

email = "your-email@example.com"
password = "your-password"

response = requests.post(
    "https://www.k2think.ai/api/auth/login",
    json={"email": email, "password": password},
    timeout=10
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
```

Если `status_code != 200`:
- **401** → Неверный email/пароль
- **400** → Неверный формат запроса
- **503** → Сервер недоступен (подождать)
- **429** → Rate limit (подождать 1-2 мин)

**Шаг 4: Включить debug mode**
```python
from k2think_client import K2ThinkClient

client = K2ThinkClient(debug=True)  # Покажет все логи API
```

Запустить чтобы увидеть детальные логи:
```
[K2Think] Initializing client for: email@example.com
[K2Think] API Base: https://www.k2think.ai
[K2Think] Attempting authentication...
[K2Think] POST https://www.k2think.ai/api/auth/login
[K2Think] Response status: ???
```

---

## ❌ "401 Unauthorized - Check credentials"

**Решение:**
1. Убедитесь что правильно вводите email и пароль
2. Проверьте что нет пробелов в начале/конце
3. Пароль чувствителен к регистру
4. Попробуйте залогиниться на https://www.k2think.ai вручную

---

## ❌ "Request timeout - API may be overloaded"

**K2Think сервер перегружен или недоступен**

**Решение:**
1. Подождать 5-10 минут
2. Проверить статус: https://www.k2think.ai
3. Попробовать позже
4. Заменить `timeout=60` на `timeout=120` в коде

---

## ❌ "Connection error"

**Сетевая проблема**

**Решение:**
1. Проверить интернет соединение
2. Отключить VPN если используется
3. Проверить firewall
4. В Colab: перезагрузить runtime

---

## ❌ "GPU not available"

**Решение для Google Colab:**
1. Runtime → Change runtime type
2. Select **GPU** as Hardware accelerator
3. Click **Save**
4. Runtime будет перезагружена
5. Запустить ячейки снова

---

## ✅ Быстрый тест

Скопировать и запустить в Colab:

```python
# Tест 1: Интернет
print("1️⃣ Testing internet...")
try:
    import requests
    r = requests.get("https://www.google.com", timeout=5)
    print(f"✓ Internet OK ({r.status_code})")
except:
    print("❌ No internet")

# Тест 2: GPU
print("\n2️⃣ Testing GPU...")
try:
    import subprocess
    result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
    print("✓ GPU available:")
    print(result.stdout[:200])
except:
    print("❌ GPU not available")

# Тест 3: K2Think API
print("\n3️⃣ Testing K2Think API...")
try:
    import requests
    email = input("Email: ")
    password = input("Password: ")
    
    r = requests.post(
        "https://www.k2think.ai/api/auth/login",
        json={"email": email, "password": password},
        timeout=10
    )
    
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("✓ K2Think auth OK")
    else:
        print(f"❌ K2Think error: {r.text[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")

# Тест 4: K2Think Client
print("\n4️⃣ Testing K2Think Client...")
try:
    from k2think_client import K2ThinkClient
    
    # Используй те же credentials из теста 3
    client = K2ThinkClient(email=email, password=password, debug=True)
    print("✓ Client initialized")
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## 📊 Возможные коды ошибок K2Think API

| Код | Значение | Решение |
|-----|----------|---------|
| 200 | OK | Все работает ✓ |
| 400 | Bad Request | Проверить формат запроса |
| 401 | Unauthorized | Проверить credentials |
| 403 | Forbidden | Аккаунт заблокирован? |
| 429 | Too Many Requests | Подождать 1-5 мин |
| 500 | Server Error | K2Think сервер упал |
| 503 | Service Unavailable | K2Think на обслуживании |

---

## 🔍 Debug режим

Включить в клиенте:
```python
client = K2ThinkClient(debug=True)
```

Покажет:
- API URL
- Request headers
- Response status
- Token (первые символы)
- Все ошибки подробно

---

## 🎯 Если ничего не помогает:

1. **Контактировать K2Think поддержку**
   - Email: support@k2think.ai
   - Telegram: https://t.me/k2think

2. **Попробовать позже** (когда сервер будет более стабилен)

3. **Использовать альтернативный API** если K2Think недоступен

4. **Контактировать AIDP**
   - Telegram: https://t.me/Aidpsupport
   - Email: support@aidp.store

---

## 💡 Pro Tips

1. **K2Think иногда перегружен** - лучше запускать не в пик
2. **Rate limit** - не делать много запросов подряд
3. **Timeout** - иногда нужно увеличить до 120 сек
4. **Reauthentication** - клиент автоматически переаутентифицируется если токен истек
5. **Debug mode** - включить если что-то не работает

---

**Основное:** Проверь credentials + интернет + GPU - 99% проблем решены!
