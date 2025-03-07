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

import pandas as pd
import sqlite3
import streamlit as st

# Conexão com o banco de dados
conn = sqlite3.connect('salesEcommerce.db')
cursor = conn.cursor()

# Criando dicionário de queries
dicQueries = {
    "queryTopCustomers": '''
        SELECT customer, SUM(sales_quantity) AS sum_quantity
        FROM sales
        GROUP BY customer
        ORDER BY SUM(sales_quantity) DESC
        LIMIT 10
    ''',
    "queryTopProducts": '''
        SELECT product, SUM(total_price) AS total_revenue
        FROM sales
        GROUP BY product
        ORDER BY SUM(total_price) DESC
        LIMIT 5
    ''',
    "queryAvgPriceCategory": '''
        SELECT category, ROUND(AVG(total_price), 2) AS avg_price
        FROM sales
        GROUP BY category
        ORDER BY AVG(total_price) DESC
    ''',
    "queryHalfYear": '''
        SELECT CASE 
            WHEN STRFTIME('%m', sales_date) BETWEEN '01' AND '06' THEN 'first half-year'
            WHEN STRFTIME('%m', sales_date) BETWEEN '07' AND '12' THEN 'second half-year'
        END AS half_year, ROUND(SUM(total_price), 2) AS total_revenue
        FROM sales
        WHERE STRFTIME('%Y', sales_date) = '2024'
        GROUP BY half_year
        ORDER BY half_year
    '''
}

# Função para executar queries
def runQuery(queryKey, params=()):
    query = dicQueries[queryKey]
    return pd.read_sql(query, conn, params=params)

# Executando consultas
dfTopCustomers = runQuery("queryTopCustomers")
dfTopProducts = runQuery("queryTopProducts")
dfAvgPriceCategory = runQuery("queryAvgPriceCategory")
dfHalfYear = runQuery("queryHalfYear")

# Exibindo os resultados
print("Top 10 Clientes:")
print(dfTopCustomers)

print("\nTop 5 Produtos mais rentáveis:")
print(dfTopProducts)

print("\nMédia de valor gasto por categoria:")
print(dfAvgPriceCategory)

print("\nComparação de faturamento Jan-Jun e Jul-Dez:")
print(dfHalfYear)

# Criando o dashboard no Streamlit

st.title("📊 Sales Dashboard - E-commerce")

# Filtro por mês
monthFilter = st.selectbox("Selecione um mês:", ["Todos"] + [f"{m:02d}/2024" for m in range(1, 13)])

# Criando dicionário de queries para visualização
dicQueriesViz = {
    "queryBarTopProducts": '''
        SELECT product, SUM(sales_quantity) AS total_quantity
        FROM sales
        {whereClause}
        GROUP BY product
        ORDER BY SUM(sales_quantity) DESC
        LIMIT 10
    ''',
    "queryLineMonthRevenue": '''
        SELECT STRFTIME('%m', sales_date) AS month, SUM(total_price) AS total_revenue
        FROM sales
        {whereClause}
        GROUP BY STRFTIME('%m', sales_date)
        ORDER BY STRFTIME('%m', sales_date)
    ''',
    "queryVipCustomers": '''
        SELECT customer, SUM(sales_quantity) AS total_quantity, SUM(total_price) AS total_amount
        FROM sales
        {whereClause}
        GROUP BY customer
        ORDER BY SUM(total_price) DESC, SUM(sales_quantity) DESC, customer
        LIMIT 10
    '''
}

# Ajustando a cláusula WHERE
whereClause = ""
params = ()
if monthFilter != "Todos":
    selectMonth = monthFilter.split("/")[0]
    whereClause = "WHERE STRFTIME('%m', sales_date) = ? AND STRFTIME('%Y', sales_date) = '2024'"
    params = (selectMonth,)

# Função para executar queries de visualização
def runQueryViz(queryKey):
    query = dicQueriesViz[queryKey].format(whereClause=whereClause)
    return pd.read_sql(query, conn, params=params)

# Exibindo gráfico de barras com os produtos mais vendidos
st.write("Gráfico de barras com os produtos mais vendidos.")
dfBarTopProducts = runQueryViz("queryBarTopProducts")
if not dfBarTopProducts.empty:
    st.bar_chart(dfBarTopProducts.set_index('product'), x_label="Products", y_label="Quantity")
else:
    st.write("Nenhum dado disponível para o período selecionado.")

# Gráfico de linha mostrando o faturamento mensal.
st.write("Gráfico de linha faturamento mensal.")
dfLineMonthRevenue = runQueryViz("queryLineMonthRevenue")
if not dfLineMonthRevenue.empty:
    st.line_chart(dfLineMonthRevenue.set_index('month'), x_label="Months", y_label="Revenue")
else:
    st.write("Nenhum dado disponível para o período selecionado.")

# Tabela interativa com os clientes VIPs.
st.write("Tabela interativa com os clientes VIPs")
dfVipCustomers = runQueryViz("queryVipCustomers")
if not dfVipCustomers.empty:
    st.dataframe(dfVipCustomers.style.highlight_max(subset=['total_quantity', 'total_amount']), hide_index=True)
else:
    st.write("Nenhum dado disponível para o período selecionado.")
# Fechando conexão
conn.close()
