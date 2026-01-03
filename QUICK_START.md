# 🚀 K2Think AIDP - Quick Start Guide

**Получение 350 USDC на AIDP GPU Compute Bounty за 30 минут**

## 🎯 Два способа запуска

### ✅ СПОСОБ 1: Google Colab (Рекомендуется - Бесплатный GPU!)

**Преимущества:**
- Бесплатный T4 GPU (Google дает!)
- Ничего не устанавливать
- Одна кнопка → готовый результат
- Идеально для demo видео

**Шаги:**

1️⃣ **Открыть Colab notebook:**
   - Прямая ссылка: 
     ```
     https://colab.research.google.com/github/HEDELKA/k2think-aidp/blob/python-colab/colab_demo.ipynb
     ```

2️⃣ **Включить GPU:**
   - В Colab нажмите: `Runtime` → `Change runtime type`
   - Выберите **GPU** 
   - Нажмите `Save`

3️⃣ **Скопировать K2Think логин и пароль**
   - Найти в `.env` файле
   - Или ввести в ячейке когда попросит

4️⃣ **Запустить все ячейки:**
   - Ctrl+F9 (Windows) или Cmd+F9 (Mac)
   - Или кнопка "Run all"

5️⃣ **Посмотреть результаты:**
   - GPU информация вверху
   - AI ответы в ячейках
   - GPU логи внизу

6️⃣ **Записать видео (1-2 мин):**
   - Скриншот или screen record
   - Показать GPU логи
   - Показать AI ответы
   - Залить на YouTube (public)

**Готово! Идет на submission!**

---

### ⚙️ СПОСОБ 2: Локально (Python)

**Нужно:**
- Python 3.8+
- NVIDIA GPU (или CPU режим)
- K2Think credentials

**Шаги:**

```bash
# 1. Клонировать репо
git clone https://github.com/HEDELKA/k2think-aidp.git
cd k2think-aidp

# 2. Переключиться на python-colab ветку
git checkout python-colab

# 3. Запустить setup
bash SETUP.sh

# 4. Отредактировать .env
nano .env
# Вставить:
# K2THINK_EMAIL=your-email@example.com
# K2THINK_PASSWORD=your-password

# 5. Запустить demo
python colab_demo.py
```

**Результат:**
- GPU logs напечатаны
- AI ответы выведены
- Все сохранено в `gpu-usage.log`

---

## 📊 Что будет видно

```
╔════════════════════════════════════════════════════════════╗
║   Custom AI Agent Wrapper - Decentralized Compute          ║
║   K2Think + AIDP GPU Network Demo                          ║
╚════════════════════════════════════════════════════════════╝

GPU Status: available
  GPU: NVIDIA A100 (или T4 в Colab)
  Memory: 40GB (или 15GB в Colab)

🤖 Initializing K2Think client...
✓ Authenticated

⚡ Task 1: Text Generation
[2024-01-03T14:23:46.234Z] DURING: Text Generation
0, 85 %, 75 %, 18432 MB, 72°C

Response: GPU compute is powerful because...
Tokens used: 145

...

✅ Demo completed!

📋 GPU Activity Log:
============================================================
[2024-01-03T14:23:45.123Z] PRE-COMPUTE GPU STATUS
GPU Details:
0, NVIDIA A100-SXM4-40GB, 535.104.05, 40960 MB

Memory & Utilization:
0, 0 MB, 40960 MB, 0 %, 35°C
```

---

## 🎥 Записать Demo Видео

### В Google Colab:

1. **Скролить вверх** - показать GPU status
2. **Скролить вниз** - показать AI responses  
3. **Скролить еще вниз** - показать GPU logs

Снимать:
- OBS Studio (бесплатно) - профессионально
- Встроенный screen recorder - просто
- ScreenFlow (Mac) - удобно

Требования:
- Длительность: 1-2 минуты
- Качество: 720p+
- Формат: MP4
- Загрузить на YouTube (public или unlisted)

---

## 📝 AIDP Submission Форма

Заполнить на: https://superteam.fun/earn

| Поле | Значение |
|------|----------|
| Link to Submission | https://github.com/HEDELKA/k2think-aidp |
| AIDP Marketplace | [Создать после GPU access] |
| Demo Video | [YouTube link с логами] |
| GPU Usage Explanation | "Real-time GPU monitoring via nvidia-smi. Pre/during/post-compute GPU status logging. GPU memory utilization visible in logs." |
| Tweet Link | [Optional] |

---

## ✅ Checklist

- [ ] Открыл Colab notebook
- [ ] Включил GPU (Runtime → GPU)
- [ ] Вввел K2Think credentials
- [ ] Запустил все ячейки (Ctrl+F9)
- [ ] Видны GPU логи
- [ ] Видны AI ответы
- [ ] Записал 1-2 мин видео
- [ ] Залил на YouTube (public)
- [ ] Скопировал YouTube link
- [ ] Готов к submission!

---

## 🔗 Ссылки

**Colab Notebook:**
https://colab.research.google.com/github/HEDELKA/k2think-aidp/blob/python-colab/colab_demo.ipynb

**GitHub Repo:**
https://github.com/HEDELKA/k2think-aidp (ветка: python-colab)

**AIDP:**
- Website: https://aidp.store
- Telegram: https://t.me/Aidpofficial
- Bounty: https://superteam.fun/earn

---

## 🆘 Проблемы?

### "GPU not available в Colab"
- ✓ Runtime → Change runtime type → GPU

### "Authentication failed"
- ✓ Проверить email/password на https://www.k2think.ai
- ✓ Нет спецсимволов в пароле?

### "Connection timeout"
- ✓ K2Think сервер может быть перегружен
- ✓ Попробовать через 1-2 минуты

---

## 🎉 Итого

1. **30 мин** → Запустить в Colab, записать видео
2. **10 мин** → Залить на YouTube
3. **5 мин** → Заполнить submission форму
4. **Submit!** 

**Готов на 350 USDC?** 🚀

Custom AI Agent Wrapper optimized for Decentralized Compute ✨
