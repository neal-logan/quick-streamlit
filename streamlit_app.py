import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment - Neal Logan")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")

category_list = df['Category'].drop_duplicates()

target_cat = st.selectbox(
    label='Select Category', 
    options=category_list,
    index=0,
    placeholder="Choose a Category", 
    disabled=False, 
    label_visibility="visible")

st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")

sub_category_list = df[df.Category == target_cat]['Sub_Category'].drop_duplicates()

target_subcat = st.multiselect(
    label='Select Subcategory', 
    options=sub_category_list, 
    placeholder="Choose a Sub-category", 
    disabled=False, 
    label_visibility="visible")

st.write("### (3) show a line chart of sales for the selected items in (2)")

target_data = df[df['Sub_Category'].isin(target_subcat)]

target_sales_by_month = target_data.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.line_chart(target_sales_by_month, y="Sales")

st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")

target_sales = target_data['Sales'].sum()
target_profit = target_data['Profit'].sum()
target_profit_margin = target_profit / target_sales

overall_profit_margin = df['Profit'].sum() / df['Sales'].sum()

profit_delta = (target_profit_margin - overall_profit_margin)

st.metric(
    label = 'Selected Subcategory: Total Sales', 
    value = target_sales, 
    delta=None, 
    delta_color="normal", 
    help=None, 
    label_visibility="visible")

st.metric(
    label = 'Selected Subcategory: Total Profit', 
    value = target_profit, 
    delta=None, 
    delta_color="normal", 
    help=None, 
    label_visibility="visible")

st.metric(
    label = 'Selected Subcategory: Overall Profit Margin (%)', 
    value = target_profit_margin*100, 
    delta= profit_delta*100, 
    delta_color="normal", 
    help=None, 
    label_visibility="visible")

st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories) \n (see above)")

