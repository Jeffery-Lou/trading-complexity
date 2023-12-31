
import numpy as np
import akshare as ak
import pandas as pd
import streamlit as st
import altair as alt

@st.cache
def load_data():
    industry_summary= ak.stock_board_industry_summary_ths()
    return industry_summary
def main():
    
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
        
    industry_summary = st.session_state.data
    percent = industry_summary['涨跌幅']
    industry_summary = industry_summary.iloc[:,[1,4,5,6,7]]
    industry_summary['成交额占比'] = industry_summary['总成交额']/industry_summary['总成交额'].sum()*100
    industry_summary['板块上涨比例']=industry_summary['上涨家数']/(industry_summary['上涨家数']+industry_summary['下跌家数'])*100
    industry_summary['涨跌幅']=percent

    st.header("General Viewing")

    with st.expander("Full Data"):
        st.dataframe(industry_summary)
    col1,col2 = st.columns(2)
    columns = col1.selectbox('select columns',industry_summary.columns[1:])
    col2.button("Refresh",on_click=load_data)
    chart = alt.Chart(industry_summary).mark_bar().encode(
    x=columns+':Q',
    y=alt.Y('板块:N', sort='-x'),
    text=alt.Text(columns+":Q")
    ).properties(width=800)
    text = chart.mark_text(align='left', dx=2)
    st.altair_chart(chart+text)

if __name__ == '__main__':
    main()
