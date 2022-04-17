from random import choice
import factory
from faker import Faker
from api.models import GEN, Sobreviventes, Inventario, Denuncia

fake = Faker()

class SobreviventesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sobreviventes

    nome = fake.name()
    idade = fake.random_int(min=0,max=100)
    sexo = choice(GEN)[0]
    latitude = fake.pyfloat(min_value=-90,max_value=90)
    longitude = fake.pyfloat(min_value=-180,max_value=180)

class InventarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventario
    dono = factory.SubFactory(SobreviventesFactory)
    agua =  fake.pyfloat(min_value=0, max_value=25)
    alimentacao =  fake.pyfloat(min_value=0, max_value=25)
    medicacao = fake.pyfloat(min_value=0, max_value=25)
    municao =  fake.pyfloat(min_value=0, max_value=25)


    
    

    