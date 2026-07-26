import json
import copy

valid_payload = {
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-07-17",
        "checkout": "2026-07-31"
    },
    "additionalneeds": "Breakfast"
}

test_cases = []

def add_case(test_name, payload, expected_status=400):
    """Вспомогательная функция для добавления тест-кейса"""
    test_cases.append({
        "testName": test_name,
        "payload": payload,
        "expectedStatus": expected_status
    })

add_case("Пустой JSON-объект", {})

for key in valid_payload.keys():
    payload = copy.deepcopy(valid_payload)
    del payload[key]
    add_case(f"Отсутствует обязательное поле: {key}", payload)
    
for key in ["firstname", "lastname", "additionalneeds"]:
    payload = copy.deepcopy(valid_payload)
    payload[key] = ""
    add_case(f"Пустая строка в поле: {key}", payload)

p = copy.deepcopy(valid_payload); p["totalprice"] = "сто рублей"
add_case("Неверный тип: totalprice является строкой", p)

p = copy.deepcopy(valid_payload); p["firstname"] = 12345
add_case("Неверный тип: firstname является числом", p)

p = copy.deepcopy(valid_payload); p["depositpaid"] = "yes"
add_case("Неверный тип: depositpaid является строкой", p)

p = copy.deepcopy(valid_payload); p["totalprice"] = -500
add_case("Негативная цена: totalprice < 0", p)

p = copy.deepcopy(valid_payload)
p["bookingdates"] = {"checkin": "2026-07-31", "checkout": "2026-07-17"}
add_case("Логика дат: checkin позже чем checkout", p)

p = copy.deepcopy(valid_payload)
p["bookingdates"] = {"checkin": "17.07.2026", "checkout": "31.07.2026"}
add_case("Невалидный формат даты (DD.MM.YYYY)", p)

for key in ["firstname", "totalprice", "bookingdates"]:
    p = copy.deepcopy(valid_payload); p[key] = None
    add_case(f"Поле {key} равно null", p)

with open("negative_postman_data.json", "w", encoding="utf-8") as f:
    json.dump(test_cases, f, ensure_ascii=False, indent=2)

print(f" Успешно сгенерировано {len(test_cases)} негативных кейсов в 'negative_postman_data.json'!")
