import streamlit as st
import pandas as pd
import plotly.express as px
from awDb import get_data_from_db


sales_fact_df = get_data_from_db("""
    SELECT 
        sf.time_key, 
        sf.product_key, 
        sf.LineTotal, 
        sf.OrderQty,
        t.fulldates,
        t.years
    FROM 
        sales_fact sf
    JOIN 
        time t ON sf.time_key = t.id
""")
product_fact_df = get_data_from_db("SELECT id, name, category FROM product")


sales_fact_df['fulldates'] = pd.to_datetime(sales_fact_df['fulldates'])


st.sidebar.header('Options')
color_palette = st.sidebar.selectbox('Select Color Palette', ['plotly', 'ggplot2', 'seaborn',])

selected_year = st.sidebar.selectbox('Select Year', sales_fact_df['years'].unique())

# line
filtered_sales_fact_df = sales_fact_df[sales_fact_df['years'] == selected_year]


sales_time_df = filtered_sales_fact_df.copy()

# scater
sales_product_df = pd.merge(filtered_sales_fact_df, product_fact_df, left_on='product_key', right_on='id')
# pie 
category_sales_df = sales_product_df.groupby('category').agg({'LineTotal': 'sum'}).reset_index()

# histogram
sales_time_hist_df = sales_time_df['LineTotal']


st.title('Sales Dashboard')


st.header('Tren Penjualan Harian')


daily_sales = sales_time_df.groupby('fulldates').agg({'LineTotal': 'sum'}).reset_index()
line_fig = px.line(daily_sales, x='fulldates', y='LineTotal', title='Tren Penjualan Harian', template=color_palette)
st.plotly_chart(line_fig)


st.header('Top 10 Produk Terlaris')
top_products = sales_product_df.groupby('name').agg({'LineTotal': 'sum'}).nlargest(10, 'LineTotal').reset_index()


for index, row in top_products.iterrows():
    progress_percent = row['LineTotal'] / top_products['LineTotal'].max()
    st.write(f"{row['name']} - Total Penjualan: {row['LineTotal']}")
    st.progress(progress_percent)


st.header('Relasi Antara Order Quantity dan Total Penjualan')
scatter_fig = px.scatter(sales_product_df, x='OrderQty', y='LineTotal', color='category', title='Relasi Antara Order Quantity dan Total Penjualan', template=color_palette)
st.plotly_chart(scatter_fig)


st.header('Kontribusi Kategori dalam Penjualan')
pie_fig = px.pie(category_sales_df, values='LineTotal', names='category', title='Kontribusi Kategori dalam Penjualan', template=color_palette)
st.plotly_chart(pie_fig)


st.header('Distribusi Jumlah Penjualan')
hist_fig = px.histogram(sales_time_hist_df, title='Distribusi Jumlah Penjualan', template=color_palette)
st.plotly_chart(hist_fig)


