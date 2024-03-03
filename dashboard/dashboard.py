import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set(style='whitegrid')


# Set tema Streamlit
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Membaca data CSV dari GitHub
alldata_df = pd.read_csv("https://raw.githubusercontent.com/fatihanadias/submission/master/all_data_ecommerce.csv")

# Header Streamlit dengan judul menarik
st.title('🛒 E-Commerce Dashboard 🚀')

# Menambahkan deskripsi untuk memberikan konteks
st.markdown(
    "Selamat datang di E-Commerce Dashboard! Dashboard ini memberikan informasi terkait review produk, "
    "penjualan per negara bagian, tipe pembayaran yang digunakan oleh pelanggan, dan korelasi antara ongkir dan nilai pembayaran."
)


# Mengatur tema background
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f4;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Membuat tab untuk subheader
selected_tab = st.sidebar.radio("Pilih Menu", ["Review Produk", "Produk Terjual", "Tipe Payment", "Ongkir vs Nilai Payment"])

# Tab "Review Produk"
if selected_tab == "Review Produk":
    st.subheader("Review Produk")

    # Menentukan produk yang mendapat rating terburuk dan terbaik
    mean_ratings_items_df = alldata_df.groupby("product_category_name_english").review_score.mean().sort_values(ascending=False).reset_index()
    mean_ratings_items_df.head(5)

    # Membuat plot bar untuk rating produk
    fig1, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(24, 6))
    sns.barplot(x="review_score", y="product_category_name_english", hue="product_category_name_english",data=mean_ratings_items_df.head(5), palette="rocket", ax=ax1,legend=False)
    ax1.set_ylabel(None)
    ax1.set_xlabel(None)
    ax1.set_title("Rata-Rata Nilai Review Produk Berdasarkan Kategori ", loc="center", fontsize=15)
    ax1.tick_params(axis ='y', labelsize=12)
    # Menampilkan gambar pada tab "Review Produk"
    st.pyplot(fig1)


# Tab "Produk Terjual"
elif selected_tab == "Produk Terjual":
    st.subheader("Produk Terjual")

    # Membuat plot bar untuk produk terjual terbanyak
    bycategory_df = alldata_df.groupby(by=["customer_state"]).order_id.nunique().reset_index()
    bycategory_df.rename(columns={
        "order_id": "cust_count"
    }, inplace=True)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(
        y="cust_count",
        x="customer_state",
        hue="cust_count",
        data=bycategory_df.sort_values(by="cust_count", ascending=False),
        palette="viridis", legend=False
    )
    plt.title("Banyaknya Produk Terjual per Negara Bagian", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    # Menampilkan gambar pada tab "Produk Terjual"
    st.pyplot(fig2)

# Tab "Tipe Payment"
elif selected_tab == "Tipe Payment":
    st.subheader("Tipe Payment")

    # Membuat plot lingkaran proporsi penggunaan tipe payment
    payment_count = alldata_df['payment_type'].value_counts()
    colors = sns.color_palette("pastel", len(payment_count))
    explode = (0.1, 0, 0, 0)

    fig3, ax3 = plt.subplots()
    ax3.pie(
        x=payment_count,
        labels=payment_count.index,
        autopct='%1.1f%%',
        colors=colors,
        explode=explode
    )
    plt.title('Proporsi Tipe Payment yang Digunakan Customer')
    # Menampilkan gambar pada tab "Tipe Payment"
    st.pyplot(fig3)

# Tab "Ongkir vs Nilai Payment"
elif selected_tab == "Ongkir vs Nilai Payment":
    st.subheader("Ongkir vs Nilai Payment")

    col1, col2 = st.columns(2)

    with col1:
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        sns.regplot(x=alldata_df['freight_value'], y=alldata_df['payment_value'])
        plt.title('Regplot: Ongkir vs Nilai Payment')
        # Menampilkan gambar pada tab "Ongkir vs Nilai Payment"
        st.pyplot(fig4)

    with col2:
        selected_columns = alldata_df[['payment_value','freight_value']]
        selected_columns.head(5)
        correlation_mat = selected_columns.corr()
        fig5, ax5 = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_mat, annot=True, cmap='viridis', fmt='.2f', linewidths=0.5)
        plt.title('Matriks Korelasi')
        # Menampilkan gambar pada tab "Ongkir vs Nilai Payment"
        st.pyplot(fig5)


st.caption("Copyright by fatihanadias")
