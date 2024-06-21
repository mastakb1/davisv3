import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st

# Set title of the Streamlit app
st.title('Analisis Film Berdasarkan Pendapatan Kotor, Distributor, dan Genre')

# Path to CSV file
file_path = 'film_data_preprocessed.csv'

# Read CSV file
df = pd.read_csv(file_path)

# Display the dataframe
st.write("Dataframe:", df)

# Pisahkan genre menjadi baris terpisah
df_genre = df.set_index(['Film Name', 'Pendapatan Kotor ($)', 'Distributor']).Genre.str.split(', ', expand=True).stack().reset_index(name='Genre').drop('level_3', axis=1)

# Sidebar for user selection
st.sidebar.header('Filter')
selected_genre = st.sidebar.multiselect('Pilih Genre', df_genre['Genre'].unique())
selected_distributor = st.sidebar.multiselect('Pilih Distributor', df['Distributor'].unique())

# Filter data based on selection
filtered_df_genre = df_genre
filtered_df = df

if selected_genre:
    filtered_df_genre = df_genre[df_genre['Genre'].isin(selected_genre)]
if selected_distributor:
    filtered_df = df[df['Distributor'].isin(selected_distributor)]
    filtered_df_genre = filtered_df_genre[filtered_df_genre['Distributor'].isin(selected_distributor)]

# Plotting
st.subheader('Visualisasi')

# Relation: Scatter plot antara pendapatan kotor dan genre film
st.write("### Pendapatan Kotor berdasarkan Genre dan Distributor")
fig = px.scatter(filtered_df_genre, x='Genre', y='Pendapatan Kotor ($)', color='Distributor', size='Pendapatan Kotor ($)', hover_data=['Film Name'])
st.plotly_chart(fig)

# Comparison: Bar chart yang menunjukkan rata-rata pendapatan kotor untuk setiap genre film
st.write("### Rata-rata Pendapatan Kotor untuk Setiap Genre")
avg_gross_per_genre = filtered_df_genre.groupby('Genre')['Pendapatan Kotor ($)'].mean().reset_index()
fig = px.bar(avg_gross_per_genre, x='Genre', y='Pendapatan Kotor ($)', color='Genre')
st.plotly_chart(fig)

# Distribution: Histogram yang menunjukkan distribusi pendapatan kotor film-film
st.write("### Distribusi Pendapatan Kotor Film-film")
fig = px.histogram(filtered_df, x='Pendapatan Kotor ($)', nbins=20, marginal='box', hover_data=['Film Name'])
st.plotly_chart(fig)

# Composition: Pie chart yang menunjukkan komposisi genre film-film
st.write("### Komposisi Genre Film-film")
genre_counts = filtered_df_genre['Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
fig = px.pie(genre_counts, names='Genre', values='Count', title='Komposisi Genre Film-film')
st.plotly_chart(fig)
