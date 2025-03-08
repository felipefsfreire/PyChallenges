"""
Desafio: Relatórios Avançados e Dashboard de Vendas
Agora que você já armazenou os dados no SQLite, o desafio será consultar e analisar os dados diretamente via SQL,
além de criar um dashboard interativo para visualização.

# Parte 1 - Consultas SQL Avançadas
1. Clientes mais frequentes 🔁
    a. Liste os 10 clientes que mais compraram (quantidade de pedidos realizados).
2. Produtos mais rentáveis 💰
    a. Encontre os 5 produtos que mais geraram receita total.
3. Média de valor gasto por categoria 📊
    a. Liste as categorias de produtos com a média de valor gasto por pedido.
4. Comparação de faturamento 📅
    a.Compare o faturamento entre o primeiro semestre (Jan-Jun) e o segundo semestre (Jul-Dez) de 2024.

# Parte 2 - Dashboard Interativo com Streamlit
Agora, crie um dashboard interativo usando Streamlit para visualizar os dados de forma dinâmica.

1. Componentes do Dashboard:
    a. Filtro por mês 📆 (para visualizar as vendas de um período específico).
    b. Gráficos interativos 📊:
        I. Gráfico de barras com os produtos mais vendidos.
        II. Gráfico de linha mostrando o faturamento mensal.
        III. Tabela interativa com os clientes VIPs.
"""

import pandas as pd  # Importa a biblioteca Pandas para manipulação de dados
import sqlite3  # Importa a biblioteca SQLite para interação com bancos de dados SQLite
import streamlit as st  # Importa a biblioteca Streamlit para criação de aplicativos web

conn = sqlite3.connect('salesEcommerce.db')  # Conecta ao banco de dados SQLite 'salesEcommerce.db'
cursor = conn.cursor()  # Cria um cursor para executar comandos SQL

# Define um dicionário com consultas SQL para diferentes análises
dicQueries = {
    "queryTopCustomers": '''
        SELECT customer, SUM(sales_quantity) AS sum_quantity
        FROM sales
        GROUP BY customer
        ORDER BY SUM(sales_quantity) DESC
        LIMIT 10
    ''',  # Consulta para obter os 10 clientes que mais compraram em quantidade
    "queryTopProducts": '''
        SELECT product, SUM(total_price) AS total_revenue
        FROM sales
        GROUP BY product
        ORDER BY SUM(total_price) DESC
        LIMIT 5
    ''',  # Consulta para obter os 5 produtos que geraram mais receita
    "queryAvgPriceCategory": '''
        SELECT category, ROUND(AVG(total_price), 2) AS avg_price
        FROM sales
        GROUP BY category
        ORDER BY AVG(total_price) DESC
    ''',  # Consulta para obter o preço médio gasto por categoria
    "queryHalfYear": '''
        SELECT CASE 
            WHEN STRFTIME('%m', sales_date) BETWEEN '01' AND '06' THEN 'first half-year'
            WHEN STRFTIME('%m', sales_date) BETWEEN '07' AND '12' THEN 'second half-year'
        END AS half_year, ROUND(SUM(total_price), 2) AS total_revenue
        FROM sales
        WHERE STRFTIME('%Y', sales_date) = '2024'
        GROUP BY half_year
        ORDER BY half_year
    '''  # Consulta para comparar o faturamento entre o primeiro e o segundo semestre de 2024
}

def runQuery(queryKey, params=()):
    """Executa uma consulta SQL e retorna o resultado como um DataFrame.

    Args:
        queryKey (str): Chave da consulta no dicionário `dicQueries`.
        params (tuple, optional): Parâmetros para a consulta SQL. Padrão é ().

    Returns:
        pandas.DataFrame: DataFrame com o resultado da consulta.
    """
    query = dicQueries[queryKey]  # Obtém a consulta SQL do dicionário
    return pd.read_sql(query, conn, params=params)  # Executa a consulta e retorna o resultado como um DataFrame

dfTopCustomers = runQuery("queryTopCustomers")  # Executa a consulta para obter os top 10 clientes
dfTopProducts = runQuery("queryTopProducts")  # Executa a consulta para obter os top 5 produtos
dfAvgPriceCategory = runQuery("queryAvgPriceCategory")  # Executa a consulta para obter o preço médio por categoria
dfHalfYear = runQuery("queryHalfYear")  # Executa a consulta para comparar o faturamento por semestre

print("Top 10 Clientes:")
print(dfTopCustomers)  # Imprime o DataFrame com os top 10 clientes

print("\nTop 5 Produtos mais rentáveis:")
print(dfTopProducts)  # Imprime o DataFrame com os top 5 produtos

print("\nMédia de valor gasto por categoria:")
print(dfAvgPriceCategory)  # Imprime o DataFrame com o preço médio por categoria

print("\nComparação de faturamento Jan-Jun e Jul-Dez:")
print(dfHalfYear)  # Imprime o DataFrame com a comparação de faturamento por semestre


st.title(" Sales Dashboard - E-commerce")  # Define o título do aplicativo Streamlit

monthFilter = st.selectbox("Selecione um mês:", ["Todos"] + [f"{m:02d}/2024" for m in range(1, 13)])  # Cria um selectbox para filtrar os dados por mês

# Define um dicionário com consultas SQL para visualização dos dados
dicQueriesViz = {
    "queryBarTopProducts": '''
        SELECT product, SUM(sales_quantity) AS total_quantity
        FROM sales
        {whereClause}
        GROUP BY product
        ORDER BY SUM(sales_quantity) DESC
        LIMIT 10
    ''',  # Consulta para obter os 10 produtos mais vendidos em quantidade
    "queryLineMonthRevenue": '''
        SELECT STRFTIME('%m', sales_date) AS month, SUM(total_price) AS total_revenue
        FROM sales
        {whereClause}
        GROUP BY STRFTIME('%m', sales_date)
        ORDER BY STRFTIME('%m', sales_date)
    ''',  # Consulta para obter o faturamento mensal
    "queryVipCustomers": '''
        SELECT customer, SUM(sales_quantity) AS total_quantity, SUM(total_price) AS total_amount
        FROM sales
        {whereClause}
        GROUP BY customer
        ORDER BY SUM(total_price) DESC, SUM(sales_quantity) DESC, customer
        LIMIT 10
    '''  # Consulta para obter os 10 clientes VIPs (que mais compraram em valor e quantidade)
}

whereClause = ""  # Inicializa a cláusula WHERE da consulta SQL
params = ()  # Inicializa os parâmetros da consulta SQL
if monthFilter != "Todos":  # Verifica se o filtro de mês foi selecionado
    selectMonth = monthFilter.split("/")[0]  # Obtém o número do mês selecionado
    whereClause = "WHERE STRFTIME('%m', sales_date) = ? AND STRFTIME('%Y', sales_date) = '2024'"  # Define a cláusula WHERE para filtrar os dados pelo mês selecionado
    params = (selectMonth,)  # Define os parâmetros da consulta SQL

def runQueryViz(queryKey):
    """Executa uma consulta SQL para visualização e retorna o resultado como um DataFrame.

    Args:
        queryKey (str): Chave da consulta no dicionário `dicQueriesViz`.

    Returns:
        pandas.DataFrame: DataFrame com o resultado da consulta.
    """
    query = dicQueriesViz[queryKey].format(whereClause=whereClause)  # Obtém a consulta SQL do dicionário e formata com a cláusula WHERE
    return pd.read_sql(query, conn, params=params)  # Executa a consulta e retorna o resultado como um DataFrame

st.write("Gráfico de barras com os produtos mais vendidos.")  # Exibe um texto no aplicativo
dfBarTopProducts = runQueryViz("queryBarTopProducts")  # Executa a consulta para obter os top 10 produtos mais vendidos
if not dfBarTopProducts.empty:  # Verifica se o DataFrame não está vazio
    st.bar_chart(dfBarTopProducts.set_index('product'), x_label="Products", y_label="Quantity")  # Cria um gráfico de barras com os top 10 produtos mais vendidos
else:
    st.write("Nenhum dado disponível para o período selecionado.")  # Exibe uma mensagem caso não haja dados para o período selecionado

st.write("Gráfico de linha faturamento mensal.")  # Exibe um texto no aplicativo
dfLineMonthRevenue = runQueryViz("queryLineMonthRevenue")  # Executa a consulta para obter o faturamento mensal
if not dfLineMonthRevenue.empty:  # Verifica se o DataFrame não está vazio
    st.line_chart(dfLineMonthRevenue.set_index('month'), x_label="Months", y_label="Revenue")  # Cria um gráfico de linha com o faturamento mensal
else:
    st.write("Nenhum dado disponível para o período selecionado.")  # Exibe uma mensagem caso não haja dados para o período selecionado

st.write("Tabela interativa com os clientes VIPs")  # Exibe um texto no aplicativo
dfVipCustomers = runQueryViz("queryVipCustomers")  # Executa a consulta para obter os clientes VIPs
if not dfVipCustomers.empty:  # Verifica se o DataFrame não está vazio
    st.dataframe(dfVipCustomers.style.highlight_max(subset=['total_quantity', 'total_amount']), hide_index=True)  # Cria uma tabela interativa com os clientes VIPs, destacando os maiores valores
else:
    st.write("Nenhum dado disponível para o período selecionado.")  # Exibe uma mensagem caso não haja dados para o período selecionado

conn.close()  # Fecha a conexão com o banco de dados