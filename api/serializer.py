from rest_framework import serializers
from api.models import Sobreviventes, Inventario, Denuncia
from django.db import transaction

class InventarioSerializerExt(serializers.ModelSerializer): #externo
    class Meta:
        model = Inventario
        fields = '__all__'

class InventarioSerializerInt(serializers.ModelSerializer): #interno
    class Meta:
        model = Inventario
        fields =['agua', 'alimentacao', 'medicacao', 'municao']

class NegociarSerializer(serializers.Serializer): #para negociar
    dono = serializers.PrimaryKeyRelatedField(queryset=Sobreviventes.objects.all())
    agua = serializers.IntegerField(min_value=0)
    alimentacao = serializers.IntegerField(min_value=0)
    medicacao = serializers.IntegerField(min_value=0)
    municao = serializers.IntegerField(min_value=0)

class LatitudeLongitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sobreviventes
        fields = ['latitude','longitude']
            
class SobreviventesSerializer(serializers.ModelSerializer):
    inventario = InventarioSerializerInt()
    class Meta:
        model = Sobreviventes
        fields = ['id','nome', 'idade', 'sexo', 'latitude', 'longitude', 'infectado','inventario']
    def create(self, validated_data):
        aux = validated_data.get("inventario")
        with transaction.atomic():
            a = Sobreviventes.objects.create(nome=validated_data['nome'],idade=validated_data['idade'],sexo=validated_data['sexo'], latitude=validated_data['latitude'], longitude=validated_data['longitude'])
            Inventario.objects.create(dono=a, **aux) 
            return a

class DenunciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denuncia
        exclude = ["id"]

class NegociarEntreSerializer(serializers.Serializer):
    inventario = NegociarSerializer()
    trocante = NegociarSerializer()
