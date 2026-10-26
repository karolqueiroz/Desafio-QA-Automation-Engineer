import random
import string
import time

from faker import Faker

_faker = Faker("pt_BR")
_faker = Faker("en_US")

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

STATES_CITIES = {
    "NCR": ["Delhi", "Gurgaon", "Noida"],
    "Uttar Pradesh": ["Agra", "Lucknow", "Merrut"],
    "Haryana": ["Karnal", "Panipat"],
    "Rajasthan": ["Jaipur", "Jaiselmer"],
}



def build_user() -> dict:
    """Gera credenciais únicas e que atendem a regra de senha da API.

    A senha da DemoQA exige: maiúscula, minúscula, número,
    caractere especial e no mínimo 8 caracteres.
    """
    suffix = f"{int(time.time())}{random.randint(100, 999)}"
    user_name = f"qa_{_faker.user_name()}_{suffix}"
    password = "Teste@" + "".join(random.choices(string.digits, k=6))
    return {"user_name": user_name, "password": password}

def build_student() -> dict:
    """Dados aleatórios para o Practice Form."""
    state = random.choice(list(STATES_CITIES))
    birth = _faker.date_of_birth(minimum_age=18, maximum_age=60)
    return {
        "first_name": _faker.first_name(),
        "last_name": _faker.last_name(),
        "email": f"{_faker.user_name()}{random.randint(100, 999)}@example.com",
        "gender": random.choice(["Male", "Female", "Other"]),
        "mobile": "9" + "".join(random.choices(string.digits, k=9)),
        "birth_date": f"{birth.day:02d} {MONTHS[birth.month - 1]} {birth.year}",
        "subject": random.choice(["Maths", "Physics", "Chemistry", "English", "Biology", "History"]),
        "hobbies": random.sample(["Sports", "Reading", "Music"], k=random.randint(1, 3)),
        "address": _faker.street_address(),
        "state": state,
        "city": random.choice(STATES_CITIES[state]),
    }


def build_record() -> dict:
    """Registro aleatório para a Web Table (e-mail único para localizar a linha)."""
    return {
        "first_name": _faker.first_name(),
        "last_name": _faker.last_name(),
        "email": f"{_faker.user_name()}{random.randint(1000, 9999)}@example.com",
        "age": str(random.randint(18, 65)),
        "salary": str(random.randint(3000, 20000)),
        "department": random.choice(["QA", "Dev", "Product", "Support", "Design"]),
    }
