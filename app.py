import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
orders = pd.read_csv("data/Orders.csv")
people = pd.read_csv("data/People.csv")
returns = pd.read_csv("data/Returns.csv")

# Merge returns into orders
orders["Returned"] = orders["Order ID"].isin(returns["Order ID"])

# Calculate Profit Margin
orders["Profit Margin"] = orders["Profit"] / orders["Sales"]

# Sidebar filters
st.sidebar.header("Filter Sales Data")
regions = st.sidebar.multiselect("Select Region", options=orders["Region"].unique(), default=orders["Region"].unique())
categories = st.sidebar.multiselect("Select Category", options=orders["Category"].unique(), default=orders["Category"].unique())

filtered = orders[(orders["Region"].isin(regions)) & (orders["Category"].isin(categories))]

# KPIs
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
returned_orders = filtered["Returned"].sum()
profit_margin = total_profit / total_sales if total_sales else 0

st.title("📊 Sales Performance Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.2%}")
col4.metric("Returned Orders", f"{returned_orders}")

# Sales over time
filtered["Order Date"] = pd.to_datetime(filtered["Order Date"])
sales_trend = filtered.groupby("Order Date")["Sales"].sum().reset_index()
fig_trend = px.line(sales_trend, x="Order Date", y="Sales", title="Sales Over Time")
st.plotly_chart(fig_trend)

# Sales by category
fig_category = px.bar(filtered.groupby("Category")["Sales"].sum().reset_index(), x="Category", y="Sales", title="Sales by Category")
st.plotly_chart(fig_category)

# Top Products
top_products = filtered.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
fig_top = px.bar(top_products, x="Sub-Category", y="Sales", title="Top 10 Sub-Categories by Sales")
st.plotly_chart(fig_top)

# Returns Heatmap
returns_by_state = filtered.groupby("State")["Returned"].mean().reset_index()
fig_return = px.choropleth(locations=returns_by_state["State"],
                           locationmode="USA-states",
                           color=returns_by_state["Returned"],
                           scope="usa",
                           title="Return Rate by State")
st.plotly_chart(fig_return)

