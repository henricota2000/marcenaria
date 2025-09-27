from django.contrib import admin
from django.urls import path
from . import views  # Certifique-se de que esta linha está presente


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Certifique-se de que a função 'home' existe em 'views.py'
    path('clientes/', views.clientes, name='clientes'),
    path('lista_clientes/', views.lista_clientes, name='lista_clientes'),
    path('pedidos/', views.cadastrar_pedido, name='pedidos'),
    path('lista_pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('cliente/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),  # Rota para detalhes do cliente
    path('cliente/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),  # Rota para excluir cliente
    path('cliente/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),  # Rota para editar cliente
    path('editar_pedido/<int:pedido_id>/', views.editar_pedido, name='editar_pedido'),
    path('excluir_pedido/<int:pedido_id>/', views.excluir_pedido, name='excluir_pedido'),
    path('detalhar_pedido_pdf/<int:pedido_id>/', views.detalhar_pedido_pdf, name='detalhar_pedido_pdf'),
]