from django.db import models
from api.validators import valida_latitude,  valida_longitude, maior_que_zero

GEN = (('fem','fem'),('masc','masc')) #generos

class Sobreviventes(models.Model):
    nome = models.CharField(max_length=50)
    idade = models.IntegerField(default=0, validators=[maior_que_zero])
    sexo = models.CharField(max_length=4, choices=GEN) #fem e masc
    latitude = models.FloatField(validators=[valida_latitude]) #(validators=[MaxValueValidator(90),MinValueValidator(-90)])
    longitude = models.FloatField(validators=[valida_longitude])
    strike = models.IntegerField(default=0) #quando reportado como infectado 3 vezes, infectado = True
    infectado = models.BooleanField(default=False)

class Inventario(models.Model):
    dono = models.OneToOneField(Sobreviventes,on_delete=models.CASCADE,related_name="inventario")
    agua = models.FloatField(default=0, validators=[maior_que_zero])
    alimentacao = models.FloatField(default=0, validators=[maior_que_zero])
    medicacao = models.FloatField(default=0, validators=[maior_que_zero])
    municao = models.FloatField(default=0, validators=[maior_que_zero])

class Denuncia(models.Model):
    doente = models.ForeignKey(Sobreviventes,on_delete=models.CASCADE,related_name="denuncias")
    autor = models.IntegerField(validators=[maior_que_zero])