from django.contrib import admin
from .models import Cliente, Pedido, ItemPedido

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone1', 'cidade', 'estado')
    search_fields = ('nome', 'cpf', 'telefone1')
    list_filter = ('cidade', 'estado')


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cliente', 'data_pedido', 'data_entrega',
        'forma_pagamento', 'subtotal', 'acrescimo',
        'desconto', 'valor_total', 'parcelas',
        'valor_parcela', 'pedido_fechado', 'situacao'
    )
    list_filter = ('forma_pagamento', 'situacao', 'pedido_fechado', 'data_pedido')
    search_fields = ('cliente__nome', 'descricao')
    inlines = [ItemPedidoInline]


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'descricao', 'quantidade', 'valor_unitario', 'total')
    search_fields = ('descricao',)
    list_filter = ('pedido',)
