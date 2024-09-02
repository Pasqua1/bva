# BovaApi SDK для Python

## Установка

Установите последнюю версию SDK с помощью команды:

```pip install git+https://github.com/yourusername/bovaapi```

## Использование

Создание экземпляра BovaClient:

```python
bova_client = BovaClient(api_host="https://bovatech.cc",
                         api_secret="your_api_secret",
                         api_token="your_api_token")

```

## P2P Транзакции

### Создание P2P транзакции

```python
payment_data = {
    "user_uuid": "364dbfc8-ae50-492f-bdd9-748edd84d5c9",
    "merchant_id": "test7",
    "bank_name": "sberbank",
    "amount": 500,
    "callback_url": "https://webhook.site/callback",
    "redirect_url": "https://ya.ru/",
    "email": "test@mail.ru",
    "customer_name": "Ivan Vasiliev",
    "currency": "rub",
    "payeer_identifier": "payeer_identifier123",
    "payeer_card_number": "1234567890123456",
    "lifetime": 1000,
    "payment_method": "card",
    "payeer_ip": "127.0.0.1",
    "payeer_type": "trust"
}

response = bova_client.create_payment(payment_data)
```

### Получение информации о P2P транзакции

```python
transaction_id := "9bb5f95f36e1e40d6b1376ed6ce5048172ebfdb7"

response = bova_client.get_payment_by_id(transaction_id)
```

### Отмена P2P транзакции

```python
transaction_id = '9bb5f95f36e1e40d6b1376ed6ce5048172ebfdb7'

response = bova_client.cancel_payment(transaction_id)
```

### Пометка P2P транзакции как оплаченной

```python
transaction_id = '9bb5f95f36e1e40d6b1376ed6ce5048172ebfdb7'

response = bova_client.mark_payment_as_paid(transaction_id)
```

## Массовые Транзакции

### Создание массовой транзакции

```python
mass_transaction_data = {
    "user_uuid": "364dbfc8-ae50-492f-bdd9-748edd84d5c9",
    "to_card": "4111111111111111",
    "amount": 200,
    "callback_url": "https://webhook.site/callback",
    "merchant_id": "test7",
    "currency": "rub",
    "payment_method": "card",
    "lifetime": 3600
}

response = bova_client.create_mass_transaction(mass_transaction_data)
```

### Получение информации о массовой транзакции

```python
mass_transaction_id = 'd9bc90bf-93d1-48e7-b3ef-380dba11b649'

response = bova_client.get_mass_transaction_by_id(mass_transaction_id)
```