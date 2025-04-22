from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Cliente, Pedido


def home(request):
    return render(request, 'prime/home.html')


def clientes(request):
    if request.method != 'POST':
        return render(request, 'prime/clientes.html')

    try:
        # Captura os dados do formulário
        data_nascimento = request.POST.get('dataNascimento') or None  # Se o campo estiver vazio, define como None
        data_nascimento = None

        # Criação de um novo cliente
        novo_cliente = Cliente()
        novo_cliente.nome = request.POST.get('nome')
        novo_cliente.cpf = request.POST.get('cpf')
        novo_cliente.rg = request.POST.get('rg')
        novo_cliente.data_nascimento = data_nascimento  # Define a data de nascimento
        novo_cliente.cep = request.POST.get('cep')
        novo_cliente.endereco = request.POST.get('endereco')
        novo_cliente.numero = request.POST.get('numero')
        novo_cliente.complemento = request.POST.get('complemento')
        novo_cliente.cidade = request.POST.get('cidade')
        novo_cliente.estado = request.POST.get('estado')
        novo_cliente.telefone1 = request.POST.get('telefone1')
        novo_cliente.telefone2 = request.POST.get('telefone2')
        novo_cliente.email = request.POST.get('email')
        novo_cliente.historico_pedidos = request.POST.get('historicoPedidos')

        # Salvar no banco de dados
        novo_cliente.save()

        # Redireciona para a lista de clientes
        return redirect('lista_clientes')

    except IntegrityError:
        # Retorna uma mensagem de erro para o template
        return render(request, 'prime/clientes.html', {
            'error': 'Erro ao salvar o cliente. Verifique os dados e tente novamente.'
        })


def pedidos(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')  # Captura o ID do cliente selecionado
        cliente = get_object_or_404(Cliente, id=cliente_id)  # Busca o cliente pelo ID
        descricao = request.POST.get('descricao')  # Captura a descrição
        data_inicio = request.POST.get('dataInicio')  # Captura a data de início
        data_entrega = request.POST.get('dataEntrega')  # Captura a data de entrega
        telefone = request.POST.get('telefone')  # Captura o telefone
        cep_entrega = request.POST.get('cepEntrega')  # Captura o CEP de entrega
        endereco_entrega = request.POST.get('enderecoEntrega')  # Captura o endereço de entrega
        cidade_entrega = request.POST.get('cidadeEntrega')  # Captura a cidade de entrega
        estado_entrega = request.POST.get('estadoEntrega')  # Captura o estado de entrega

        # Cria o pedido vinculado ao cliente
        Pedido.objects.create(
            cliente=cliente,
            descricao=descricao,
            data_pedido=data_inicio,
            valor_total=0.0  # Ajuste conforme necessário
        )
        return redirect('lista_pedidos')  # Redireciona para a lista de pedidos

    # Busca todos os clientes para exibir no formulário
    clientes = Cliente.objects.all()
    return render(request, 'prime/pedidos.html', {'clientes': clientes})


def lista_clientes(request):
    termo = request.GET.get('q', '')  # Captura o termo de busca
    if termo:
        clientes = Cliente.objects.filter(nome__icontains=termo)  # Busca clientes pelo nome
    else:
        clientes = Cliente.objects.all()  # Busca todos os clientes
    return render(request, 'prime/lista_clientes.html', {'clientes': clientes, 'termo': termo})


def lista_pedidos(request):
    termo = request.GET.get('q', '')  # Captura o termo de busca
    pedidos = []  # Substitua por sua lógica para buscar pedidos no banco de dados
    return render(request, 'prime/lista_pedidos.html', {'pedidos': pedidos, 'termo': termo})


def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)  # Busca o cliente pelo ID ou retorna 404
    return render(request, 'prime/detalhes_cliente.html', {'cliente': cliente})


def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)  # Busca o cliente pelo ID ou retorna 404
    cliente.delete()  # Exclui o cliente do banco de dados
    return redirect('lista_clientes')  # Redireciona para a lista de clientes


def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)  # Busca o cliente pelo ID ou retorna 404

    if request.method == 'POST':
        cliente.nome = request.POST.get('nome')
        cliente.cpf = request.POST.get('cpf')
        cliente.email = request.POST.get('email')
        cliente.telefone1 = request.POST.get('telefone1')
        cliente.telefone2 = request.POST.get('telefone2')
        cliente.data_nascimento = request.POST.get('dataNascimento')
        cliente.endereco = request.POST.get('endereco')
        cliente.cidade = request.POST.get('cidade')
        cliente.estado = request.POST.get('estado')
        cliente.save()  # Salva as alterações no banco de dados
        return redirect('lista_clientes')  # Redireciona para a lista de clientes

    return render(request, 'prime/editar_cliente.html', {'cliente': cliente})


def gerar_pdf_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)  # Busca o pedido pelo ID
    template_path = 'prime/pedido_pdf.html'  # Template para o PDF
    context = {'pedido': pedido}  # Dados do pedido para o template

    # Renderiza o template como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pedido_{pedido.id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)
    return response


def excluir_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)  # Busca o pedido pelo ID ou retorna 404
    pedido.delete()  # Exclui o pedido do banco de dados
    return redirect('lista_pedidos')  # Redireciona para a lista de pedidos



