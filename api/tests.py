from django.test import TestCase
from api.factories import SobreviventesFactory, InventarioFactory
from api.models import Sobreviventes, Inventario, Denuncia
from api.serializer import SobreviventesSerializer, NegociarEntreSerializer, LatitudeLongitudeSerializer, DenunciaSerializer
from rest_framework.exceptions import ValidationError

class TestarModelos(TestCase):
    
    def test_Sobreviventes(self):
        sobrevivente = SobreviventesFactory()
        self.assertTrue(isinstance(sobrevivente,Sobreviventes))

    def test_Inventario(self):
        inventario = InventarioFactory()
        self.assertTrue(isinstance(inventario, Inventario))
    
    def test_denuncia(self):
        sobrevivente = SobreviventesFactory()
        denuncia = Denuncia.objects.create(doente = sobrevivente, autor = 2)
        self.assertTrue(isinstance(denuncia, Denuncia))

class TestarSerializers(TestCase):
    def setUp(self):
        self.sobrevivente= {
            "nome": "Ana",
            "idade": 21,
            "sexo": "fem",
            "latitude": 56.5,
            "longitude": 25.65,
            "inventario": {
                "agua": 5,
                "municao":2
            }
        }
        self.negociar ={
        "inventario": {
            "dono": 1,
            "agua": 0,
            "alimentacao": 0,
            "medicacao": 0,
            "municao": 4
        },
        "trocante": {
            "dono": 2,
            "agua": 1,
            "alimentacao": 0,
            "medicacao": 0,
            "municao": 0
            }
        }
        self.latlon = {
            "latitude": 15.7,
            "longitude": 39.8
        }
        self.denuncia = {
            "doente": 1,
            "autor": 2
        }       
    
    def test_criar_sobreviventes(self):
        pessoa = SobreviventesSerializer(data = self.sobrevivente)
        self.assertTrue(pessoa.is_valid())

    def test_criar_sobreviventes_salvar(self):
        pessoa = SobreviventesSerializer(data = self.sobrevivente)
        pessoa.is_valid(raise_exception=True)
        obj = pessoa.save()
        self.assertTrue(isinstance(obj, Sobreviventes))
        self.assertTrue(isinstance(obj.inventario, Inventario))

    def test_criar_sobreviventes_invalido(self):
        self.sobrevivente["idade"] = -1
        pessoa = SobreviventesSerializer(data = self.sobrevivente)
        with self.assertRaises(ValidationError):
            pessoa.is_valid(raise_exception=True)

    def test_negociar(self):
        aux = SobreviventesFactory(id = 1)
        InventarioFactory(dono = aux, agua = 1)
        aux2 = SobreviventesFactory(id = 2)
        InventarioFactory(dono = aux2, municao= 4)
        troca = NegociarEntreSerializer(data = self.negociar)
        self.assertTrue(troca.is_valid())
    
    def test_latitude_longitude(self):
        aux = SobreviventesFactory()
        InventarioFactory(dono = aux)
        latlon = LatitudeLongitudeSerializer(data = self.latlon)
        self.assertTrue(latlon.is_valid())

    def test_denuncia(self):
        aux = SobreviventesFactory(id = 1)
        InventarioFactory(dono = aux)
        denuncia = DenunciaSerializer(data = self.denuncia)
        self.assertTrue(denuncia.is_valid())

    def test_denuncia_save(self):
        aux = SobreviventesFactory(id = 1)
        InventarioFactory(dono = aux)
        denuncia = DenunciaSerializer(data = self.denuncia)
        denuncia.is_valid()
        obj = denuncia.save()
        self.assertTrue(isinstance(obj, Denuncia))


class TestarViews(TestCase):
    def setUp(self):
        self.sobrevivente= {
            "nome": "Ana",
            "idade": 21,
            "sexo": "fem",
            "latitude": 56.5,
            "longitude": 25.65,
            "inventario": {
                "agua": 5,
                "municao":2
            }
        }
        self.denuncia= {
        "doente": 3,
        "autor": 1
        }
        self.negociar ={
            "inventario": {
                "dono": 1,
                "agua": 0,
                "alimentacao": 0,
                "medicacao": 0,
                "municao": 4
            },
            "trocante": {
                "dono": 2,
                "agua": 1,
                "alimentacao": 0,
                "medicacao": 0,
                "municao": 0
                }
            }


    def test_sobrevivente_get(self):
        aux = SobreviventesFactory()
        InventarioFactory(dono = aux)
        response = self.client.get('/sobreviventes/')
        self.assertEqual(response.status_code, 200)
    
    def test_sobrevivente_post(self):
        response = self.client.post('/sobreviventes/', data=self.sobrevivente,content_type="application/json")
        self.assertEqual(response.status_code, 201)
        print(response.json())

    def test_sobrevivente_patch(self):
        aux = SobreviventesFactory()
        InventarioFactory(dono = aux)
        response = self.client.patch(f'/sobreviventes/{aux.id}/', data={"latitude": 12, "longitude": 1},content_type="application/json")
        self.assertEqual(response.status_code, 200)
    
    def test_relatorio_1(self):
        response = self.client.get('/relatorios/1/')
        self.assertEqual(response.status_code, 200)

    def test_relatorio_2(self):
        response = self.client.get('/relatorios/2/')
        self.assertEqual(response.status_code, 200)

    def test_relatorio_3(self):
        response = self.client.get('/relatorios/3/')
        self.assertEqual(response.status_code, 200)

    def test_relatorio_4(self):
        response = self.client.get('/relatorios/4/')
        self.assertEqual(response.status_code, 200)

    def test_relatorio_5(self):
        response = self.client.get('/relatorios/5/')
        self.assertEqual(response.status_code, 400)

    def test_denunciar_infectado(self):
        doente = SobreviventesFactory(id = 3)
        autor = SobreviventesFactory(id = 1)
        response = self.client.post('/denunciar/', data =self.denuncia,content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_denunciar_infectado_autor_invalido(self):
        doente = SobreviventesFactory(id = 1)
        response = self.client.post('/denunciar/', data =self.denuncia,content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_denunciar_infectado_doente_invalido(self):
        autor = SobreviventesFactory(id = 2)
        response = self.client.post('/denunciar/', data =self.denuncia,content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_denunciar_infectado_iguais_invalido(self):
        doente = SobreviventesFactory(id = 3)
        self.denuncia["autor"] = 3
        response = self.client.post('/denunciar/', data =self.denuncia,content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_denunciar_infectado_antes_invalido(self):
        doente = SobreviventesFactory(id = 3)
        autor = SobreviventesFactory(id = 1)
        self.client.post('/denunciar/', data =self.denuncia,content_type="application/json")
        response = self.client.post('/denunciar/', data =self.denuncia,content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_negociar(self):
        aux = SobreviventesFactory(id=1)
        InventarioFactory(dono=aux,municao=4)
        aux2 = SobreviventesFactory(id=2)
        InventarioFactory(dono=aux2,agua=1)
        response=self.client.post('/negociar/', data = self.negociar, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_negociar_infectado(self):
        aux = SobreviventesFactory(id=1,infectado=True)
        InventarioFactory(dono=aux,municao=4)
        aux2 = SobreviventesFactory(id=2)
        InventarioFactory(dono=aux2,agua=1)
        response=self.client.post('/negociar/', data = self.negociar, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_negociar_excesso_autor(self):
        aux = SobreviventesFactory(id=1)
        InventarioFactory(dono=aux,municao=4)
        aux2 = SobreviventesFactory(id=2)
        InventarioFactory(dono=aux2,agua=2)
        self.negociar["inventario"]["municao"] = 8
        response=self.client.post('/negociar/', data = self.negociar, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_negociar_excesso_trocador(self):
        aux = SobreviventesFactory(id=1)
        InventarioFactory(dono=aux,municao=8)
        aux2 = SobreviventesFactory(id=2)
        InventarioFactory(dono=aux2,agua=1)
        self.negociar["trocante"]["agua"] = 2
        response=self.client.post('/negociar/', data = self.negociar, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_negociar_pontos_incorretos(self):
        aux = SobreviventesFactory(id=1)
        InventarioFactory(dono=aux,municao=4)
        aux2 = SobreviventesFactory(id=2)
        InventarioFactory(dono=aux2,agua=1)
        self.negociar["inventario"]["municao"] = 3
        response=self.client.post('/negociar/', data = self.negociar, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    
