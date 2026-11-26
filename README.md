# Лабораторна робота №5

## Загальний опис роботи
Даний проект є реалізацією лабораторної роботи №5 «Збережені програми в MySQL» (Stored Programs in MySQL) для бази даних `animators_db` на базі бекенд-застосунку Flask (з Лабораторної роботи №4).

---

## Реалізовані програмні конструкції

### 1. Додаткова таблиця 1:M без фізичного зовнішнього ключа (`animator_reviews`)
- **Таблиця:** `animator_reviews` (відгуки про роботу аніматорів) зі стовпцями `review_id`, `animator_id`, `rating`, `comment`, `review_date`.
- **Зв'язок 1:M:** один аніматор (`animators`) може мати багато відгуків (`animator_reviews`).
- **Забезпечення цілісності значень:** Фізичний `FOREIGN KEY` відсутній. Цілісність контролюється набором SQL-тригерів:
  - `trg_reviews_check_fk_insert` (`BEFORE INSERT ON animator_reviews`) — перевіряє існування `animator_id` в таблиці `animators`. Якщо аніматора немає — генерація помилки через `SIGNAL SQLSTATE '45000'`.
  - `trg_reviews_check_fk_update` (`BEFORE UPDATE ON animator_reviews`) — перевіряє існування нового `animator_id`.
  - `trg_animators_restrict_delete` (`BEFORE DELETE ON animators`) — забороняє видалення аніматора (RESTRICT), якщо у нього є хоча б один відгук у `animator_reviews`.
  - `trg_animators_cascade_update` (`AFTER UPDATE ON animators`) — каскадно оновлює `animator_id` у пов'язаних відгуках при зміні первинного ключа.

---

### 2. Збережені процедури та користувацькі функції

#### Процедура 1: `sp_insert_client` (Параметризована вставка)
- Забезпечує вставку нових значень (`full_name`, `phone`, `email`) у таблицю `clients`.
- Повертає згенерований `client_id` через вихідний параметр `OUT p_client_id`.
- **Ендпоінт бекенду:** `POST /api/procedures/insert-client`

#### Процедура 2: `sp_link_animator_specialization` (Зв'язок M:M за реальними іменами)
- Приймає рядкові параметри: ім'я (`first_name`) та прізвище (`last_name`) аніматора, а також назву спеціалізації (`specialization_name`).
- Знаходить відповідні первинні ключі `animator_id` та `specialization_id`.
- Вставляє запис у стикувальну таблицю `animator_specializations`.
- **Ендпоінт бекенду:** `POST /api/procedures/link-m2m`

#### Процедура 3: `sp_insert_ten_nonames` (Пакетна вставка 10 стрічок &lt;Noname+№&gt;)
- Знаходить максимальний існуючий порядковий номер Noname і через цикл `WHILE` вставляє 10 послідовних записів у таблицю `specializations` у форматі `Noname1`, `Noname2`... (або `Noname5`, `Noname6`...).
- **Ендпоінт бекенду:** `POST /api/procedures/insert-nonames`

#### Користувацька функція 4: `fn_get_avg_hourly_rate` та Процедура: `sp_get_animators_above_avg_rate`
- **Функція `fn_get_avg_hourly_rate`:** обчислює та повертає середню погодинну ставку (`AVG(hourly_rate)`) серед усіх аніматорів.
- **Процедура `sp_get_animators_above_avg_rate`:** викликає створену функцію безпосередньо у виразі `SELECT`, фільтрує аніматорів зі ставкою >= середньої та розраховує відхилення (`hourly_rate - fn_get_avg_hourly_rate()`).
- **Ендпоінт бекенду:** `GET /api/procedures/stats-avg`

#### Процедура 5 (з курсором): `sp_cursor_split_animators`
- Реалізує перше завдання з курсором:
  1. Динамічно створює 2 нові таблиці зі штампом часу (наприклад, `animators_split1_20261119_170000` та `animators_split2_20261119_170000`), що мають ідентичну структуру до `animators`.
  2. За допомогою курсора `cur_anim` покроково зчитує рядки з `animators`.
  3. За допомогою функції `RAND() < 0.5` випадковим чином копіює поточний рядок в одну або іншу новостворену таблицю через підготовлені динамічні SQL-запити (`PREPARE / EXECUTE`).
- **Ендпоінт бекенду:** `POST /api/procedures/cursor-split`

---

### 3. Три довільні бізнес-тригери

1. **Заборона видалення стрічок з таблиці:**
   - Тригер: `trg_payments_prevent_delete` (`BEFORE DELETE ON payments`).
   - Повністю забороняє видалення записів про оплати для забезпечення фінансової цілісності.
2. **Таблиця-журнал та аудит модифікації даних:**
   - Таблиця журналу: `animator_audit_logs` (`log_id`, `animator_id`, `old_hourly_rate`, `new_hourly_rate`, `modified_at`, `details`).
   - Тригер: `trg_animators_log_update` (`AFTER UPDATE ON animators`).
   - Фіксує стару і нову ставку, точний штамп часу та опис зміни.
3. **Обмеження формату значень (не може закінчуватися двома нулями):**
   - Тригери: `trg_animators_no_double_zeros_insert` та `trg_animators_no_double_zeros_update` (`BEFORE INSERT/UPDATE ON animators`).
   - Перевіряють `MOD(ROUND(NEW.hourly_rate), 100) = 0`. Значення на кшталт `500.00`, `600.00` відхиляються з помилкою.

---

## Структура папки BD-5
\\	ext
BD-5/
├── lab5_animators_db.sql            # Повний SQL-скрипт БД зі схемою, даними, тригерами, процедурами, функціями
├── stored_programs.sql              # Окремий концентрований файл збережених програм та тригерів з коментарями
├── README.md                        # Документація проекту
├── docs/                            # Звіти та матеріали до захисту
│   ├── Завдання до лабор №5.docx    # Текст завдання лабораторної роботи №5
│   ├── Звіт_ЛР5.docx                # Повний офіційний звіт до захисту
│   ├── Звіт_SQL_Пояснення_коду.docx # Детальне пояснення SQL-коду
│   ├── Звіт_Програма_Пояснення_коду.docx # Пояснення архітектури Flask-застосунку
│   └── Пояснення_коду_програми_по_рядках.docx # Порядковий аналіз коду бекенду
├── .vscode/                         # Конфігурація запуску у VS Code
└── app/
    ├── config/
    │   └── app.yml                  # Конфігурація підключення до MySQL (та авто-fallback SQLite)
    ├── my_project/
    │   ├── auth/
    │   │   ├── controller/          # Web-контролери (включаючи procedure, review, audit_log)
    │   │   ├── dao/                 # DAO-класи (включаючи procedure_dao, review_dao, audit_log_dao)
    │   │   ├── domain/              # ORM-моделі (включаючи review, audit_log)
    │   │   ├── route/               # Flask маршрути для процедур та сутностей
    │   │   └── service/             # Бізнес-сервіси
    │   ├── ui/
    │   │   ├── dashboard.html       # Повнофункціональний Web UI з інтерактивною панеллю для процедур
    │   │   └── dashboard.py
    │   └── __init__.py              # Application Factory
    ├── tests/
    │   ├── postman_collection.json  # Повна колекція Postman (CRUD + Процедури + Тригери)
    │   └── test_api.py              # 17 автоматизованих pytest тестів
    ├── app.py                       # Точка входу Flask веб-сервера
    ├── data.sql                     # SQL-дамп структури, початкових даних та збережених програм
    ├── seed_data.py                 # Скрипт первинного наповнення
    ├── requirements.txt             # Залежності проекту
    └── setup.py
\
---

## Встановлення та запуск

### 1. Встановлення залежностей
\\ash
cd app
pip install -r requirements.txt
\
### 2. Запуск у СУБД MySQL
Імпортуйте файл \lab5_animators_db.sql\ або \stored_programs.sql\ у вашу базу даних:
\\ash
mysql -u root -p animators_db < ../lab5_animators_db.sql
\
### 3. Запуск веб-сервера Flask
\\ash
cd app
python app.py
\Відкрийте у браузері: **\http://127.0.0.1:5000\** або **\http://127.0.0.1:5000/dashboard\**

### 4. Автоматичні тести
\\ash
cd app
pytest tests/test_api.py -v
\
