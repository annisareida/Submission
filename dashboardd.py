import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gdown


file_url = 'https://drive.google.com/uc?id=1KB7H76vv75ObaQ1038zukubkI7wteOCf'  # Ganti FILE_ID dengan ID file dari link

gdown.download(file_url, 'order_reviews_products_data.csv', quiet=False)

order_reviews_products_df = pd.read_csv('order_reviews_products_data.csv')

file_url = 'https://drive.google.com/uc?id=1wBmTX1IwvS1DGTJjr0UKqmfNu28sPrxu'  # Ganti FILE_ID dengan ID file dari link

gdown.download(file_url, 'order_seller_geo_datasets.csv', quiet=False)

order_seller_geo_df = pd.read_csv('order_seller_geo_datasets.csv')

orders_dataset = pd.read_csv('orders_dataset.csv')
order_items_dataset = pd.read_csv('order_items_dataset.csv')


st.title("E-COMMERCE DASHBOARD")

tab1, tab2, tab3 = st.tabs(["TAB 1", "TAB 2", "TAB3"])

with tab1:
    st.subheader('Analisis Kategori Produk dan Rata-rata Ulasan')

    average_review_scores = order_reviews_products_df.groupby('product_category_name_english').agg(
        average_review_score=('review_score', 'mean'),
    ).reset_index()

    sorted_average_review_scores = average_review_scores.sort_values(by='average_review_score', ascending=False)

    st.write('Top 10 Kategori Produk Berdasarkan Rata-rata Skor Ulasan:')
    st.dataframe(sorted_average_review_scores.head(10))

    colors = ["#72BCD4"] + ["#D3D3D3"] * 9 

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x='average_review_score', 
        y='product_category_name_english', 
        data=sorted_average_review_scores.head(10), 
        palette=colors
    )
    plt.title('Kategori Produk dengan Review Terbesar', fontsize=16)
    plt.xlabel('Rata-rata Skor Ulasan', fontsize=12)
    plt.ylabel('Kategori Produk', fontsize=12)

    st.pyplot(plt)

with tab2:
    st.subheader('Analisis Distribusi Geografis Penjualan')

    sales_by_location = order_seller_geo_df.groupby(['seller_city', 'seller_state']).agg(
        total_sales=('price', 'sum'),
        total_orders=('order_id', 'count') 
    ).reset_index()

    sorted_sales_by_location = sales_by_location.sort_values(by='total_sales', ascending=False)

    st.write('Top 10 Kota Berdasarkan Total Penjualan:')
    st.dataframe(sorted_sales_by_location.head(10))

    colors = ["#72BCD4"] + ["#D3D3D3"] * 9  

    plt.figure(figsize=(12, 6))
    sns.barplot(
        x='total_sales', 
        y='seller_city', 
        data=sorted_sales_by_location.head(10), 
        palette=colors
    )
    plt.title('Total Penjualan Berdasarkan Kota Penjual', fontsize=16)
    plt.xlabel('Total Penjualan', fontsize=12)
    plt.ylabel('Kota Penjual', fontsize=12)

    st.pyplot(plt)

with tab3:
    orders_dataset['order_purchase_timestamp'] = pd.to_datetime(orders_dataset['order_purchase_timestamp'])
    max_date = orders_dataset['order_purchase_timestamp'].max()
    reference_date = max_date + pd.DateOffset(days=1)

    merged_df = orders_dataset.merge(order_items_dataset, on='order_id')

    rfm_df = merged_df.groupby('customer_id').agg(
        Recency=('order_purchase_timestamp', lambda x: (reference_date - x.max()).days),
        Frequency=('order_purchase_timestamp', 'count'),
        Monetary=('price', 'sum')
    ).reset_index()

    st.subheader("Visualisasi RFM")
    fig, ax = plt.subplots(3, 1, figsize=(10, 15))

    sns.histplot(rfm_df['Recency'], bins=30, ax=ax[0], kde=True)
    ax[0].set_title('Distribusi Recency', fontsize=14)
    ax[0].set_xlabel('Recency (Hari)', fontsize=12)

    sns.histplot(rfm_df['Frequency'], bins=30, ax=ax[1], kde=True)
    ax[1].set_title('Distribusi Frequency', fontsize=14)
    ax[1].set_xlabel('Frequency (Jumlah Transaksi)', fontsize=12)

    sns.histplot(rfm_df['Monetary'], bins=30, ax=ax[2], kde=True)
    ax[2].set_title('Distribusi Monetary', fontsize=14)
    ax[2].set_xlabel('Monetary (Total Pembelanjaan)', fontsize=12)

    st.pyplot(fig)
