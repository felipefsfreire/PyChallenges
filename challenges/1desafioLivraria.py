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

from faker import Faker  # Importa a biblioteca Faker para gerar dados falsos
import pandas as pd  # Importa a biblioteca Pandas para manipulação de dados
import numpy as np  # Importa a biblioteca NumPy para operações numéricas
import random  # Importa a biblioteca Random para geração de números aleatórios
import matplotlib.pyplot as plt  # Importa a biblioteca Matplotlib para criação de gráficos

def generateData (numRows = 1500, numCustomer = 1270):
    """Gera um DataFrame com dados de vendas de livros.

    Args:
        numRows (int, optional): Número de linhas a serem geradas no DataFrame. Padrão é 1500.
        numCustomer (int, optional): Número de clientes únicos a serem gerados. Padrão é 1270.

    Returns:
        pandas.DataFrame: Um DataFrame contendo dados de vendas de livros.
    """
    fake = Faker('en_US')  # Inicializa o Faker para gerar dados em inglês (EUA)
    bookList = ["Competing on Analytics", "Data Science for Business", "The Data Warehouse Toolkit",
                "Analytics at Work", "Naked Statistics", "Data-Driven", "Winning with Data",
                "Big Data: A Revolution",
                "Data Smart", "The Analytics Edge", "Storytelling with Data", 
                "The Art of Data Science", "Lean Analytics", "Data Strategy",
                "Predictive Analytics", "Data Science for Executives", "Monetizing Data",
                "The Data Detective", "Analytics in a Big Data World", "Data Science for Business Leaders"]  # Lista de títulos de livros

    publisherList = ["Harvard Business Review Press", "O'Reilly Media", "Wiley",
                    "Harvard Business Review Press", "W.W. Norton & Company", "O'Reilly Media", "Wiley",
                    "Eamon Dolan/Houghton Mifflin Harcourt", "Wiley", "MIT Press", "Wiley",
                    "O'Reilly Media", "O'Reilly Media", "Kogan Page",
                    "Wiley", "Columbia Business School Publishing", "Harvard Business Review Press",
                    "Penguin Books", "Wiley", "O'Reilly Media"]  # Lista de editoras

    authorList = [fake.name() for _ in range(len(bookList))]  # Cria uma lista de nomes de autores usando Faker
    customerName = [fake.first_name() for _ in range(numCustomer)]  # Cria uma lista de nomes de clientes usando Faker

    randomIds = random.sample(range(1001, 2000), len(bookList))  # Gera IDs aleatórios para os livros
    booksIds = {book: bookId for book, bookId in zip(bookList, randomIds)}  # Cria um dicionário associando títulos de livros a IDs

    df = pd.DataFrame({'book': np.random.choice(bookList,numRows),
                        'publisher': np.random.choice(publisherList,numRows),
                        'author': np.random.choice(authorList,numRows),
                        'unit_price': np.round(np.random.uniform(25, 250,numRows),2),
                        'sales_quantity': np.random.randint(1,14,numRows),
                        'sales_date': np.random.choice(pd.date_range(start = '2024-01-01', end = '2024-12-31')),
                        'customer': np.random.choice(customerName,numRows),
                        'birth_date': np.random.choice(pd.date_range(start = '1950-01-01', end = '2009-12-31'))
                        })  # Cria o DataFrame com dados aleatórios

    df["book_id"] = df["book"].map(booksIds)  # Adiciona a coluna 'book_id' mapeando os títulos dos livros para seus IDs
    df["sales_value"] = df["sales_quantity"]*df["unit_price"]  # Calcula o valor total das vendas
    df["%_discount"] = np.round(np.random.uniform(0, 10,numRows),1)  # Gera descontos aleatórios
    df["total_price"] = np.round((df["sales_quantity"]*df["unit_price"])*(1-df["%_discount"]/100),2)  # Calcula o preço total após o desconto

    return df  # Retorna o DataFrame gerado

df = generateData()  # Gera os dados chamando a função generateData()
df.to_csv('C:/Users/santo/Documents/dataBases/salesBooks.csv', index = False)  # Salva o DataFrame em um arquivo CSV
print("\nExemplo dos dados:")
print(df.head())  # Imprime as primeiras linhas do DataFrame
print("\nArquivo carregado com sucesso")

salesBook = df  # Atribui o DataFrame 'df' à variável 'salesBook'
totalQuant = salesBook.groupby('book')['sales_quantity'].sum()  # Agrupa os dados por livro e soma a quantidade vendida
sortBook = totalQuant.sort_values(ascending = False)  # Ordena os livros por quantidade vendida em ordem decrescente
bookRank10 = sortBook[:10]  # Seleciona os 10 livros mais vendidos
print("\nTOP 10 Livros mais vendidos\n")
print(bookRank10)  # Imprime os 10 livros mais vendidos

plt.figure(figsize=(12, 6))  # Define o tamanho da figura do gráfico
bars = plt.bar(totalQuant.index, totalQuant.values, color='skyblue')  # Cria um gráfico de barras com os dados de vendas
plt.xlabel('Book Title')  # Define o rótulo do eixo x
plt.ylabel('Total Sales Quantity')  # Define o rótulo do eixo y
plt.title('Total Sales Quantity by Book')  # Define o título do gráfico
plt.xticks(rotation=90, ha='right')  # Rotaciona os rótulos do eixo x para melhor legibilidade
plt.tight_layout()  # Ajusta o layout do gráfico para evitar sobreposição

for bar in bars:  # Itera sobre cada barra no gráfico
    yval = bar.get_height()  # Obtém a altura da barra
    plt.text(bar.get_x() + bar.get_width()/2, yval, str(int(yval)), ha='center', va='bottom')  # Adiciona o valor da barra acima dela

plt.show()  # Exibe o gráfico