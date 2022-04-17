from django.shortcuts import render
from rest_framework import viewsets, status
from api.models import Sobreviventes, Denuncia, Inventario
from api.serializer import SobreviventesSerializer, LatitudeLongitudeSerializer, DenunciaSerializer, NegociarEntreSerializer
from rest_framework.response import Response
from django.db import transaction

class RelatoriosView(viewsets.ViewSet):
    def retrieve(self, request, pk = None):
        pk = int(pk)
        if pk == 1:
            aux = Sobreviventes.objects.all()
            saudaveis = aux.filter(infectado = True)
            resultado = (saudaveis.count()/aux.count())*100 if saudaveis.count() > 0 else 0
            retorno = "A porcentagem de sobreviventes infectados é de " +str(round(resultado,2))+ "%."
            return Response({"Relatorio I:":retorno},
                status=status.HTTP_200_OK)
        elif pk == 2:
            aux = Sobreviventes.objects.all()
            saudaveis = aux.filter(infectado = False)
            resultado = (saudaveis.count()/aux.count())*100 if saudaveis.count() > 0 else 0
            retorno = "A porcentagem de sobreviventes saudaveis é de " +str(round(resultado,2))+ "%."
            return Response({"Relatorio II:":retorno},
                status=status.HTTP_200_OK)
        elif pk== 3:
            agua = alimentacao = medicacao = municao = 0
            aux = Inventario.objects.all()
            for i in aux:
                agua += i.agua
                alimentacao = i.alimentacao
                medicacao = i.medicacao
                municao = i.municao
                #value_1 if condition else value_2
            agua = round(agua/aux.count(), 2) if agua > 0 else 0
            alimentacao = round(alimentacao/aux.count(), 2) if alimentacao > 0 else 0
            medicacao = round(medicacao/aux.count(),2) if medicacao > 0 else 0
            municao = round(municao/aux.count(), 2) if municao > 0 else 0
            msg = {"agua":agua, "alimentacao":alimentacao, "medicacao":medicacao, "municao":municao}
            return Response({"Relatorio III (Médias):":msg},
                status=status.HTTP_200_OK)
        elif pk == 4:
            agua = alimentacao = medicacao = municao = 0
            aux = Sobreviventes.objects.filter(infectado = True)
            for i in aux:
                agua += i.inventario.agua
                alimentacao = i.inventario.alimentacao
                medicacao = i.inventario.medicacao
                municao = i.inventario.municao
            pontos = agua*4 + alimentacao*3 + medicacao*2 + municao
            retorno = "A quantidade de pontos perdidos devido a sobreviventes infectados é " +str(pontos)+ "."
            return Response({"Relatorio IV:":retorno},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Esse numero de relatório não existe."},
                status=status.HTTP_400_BAD_REQUEST,
            ) 

class SobreviventesView(viewsets.ModelViewSet):
    queryset = Sobreviventes.objects.all()
    serializer_class = SobreviventesSerializer
    def partial_update(self, request, *args, **kwargs):
        id = kwargs["pk"]
        pessoa = Sobreviventes.objects.get(id = id)
        serial = LatitudeLongitudeSerializer(pessoa, data=request.data)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(serial.data,status=status.HTTP_200_OK)

class DenunciarInfectadoView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serial = DenunciaSerializer(data = request.data)
        serial.is_valid(raise_exception = True)
        pessoa = Sobreviventes.objects.get(id = serial.data['doente'])
        autor = Sobreviventes.objects.filter(id = serial.data['autor'])
        if serial.data['doente'] == serial.data['autor']:
            return Response(
                {"error": "O doente e o autor são a mesma pessoa."},
                status=status.HTTP_400_BAD_REQUEST,
            ) 
        if autor.count() == 0:
            return Response(
                {"error": "Esse autor não existe."},
                status=status.HTTP_400_BAD_REQUEST,
            ) 
        teste = Denuncia.objects.filter(doente = serial.data['doente'], autor = serial.data['autor'])
        if teste.count() != 0:
            return Response(
                {"error": "Esse autor ja denunciou esse infectado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        with transaction.atomic():
            pessoa.strike += 1
            if pessoa.strike == 3:
                pessoa.infectado = True
            pessoa.save()
            serial = DenunciaSerializer(data = serial.data)
            serial.is_valid(raise_exception = True)
            serial.save()
            return Response({"sucesso": "Infectado denunciado."},status=status.HTTP_200_OK)

class NegociarView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serial = NegociarEntreSerializer(data = request.data)
        serial.is_valid(raise_exception = True)
        dono = serial.data["inventario"] #itens a serem trocados
        trocador = serial.data["trocante"] #itens a serem trocados
        donoAux = Sobreviventes.objects.get(id = dono['dono']) #recupera a pessoa para checars se esta infectada
        trocadorAux = Sobreviventes.objects.get(id = trocador['dono']) #recupera a pessoa para checar se esta infectada

        if donoAux.infectado or trocadorAux.infectado:
            return Response(
                {"error": "Pessoas infectadas não podem negociar."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (dono['agua']-trocador['agua'] > donoAux.inventario.agua 
            or dono['alimentacao']-trocador['alimentacao'] > donoAux.inventario.alimentacao
            or dono['medicacao']-trocador['medicacao'] > donoAux.inventario.medicacao
            or dono['municao']-trocador['municao'] > donoAux.inventario.municao):
            return Response(
                {"error": "Quantidade de itens a serem trocados não podem ser maior do que os disponiveis no inventario."},
                status=status.HTTP_400_BAD_REQUEST,
            ) #verifica se o dono quer trocar mais itens do que ele pode

        if (trocador['agua']-dono['agua'] > trocadorAux.inventario.agua 
            or trocador['alimentacao']-dono['alimentacao'] > trocadorAux.inventario.alimentacao
            or trocador['medicacao']-dono['medicacao'] > trocadorAux.inventario.medicacao
            or trocador['municao']-dono['municao'] > trocadorAux.inventario.municao):
            return Response(
                {"error": "Quantidade de itens a serem trocados não podem ser maior do que os disponiveis"},
                status=status.HTTP_400_BAD_REQUEST,
            ) #verifica se o trocador que trocar mais itens do que ele pode

        pontosDono = dono['agua']*4 + dono['alimentacao']*3 + dono['medicacao']*2 + dono['municao']
        pontosTrocador = trocador['agua']*4 + trocador['alimentacao']*3 + trocador['medicacao']*2 + trocador['municao'] #calcula a troca
        if pontosDono != pontosTrocador: #verifica se a troca é exata
            return Response(
                {"error": "Os pontos não foram o suficiente para efetuar a troca."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        #realiza as trocas no bd
        donoAux.inventario.agua = donoAux.inventario.agua - dono['agua'] + trocador['agua']
        donoAux.inventario.alimentacao = donoAux.inventario.alimentacao - dono['alimentacao'] + trocador['alimentacao']
        donoAux.inventario.medicacao = donoAux.inventario.medicacao - dono['medicacao'] + trocador['medicacao']
        donoAux.inventario.municao = donoAux.inventario.municao - dono['municao'] + trocador['municao'] 
        trocadorAux.inventario.agua = trocadorAux.inventario.agua - trocador['agua'] + dono['agua']
        trocadorAux.inventario.alimentacao = trocadorAux.inventario.alimentacao - trocador['alimentacao'] + dono['alimentacao']
        trocadorAux.inventario.medicacao = trocadorAux.inventario.medicacao - trocador['medicacao'] + dono['medicacao']
        trocadorAux.inventario.municao = trocadorAux.inventario.municao - trocador['municao'] + dono['municao']
        with transaction.atomic():
            donoAux.inventario.save()
            trocadorAux.inventario.save()
            return Response({"sucesso:":"troca efetuada com sucesso."},
                status=status.HTTP_200_OK)

