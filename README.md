# **Разработка и внедрение сервиса прогнозирования дефолта по кредитным картам с контейнеризацией и A/B-тестированием**


## **Описание проекта**

В рамках проекта разработан сервис машинного обучения для прогнозирования дефолта по кредитным картам.


Сервис включает:

- обучение модели RandomForestClassifier;

- Flask API с эндпоинтами `/health` и `/predict`;

- Docker-контейнеризацию;

- Предложение дополнительных метрик, инструментов для масштабирования, логирования;

- План A/B-тестирования

---

## **Структура проекта**

```
credit-card-default-ab-testing/
│
├── app/
│   ├── api.py
│   ├── model_handler.py
│   └── __init__.py
│
├── data/
│   └── raw/
│       └── UCI_Credit_Card.csv
│
├── docker/
│   └── Dockerfile
│
├── models/
│   ├── model_v1.joblib
│   └── features.json
│
├── reports/
│   └── metrics_v1.json
│
├── src/
│   └── models/
│       └── train_model.py
│
├── screenshots/
│   ├── DockerDesktop.JPG
│   ├── health.JPG
│   └── predict.JPG
│
├── ab_test_plan.md
├── docker-compose.yml
├── request.json
├── requirements.txt
└── README.md
```

---


## **Запуск локально**

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
python app/api.py
```


### **Обучение модели**

```bash
python src/models/train_model.py

```

## API

### GET /health

Проверка работоспособности сервиса

Пример запроса:
```bash
curl.exe http://127.0.0.1:5000/health
```

Пример ответа:
```json
{
  "model_version": "v1",
  "service": "credit-card-default-prediction",
  "status": "ok"
}
```

### POST /predict

Пример запроса:
```bash
curl.exe -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "@request.json"
```

Пример запроса:
```JSON
{
  "LIMIT_BAL": 20000,
  "SEX": 2,
  "EDUCATION": 2,
  "MARRIAGE": 1,
  "AGE": 24,
  "PAY_0": 2,
  "PAY_2": 2,
  "PAY_3": 0,
  "PAY_4": 0,
  "PAY_5": 0,
  "PAY_6": 0,
  "BILL_AMT1": 3913,
  "BILL_AMT2": 3102,
  "BILL_AMT3": 689,
  "BILL_AMT4": 0,
  "BILL_AMT5": 0,
  "BILL_AMT6": 0,
  "PAY_AMT1": 0,
  "PAY_AMT2": 689,
  "PAY_AMT3": 0,
  "PAY_AMT4": 0,
  "PAY_AMT5": 0,
  "PAY_AMT6": 0
}
```

Пример ответа:
```json
{"prediction":1,"probability":0.7898}
```


---

## **Docker**

Сборка:

```bash
docker build -f docker/Dockerfile -t credit-card-default-service .
```

Запуск:

```bash
docker pull vpetrov23ml/credit-card-default-service:v1
docker run -p 5000:5000 vpetrov23ml/credit-card-default-service:v1
```

---

## **Docker Hub**

https://hub.docker.com/r/vpetrov23ml/credit-card-default-service

---


## **Архитектура сервиса (концепт):**


### **Монолит vs микросервисы**

В рамках данного учебного проекта выбран **монолитный подход**.

Причины:

- простота реализации;

- быстрее разработка и деплой;

- нет необходимости масштабирования;


### **Концепт брокеров сообщений**

В будущем можно использовать **RabbitMQ** для:

- асинхронной обработки запросов;

- необходимости внедрения инфраструктуры с участием очереди;

- логирования
---

### **Логирование**

Для сбора и анализа логов может использоваться ELK-стек (Elasticsearch, Logstash, Kibana), который позволяет:

- мониторить работу сервиса

- анализировать поведение модели

- отслеживать ошибки

- визуализировать метрики


Также можно использовать связку Prometheus (для сбора и хранения метрик, а также для настройки системы мониторинга и оповещений ) и Grafana (для визуализации данных).

## **Оркестрация**

В рамках проекта создан файл docker-compose.yml

Запуск:

```bash
docker compose up --build
```


## **Обзор инструментов MLops (концепт)**


### **DVC**


**DVC** позволяет управлять версиями файлов и каталогов данных, промежуточными результатами и моделями ML с использованием системы Git.


### **MLflow**

**MLflow** используется для логирования экспериментов, хранения кода, данных, результатов обучения.



## **Бизнес-метрики**

- Ожидаемые финансовые потери (рассчитываются на основе вероятности дефолта и суммы кредита);

- Default Rate - отношение дефолтов к количеству одобренных кредитов.

---

## **Организация A/B-тестирования**

См. ab_test_plan.md

---

## Демонстрация работы

Скриншоты работы сервиса находятся в папке `screenshots/`

