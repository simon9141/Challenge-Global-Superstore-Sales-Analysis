import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("superstore.csv")  # Ensure your data file is correct

# Set page layout
st.set_page_config(layout="wide", page_title="Superstore Sales Dashboard")
st.title("Superstore Sales Dashboard")

# Summary statistics
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_quantity = df['Quantity'].sum()

# Header Section with Styling
st.markdown("<h2 style='text-align: center; color: #007acc;'>Global Superstore Sales Overview</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# Display Key Metrics
with col1:
    st.metric("Total Profit", f"${total_profit/1e6:.2f}M", delta=f"{(total_profit/total_sales)*100:.1f}% Profit Margin")
with col2:
    st.metric("Total Quantity", f"{total_quantity:,.0f} Units")
with col3:
    st.metric("Total Sales", f"${total_sales/1e6:.1f}M")

# Sidebar Filters
st.sidebar.header("Filter Options")
market_filter = st.sidebar.selectbox("Market", options=["All"] + list(df['Market'].unique()))
segment_filter = st.sidebar.selectbox("Segment", options=["All"] + list(df['Segment'].unique()))
category_filter = st.sidebar.multiselect("Category", options=df['Category'].unique(), default=df['Category'].unique())

# Apply Filters
if market_filter != "All":
    df = df[df['Market'] == market_filter]
if segment_filter != "All":
    df = df[df['Segment'] == segment_filter]
if category_filter:
    df = df[df['Category'].isin(category_filter)]

# Detailed Insights Section
st.markdown("## Sales Insights")

# Row 1: Sales by Region & Segment
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sales by Region and Sub-Category")
    fig, ax = plt.subplots(figsize=(8, 5))
    region_subcategory_sales = df.groupby(['Region', 'Sub.Category'])['Sales'].sum().unstack()
    sns.heatmap(region_subcategory_sales, cmap="Blues", annot=True, fmt=".1f", linewidths=.5, ax=ax)
    st.pyplot(fig)

with col2:
    st.markdown("### Sales by Segment")
    fig, ax = plt.subplots(figsize=(5, 4))
    segment_sales = df.groupby('Segment')['Sales'].sum()
    colors = sns.color_palette("Set2")
    ax.pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%', startangle=140, colors=colors)
    st.pyplot(fig)

# Row 2: Profit by Category & Quantity by Ship Mode
col3, col4 = st.columns(2)

with col3:
    st.markdown("### Profit by Category")
    fig, ax = plt.subplots(figsize=(5, 5))
    category_profit = df.groupby('Category')['Profit'].sum()
    ax.barh(category_profit.index, category_profit.values, color=sns.color_palette("pastel"))
    ax.set_xlabel("Profit ($)")
    st.pyplot(fig)

with col4:
    st.markdown("### Quantity by Ship Mode")
    fig, ax = plt.subplots(figsize=(5, 5))
    shipmode_quantity = df.groupby('Ship.Mode')['Quantity'].sum()
    ax.pie(shipmode_quantity, labels=shipmode_quantity.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("muted"))
    st.pyplot(fig)

# Row 3: Quantity by Month & Top 5 Countries by Quantity Sold
col5, col6 = st.columns(2)

with col5:
    st.markdown("### Monthly Quantity Sold")
    df['Order.Date'] = pd.to_datetime(df['Order.Date'])
    df['Month'] = df['Order.Date'].dt.month
    quantity_by_month = df.groupby('Month')['Quantity'].sum()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(x=quantity_by_month.index, y=quantity_by_month.values, marker='o', ax=ax, color='navy')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax.set_ylabel("Quantity Sold")
    st.pyplot(fig)

with col6:
    st.markdown("### Top 5 Countries by Quantity Sold")
    top_countries_quantity = df.groupby('Country')['Quantity'].sum().nlargest(5)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(y=top_countries_quantity.index, x=top_countries_quantity.values, palette="viridis", ax=ax)
    ax.set_xlabel("Quantity Sold")
    st.pyplot(fig)

# Row 4: Monthly Sales / Discount Analysis
st.markdown("### Monthly Sales and Discount Trends")
monthly_sales = df.groupby('Month')['Sales'].sum()
monthly_discount = df.groupby('Month')['Discount'].mean() * 100  # assuming discount in percentage

fig, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=monthly_sales.index, y=monthly_sales.values, color='skyblue', ax=ax1, label='Sales')
ax1.set_ylabel("Total Sales ($)", color='blue')
ax1.set_xticks(range(0, 12))
ax1.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

# Plotting the discount trend on a secondary y-axis
ax2 = ax1.twinx()
sns.lineplot(x=monthly_discount.index, y=monthly_discount.values, color='purple', marker='o', ax=ax2, label='Discount')
ax2.set_ylabel("Discount (%)", color='purple')
fig.legend(loc='upper left')
st.pyplot(fig)

# Footer Notes or Insights Section
st.markdown("<h4 style='text-align: center; color: grey;'>Data from Global Superstore</h4>", unsafe_allow_html=True)
