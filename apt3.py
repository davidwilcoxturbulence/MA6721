# Importing libraries
import streamlit as st

st.set_page_config(layout="wide")
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt  # Optional for older functions
'''
streamlit run apt3.py
'''


# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("superstore.csv", encoding="latin")

# All visualization functions go here
def sales_total(dataframe):
    df=dataframe.copy()
    total_revenue = df['Sales'].sum()
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode = "number",
        value = total_revenue,
        title = {"text": "Total Sales"},
        number = {'prefix': "$", 'valueformat': ",.2f"},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    
    # fig.update_layout(
    #     font=dict(size=18),
    # #     font_color = 'white',
    # #     paper_bgcolor='rgba(0, 0, 0, 0)',
    # )
    
    return fig


def sales_and_profit_trend(dataframe):
    df = dataframe.copy()
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
    df['Shipping Delay'] = (df['Ship Date'] - df['Order Date']).dt.days
    sales_trend = df.groupby('Order Date').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sales_trend['Order Date'], y=sales_trend['Sales'], mode='lines', name='Sales', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=sales_trend['Order Date'], y=sales_trend['Profit'], mode='lines', name='Profit', line=dict(color='blue')))
    fig.update_layout(
##        title="Sales and Profit Trends",
                      xaxis_title="Order Date", yaxis_title="Value", width=800, height=600)
    return fig

def regional_performance(dataframe):
    df = dataframe.copy()
    region_stats = df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
    fig = px.bar(region_stats, x='Region', y=['Sales', 'Profit'], barmode='group',
##                 title="Sales and Profit by Region"
                 )
    fig.update_layout(xaxis_title="Region", yaxis_title="Amount", width=800, height=600)
    return fig

def average_shipping_delay_by_mode(dataframe):
    df = dataframe.copy()
    df['Shipping Delay'] = (pd.to_datetime(df['Ship Date'], errors='coerce') - pd.to_datetime(df['Order Date'], errors='coerce')).dt.days
    shipping_delay = df.groupby('Ship Mode')['Shipping Delay'].mean().reset_index()
    fig = px.bar(shipping_delay, x='Ship Mode', y='Shipping Delay',
##                 title='Average Shipping Delay by Shipping Mode',
                 color='Ship Mode', color_continuous_scale='coolwarm')
    fig.update_layout(xaxis_title='Shipping Mode', yaxis_title='Average Delay (Days)', width=800, height=600)
    return fig

def top_5_products_by_sales(dataframe):
    df = dataframe.copy()
    top_sales = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
    fig = px.bar(top_sales, x='Sales', y='Product Name', orientation='h',
##                 title='Top 5 Products by Sales',
                 color='Sales', color_continuous_scale='magma')
    fig.update_layout(xaxis_title='Sales', yaxis_title='Product Name',
##                      width=1500, height=400,
                      coloraxis_showscale=False)
    return fig

def plot_quantity_sunburst(dataframe):
    df = dataframe.copy()
    quantity_subcat_cat = df.groupby(['Sub-Category', 'Category'])['Quantity'].sum().reset_index()
    quantity_subcat_cat['Root'] = 'Total'
    fig = px.sunburst(quantity_subcat_cat, path=['Root', 'Category', 'Sub-Category'], values='Quantity',
##                      title='Quantity Distribution by Category and Sub-Category'
                      )
    fig.update_layout(width=500, height=500)
    return fig

def plot_treemap_sales(dataframe):
    df = dataframe.copy()  # Work with a copy of the input DataFrame

    # Create the treemap
    fig = px.treemap(
        df,
        path=['State'],  # Hierarchical path for the treemap
        values='Sales',  # Values to represent in the treemap
        color='Sales',  # Color based on sales values
        color_continuous_scale='Viridis',  # Use the Viridis color scale
##        title='Sales by Location'
    )

    # Customize layout
    fig.update_layout(
        font=dict(size=24, color='white'),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
    )

    # Customize traces
    fig.update_traces(
        hovertemplate="<b>%{label} </b><br> Sales: %{customdata[0]}"
    )

    # Customize layout
    fig.update_layout(
        width=1200,
        height=500,
    )

    return fig

def plot_quantity_sunburst_by_category(dataframe):
    df = dataframe.copy()  # Work with a copy of the input DataFrame

    # Grouping the data to create the sunburst structure
    quantity_cat = df.groupby('Category')['Quantity'].sum().reset_index()

    # Plotting the sunburst
    fig = px.sunburst(
        quantity_cat,
        path=['Category'],  # Define the hierarchy: Category
        values='Quantity',  # Values for segment size
##        title='Quantity Distribution by Category'
    )
    fig.update_layout(width=400, height=400)

    return fig

def plot_quantity_by_subcategory(dataframe):
    df = dataframe.copy()  # Work with a copy of the input DataFrame

    # Group data to calculate total quantity sold by sub-category
    quantity_subcat = df.groupby('Sub-Category')['Quantity'].sum().reset_index()

    # Create a horizontal bar plot with Plotly Express
    fig = px.bar(
        quantity_subcat.sort_values(by='Quantity', ascending=False),
        x='Quantity',
        y='Sub-Category',
        orientation='h',  # Horizontal bars
##        title='Total Quantity Sold by Sub-Category',
        labels={'Quantity': 'Quantity', 'Sub-Category': 'Sub-Category'},
        color='Sub-Category',  # Color bars by quantity
        color_continuous_scale='coolwarm',  # Use the coolwarm palette
    )

    # Customize layout
    fig.update_layout(
        xaxis_title='Quantity',
        yaxis_title='Sub-Category',
        coloraxis_showscale=False,
        showlegend=False,
        width=1200,
        height=600,
    )

    return fig




def gauge_chart(dataframe,item):
    df=dataframe.copy()
    top_profit = df.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(5).reset_index()
    value=top_profit.iloc[item][1]
    target=35000
    # Create a gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,  # Adjust this value for the needle position
        number={"prefix": "$"},
        gauge={
            'axis': {'range': [0, target]},  # Define the range
            'bar': {'color': "red"},  # Color of the needle
            'steps': [
                {'range': [0, target/2], 'color': "lightgray"},
                {'range': [target/2, target], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value  # Adjust this for a threshold indicator
            }
        }
    ))
    
    # Adjust layout for appearance
    fig.update_layout(
        title=top_profit.iloc[item][0],
        height=400,
        width=800
    )
    
    # Show the chart
    return fig


def scatter(dataframe):
    df=dataframe.copy()
    df2=df.copy()
    
    df2 = df2[df2['Profit'] >= 0]
    df2 = df2.reset_index(drop=True)
    fig = px.scatter(df2, 
                     y='Profit', 
                     x='Sales', 
                     size='Quantity', 
                     color='Category',
                     # hover_name='SKU',
                     # title='Relationship between Number of Products Sold and Total Shipping Costs',
                     # labels={'Number of products sold': 'Number of Products Sold', 'Total shipping costs': 'Total Shipping Costs ($)', 'Customer demographics': 'Customer Segment'},
                     # template='plotly_dark'
                    )
    
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    
    fig.update_layout(
        font=dict(size=14, color='black'),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    # fig.update_yaxes(range=[900, 9000])
    return fig






# Main Streamlit App
def main():
    st.title("MA6721 | Data Exploration and Visualization")
    
    # Load data
    df = load_data()

    st.write("## Key Performance Insights")

    st.plotly_chart(sales_total(df), use_container_width=True) 

    st.write("### Sales and Profit Trends")
    st.plotly_chart(sales_and_profit_trend(df), use_container_width=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("### Ranked Order Quantity Distribution by Sub-Category")
        st.plotly_chart(plot_quantity_by_subcategory(df), use_container_width=True)
    with col2:
        st.write("### Regional Performance")
        st.plotly_chart(regional_performance(df), use_container_width=True)
    with col3:
        st.write("### Average Shipping Delay by Mode")
        st.plotly_chart(average_shipping_delay_by_mode(df), use_container_width=True)

    st.write("### Gauge Charts")
    col4, col5, col6 = st.columns(3)
    
    with col4:
        
        st.plotly_chart(gauge_chart(df,0), use_container_width=True)
    with col5:
##      
        st.plotly_chart(gauge_chart(df,2), use_container_width=True)
    with col6:
##        
        st.plotly_chart(gauge_chart(df,3), use_container_width=True)
##
##
##


    col4, col5 = st.columns(2)
    with col4:
        st.write("### Top 5 Products by Sales")
        st.plotly_chart(top_5_products_by_sales(df), use_container_width=True)
    with col5:
        st.write("### Quantity Distribution by Category")
        fig = plot_quantity_sunburst_by_category(df)
        st.plotly_chart(fig,use_container_width=True)

        
    st.write("### Sales Distribution by State")
    fig = plot_treemap_sales(df)
    st.plotly_chart(fig)

    st.write("### Scatterplot of Profit vs Sales")
    fig = scatter(df)
    st.plotly_chart(fig)

    
    st.write("### Quantity Distribution by Category and Sub-Category")
    st.plotly_chart(plot_quantity_sunburst(df), use_container_width=True)

    

    

        

# Run the Streamlit app
if __name__ == "__main__":
    main()
