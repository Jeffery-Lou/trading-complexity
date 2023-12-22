import sys
import subprocess
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'akshare'])

import numpy as np
import akshare as ak
import pandas as pd
import streamlit as st

@st.cache_data
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
    industry_summary = industry_summary.set_index('板块')
    industry_summary = industry_summary.sort_values(by=['成交额占比'],ascending=[False])

    st.header("General Viewing")

    with st.expander("Full Data"):
        st.dataframe(industry_summary)
    col1,col2 = st.columns(2)
    columns = col1.selectbox('select columns',industry_summary.columns)
    st.bar_chart(industry_summary[columns])

if __name__ == '__main__':
    main()
