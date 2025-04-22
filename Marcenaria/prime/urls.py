from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clientes/', views.clientes, name='clientes'),
    path('lista_clientes/', views.lista_clientes, name='lista_clientes'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('lista_pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('cliente/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),  # Nova rota para detalhes do cliente
    path('cliente/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),  # Nova rota para excluir cliente
    path('cliente/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),  # Nova rota para editar cliente
    path('pedido/pdf/<int:id>/', views.gerar_pdf_pedido, name='gerar_pdf_pedido'),  # Rota para gerar PDF
    path('pedido/excluir/<int:id>/', views.excluir_pedido, name='excluir_pedido'),  # Rota para excluir pedido
]
