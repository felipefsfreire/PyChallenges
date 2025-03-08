"""
Desafio: Análise de Vendas e Clientes VIP em um E-commerce
Gere um banco de dados simulado de vendas de um e-commerce e realize análises para identificar os clientes VIP.

# Requisitos:
1. Gerar um DataFrame com 3.000 registros de vendas.
2. Criar uma lista de 15 categorias de produtos e gerar automaticamente 100 produtos diferentes com preços variados.
3. Gerar clientes fictícios, incluindo nome, e-mail e cidade.
4. Criar uma coluna de valor total da compra, levando em conta a quantidade comprada e possíveis descontos.
4. Adicionar um identificador único para cada cliente e permitir que cada um possa fazer várias compras.

# Análises Requeridas:
1. Identificar os 10 produtos mais vendidos (por quantidade).
2. Encontrar os 5 clientes que mais gastaram no total.
3. Criar um gráfico de faturamento mensal.
4. Criar um sistema para marcar clientes VIP, onde um cliente é VIP se gastar acima de R$ 5.000 no total.

# Desafios Extras (opcional)
1. Criar um gráfico de barras com as 10 cidades que mais compraram.
2. Salvar os dados em um banco de dados SQLite e permitir consultas SQL.
3. Criar um relatório final mostrando:
  a. Número total de vendas
  b. Faturamento total
  c. Média de valor gasto por cliente
"""

from faker import Faker  # Importa a biblioteca Faker para gerar dados falsos
import pandas as pd  # Importa a biblioteca Pandas para manipulação de dados
import numpy as np  # Importa a biblioteca NumPy para operações numéricas
import uuid  # Importa a biblioteca UUID para gerar identificadores únicos
import random  # Importa a biblioteca Random para geração de números aleatórios
import matplotlib.pyplot as plt  # Importa a biblioteca Matplotlib para criação de gráficos
from datetime import datetime  # Importa a classe datetime para manipulação de datas e horários
import sqlite3  # Importa a biblioteca SQLite para interação com bancos de dados SQLite

fake = Faker('pt_BR')  # Inicializa o Faker para gerar dados em português do Brasil

conn = sqlite3.connect('salesEcommerce.db')  # Conecta ao banco de dados SQLite 'salesEcommerce.db'
cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

numRows = 3000  # Define o número de linhas a serem geradas no DataFrame
numCustomer = 1600  # Define o número de clientes únicos a serem gerados

categoriesList = {"Eletronicos": ["Smartphone X", "Tablet Y", "Fone Bluetooth", "TV 4K", "Smartwatch", "Carregador Turbo", "Caixa de Som Bluetooth"],
                  "Computadores": ["Notebook Ultra", "PC Gamer", "Monitor Curvo", "Teclado Mecânico", "Mouse RGB", "Webcam Full HD", "SSD 1TB"],
                  "Roupas": ["Camiseta Dry Fit", "Jaqueta Jeans", "Tênis Running", "Vestido Casual", "Boné Esportivo", "Mochila Casual", "Óculos de Sol"],
                  "Livros": ["Python para Iniciantes", "Data Science Avançado", "O Poder do Hábito", "1984", "Mindset", "Clean Code", "A Arte da Guerra"],
                  "Beleza": ["Perfume Elegance", "Kit Skincare", "Batom Matte", "Shampoo Orgânico", "Máscara Facial", "Base Líquida", "Protetor Solar"],
                  "Automotivo": ["Pneu Aro 17", "Óleo Sintético", "Câmera de Ré", "Suporte Celular", "Capa para Banco", "Kit Ferramentas", "Lâmpada LED Automotiva"],
                  "Brinquedos": ["Carrinho Controle Remoto", "Boneca Fashion", "Lego Criativo", "Quebra-Cabeça 1000pçs", "Jogo Educativo", "Playset Cozinha", "Bola de Vinil"],
                  "Esportes": ["Bola de Futebol", "Raquete de Tênis", "Corda de Pular", "Mochila Esportiva", "Kit de Halteres", "Bicicleta Speed", "Luvas de Boxe"],
                  "Moveis": ["Sofá Retrátil", "Mesa de Jantar", "Cadeira Gamer", "Guarda-Roupa 6 Portas", "Cama Box Queen", "Estante de Livros", "Mesa de Escritório"],
                  "Eletrodomesticos": ["Geladeira Frost Free", "Micro-ondas Inox", "Máquina de Lavar", "Aspirador de Pó", "Fogão 5 Bocas", "Cafeteira Elétrica", "Liquidificador"],
                  "Ferramentas": ["Furadeira Elétrica", "Chave de Fenda", "Serra Circular", "Martelo Reforçado", "Trena Digital", "Alicate Universal", "Kit Brocas"],
                  "Petshop": ["Ração Premium", "Coleira Ajustável", "Brinquedo Interativo", "Cama para Cachorro", "Areia para Gato", "Shampoo para Pets", "Arranhador para Gatos"],
                  "Perfumaria": ["Desodorante Roll-on", "Hidratante Corporal", "Shampoo Anticaspa", "Sabonete Líquido", "Óleo Capilar", "Condicionador Nutritivo", "Creme para Mãos"],
                  "Papelaria": ["Caderno Universitário", "Caneta Esferográfica", "Marcador Permanente", "Papel Sulfite A4", "Planner Diário", "Grampeador", "Estojo Organizador"],
                  "Games": ["Console NextGen", "Controle Sem Fio", "Teclado Gamer RGB", "Headset Surround", "Cadeira Gamer Pro", "Mousepad XL", "Cartão Presente PSN"]}  # Define um dicionário de categorias e seus respectivos produtos

def generateCustomer(numCustomer):
    """Gera dados de clientes fictícios.

    Args:
        numCustomer (int): Número de clientes a serem gerados.

    Returns:
        tuple: Uma tupla contendo uma lista de nomes de clientes e um dicionário com informações dos clientes.
    """
    customerName = [fake.first_name() for _ in range(numCustomer)]  # Cria uma lista de nomes de clientes usando Faker
    randomIds = [str(customerId) for customerId in random.sample(range(1001, 9999), numCustomer)]  # Gera IDs aleatórios para os clientes
    customerInfo = {'customersIds': {customer: customerId for customer, customerId in zip(customerName, randomIds)},
                    'customersCities': {customer: fake.city() for customer in customerName},
                    'customersEmails': {customer: fake.email() for customer in customerName},
                    'customersBirthsDates': {customer: fake.date_of_birth(minimum_age=18, maximum_age=80) for customer in customerName}
                    }  # Cria um dicionário com informações dos clientes
    return customerName, customerInfo  # Retorna a lista de nomes e o dicionário de informações

def generateSalesData(numRows, customerInfo, categoriesList):
    """Gera dados de vendas fictícias.

    Args:
        numRows (int): Número de linhas de dados a serem geradas.
        customerInfo (dict): Dicionário com informações dos clientes.
        categoriesList (dict): Dicionário com categorias e produtos.

    Returns:
        pandas.DataFrame: Um DataFrame contendo dados de vendas.
    """
    df = pd.DataFrame({'category': np.random.choice(list(categoriesList.keys()), numRows),
                       '%_discount': np.round(np.random.uniform(0, 10, numRows), 1),
                       'unit_price': np.round(np.random.uniform(25, 600, numRows), 2),
                       'sales_quantity': np.random.randint(1, 14, numRows),
                       'sales_date': pd.to_datetime(datetime(2024, 1, 1) + pd.to_timedelta(np.random.randint(0, 365, numRows), unit='D')),
                       'customer': np.random.choice(list(customerInfo['customersIds'].keys()), numRows),
                       })  # Cria um DataFrame com dados aleatórios
    df['sales_code'] = [str(uuid.uuid4())[:8] for _ in range(len(df))]  # Gera códigos de venda únicos
    df["customer_id"] = df["customer"].map(customerInfo['customersIds']).astype(str)  # Adiciona a coluna 'customer_id' mapeando os nomes dos clientes para seus IDs
    df['city'] = df['customer'].map(customerInfo['customersCities'])  # Adiciona a coluna 'city' mapeando os nomes dos clientes para suas cidades
    df['email'] = df['customer'].map(customerInfo['customersEmails'])  # Adiciona a coluna 'email' mapeando os nomes dos clientes para seus emails
    df['customer_birth_date'] = df['customer'].map(customerInfo['customersBirthsDates'])  # Adiciona a coluna 'customer_birth_date' mapeando os nomes dos clientes para suas datas de nascimento
    df["sales_value"] = df["sales_quantity"] * df["unit_price"]  # Calcula o valor total das vendas
    df['product'] = df['category'].apply(lambda cat: np.random.choice(categoriesList[cat]))  # Adiciona a coluna 'product' selecionando um produto aleatório da categoria
    df["total_price"] = np.round(df["sales_value"] * (1 - df["%_discount"] / 100), 2)  # Calcula o preço total após o desconto
    return df  # Retorna o DataFrame gerado

customersNames, customerData = generateCustomer(numCustomer)  # Gera os dados dos clientes
salesEcommerce = generateSalesData(numRows, customerData, categoriesList)  # Gera os dados de vendas

salesEcommerce.head()  # Exibe as primeiras linhas do DataFrame

print('DataFrame criado com sucesso\n')

dtypeDict = {'category': 'TEXT',
             '%_discount': 'REAL',
             'unit_price': 'REAL',
             'sales_code': 'TEXT',
             'sales_quantity': 'INTEGER',
             'sales_date': 'DATE',
             'customer': 'TEXT',
             'customer_id': 'TEXT',
             'city': 'TEXT',
             'email': 'TEXT',
             'customer_birth_date': 'DATE',
             'sales_value': 'REAL',
             'product': 'TEXT',
             'total_price': 'REAL'
             }  # Define um dicionário com os tipos de dados para cada coluna do DataFrame

salesEcommerce.to_sql('sales', conn, if_exists='replace', index=False, dtype=dtypeDict)  # Salva o DataFrame no banco de dados SQLite

query = 'SELECT * FROM sales LIMIT 5'  # Define uma consulta SQL para selecionar as primeiras 5 linhas da tabela 'sales'
df_check = pd.read_sql(query, conn)  # Executa a consulta SQL e carrega os resultados em um DataFrame

print(df_check)  # Exibe o DataFrame com os dados do banco de dados
print('\nBanco de dados atualizado com sucesso')

conn.close()  # Fecha a conexão com o banco de dados

totalQuant = salesEcommerce.groupby('product')['sales_quantity'].sum()  # Agrupa os dados por produto e soma a quantidade vendida
sortBook = totalQuant.sort_values(ascending=False)  # Ordena os produtos por quantidade vendida em ordem decrescente
productRank10 = sortBook[:10]  # Seleciona os 10 produtos mais vendidos
print("\nTOP 10 produtos mais vendidos\n")
print(productRank10)  # Imprime os 10 produtos mais vendidos

totalQuant = salesEcommerce.groupby('customer')['total_price'].sum()  # Agrupa os dados por cliente e soma o valor total das compras
sortBook = totalQuant.sort_values(ascending=False)  # Ordena os clientes por valor total de compra em ordem decrescente
customerRank5 = sortBook[:5]  # Seleciona os 5 clientes com maior valor total de compra
print("\nTOP 5 clientes com maior valor total de compra\n")
print(customerRank5)  # Imprime os 5 clientes com maior valor total de compra

totalQuant = salesEcommerce.groupby('city')['sales_quantity'].sum()  # Agrupa os dados por cidade e soma a quantidade vendida
sortBook = totalQuant.sort_values(ascending=False)  # Ordena as cidades por quantidade vendida em ordem decrescente
cityRank10 = sortBook[:10]  # Seleciona as 10 cidades com maior volume de vendas
print("\nTOP 10 Cidades com maior volume de vendas\n")
print(cityRank10)  # Imprime as 10 cidades com maior volume de vendas

soldQuantity = salesEcommerce['sales_quantity'].agg('sum')  # Calcula a quantidade total de itens vendidos
revenue = salesEcommerce['total_price'].agg('sum')  # Calcula o faturamento total
salesCustomerAvg = np.round((revenue / numCustomer), 2)  # Calcula a média de valor gasto por cliente

print(f"Report \nNúmero total de vendas: {numRows} \nQuantidade de Itens vendidos: {soldQuantity} \nFaturamento Total: {np.round(revenue, 2)} \nMédia de valor gasto por cliente: {salesCustomerAvg}")  # Imprime um relatório com as métricas

dfVips = salesEcommerce  # Cria uma cópia do DataFrame 'salesEcommerce'
dfVips = dfVips.groupby('customer')['total_price'].sum().reset_index()  # Agrupa os dados por cliente e soma o valor total das compras
dfVips['vip'] = dfVips['total_price'].apply(lambda x: 'Sim' if x > 5000 else 'Não')  # Adiciona uma coluna 'vip' indicando se o cliente é VIP (gasto total > 5000)
print("\nClientes VIPs:\n")
print(dfVips)  # Imprime o DataFrame com os clientes VIPs

dfMonthRevenue = salesEcommerce  # Cria uma cópia do DataFrame 'salesEcommerce'
dfMonthRevenue['month_name'] = dfMonthRevenue['sales_date'].dt.strftime('%m/%Y')  # Adiciona uma coluna 'month_name' com o mês e ano da venda
monthRevenue = dfMonthRevenue.groupby('month_name')['total_price'].sum()  # Agrupa os dados por mês e soma o faturamento
print("\nFaturamento mensal:\n")
print(monthRevenue)  # Imprime o faturamento mensal

plt.figure(figsize=(12, 6))  # Define o tamanho da figura do gráfico
bars = plt.bar(cityRank10.index, cityRank10.values, color='skyblue')  # Cria um gráfico de barras com os dados de vendas por cidade
plt.xlabel('City')  # Define o rótulo do eixo x
plt.ylabel('Total Sales Quantity')  # Define o rótulo do eixo y
plt.title('Total Sales Quantity by Top 10 Cities')  # Define o título do gráfico
plt.xticks(rotation=90, ha='right')  # Rotaciona os rótulos do eixo x para melhor legibilidade
plt.tight_layout()  # Ajusta o layout do gráfico para evitar sobreposição

for bar in bars:  # Itera sobre cada barra no gráfico
    yval = bar.get_height()  # Obtém a altura da barra
    plt.text(bar.get_x() + bar.get_width() / 2, yval, str(int(yval)), ha='center', va='bottom')  # Adiciona o valor da barra acima dela

plt.show()  # Exibe o gráfico

plt.figure(figsize=(12, 6))  # Define o tamanho da figura do gráfico
plt.plot(monthRevenue.index, monthRevenue.values, marker='o', linestyle='-', color='b', label="Revenue")  # Cria um gráfico de linha com o faturamento mensal
plt.xlabel('Month')  # Define o rótulo do eixo x
plt.ylabel('Revenue')  # Define o rótulo do eixo y
plt.title('Monthly Revenue')  # Define o título do gráfico
plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo x para melhor legibilidade
plt.grid(True, linestyle='--', alpha=0.4)  # Adiciona um grid ao gráfico
plt.legend()  # Adiciona uma legenda ao gráfico

plt.show()  # Exibe o gráfico