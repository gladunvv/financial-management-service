
[![Build Status](https://travis-ci.org/gladunvv/financial-management-service.svg?branch=master)](https://travis-ci.org/gladunvv/financial-management-service)

[![codecov](https://codecov.io/gh/gladunvv/financial-management-service/branch/master/graph/badge.svg)](https://codecov.io/gh/gladunvv/financial-management-service)

# financial-management-service
Simple financial management service on django rest framework


## Простой сервис управления финансами на основе Django rest framework

### Содержание:
+ [Краткое описание](#краткое-описание)
+ [Полезные ссылки](#полезные-ссылки)
+ [Requirements](#requirements)
+ [Сборка и запуск проекта](#сборка-и-запуск)
+ [Запросы](#запросы)
  * User
  * Wallet
  * Transaction
+ [Особенности](#особенности)
+ [Примеры ответа](#примеры-ответа)
  * [Endpoint 1](#endpoint-1)
  * [Endpoint 2](#endpoint-2)
  * [Endpoint 3](#endpoint-3)
+ [License](#license)


### Краткое описание:

Проект представляет собой простое API для управления финансами посредством транзакций. Приложение является приватным, пользователь 
может быть только один, он способен создавать, изменять, удалять кошельки, выполнять транзакции как на зачисление так и на списание 
средств (это единственный способ влияния на баланс кошелька). Внутри кошелька ведется история транзакций, есть возможность удалять транзакции,
у каждой транзакции есть сумма, дата, произвольный комментарий от пользователя. Есть возможность просматривать список кошельков и список
транзакций как в рамках одного конкретного кошелька так и все транзакции сразу.

### Полезные ссылки:

+ [Django documentation](https://docs.djangoproject.com/en/2.2/)
+ [Django rest framework](https://www.django-rest-framework.org/)
+ [API](https://ru.wikipedia.org/wiki/API)

### Requirements:
+ coverage==4.5.4
+ Django==2.2.5
+ django-debug-toolbar==2.0
+ djangorestframework==3.10.3
+ flake8==3.7.8

### Сборка и запуск:
```
git clone git@github.com:gladunvv/financial-management-service.git
cd financial-management-service/
pip install virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd fms_api/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Запросы:
+ User:
  * Create: 
  POST http://127.0.0.1:8000/api/v1/user/create/
  * Login:
  POST http://127.0.0.1:8000/api/v1/user/login/
  * Logout:
  POST http://127.0.0.1:8000/api/v1/user/logout/
  * Delete:
  DELETE http://127.0.0.1:8000/api/v1/user/delete/
  
+ Wallet:
  * Create:
  POST http://127.0.0.1:8000/api/v1/wallet/create/
  * One-Wallet:      
  GET http://127.0.0.1:8000/api/v1/wallet/1    
  PATCH http://127.0.0.1:8000/api/v1/wallet/1      
  DELETE http://127.0.0.1:8000/api/v1/wallet/1
  * All-Wallet:
  GET http://127.0.0.1:8000/api/v1/wallet/all/
  
+ Transaction:
  * Create: 
  POST http://127.0.0.1:8000/api/v1/wallet/transaction/create/
  * All-transactions:
  GET http://127.0.0.1:8000/api/v1/wallet/transaction/all/
  * Delete:
  DELETE http://127.0.0.1:8000/api/v1/wallet/transaction/delete/
  
  
### Особенности:
Пользователь может быть только один, не считая суперюзеров для администрирования и внутреннего управления приложением.    
При регистрации пользователю отдается уникальный токен, который в последующем нужно вложить в заголовок запроса 
для корректного доступа к данным. При выходе из приложения токен удаляется, заполучить новый можно только посредством 
входа.   
Есть два типа транзакций: зачисление средств (Contribution) и списание средств (Write-off), эти маркеры следует 
передавать в теле запроса с ключом ***"type_trans"***.     
Транзакция не будет выполнена если:
+ На балансе кошелька недостаточно средств
+ Сумма транзакции 0 или меньше
+ Какое либо поле не верно или отсутствует



### Примеры ответа:

### Endpoint 1:   
> POST http://127.0.0.1:8000/api/v1/user/create/        

Тело запроса:
```
{
	"username": "Vladislav",
	"email": "test@email.com",
	"password": "qwerty123"
}
```

Тело отвеа:
```
{
    "id": 1,
    "username": "Vladislav",
    "email": "test@email.com",
    "token": "3a9e6c18d20474e8fa6e481111aeeb9ccbfa7083"
}
```
### Endpoint 2:
> POST http://127.0.0.1:8000/api/v1/wallet/create/         

Заголовок запроса:
```
Authorization Token 3a9e6c18d20474e8fa6e481111aeeb9ccbfa7083
```
Тело запроса:
```
{
    "name": "Wallet 1"
}
```
Тело ответа:
```
{
    "id": 1,
    "name": "Wallet 1"
}
```
### Endpoint 3:
> POST http://127.0.0.1:8000/api/v1/wallet/transaction/create/        

Заголовок запроса:
```
Authorization Token 3a9e6c18d20474e8fa6e481111aeeb9ccbfa7083
```
Тело запроса:
```
{
	"wallet": "1",
	"amount": "666.66",
	"type_trans": "Contribution",
	"comment": "My first transaction"
}
```
Тело ответа:
```
{
    "id": 1,
    "amount": "666.66",
    "type_trans": "Contribution",
    "date_time": "2019-09-16T07:16:35.270840Z",
    "comment": "My first transaction"
}
```

### License
This project is licensed under the terms of the MIT license
