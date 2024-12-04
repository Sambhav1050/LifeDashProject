import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# Importing and Cleaning Data
data = pd.read_csv(r'MasterIndustryData.csv', index_col='Company Acronym')
for col in data.select_dtypes(include=['object']).columns:
    data[col] = data[col].str.replace(',', '')
    data[col] = data[col].astype('Int64')

# Bar Creator Function
def bar_creator(x_values, y_values, orientation='v', title="", x_label="", y_label="", color='blue'):
    if orientation=='v':
        fig = px.bar(x=x_values, y=y_values)
        fig.update_layout(
            title = '<b>'+title+'</b>',
            xaxis_title_text = '<b>'+x_label+'</b>',
            yaxis_title_text = '<b>'+y_label+'</b>',
            showlegend = False,
        )
        fig.update_traces(
            marker_color=color, 
            marker_line_width=2, 
            marker_line_color='black'
        )
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x = x_values,
                y = y_values,
                orientation='h'
            )
        )
        fig.update_layout(
            title = '<b>'+title+'</b>',
            xaxis_title_text = '<b>'+x_label+'</b>',
            yaxis_title_text = '<b>'+y_label+'</b>',
            showlegend=False,
            bargap = 0.2
        )
        fig.update_traces(
            marker_color=color, 
            marker_line_width=0.9, 
            marker_line_color='black'
        )
    return fig

# Setting the layout of the streamlit to wide
st.set_page_config(layout='wide')

dashboard, analysis = st.tabs(["Dashboard", "Analysis"])

with dashboard:
    st.header("DASHBOARD")
    
    col1, col2 = st.columns([1,3], gap="small")

    with col1:
        st.success("MARKET AND SIZE")
        
        # Adding pie-chart: Percentage of Market
        fig = go.Figure()
        fig.add_trace(
            go.Pie(
                labels = data.index,
                values = data['First Year Premiums']
            )
        )
        fig.update_layout(
            title = '<b>Market Share of Life Insurance Companies</b>'
        )
        fig.update_traces(
            pull=[0.1, 0, 0.2, 0, 0, 0.3, 0, 0.1, 0, 0.1, 0.1],
            marker_line_width=0.5,
            marker_line_color='black'
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.success("ASSET AND LIABILITIES")

        col21, col22, col23 = st.columns([1, 1, 1], gap="small")

        # Chart: Gross Insurance Contract Liabilities
        with col21:
            fig = bar_creator(
                orientation='h',
                x_values = data['Gross Insurance Contract Liabilities'],
                y_values = data.index,
                title='Gross Insurance Contract Liabilities',
                x_label = 'Amount (in Rs.)',
                y_label = 'Company Acronym',
                color = '#F8BB5A'
            )
            st.plotly_chart(fig)
        # Chart: Catastrophic Reserves Ratio
        with col22:
            catastrophic_reserves_ratio = data['Catastrophic Reserves'] / data['Gross Insurance Contract Liabilities']
            fig = bar_creator(
                orientation = 'h',
                x_values = catastrophic_reserves_ratio,
                y_values = data.index,
                title = 'Catastrophic Reserves Ratio',
                x_label = 'Catastrophic Reserves / Gross Insurance Contract Liabilities',
                y_label = 'Company Acronym',
                color = '#5AE2F8'
            )
            st.plotly_chart(fig)
        # Chart: Asset-Liability Ratio
        with col23:
            asset_liability_ratio = data['Asset'] / data['Liability']
            fig = bar_creator(
                orientation = 'v',
                x_values = data.index,
                y_values = asset_liability_ratio,
                title = 'Asset Liability Ratio',
                x_label = 'Company Acronym',
                y_label = 'Total Assets / Total Liabilities',
                color = '#F8E75A'
            )
            st.plotly_chart(fig)
    col1, col2 = st.columns([1, 3], gap="small")
    
    # Chart: Paid-up Capital
    with col1:
        fig = bar_creator(
            orientation='v',
            x_values = data.index,
            y_values = data['Paid-up Capital'],
            title='Paid Up Capital of Life Insurance Companies',
            x_label='Company Acronym',
            y_label='Paid Up Capital',
            color='#8BF85A'
        )
        st.plotly_chart(fig, use_container_width=True)
    # Profitability Section
    with col2:
        st.success("PROFITABILITY")
        col21, col22 = st.columns([1, 1], gap="small")

        # Chart: Profit Margin
        with col21:
            profit_margin = data['Net Profit'] / data['Gross Earned Premiums']
            fig = bar_creator(
                x_values = data.index,
                y_values = profit_margin,
                title = 'Profit Margin',
                x_label = 'Company Acronym',
                color = '#F8F85A'
            )
            st.plotly_chart(fig)
        # Chart: Net Profit
        with col22:
            fig = bar_creator(
                orientation='h',
                y_values = data.index,
                x_values = data['Net Profit'],
                title = 'Net Profit',
                y_label = 'Company Acronym',
                x_label = 'Amount (in NPR)',
                color = '#5A6EF8'
            )
            st.plotly_chart(fig)
    
    col1, col2 = st.columns([1, 3], gap="small")

    # Business Section:
    with col1:
        st.success("BUSINESS")
        # Chart: Gross Premiums Recieved
        fig = bar_creator(
            orientation='h',
            x_values = data['Gross Earned Premiums'],
            y_values = data.index,
            title='Gross Earned Premiums',
            x_label = 'Earned Premiums (in NPR)',
            y_label = 'Company Acronym',
            color = '#C65AF8'
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.success("EXPENSE")
        col21, col22 = st.columns([1, 1], gap="small")
        # Chart: Claim Expense Ratio
        with col21:
            claim_expense_ratio = data['Net Claims and Benefits Paid'] / data['Gross Earned Premiums']
            fig = bar_creator(
                orientation = 'v',
                x_values = data.index,
                y_values = claim_expense_ratio,
                title = 'Claim Expense Ratio',
                x_label = 'Company Acronym',
                y_label = 'Claim Expense Ratio',
                color = '#5AF8D1'
            )
            st.plotly_chart(fig, use_container_width=True)
        # Chart: Expense Ratio
        with col22: 
            expense_ratio = data['Operating Expense'] / data['Gross Earned Premiums']
            fig = bar_creator(
                x_values = data.index,
                y_values = expense_ratio,
                title = 'Expense Ratio',
                x_label = 'Company Acronym',
                color = '#F8AA5A'
            )
            st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns([2, 1], gap="small")
    # Growth Section
    with col1:
        st.success('GROWTH')
        col11, col12 = st.columns([1, 1], gap="small")
        # Chart: First Year Premium growth rate:
        with col11:
            first_year_premium_growth_rate = [-20.97, -10.84, -23.50, -17.60, -17.56, 0, -29.00, -9.32, -38.48, 7.48, -28.94, 41.96, 40.51]
            fig = bar_creator(
                x_values = data.index,
                y_values = first_year_premium_growth_rate,
                title = 'First Year Premium Growth Rate',
                x_label = 'Company Acronym',
                y_label = 'Growth Rate (in %)',
                color = '#DC5AF8'
            )
            st.plotly_chart(fig)
        # Chart: Gross Premium Growth Rate
        with col12:
            gross_premium_growth_rate = [16.67, 4.72, -4.20, 0.58, 18.93, 7.46, 1.50, 17.96, -6.14, 18.46, 10.88, 52.23, 55.04]
            fig = bar_creator(
                x_values = data.index,
                y_values = gross_premium_growth_rate,
                title = 'Gross Premium Growth Rate',
                x_label = 'Company Acronym',
                y_label = 'Growth Rate (in %)',
                color = '#F85ACC'
            )
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.success("SOLVENCY")
        solvency_margin = [473.00, 322.00, 376.20, 416.00, 334.15, 333.38, 221.00, 280.00, 184.00, 277.72, 182.00, 144.00, 177.26]
        fig = bar_creator(
            x_values = data.index,
            y_values = solvency_margin,
            title = 'Solvency Margin',
            x_label = 'Company Acronym',
            y_label = 'Solvency Margin (in %)',
            color = '#BC6DFF'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns([2, 1], gap="small")
    # Reach Section
    with col1:
        st.success("REACH")
        col11, col12 = st.columns([1, 1], gap="small")
        # Chart: Number of Branches
        with col11:
            fig = bar_creator(
                orientation='h',
                y_values = data.index,
                x_values = data['Offices'],
                title = 'Number of Branches',
                y_label = 'Company Acronym',
                x_label = '',
                color = '#F8A55A'
            )
            st.plotly_chart(fig, use_container_width=True)
        # Chart: Number of Agents
        with col12:
            fig = bar_creator(
                orientation='h',
                y_values = data.index,
                x_values = data['Agents'],
                title = 'Number of Agents',
                y_label = 'Company Acronym',
                x_label = '',
                color = '#F8C05A'
            )
            st.plotly_chart(fig, use_container_width=True)
    # Workforce Section
    with col2:
        st.success("WORKFORCE")
        fig = bar_creator(
            orientation='h',
            y_values = data.index,
            x_values = data['Employees'],
            title = 'Number of Employees',
            y_label = 'Company Acronym',
            x_label = '',
            color = '#5AF8B5'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Solvency and Liquidity Section
    col1, col2 = st.columns([1, 1], gap='small')

    # Chart: Solvency Margin