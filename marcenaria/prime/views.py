from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db import transaction, IntegrityError
from weasyprint import HTML
from decimal import Decimal
from .models import Cliente, Pedido, ItemPedido, LeituraSensor
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

def home(request):
    ultima_leitura = LeituraSensor.objects.order_by("-criado_em").first()
    return render(request, 'prime/home.html', {'ultima_leitura': ultima_leitura})


def clientes(request):
    if request.method == 'POST':
         # Verifica se o CPF ou RG já existem no banco de dados
        if Cliente.objects.filter(cpf=request.POST.get('cpf')).exists():
            return render(request, 'prime/clientes.html', {'error': 'CPF já cadastrado.'})
        if Cliente.objects.filter(rg=request.POST.get('rg')).exists():
            return render(request, 'prime/clientes.html', {'error': 'RG já cadastrado.'})

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

        cliente_id = request.POST.get('nomeCliente')
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        # Dados do pedido
        descricao = request.POST.get('obsGeral') or ''
        data_pedido = request.POST.get('dataInicio') or None
        data_entrega = request.POST.get('dataEntrega') or None
        forma_pagamento = request.POST.get('formaPagamento') or ''
        parcelas = int(request.POST.get('parcelas') or 1)
        valor_total = float(request.POST.get('valorTotal') or 0)
        valor_parcela = float(request.POST.get('valorParcela') or 0)
        subtotal = float(request.POST.get('subtotal') or 0)
        acrescimo = float(request.POST.get('acrescimo') or 0)
        desconto = float(request.POST.get('desconto') or 0)
        situacao = request.POST.get('situacao') or 'nao_iniciado'
        pedido_fechado = request.POST.get('pedidoFechado') == 'sim'

        pedido = Pedido.objects.create(
            cliente=cliente,
            descricao=descricao,
            data_pedido=data_pedido,
            data_entrega=data_entrega,
            forma_pagamento=forma_pagamento,
            parcelas=parcelas,
            valor_total=valor_total,
            valor_parcela=valor_parcela,
            subtotal=subtotal,
            acrescimo=acrescimo,
            desconto=desconto,
        )

        # Salvar itens do pedido
        for i in range(1, 6):
            descricao_item = request.POST.get(f'descricaoItem{i}')
            quantidade = request.POST.get(f'quantidadeItem{i}')
            valor_unitario = request.POST.get(f'valorUnitarioItem{i}')
            total = request.POST.get(f'totalItem{i}')

            if descricao_item and valor_unitario:
                ItemPedido.objects.create(
                    pedido=pedido,
                    descricao=descricao_item,
                    quantidade=int(quantidade or 0),
                    valor_unitario=float(valor_unitario or 0),
                    total=float(total or 0)
                )

        return redirect('lista_pedidos')

    # GET
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
        pass
    
        # Salva o pedido
        pedido.save()

        # Redireciona para a página de sucesso
        return redirect('lista_pedidos')  # Substitua pelo nome correto da URL

    context = {
        'pedido': pedido,
        'nomeCliente': pedido.cliente.nome,
        
         
           
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

#parte do sensor iot

@csrf_exempt
@require_http_methods(["POST", "GET"])
def leitura_sensor(request):
    # Verifica a API Key apenas no POST
    if request.method == "POST":
        api_key = request.headers.get("X-API-Key")
        if api_key != settings.API_KEY_SENSOR:
            return JsonResponse({"status": "erro", "mensagem": "Não autorizado"}, status=403)

        try:
            dados = json.loads(request.body)
            leitura = LeituraSensor.objects.create(
                temperatura=dados["temperatura"],
                umidade=dados["umidade"]
            )
            return JsonResponse({
                "status": "ok",
                "id": leitura.id,
                "temperatura": leitura.temperatura,
                "umidade": leitura.umidade,
                "criado_em": leitura.criado_em.isoformat()
            }, status=201)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)

    leituras = LeituraSensor.objects.order_by("-criado_em")[:100]
    dados = [{
        "id": l.id,
        "temperatura": l.temperatura,
        "umidade": l.umidade,
        "criado_em": l.criado_em.isoformat()
    } for l in leituras]
    return JsonResponse({"leituras": dados})

