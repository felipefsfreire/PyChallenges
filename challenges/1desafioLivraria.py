"""
Desafio: Gerar e analisar dados de venda de uma livraria
Crie um DataFrame que simule as vendas de uma livraria fictícia. 

# O conjunto de dados deve conter:
1. Informações sobre os livros vendidos
2. Preços
3. Datas das vendas
4. Clientes

# Requisitos:
1. Gerar um DataFrame com 1.500 registros.
2. Criar listas de livros e autores fictícios.
3. Gerar nomes de clientes aleatórios com a biblioteca Faker.
4. Adicionar quantidade vendida, preço unitário e data da venda.
5. Adicionar a data de nascimento dos clientes (para possíveis análises futuras).
6. Salvar os dados em um arquivo CSV.

# Desafios Extras (opcional):
1. Criar um gráfico de barras mostrando a quantidade de vendas por livro.
2. Filtrar os 10 livros mais vendidos e exibi-los.
3. Adicionar uma coluna com descontos aleatórios e calcular o preço final da compra.
"""

# Gerando os dados
#=================

# Importando as bibliotecas
from faker import Faker
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


# Criando função para gerar dados do DataFrame
def generateData (numRows = 1500, numCustomer = 1270):
    fake = Faker('en_US') # Importa e inicializa a biblioteca Faker, além de selecionar localidade
    # listas de 20 livros e editoras
    bookList = ["Competing on Analytics", "Data Science for Business", "The Data Warehouse Toolkit",
                "Analytics at Work", "Naked Statistics", "Data-Driven", "Winning with Data",
                "Big Data: A Revolution",
                "Data Smart", "The Analytics Edge", "Storytelling with Data", 
                "The Art of Data Science", "Lean Analytics", "Data Strategy",
                "Predictive Analytics", "Data Science for Executives", "Monetizing Data",
                "The Data Detective", "Analytics in a Big Data World", "Data Science for Business Leaders"]

    publisherList = ["Harvard Business Review Press", "O'Reilly Media", "Wiley",
                    "Harvard Business Review Press", "W.W. Norton & Company", "O'Reilly Media", "Wiley",
                    "Eamon Dolan/Houghton Mifflin Harcourt", "Wiley", "MIT Press", "Wiley",
                    "O'Reilly Media", "O'Reilly Media", "Kogan Page",
                    "Wiley", "Columbia Business School Publishing", "Harvard Business Review Press",
                    "Penguin Books", "Wiley", "O'Reilly Media"]

    # lista de 20 autores usando Faker(fullname)
    authorList = [fake.name() for _ in range(len(bookList))]
    #print(authorList)

    # lista de clientes usando Faker(first name)
    customerName = [fake.first_name() for _ in range(numCustomer)]

    # gerando Ids únicos e aleatórios para os livros
    randomIds = random.sample(range(1001, 2000), len(bookList))
    # gerando biblioteca com livros e Ids
    booksIds = {book: bookId for book, bookId in zip(bookList, randomIds)}

    # Gerando DataFrame usando random da biblioteca numpy para gerar as informações de forma aleatória
    df = pd.DataFrame({'book': np.random.choice(bookList,numRows),
                       'publisher': np.random.choice(publisherList,numRows),
                       'author': np.random.choice(authorList,numRows),
                       'unit_price': np.round(np.random.uniform(25, 250,numRows),2),
                       'sales_quantity': np.random.randint(1,14,numRows),
                       'sales_date': np.random.choice(pd.date_range(start = '2024-01-01', end = '2024-12-31')),
                       'customer': np.random.choice(customerName,numRows),
                       'birth_date': np.random.choice(pd.date_range(start = '1950-01-01', end = '2009-12-31'))
                       })
    
    #Adicionando Ids aos livros (criando a coluna de Ids no DataFrame)
    df["book_id"] = df["book"].map(booksIds)

    # Valor da venda (criando a coluna de valor da venda no DataFrame)
    df["sales_value"] = df["sales_quantity"]*df["unit_price"]

    # Desconto (criando a coluna de descontos no DataFrame)
    df["%_discount"] = np.round(np.random.uniform(0, 10,numRows),1)

    # Valor total da venda com desconto
    df["total_price"] = np.round((df["sales_quantity"]*df["unit_price"])*(1-df["%_discount"]/100),2)

    return df

# invocando a função que gera o DataFrame
df = generateData()

# criando arquivo csv
df.to_csv('C:/Users/santo/Documents/dataBases/salesBooks.csv', index = False)
print("\nExemplo dos dados:")
print(df.head()) # .head exibe apenas as linhas iniciais do DataFrame
print("\nArquivo carregado com sucesso😊")


# Realizando as análises
#=======================

# Renomeando o DataFrame para fazer as análises
salesBook = df

# Criando ranking dos 10 livos mais vendidos
#Agrupando livros pela quantidade vendida
totalQuant = salesBook.groupby('book')['sales_quantity'].sum()
#Ordenando pela maior quantidade vendida
sortBook = totalQuant.sort_values(ascending = False)
#realizando um slice dos 10 primeiros livros com maior quantidade
bookRank10 = sortBook[:10]
print("\nTOP 10 Livros mais vendidos\n")
print(bookRank10)


# Visualização dos dados
#========================

# Cria o gráfico de barras
plt.figure(figsize=(12, 6))  # Ajusta o tamanho da figura para melhor visualização
bars = plt.bar(totalQuant.index, totalQuant.values, color='skyblue')  # Cria as barras e armazena os objetos das barras na variável 'bars'
plt.xlabel('Book Title')  # Rótulo do eixo x
plt.ylabel('Total Sales Quantity')  # Rótulo do eixo y
plt.title('Total Sales Quantity by Book')  # Título do gráfico
plt.xticks(rotation=90, ha='right')  # Rotaciona os rótulos do eixo x para melhor legibilidade
plt.tight_layout()  # Ajusta o layout para evitar cortes nos rótulos

for bar in bars: # Itera sobre cada barra no gráfico
    yval = bar.get_height() # Obtém a altura da barra atual
    plt.text(bar.get_x() + bar.get_width()/2, yval, str(int(yval)), ha='center', va='bottom') # Adiciona o rótulo de texto acima da barra
    # bar.get_x() + bar.get_width()/2: Calcula a posição horizontal central da barra
    # yval: Define a posição vertical do rótulo (acima da barra)
    # str(int(yval)): Converte a altura da barra (yval) para um inteiro e, em seguida, para uma string (texto do rótulo)
    # ha='center': Alinhamento horizontal do texto (centralizado)
    # va='bottom': Alinhamento vertical do texto (na parte inferior, para ficar acima da barra)

plt.show()  # Mostra o gráfico


# Análises adicionais
#========================