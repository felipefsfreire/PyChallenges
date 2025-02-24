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

# Gerando os dados
#=================

# Importando as bibliotecas
from faker import Faker
import pandas as pd
import numpy as np
import uuid
import random
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3

fake = Faker('pt_BR') # Inicializa o Faker com dados fictícios em português do Brasil

# Conectando com SQLite
conn = sqlite3.connect('salesEcommerce.db') 
cursor = conn.cursor()

# Quantidade de registros e clientes
numRows = 3000
numCustomer = 1600

# Biblioteca de categorias e produtos
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
                "Games": ["Console NextGen", "Controle Sem Fio", "Teclado Gamer RGB", "Headset Surround", "Cadeira Gamer Pro", "Mousepad XL", "Cartão Presente PSN"]}

#Criando função para gerar dados dos clientes
def generateCustomer(numCustomer):
    customerName = [fake.first_name() for _ in range(numCustomer)]
    randomIds = [str(customerId) for customerId in random.sample(range(1001, 9999), numCustomer)]
    customerInfo = {'customersIds':{customer: customerId for customer, customerId in zip(customerName, randomIds)},
                    'customersCities':{customer: fake.city() for customer in customerName},
                    'customersEmails':{customer: fake.email() for customer in customerName},
                    'customersBirthsDates':{customer: fake.date_of_birth(minimum_age = 18, maximum_age = 80) for customer in customerName}
    }
    return customerName, customerInfo

#Criando função para gerar dados do DataFrame
def generateSalesData (numRows, customerInfo, categoriesList):
    df = pd.DataFrame({'category': np.random.choice(list(categoriesList.keys()),numRows),
                   '%_discount': np.round(np.random.uniform(0, 10,numRows),1),
                   'unit_price': np.round(np.random.uniform(25, 600,numRows),2),
                   #'sales_code':np.random.randint(100001, 999999, numRows).astype(str),
                   'sales_quantity': np.random.randint(1,14,numRows),
                   'sales_date':  pd.to_datetime(datetime(2024, 1, 1) + pd.to_timedelta(np.random.randint(0, 365, numRows), unit='D')),
                   'customer': np.random.choice(list(customerInfo['customersIds'].keys()),numRows),
                   })
    # Gera um código único de venda para cada registro, utilizando os primeiros 8 caracteres de um UUID aleatório.
    # Isso garante que cada venda tenha um identificador único, reduzindo a chance de duplicação.
    df['sales_code'] = [str(uuid.uuid4())[:8] for _ in range(len(df))]
    df["customer_id"] = df["customer"].map(customerInfo['customersIds']).astype(str)
    df['city'] = df['customer'].map(customerInfo['customersCities'])
    df['email'] = df['customer'].map(customerInfo['customersEmails'])
    df['customer_birth_date'] = df['customer'].map(customerInfo['customersBirthsDates'])
    df["sales_value"] = df["sales_quantity"]*df["unit_price"]
    df['product'] = df['category'].apply(lambda cat: np.random.choice(categoriesList[cat])) # Escolhe um produto aleatório dentro da categoria correspondente
    df["total_price"] = np.round(df["sales_value"]*(1-df["%_discount"]/100),2)
    return df

customersNames, customerData = generateCustomer(numCustomer)
salesEcommerce = generateSalesData(numRows, customerData, categoriesList)

salesEcommerce.head()

print('DataFrame criado com sucesso\n')

# Definindo tipos de dados para gerar tabela no banco SQLite
dtypeDict = {'category':'TEXT',
             '%_discount':'REAL',
             'unit_price':'REAL',
             'sales_code':'TEXT',
             'sales_quantity':'INTEGER',
             'sales_date':'DATE',
             'customer':'TEXT',
             'customer_id':'TEXT',
             'city':'TEXT',
             'email':'TEXT',
             'customer_birth_date':'DATE',
             'sales_value':'REAL',
             'product':'TEXT',
             'total_price':'REAL'
             }

# Envia os dados do DataFrame para o SQLite
salesEcommerce.to_sql('sales', conn, if_exists = 'replace', index = False, dtype = dtypeDict)

# Consulta para confirmar inserção dos dados
query = 'SELECT * FROM sales LIMIT 5'
df_check = pd.read_sql(query, conn)

print(df_check)
print('\nBanco de dados atualizado com sucesso')

# Fecha conexão com SQLite
conn.close()


# Realizando as análises
#=======================

# Criando ranking dos 10 livos mais vendidos
#Agrupando produtos pela quantidade vendida
totalQuant = salesEcommerce.groupby('product')['sales_quantity'].sum()
#Ordenando pela maior quantidade vendida
sortBook = totalQuant.sort_values(ascending = False)
#realizando um slice dos 10 primeiros produtos com maior quantidade
productRank10 = sortBook[:10]
print("\nTOP 10 produtos mais vendidos\n")
print(productRank10)


# Criando ranking dos 5 clientes
#Agrupando clientes pelo total de compras
totalQuant = salesEcommerce.groupby('customer')['total_price'].sum()
#Ordenando pelo maior valor
sortBook = totalQuant.sort_values(ascending = False)
#realizando um slice dos 5 primeiros clientes com maior valor gasto
customerRank5 = sortBook[:5]
print("\nTOP 5 clientes com maior valor total de compra\n")
print(customerRank5)


# Criando ranking das 10 cidades
#Agrupando cidades pela quantidade vendida
totalQuant = salesEcommerce.groupby('city')['sales_quantity'].sum()
#Ordenando pela maior quantidade vendida
sortBook = totalQuant.sort_values(ascending = False)
#realizando um slice das 10 primeiras cidades com maior quantidade
cityRank10 = sortBook[:10]
print("\nTOP 10 Cidades com maior volume de vendas\n")
print(cityRank10)


# Criando Report
# Soma da quantidade e valor total
soldQuantity = salesEcommerce['sales_quantity'].agg('sum')
revenue = salesEcommerce['total_price'].agg('sum')
# Cálculo da média de valor gasto por cliente
salesCustomerAvg = np.round((revenue/numCustomer),2)

print(f"Report \nNúmero total de vendas: {numRows} \nQuantidade de Itens vendidos: {soldQuantity} \nFaturamento Total: {np.round(revenue,2)} \nMédia de valor gasto por cliente: {salesCustomerAvg}")

# Clientes VIP's
dfVips = salesEcommerce
dfVips = dfVips.groupby('customer')['total_price'].sum().reset_index()
# Marca clientes como VIP se gastaram mais de 5000
dfVips['vip'] = dfVips['total_price'].apply(lambda x: 'Sim' if x > 5000 else 'Não')
dfVips

#Faturamento mensal
dfMonthRevenue = salesEcommerce
dfMonthRevenue['month_name'] = dfMonthRevenue['sales_date'].dt.strftime('%m/%Y')
monthRevenue = dfMonthRevenue.groupby('month_name')['total_price'].sum()
print(monthRevenue)


# Visualização dos dados
#========================

# Cria o gráfico 10 cidades
plt.figure(figsize=(12, 6))  # Ajusta o tamanho da figura para melhor visualização
bars = plt.bar(cityRank10.index, cityRank10.values, color='skyblue')  # Cria as barras e armazena os objetos das barras na variável 'bars'
plt.xlabel('City')  # Rótulo do eixo x
plt.ylabel('Total Sales Quantity')  # Rótulo do eixo y
plt.title('Total Sales Quantity by Top 10 Cities')  # Título do gráfico
plt.xticks(rotation=90, ha='right')  # Rotaciona os rótulos do eixo x para melhor legibilidade
plt.tight_layout()  # Ajusta o layout para evitar cortes nos rótulos

for bar in bars: # Adiciona rótulos com os valores acima das barras
    yval = bar.get_height() # Obtém a altura da barra atual
    plt.text(bar.get_x() + bar.get_width()/2, yval, str(int(yval)), ha='center', va='bottom') # Adiciona o rótulo de texto acima da barra
    # bar.get_x() + bar.get_width()/2: Calcula a posição horizontal central da barra
    # yval: Define a posição vertical do rótulo (acima da barra)
    # str(int(yval)): Converte a altura da barra (yval) para um inteiro e, em seguida, para uma string (texto do rótulo)
    # ha='center': Alinhamento horizontal do texto (centralizado)
    # va='bottom': Alinhamento vertical do texto (na parte inferior, para ficar acima da barra)

plt.show()  # Mostra o gráfico

# Cria o gráfico faturamento mensal
plt.figure(figsize=(12, 6))  # Ajusta o tamanho da figura para melhor visualização

# Plota o faturamento mensal no eixo Y, usando marcadores para destacar os pontos
plt.plot(monthRevenue.index, monthRevenue.values, marker='o', linestyle='-', color='b', label="Revenue")

# Configurações do gráfico para melhor apresentação
plt.xlabel('Month')  # Rótulo do eixo x
plt.ylabel('Revenue')  # Rótulo do eixo y
plt.title('Monthly Revenue')  # Título do gráfico
plt.xticks(rotation=45)  # Rotaciona os meses para melhor leitura
plt.grid(True, linestyle='--', alpha=0.4)  # Adiciona uma grade para facilitar a visualização
plt.legend()  # Adiciona legenda

plt.show()  # Mostra o gráfico


# Análises adicionais
#========================