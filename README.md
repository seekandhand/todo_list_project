Web-приложение для управления ToDo списками
===

### Инструкция по запуску

Перед началом работы необходимо:

1. Установить следующие
програмные пакеты:

    1. Интерпретатор python версии 3.7.6 - [python.org](http://python.org)
    2. Git - [https://git-scm.com/book/ru/v2/Введение-Установка-Git](https://git-scm.com/book/ru/v2/Введение-Установка-Git)
    
2. Скачать git репозиторий на локальный ПК:
```bash
git clone https://github.com/seekandhand/todo_list_project
```

3. Установить зависимости проекта (в созданной папке):
```bash
pip install -r requirements.txt
```

4. Запустить Django сервер:
```bash
python manage.py runserver
```

---
### Workflow

1. Регистрация пользователя:  http://localhost:8000/api/register/
(Поскольку таблица User имеет поле organization, которое является внешним ключом и ссылается на таблицу Organization,
 понадобится сначала создать объект Organization, например, в shell)
2. Авторизация: http://localhost:8000/api/login/
3. Управление ToDo листом: http://localhost:8000/api/todo_lists/
4. Выход из учетной записи: http://localhost:8000/api/logout/
   
В тестах рассмотрены основные кейсы. 
Работают команда createsuperuser, админка (если заранее авторизоваться superuser'ом)

---

### Запуск тестов
```bash
pytest
```
или
```bash
python manage.py test
```
