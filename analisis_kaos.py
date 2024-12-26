pip install streamlit plotly pandas


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Tokopedia Men's Clothing Analysis",
    page_icon="👕",
    layout="wide"
)

# Add title and description
st.title("👕 Tokopedia Men's Clothing Analysis")
st.write("Interactive dashboard for analyzing men's clothing products on Tokopedia")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("tokopedia_kaos_pria.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Price range filter
price_range = st.sidebar.slider(
    "Select Price Range (IDR)",
    min_value=int(df['price'].min()),
    max_value=int(df['price'].max()),
    value=(int(df['price'].min()), int(df['price'].max()))
)

# Rating filter
ratings = sorted(df['rating'].unique())
selected_ratings = st.sidebar.multiselect(
    "Select Ratings",
    ratings,
    default=ratings
)

# Filter data based on selections
filtered_df = df[
    (df['price'].between(price_range[0], price_range[1])) &
    (df['rating'].isin(selected_ratings))
]

# Create two columns for the first row of visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Distribution")
    fig_price = px.histogram(
        filtered_df,
        x='price',
        nbins=50,
        title="Distribution of Product Prices"
    )
    fig_price.update_layout(bargap=0.1)
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    st.subheader("Reviews vs Price")
    fig_scatter = px.scatter(
        filtered_df,
        x='price',
        y='countReview',
        color='rating',
        hover_data=['name'],
        title="Review Count vs Price"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Create two columns for the second row of visualizations
col3, col4 = st.columns(2)

with col3:
    st.subheader("Discount Distribution")
    fig_discount = px.histogram(
        filtered_df,
        x='discountPercentage',
        nbins=30,
        title="Distribution of Discount Percentages"
    )
    fig_discount.update_layout(bargap=0.1)
    st.plotly_chart(fig_discount, use_container_width=True)

with col4:
    st.subheader("Rating Distribution")
    rating_counts = filtered_df['rating'].value_counts().sort_index()
    fig_rating = px.bar(
        x=rating_counts.index,
        y=rating_counts.values,
        title="Distribution of Ratings"
    )
    fig_rating.update_layout(xaxis_title="Rating", yaxis_title="Number of Products")
    st.plotly_chart(fig_rating, use_container_width=True)

# Add top products analysis
st.subheader("Top 10 Most Reviewed Products")
top_reviewed = filtered_df.nlargest(10, 'countReview')
fig_top = px.bar(
    top_reviewed,
    x='countReview',
    y='name',
    orientation='h',
    title="Top 10 Most Reviewed Products"
)
fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_top, use_container_width=True)

# Add summary metrics
st.subheader("Summary Metrics")
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Average Price",
        f"IDR {filtered_df['price'].mean():,.0f}"
    )

with col6:
    st.metric(
        "Average Rating",
        f"{filtered_df['rating'].mean():.2f}⭐"
    )

with col7:
    st.metric(
        "Average Reviews",
        f"{filtered_df['countReview'].mean():.0f}"
    )

with col8:
    st.metric(
        "Average Discount",
        f"{filtered_df['discountPercentage'].mean():.1f}%"
    )

# Add data table with search
st.subheader("Product Data")
search_term = st.text_input("Search products by name:")

if search_term:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_term, case=False)]

st.dataframe(
    filtered_df,
    column_config={
        "price": st.column_config.NumberColumn(
            "Price",
            format="IDR %d"
        ),
        "rating": st.column_config.NumberColumn(
            "Rating",
            format="%.1f ⭐"
        )
    },
    hide_index=True
)

# Add footer
st.markdown("---")
st.markdown("Data source: Tokopedia")
