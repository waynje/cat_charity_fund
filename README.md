# Cat Charity Fund :coin:

## Оглавление
- [Cat Charity Fund :coin:](#cat-charity-fund-coin)
  - [Оглавление](#оглавление)
  - [Используемые технологии](#используемые-технологии)
  - [Структура проекта](#структура-проекта)
  - [Описание проекта](#описание-проекта)
    - [Права пользователей (Проекты)](#права-пользователей-проекты)
    - [Права пользователей (Пожертвования)](#права-пользователей-пожертвования)
    - [Процесс инвестирования](#процесс-инвестирования)
  - [Заполнение .env файла](#заполнение-env-файла)
  - [Запуск проекта](#запуск-проекта)

## Используемые технологии
:snake: Python 3.9, :incoming_envelope: FastAPI 0.78.0, :busts_in_silhouette: FastAPI-Users 10.0.4, :recycle: Pydantic 1.9.1, :package: SQLAlchemy 1.4.36, :notebook: aiosqlite 0.17.0, :memo: Alembic 1.7.7, :white_check_mark: Flake8 4.0.1

## Структура проекта
```
cat_charity_fund:
    ├── alembic
    │   ├── README
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions
    ├── app
    │   ├── __init__.py
    │   ├── api
    │   │   ├── endpoints
    │   │   │   └──...
    │   │   └── ...
    │   ├── core
    │   │   └── ...
    │   ├── crud
    │   │   └── ...
    │   ├── main.py
    │   ├── models
    │   │   └── ...
    │   ├── schemas
    │   │   └── ...
    │   └── services
    │       └── ...
    ├── tests
    │   └── ...
    ├── venv
    │   └── ...
    ├── .flake8
    ├── .gitignore
    ├── alembic.ini
    ├── fastapi.db
    ├── openapi.json
    ├── pytest.ini
    ├── README.md
    └── requirements.txt
```

## Описание проекта
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

**Проекты**

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

**Пожертвования**

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

**Пользователи**

Целевые проекты создаются администраторами сайта.
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

[:top: Вернуться к оглавлению](#оглавление)

<details><summary>Более подробная информация о проекте:</summary>
<p>

### Права пользователей (Проекты)
Любой посетитель сайта (в том числе неавторизованный) может посмотреть список всех проектов.

**Суперпользователь** может:
- создавать проекты;
- удалять проекты, в которые не было внесено средств;
- изменять название и описание существующего проекта, устанавливать для него новую требуемую сумму (но не меньше уже внесённой).

> *Никто не может менять через API размер внесённых средств, удалять или модифицировать закрытые проекты, изменять даты создания и закрытия проектов.

### Права пользователей (Пожертвования)

Любой **зарегистрированный пользователь** может сделать пожертвование.
**Зарегистрированный пользователь** может просматривать только свои пожертвования, при этом ему выводится только четыре поля:
- id;
- comment;
- full_amount;
- create_date.

> *Информация о том, инвестировано пожертвование в какой-то проект или нет, обычному пользователю **недоступна**.

**Суперпользователь** может просматривать список всех пожертвований, при этом ему выводятся все поля модели.

> *Редактировать или удалять пожертвования **не может никто**.

### Процесс инвестирования

Сразу после создания нового проекта или пожертвования запускается процесс **«инвестирования»** (``make_investment`` в директории ``app/services/investment.py``) (увеличение ``invested_amount`` как в пожертвованиях, так и в проектах, установка значений ``fully_invested`` и ``close_date``, при необходимости).

Если создан новый проект, а в базе были **«свободные»** (не распределённые по проектам) суммы пожертвований — они автоматически инвестируются в новый проект, и в ответе API эти суммы учитываются. То же касается и создания пожертвований: если в момент пожертвования есть открытые проекты, эти пожертвования автоматически зачисляются на их счета.

Функция, отвечающая за инвестирование, вызывается непосредственно из API-функций, отвечающих за создание пожертвований и проектов. Сама функция инвестирования расположена в директории ``app/services/`` в файле ``investment.py``.

[:top: Вернуться к оглавлению](#оглавление)

</p>
</details>

## Заполнение .env файла

Пример заполнения **.env** файла находится в файле **.env.example**


## Запуск проекта
1. Клонировать репозиторий:
```bash
git clone https://github.com/waynje/cat_charity_fund.git
```

2. Создать и активировать виртуальное окружение:
```bash
python3 -m venv .venv

bash/zsh
source .venv/bin/activate

Windows:
.venv\Scripts\activate.bat
```

3. Обновить pip и установить зависимости из ```requirements.txt```
```bash
python3 -m pip install --upgrade pip

pip install -r requirements.txt
pip install "uvicorn[standard]==0.17.6"   
```

4. Создать и заполнить файл **.env** в соответствии с [рекомендациями](#заполнение-конфигурационного-env-файла):

```bash
touch .env
```

5. Выполнить миграции:
```bash
alembic upgrade head
```

6. Запустить проект:
```bash
uvicorn app.main:app
```

После запуска проект будет доступен по адресу: http://127.0.0.1:8000

Документация к API досупна по адресам:
- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

[:top: Вернуться к оглавлению](#оглавление)


**Автор проекта:** [waynje](https://github.com/waynje/)

**Pytests:** [YandexPracticum](https://github.com/yandex-praktikum/cat_charity_fund/tree/master/tests)