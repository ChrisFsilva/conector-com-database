Colunas:
	Cliente,Email,OrcamentoSolicitado,Telefone,AutorizacaoDeContato,Loja,VendedorAssociado,Status,DataSolicita,Feedback

Regras
1° Sempre seguir a sequencia das colunas, caso deseje enviar a informação em branco ou vazia apenas adicionar a , respeitando a quantidade de 8 virgulas totais

2° Campos Clientes e Telefone e Loja são campo obrigatórios de informação

3° Campos Email, OrcamentoSolicitado e AutorizacaoDeContato poderão ser enviados em branco, porem serão salvos com a informação 'Whatsapp' no banco de dados

4° Campo status, caso seja enviado em branco será tratado como 'Enviado ao gerente'

5° Campo DataSolicita, caso seja enviado em branco será tratada com a data do envio do arquivo

6° Campo vendedorAssociado, Caso enviado em branco não armazenará informações

Significado de cada campo

Cliente = Nome do cliente
Email = Email de contato com o cliente
OrcamentoSOlicitado = Produto qual o cliente deseja orçar
Telefone = Telefone de contato do cliente
AutorizacaoDeContato = Forma que o cliente aceita receber contato do consultor
Loja = Loja para qual o orçamento seja solicitado
VendedorAssociado = Vendedor que irá atender o cliente
Status = Posição da tratativa
	Opções:
		Enviado ao gerente
		Enviado ao vendedor
		Venda Realizada
		Cliente queria apenas informações
		Comprou na concorrente
		Solicitando feedback
DataSolicita = Data do contato da solicitação do cliente, deverá esta no padrão americano de ano (6 digitos), mês (2 Digitos), dia (2 digitos) ex: 2026-05-24
Feedback = Qualquer texto ou informação que o vendedor queirá colocar como observação
		

 