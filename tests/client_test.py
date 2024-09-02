import pytest
from unittest.mock import patch, MagicMock

from bva.bova_client import BovaClient

@pytest.fixture
def bova_client():
    return BovaClient(api_host="https://bovatech.cc", api_secret="74f9589ecae089b23668b92e29q2u1hiddad2", api_token="123123123123")


@pytest.fixture
def get_signature():
    return '29a530919cf575d8440fbdd7952bb917cc0f28d6'

def test_generate_signature(bova_client, get_signature):
    payload = {
        "user_uuid": "364dbfc8-ae50-492f-bdd9-748edd84d5c9",
        "amount": 300,
        "callback_url": "https://weebhook.site/callback123",
        "bank_name": "sberbank"
    }

    # Call the _generate_signature method
    generated_signature = bova_client._generate_signature(payload)

    # Assert that the generated signature matches the expected one
    assert generated_signature == get_signature


@pytest.fixture
def get_header():
    return {
        'Content-Type': 'application/json',
        'Signature': '29a530919cf575d8440fbdd7952bb917cc0f28d6',
        'Authorization': 'Bearer 123123123123'
    }

def test_generate_headers(bova_client, get_signature, get_header):
    # Call the _generate_signature method
    generated_header = bova_client._headers(get_signature)

    # Assert that the generated signature matches the expected one
    assert generated_header == get_header


@pytest.fixture
def create_payment_request_data():
    return {
        "user_uuid": "0091e581-d96f-478b-be98-51937b66204d",
        "merchant_id": "test",
        "bank_name": "sberbank",
        "amount": 500,
        "callback_url": "https://webhook.site/cfe48fa4-dd15-4a8b-a318-c918e94cb020",
        "redirect_url": "https://ya.ru/",
        "email": "test@mail.ru",
        "customer_name": "Ivan Vasiliev",
        "currency": "rub",
        "payeer_identifier": "payeer_identifier123",
        "payeer_card_number": "1234567890123456",
        "lifetime": 1000,
        "payment_method": "card",
        "payeer_ip": "127.0.0.1",
        "payeer_type": "ftd"
    }

@pytest.fixture
def create_payment_response_data():
    return {
        "result_code": "ok",
        "payload": {
            "id": "666b32d60ad6fe9cc30bb0f2c3497976f29ec8d8",
            "merchant_id": "string",
            "currency": "rub",
            "form_url": "https://p2p.bovatech.pw/666b32d60ad6fe9cc30bb0f2c3497976f29ec8d8",
            "state": "waiting_payment",
            "created_at": "2024-04-08T14:06:00.471+03:00",
            "updated_at": "2024-04-08T14:06:00.516+03:00",
            "close_at": "2024-04-08T14:36:00.248+03:00",
            "callback_url": "https://webhook.site/cfe48fa4-dd15-4a8b-a318-c918e94cb020",
            "redirect_url": "https://ya.ru/",
            "email": "test@mail.ru",
            "customer_name": "Ivan Vasiliev",
            "rate": "94.98",
            "amount": "5.26",
            "fiat_amount": "500.0",
            "old_fiat_amount": "500.0",
            "service_commission": "6.5",
            "total_amount": "4.9181",
            "payment_method": "sberpay",
            "resipient_card": {
                "id": "41fa3334-0e17-46db-b1a4-22cd5b2d5422",
                "number": "4111111111111111",
                "bank_name": "sberbank",
                "bank_full_name": "Сбербанк",
                "bank_colors": {},
                "brand": None,
                "card_holder": "Ivan Ivanov",
                "payment_method": "card",
                "updated_at": "2024-04-08T14:06:00.248+03:00",
                "created_at": "2024-04-08T14:06:00.248+03:00",
                "sberpay_url": "https://www.sberbank.com/sms/pbpn?requisiteNumber=9047649900"
            }
        }
    }

@patch('requests.post')
def test_create_payment(mock_post, bova_client, create_payment_request_data, create_payment_response_data):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = create_payment_response_data
    mock_post.return_value = mock_response

    # Call the method
    response = bova_client.create_payment(create_payment_request_data)

    # Assert that the request was made correctly
    mock_post.assert_called_once_with(
        "https://bovatech.cc/v1/p2p_transactions",
        headers=bova_client._headers(bova_client._generate_signature(create_payment_request_data)),
        data=create_payment_request_data,
    )

    # Assert the response
    assert response["result_code"] == "ok"
    assert response["payload"] == create_payment_response_data["payload"]


@pytest.fixture
def get_tx_id():
    return '9bb5f95f36e1e40d6b1376ed6ce5048172ebfdb7'

@pytest.fixture
def mark_payment_as_paid_response_data():
    return {
        "result_code": "ok",
        "payload": {
            "id": "9bb5f95f36e1e40d6b1376ed6ce5048172ebfdb7",
            "merchant_id": "string",
            "amount": "300.0",
            "old_amount": "300.0",
            "form_url": "https://p2p.bovapay.io/9bb5f95f36e1e40d6b1376ed6ce5048172ebfdb7",
            "state": "paid",
            "created_at": "2022-05-24T21:43:04.613+03:00",
            "updated_at": "2022-05-24T21:45:07.487+03:00",
            "callback_url": "https://webhook.site/4317036e-3ebc-4b35-b475-96bbaf83ff2a",
            "resipient_card": {
            "id": 82,
            "number": "5280413754741010",
            "bank_name": "Tinkoff Bank",
            "bank_colors": [
                "#444444",
                "#222222"
            ],
            "brand": "mastercard",
            "updated_at": "2022-05-24T21:44:15.514+03:00",
            "created_at": "2022-05-24T21:43:02.113+03:00"
            }
        }
    }

@patch('requests.put')
def test_mark_payment_as_paid(mock_put, bova_client, mark_payment_as_paid_response_data, get_tx_id):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = mark_payment_as_paid_response_data
    mock_put.return_value = mock_response

    # Call the method
    response = bova_client.mark_payment_as_paid(get_tx_id)

    # Assert that the request was made correctly
    mock_put.assert_called_once_with(
        f"https://bovatech.cc/v1/p2p_transactions/{get_tx_id}/paid",
        headers=bova_client._headers()
    )

    # Assert the response 
    assert response["result_code"] == "ok"
    assert response["payload"] == mark_payment_as_paid_response_data["payload"]


@pytest.fixture
def cancel_payment_response_data():
    return {
        "result_code": "ok",
        "payload": {
            "id": "9fdb097bb7bf683442cc921755357f57e33ffc18",
            "merchant_id": "string",
            "amount": "520.0",
            "old_amount": "520.0",
            "form_url": "https://p2p.bovapay.io/9bb5f95f36e1e40d6b1376ed6ce5048172ebfdb7",
            "state": "failed",
            "created_at": "2022-06-17T17:32:29.771+03:00",
            "updated_at": "2022-06-17T18:08:31.710+03:00",
            "callback_url": "https://webhook.site/4317036e-3ebc-4b35-b475-96bbaf83ff2a",
            "resipient_card": {
            "id": 194235,
            "number": "4276300058274294",
            "bank_name": "Сбербанк RUB",
            "bank_colors": {},
            "brand": "visa",
            "updated_at": "2022-06-17T18:08:31.646+03:00",
            "created_at": "2022-06-17T17:32:29.758+03:00"
            }
        }
    }

@patch('requests.put')
def test_cancel_payment(mock_put, bova_client, cancel_payment_response_data, get_tx_id):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = cancel_payment_response_data
    mock_put.return_value = mock_response

    # Call the method
    response = bova_client.cancel_payment(get_tx_id)

    # Assert that the request was made correctly
    mock_put.assert_called_once_with(
        f"https://bovatech.cc/v1/p2p_transactions/{get_tx_id}/cancel",
        headers=bova_client._headers()
    )

    # Assert the response 
    assert response["result_code"] == "ok"
    assert response["payload"] == cancel_payment_response_data["payload"]


@pytest.fixture
def get_payment_id():
    return '6092c858b2ba7f2b85906879157517d276e438'

@pytest.fixture
def get_payment_by_id_response_data():
    return {
        "result_code": "ok",
        "payload": {
            "id": "6092c858b2ba7f2b85906879157517d276e438",
            "merchant_id": "21716214349756161997",
            "currency": "rub",
            "to_currency": None,
            "form_url": "https://pay.bova.cash/payments/6092c858b2ba7f2b85906879157517c2d276e438",
            "state": "failed",
            "created_at": "2024-05-20T17:12:30.179+03:00",
            "updated_at": "2024-05-20T17:13:59.364+03:00",
            "close_at": "2024-05-20T17:42:30.168+03:00",
            "callback_url": "https://example.com/webhook",
            "redirect_url": None,
            "email": "test@gmail.com",
            "customer_name": "Test Test",
            "rate": "92.78",
            "amount": "37.72",
            "fiat_amount": "3500.0",
            "old_fiat_amount": "3500.0",
            "service_commission": "6.5",
            "total_amount": "35.2682",
            "payment_method": "sberpay",
            "card_number": None,
            "resipient_card": {
            "id": "8fe1d6c3-4a4c-41f4-a7c7-9c14ba2a35f2",
            "number": "+79371151137",
            "bank_name": "sberbank",
            "bank_full_name": "Сбербанк",
            "bank_colors": {},
            "brand": None,
            "card_holder": "LEONTIY VIDYAKOV",
            "payment_method": "sberpay",
            "updated_at": "2024-05-20T17:12:30.168+03:00",
            "created_at": "2024-05-20T17:12:30.168+03:00",
            "sberpay_url": "https://www.sberbank.com/sms/pbpn?requisiteNumber=9371850137"
            }
        }
    }

@patch('requests.get')
def test_get_payment_by_id(mock_get, bova_client, get_payment_by_id_response_data, get_payment_id):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = get_payment_by_id_response_data
    mock_get.return_value = mock_response

    # Call the method
    response = bova_client.get_payment_by_id(get_payment_id)

    # Assert that the request was made correctly
    mock_get.assert_called_once_with(
        f"https://bovatech.cc/v1/p2p_transactions/{get_payment_id}",
        headers=bova_client._headers()
    )

    # Assert the response 
    assert response["result_code"] == "ok"
    assert response["payload"] == get_payment_by_id_response_data["payload"]


@pytest.fixture
def create_dispute_response_data():
    return {
        "id": 524,
        "state": "opened",
        "proof_image": "",
        "proof_image2": "",
        "p2p_transaction_id": "db42949bc938cff189c8166a579b1965631d393e",
        "repeated": False,
        "amount": 1005,
        "updated_at": "2022-07-01T01:28:34.958+03:00",
        "created_at": "2022-07-01T01:28:34.898+03:00",
        "resipient_card": {
            "id": 254281,
            "number": "4274170048174850",
            "bank_name": "Сбербанк RUB",
            "bank_colors": {},
            "brand": "visa",
            "updated_at": "2022-06-30T13:16:22.482+03:00",
            "created_at": "2022-06-30T12:40:03.429+03:00"
        }
    }

@patch('requests.post')
def test_create_dispute(mock_post, bova_client, create_dispute_response_data):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = create_dispute_response_data
    mock_post.return_value = mock_response

    transaction_id = "db42949bc938cff189c8166a579b1965631d393e"
    amount = 1005

    # Call the method
    response = bova_client.create_dispute(
        transaction_id=transaction_id,
        amount=amount,
        proof_images=None  # Assuming no proof image for this test
    )

    # Assert that the request was made correctly
    mock_post.assert_called_once_with(
        "https://bovatech.cc/v1/p2p_disputes/from_client",
        headers=bova_client._headers(),
        data={
            "transaction_id": transaction_id,
            "p2p_dispute[amount]": str(amount),
        },
        files={}
    )

    # Assert the response
    assert response == create_dispute_response_data

@pytest.fixture
def create_dispute_with_proof_images_response_data():
    return {
        "id": 524,
        "state": "opened",
        "proof_image": "https://bovatech.cc/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBdDRDIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--740f67f5a74a38f025ae46ec31cd7df9cb482234/photo_2022-06-29_10-41-27.jpg",
        "proof_image2": "https://bovatech.cc/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBdDRDIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--740f67f5a74a38f025ae46ec31cd7df9cb482234/photo_2022-06-29_10-41-27.jpg",
        "p2p_transaction_id": "db42949bc938cff189c8166a579b1965631d393e",
        "repeated": False,
        "amount": 1005,
        "updated_at": "2022-07-01T01:28:34.958+03:00",
        "created_at": "2022-07-01T01:28:34.898+03:00",
        "resipient_card": {
            "id": 254281,
            "number": "4274170048174850",
            "bank_name": "Сбербанк RUB",
            "bank_colors": {},
            "brand": "visa",
            "updated_at": "2022-06-30T13:16:22.482+03:00",
            "created_at": "2022-06-30T12:40:03.429+03:00"
        }
    }

@patch('requests.post')
def test_create_dispute_with_proof_image(mock_post, bova_client, create_dispute_with_proof_images_response_data):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = create_dispute_with_proof_images_response_data
    mock_post.return_value = mock_response

    transaction_id = "db42949bc938cff189c8166a579b1965631d393e"
    amount = 1005
    proof_images = [
        "https://bovatech.cc/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBdDRDIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--740f67f5a74a38f025ae46ec31cd7df9cb482234/photo_2022-06-29_10-41-27.jpg",
        "https://bovatech.cc/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBdDRDIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--740f67f5a74a38f025ae46ec31cd7df9cb482234/photo_2022-06-29_10-41-27.jpg"
    ]

    # Call the method
    response = bova_client.create_dispute(
        transaction_id=transaction_id,
        amount=amount,
        proof_images=proof_images
    )

    # Assert that the request was made correctly
    mock_post.assert_called_once_with(
        "https://bovatech.cc/v1/p2p_disputes/from_client",
        headers=bova_client._headers(),
        data={
            "transaction_id": transaction_id,
            "p2p_dispute[amount]": str(amount),
        },
        files={
            "p2p_dispute[proof_image]": proof_images[0],
            "p2p_dispute[proof_image2]": proof_images[1]
        }
    )

    # Assert the response
    assert response == create_dispute_with_proof_images_response_data


@pytest.fixture
def create_mass_transaction_request_data():
    return {
        "user_uuid": "364dbfc8-ae50-492f-bdd9-748edd84d5c9",
        "to_card": "4111111111111111",
        "amount": 200,
        "callback_url": "https://webhook.site/2ebae889-65ce-43a3-920f-425ff83404bf",
        "merchant_id": "test7",
        "currency": "rub",
        "payment_method": "card",
        "lifetime": 3600
    }

@pytest.fixture
def create_mass_transaction_response_data():
    return {
        "result_code": "ok",
        "payload": {
            "id": "86956ea6-15c2-4440-a7ae-d501e3e17466",
            "amount": "2.0",
            "commission_type": "relative",
            "service_commission": "3.0",
            "rate": "100.0",
            "fiat_amount": "200.0",
            "old_fiat_amount": "200.0",
            "state": "created",
            "currency": "rub",
            "r_line": "",
            "created_at": "2023-12-19T08:01:58.140+03:00",
            "updated_at": "2023-12-19T08:01:58.140+03:00",
            "recipient_card": "411111******1111"
        }
    }

@patch('requests.post')
def test_create_mass_transaction(mock_post, bova_client, create_mass_transaction_request_data, create_mass_transaction_response_data):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = create_mass_transaction_response_data
    mock_post.return_value = mock_response

    # Call the method
    response = bova_client.create_mass_transaction(create_mass_transaction_request_data)

    # Assert that the request was made correctly
    mock_post.assert_called_once_with(
        "https://bovatech.cc/v1/mass_transactions",
        headers=bova_client._headers(bova_client._generate_signature(create_mass_transaction_request_data)),
        data=create_mass_transaction_request_data,
    )

    # Assert the response
    assert response["result_code"] == "ok"
    assert response == create_mass_transaction_response_data


@pytest.fixture
def get_mass_transaction_id():
    return 'd9bc90bf-93d1-48e7-b3ef-380dba11b649'

@pytest.fixture
def get_mass_transaction_by_id_response_data():
    return {
        "result_code": "ok",
        "payload": {
            "id": "d9bc90bf-93d1-48e7-b3ef-380dba11b649",
            "amount": "20.08",
            "commission_type": "relative",
            "service_commission": "2.0",
            "rate": "92.15",
            "fiat_amount": "1850.0",
            "old_fiat_amount": "1850.0",
            "state": "paid",
            "r_line": "5",
            "created_at": "2024-01-11T21:46:29.211+03:00",
            "updated_at": "2024-01-11T21:54:49.933+03:00",
            "total_amount": "20.4816",
            "recipient_card": "220220******0303"
        }
    }

@patch('requests.get')
def test_get_mass_transaction_by_id(mock_get, bova_client, get_mass_transaction_id, get_mass_transaction_by_id_response_data):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = get_mass_transaction_by_id_response_data
    mock_get.return_value = mock_response

    # Call the method
    response = bova_client.get_mass_transaction_by_id(get_mass_transaction_id)

    # Assert that the request was made correctly
    mock_get.assert_called_once_with(
        f"https://bovatech.cc/v1/mass_transactions/{get_mass_transaction_id}",
        headers=bova_client._headers()
    )

    # Assert the response 
    assert response["result_code"] == "ok"
    assert response["payload"] == get_mass_transaction_by_id_response_data["payload"]


@pytest.fixture
def get_account_balances_response_data():
    return {
        "result_code": "ok",
        "payload": [
            {
                "name": "merchant_income",
                "balance": "29167.252106",
                "currency": "usdt_trc20",
                "created_at": "2024-01-04T12:26:53.782+03:00",
                "updated_at": "2024-01-04T12:26:53.782+03:00",
                "balance_rub": "3879292.46208",
                "balance_uzs": "574916771.31798"
            },
            {
                "name": "escrow",
                "balance": "0.0",
                "currency": "usdt_trc20",
                "created_at": "2024-01-04T12:26:53.787+03:00",
                "updated_at": "2024-01-04T12:26:53.787+03:00",
                "balance_rub": "0.0",
                "balance_uzs": "0.0"
            }
        ]
    }

@patch('requests.get')
def test_get_account_balances(mock_get, bova_client, get_account_balances_response_data):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = get_account_balances_response_data
    mock_get.return_value = mock_response

    # Call the method
    response = bova_client.get_account_balances()

    # Assert that the request was made correctly
    mock_get.assert_called_once_with(
        "https://bovatech.cc/v1/merchant/accounts",
        headers=bova_client._headers()
    )

    # Assert the response 
    assert response["result_code"] == "ok"
    assert response["payload"] == get_account_balances_response_data["payload"]


@pytest.fixture
def get_get_merchant_rates():
    return {
        "usdt_rub": "91.25",
        "usdt_uah": "41.69",
        "usdt_uzs": "13699.0",
        "usdt_kgs": "88.0"
    }

@patch('requests.get')
def test_get_merchant_rates(mock_get, bova_client, get_get_merchant_rates):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = get_get_merchant_rates
    mock_get.return_value = mock_response

    # Call the method
    response = bova_client.get_merchant_rates()

    # Assert that the request was made correctly
    mock_get.assert_called_once_with(
        "https://bovatech.cc/v1/merchant/rates",
        headers=bova_client._headers()
    )

    # Assert the response 
    assert response == get_get_merchant_rates


@pytest.fixture
def get_merchant_deposits_request_data():
    return {
        "user_uuid": "0091e581-d96f-478b-be98-51937b66204d",
        "merchant_id": "string",
        "amount": 1000,
        "callback_url": "https://webhook.site/f9d55aae-e554-48c5-b56a-f7cd93fcca7d",
        "redirect_url": "https://ya.ru/", 
        "email": "test@mail.ru", 
        "customer_name": "Ivan Vasiliev", 
        "currency": "rub", 
        "payeer_identifier": "payeer_identifier",
        "payeer_ip": "127.0.0.1",
        "payeer_type": "ftd",
        "lifetime": 1000
    }

@pytest.fixture
def get_merchant_deposits_response_data():
    return {
        "data": {
            "uuid": "217ccaa2-80c9-408f-ab22-597eaa4436fc",
            "merchant_id": "string",
            "amount": "1000.0",
            "fiat_amount": "1000.0",
            "currency": "rub",
            "state": "created",
            "selected_crypto_currency": None,
            "callback_url": "https://webhook.site/f9d55aae-e554-48c5-b56a-f7cd93fcca7d",
            "redirect_url": "https://ya.ru/",
            "created_at": "2024-04-30 15:52:37 +0300",
            "updated_at": "2024-04-30 15:52:37 +0300",
            "form_url": "https://pay.bova.cash/payments/217ccaa2-80c9-408f-ab22-597eaa4436fc",
            "source_transaction_class": "NilClass",
            "source_transaction": None
        },
        "errors": {},
        "message": None,
        "status": "ok",
        "meta": {}
    }

@patch('requests.post')
def test_get_merchant_deposits(mock_post, bova_client, get_merchant_deposits_request_data, get_merchant_deposits_response_data):
    # Mock the requests.post response
    mock_response = MagicMock()
    mock_response.json.return_value = get_merchant_deposits_response_data
    mock_post.return_value = mock_response

    # Call the method
    response = bova_client.get_merchant_deposits(get_merchant_deposits_request_data)

    # Assert that the request was made correctly
    mock_post.assert_called_once_with(
        "https://bovatech.cc/merchant/v1/deposits",
        headers=bova_client._headers(bova_client._generate_signature(get_merchant_deposits_request_data)),
        data=get_merchant_deposits_request_data,
    )

    # Assert the response
    assert response == get_merchant_deposits_response_data

