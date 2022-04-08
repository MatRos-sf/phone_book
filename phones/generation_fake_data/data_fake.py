from random import choice, randint, choices

from faker import Faker

def data_email():

    faker = Faker('pl_PL')
    data = {
        'mail': faker.email()
    }
    return data

def data_phone():

    fake = Faker('pl_PL')
    data={
        'phone': fake.phone_number()
    }
    return data


def data_person():

    fake = Faker('pl_PL')
    name_surname = fake.name().split()
    data = {
        'name': name_surname[0],
        'surname': name_surname[1]
    }
    return data

def create_or_no():
    return choice([True, False])

def hom_many():
    population = [1,2,3,4,5]
    weights = [0.6, 0.2, 0.1, 0.06, 0.04]

    return choices(population,weights)[0]