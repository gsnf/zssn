from django.contrib import admin
from django.urls import path, include
from api.views import SobreviventesView, DenunciarInfectadoView, NegociarView, RelatoriosView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'sobreviventes', SobreviventesView)
router.register(r'negociar', NegociarView,basename='negociar')
router.register(r'denunciar', DenunciarInfectadoView,basename='denunciar')
router.register(r'relatorios', RelatoriosView,basename='relatorios')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
