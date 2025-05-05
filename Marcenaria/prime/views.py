from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db import transaction, IntegrityError
from weasyprint import HTML
from decimal import Decimal
from .models import Cliente, Pedido, ItemPedido


def home(request):
    return render(request, 'prime/home.html')


def clientes(request):
    if request.method == 'POST':
        try:
            # Cria um novo cliente com os dados do formulário
            novo_cliente = Cliente(
                nome=request.POST.get('nome'),
                cpf=request.POST.get('cpf'),
                rg=request.POST.get('rg'),
                data_nascimento=request.POST.get('dataNascimento'),
                cep=request.POST.get('cep'),
                endereco=request.POST.get('endereco'),
                numero=request.POST.get('numero'),
                complemento=request.POST.get('complemento'),
                cidade=request.POST.get('cidade'),
                estado=request.POST.get('estado'),
                telefone1=request.POST.get('telefone1'),
                telefone2=request.POST.get('telefone2'),
                email=request.POST.get('email'),
                historico_pedidos=request.POST.get('historicoPedidos'),
            )
            novo_cliente.save()
            return redirect('lista_clientes')  # Redireciona para a lista de clientes após salvar
        except Exception as e:
            return render(request, 'prime/clientes.html', {'error': str(e)})

    return render(request, 'prime/clientes.html')


def cadastrar_pedido(request):
    if request.method == 'POST':
        print(request.POST)  # Verificar os dados enviados pelo formulário
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        descricao = request.POST.get('descricao') or "Sem descrição"  # Valor padrão caso esteja vazio
        data_pedido = request.POST.get('dataInicio')
        forma_pagamento = request.POST.get('formaPagamento')
        parcelas = int(request.POST.get('parcelas', 1))
        valor_total = float(request.POST.get('valorTotal', 0))

        # Salva o pedido no banco de dados
        Pedido.objects.create(
            cliente=cliente,
            descricao=descricao,
            data_pedido=data_pedido,
            forma_pagamento=forma_pagamento,
            valor_total=valor_total,
            parcelas=parcelas
        )

        return redirect('lista_pedidos')  # Redireciona para a lista de pedidos

    clientes = Cliente.objects.all()
    return render(request, 'prime/pedidos.html', {'clientes': clientes})


def lista_clientes(request):
    termo = request.GET.get('q', '')
    if termo:
        clientes = Cliente.objects.filter(nome__icontains=termo)
    else:
        clientes = Cliente.objects.all()
    return render(request, 'prime/lista_clientes.html', {'clientes': clientes, 'termo': termo})


def lista_pedidos(request):
    pedidos = Pedido.objects.all()  # Busca todos os pedidos no banco de dados
    return render(request, 'prime/lista_pedidos.html', {'pedidos': pedidos})


def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, 'prime/detalhes_cliente.html', {'cliente': cliente})


def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('lista_clientes')


def editar_cliente(request, cliente_id):  # Certifique-se de que o nome do argumento corresponde ao definido no urls.py
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        cliente.nome = request.POST.get('nome')
        cliente.cpf = request.POST.get('cpf')
        cliente.email = request.POST.get('email')
        cliente.telefone1 = request.POST.get('telefone1')
        cliente.telefone2 = request.POST.get('telefone2')
        cliente.data_nascimento = request.POST.get('dataNascimento') or None
        cliente.endereco = request.POST.get('endereco')
        cliente.cidade = request.POST.get('cidade')
        cliente.estado = request.POST.get('estado')

        cliente.save()
        return redirect('lista_clientes')

    return render(request, 'prime/editar_cliente.html', {'cliente': cliente})


def gerar_pdf_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)

    # Renderiza o template HTML com os dados do pedido
    html_string = render_to_string('prime/pedido_pdf.html', {'pedido': pedido})

    # Gera o PDF usando WeasyPrint
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Retorna o PDF como resposta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="pedido_{pedido.id}.pdf"'
    return response


def imprimir_pedido(request, id):
    # Obtém o pedido pelo ID
    pedido = get_object_or_404(Pedido, id=id)

    # Renderiza o template HTML com os dados do pedido
    html_string = render_to_string('prime/pedido_pdf.html', {'pedido': pedido})

    # Gera o PDF usando WeasyPrint
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Retorna o PDF como resposta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="pedido_{pedido.id}.pdf"'
    return response


def excluir_pedido(request, pedido_id):
    # Busca o pedido pelo ID ou retorna 404 se não encontrado
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        # Exclui o pedido
        pedido.delete()
        # Redireciona para a lista de pedidos após a exclusão
        return redirect('lista_pedidos')

    # Caso o método não seja POST, redirecione para a lista de pedidos
    return redirect('lista_pedidos')


def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        # Atualiza os campos do pedido
        pedido.nome_cliente = request.POST.get('nomeCliente')
        pedido.data_inicio = request.POST.get('dataInicio')
        pedido.data_entrega = request.POST.get('dataEntrega')
        pedido.telefone = request.POST.get('telefone')
        pedido.cep_entrega = request.POST.get('cepEntrega')
        pedido.endereco_entrega = request.POST.get('enderecoEntrega')
        pedido.numero_entrega = request.POST.get('numeroEntrega')
        pedido.complemento_entrega = request.POST.get('complementoEntrega')
        pedido.cidade_entrega = request.POST.get('cidadeEntrega')
        pedido.estado_entrega = request.POST.get('estadoEntrega')
        pedido.subtotal = request.POST.get('subtotal') or 0
        pedido.acrescimo = request.POST.get('acrescimo') or 0
        pedido.desconto = request.POST.get('desconto') or 0
        pedido.valor_total = request.POST.get('valorTotal') or 0
        pedido.valor_parcela = request.POST.get('valorParcela') or 0
        pedido.obs_geral = request.POST.get('obsGeral')
        pedido.pedido_fechado = request.POST.get('pedidoFechado')
        pedido.situacao = request.POST.get('situacao')
        pedido.forma_pagamento = request.POST.get('formaPagamento')
        pedido.parcelas = request.POST.get('parcelas') or 1

        # Salva o pedido
        pedido.save()

        # Redireciona para a página de sucesso
        return redirect('lista_pedidos')  # Substitua pelo nome correto da URL

    context = {
        'pedido': pedido,
    }
    return render(request, 'prime/editar_pedido.html', context)


def detalhar_pedido_pdf(request, pedido_id):
    # Busca o pedido pelo ID ou retorna 404 se não encontrado
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Passa o pedido para o template
    context = {
        'pedido': pedido,
    }
    return render(request, 'prime/detalhar_pedido_pdf.html', context)



