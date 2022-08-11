#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import os
import pandas as pd
#from st_aggrid import AgGrid
import seaborn as sns
import pydeck as pdk
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FixedTicker
from random import randrange


# =============================================================================
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)
# =============================================================================


st.session_state.tectSettingsPath = '/Users/dominik/Documents/GitHub/GeoROC/data/'
st.session_state.tectSettingsPath = 'data/'

st.session_state.el = pd.read_csv(st.session_state.tectSettingsPath + 'Archean Cratons/Bastar Craton.csv').columns[27:160]

st.session_state.tectSettingsFolder = os.listdir(st.session_state.tectSettingsPath)
st.session_state.tectSettings=[]
for i in st.session_state.tectSettingsFolder:
    if os.path.isdir(st.session_state.tectSettingsPath + i):
        st.session_state.tectSettings.append(i)

#---------------------------------#
#------ Welcome  -----------------#
#---------------------------------#  
def welcome():
    st.header('Welcome to GeoROC Viewer')
    st.write("The world's most advanced data viewer")
    
    

#---------------------------------#
#------ Scatter Plots  -----------#
#---------------------------------#  
def scatterplots():
    st.sidebar.header('all cool')
    st.sidebar.info('This is a purely informational message')
    st.sidebar.success('This is a success message!')
    
    col1, col2 = st.columns(2)
    
    with col1:
        tectSettingsFolder = st.selectbox('sel', st.session_state.tectSettings)
        tectSettingsContent = os.listdir(st.session_state.tectSettingsPath + tectSettingsFolder)
    
        xAxisScatterData = st.selectbox('x-axis', st.session_state.el)
        yAxisScatterData = st.selectbox('y-axis', st.session_state.el)
    
    with col2:
        fig = figure(width=600, height=400)
        
        selLatLonList=[]
        labelList = []
        for file in tectSettingsContent:
            if file.endswith('.csv'):
                singleTectSetting = st.session_state.tectSettingsPath + tectSettingsFolder + '/' + file
            readTectSetting = pd.read_csv(singleTectSetting)
            selLatLon = readTectSetting[['Latitude (Min)', 'Longitude (Min)']]
            selLatLon = selLatLon.rename(columns={'Latitude (Min)':'lat', 'Longitude (Min)':'lon'})
            randColor = [randrange(255), randrange(255), randrange(255)]
            layers = pdk.Layer(
                'ScatterplotLayer',
                   selLatLon,
                   pickable=True,
                   opacity=0.8,
                   stroked=True,
                   filled=True,
                   radius_scale=6,
                   radius_min_pixels=5,
                   radius_max_pixels=100,
                   line_width_min_pixels=1,
                   get_position='[lon, lat]',
                   get_radius="exits_radius",
                   get_fill_color=randColor,
                   get_line_color=[0, 0, 0],
            )
            selLatLonList.append(layers)
            fig.circle(readTectSetting[xAxisScatterData]/10000, readTectSetting[yAxisScatterData]/10000, color=tuple(randColor))
            fig.xaxis.axis_label = xAxisScatterData + ' wt%'
            fig.yaxis.axis_label = yAxisScatterData + ' wt%'
            labelList.append(file)
            
            
        st.bokeh_chart(fig)
            
    st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=50.110924,
                longitude=8.682127,
                zoom=1,
                height=500,
                width=800
            ),
            layers=selLatLonList,
        ))
        
    
    
    st.write(labelList)
    

#---------------------------------#
#------ Paired Plots  ------------#
#---------------------------------#  
def paired_plots():
    #import seaborn as sns

    st.sidebar.header('all cool')
    st.sidebar.info('This is a purely informational message')
    st.sidebar.success('This is a success message!')
    
    tectSettingsFolder = st.selectbox('sel', st.session_state.tectSettings)
    tectSettingsContent = os.listdir(st.session_state.tectSettingsPath + tectSettingsFolder)
    
    xAxisScatterData = st.multiselect('x-axis', st.session_state.el, ['Mg', 'Si', 'Ca', 'Al'])

    for file in tectSettingsContent:
        if file.endswith('.csv'):
            singleTectSetting = st.session_state.tectSettingsPath + tectSettingsFolder + '/' + file
        readTectSetting = pd.read_csv(singleTectSetting)
    
    data = readTectSetting[xAxisScatterData].dropna()
    #penguins = sns.load_dataset("penguins")
    
    fig = sns.pairplot(data/10000)#, hue='category')
    st.pyplot(fig)
    
    

#---------------------------------#
#------ REE  ---------------------#
#---------------------------------#  
def REE():
    tectSettingsFolder = st.selectbox('sel', st.session_state.tectSettings)
    tectSettingsContent = os.listdir(st.session_state.tectSettingsPath + tectSettingsFolder)
    incl_lines = st.checkbox('include lines')
    
    for file in tectSettingsContent:
        if file.endswith('.csv'):
            singleTectSetting = st.session_state.tectSettingsPath + tectSettingsFolder + '/' + file
        readTectSetting = pd.read_csv(singleTectSetting)
        
    
    #readTectSetting.dropna(inplace=True)  # Drop rows with missing attributes
    #readTectSetting.drop_duplicates(inplace=True)  # Remove duplicates
    
    # Drop all the column I don't use for now

    el = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    ci = [2,2,2,2,2,2,2,2,2,2,2,2,2,2000]
    data = readTectSetting[el]
    dataT = readTectSetting[el].T
    
    

    fig = figure(width=600, height=400, y_axis_type='log')
    nr_of_el = range(len(el))

    for i in nr_of_el:
        fig.circle(i, data[el[i]]/ci[i])
    
    if incl_lines == True: 
        for i in range(dataT.shape[1]):
            fig.line(nr_of_el, dataT[i])
    
    fig.xaxis.ticker = FixedTicker(ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
    fig.xaxis.major_label_overrides = {0:'La', 1:'Ce', 2:'Pr', 3:'Nd', 4:'Sm', 5:'Eu', 6:'Gd', 7:'Tb', 8:'Dy', 9:'Ho', 10:'Er', 11:'Tm', 12:'Yb', 13:'Lu'}
    
    st.bokeh_chart(fig)
    

#---------------------------------#
#------ d  --------------------#
#---------------------------------#
def d():
    st.write('Cosmochemistry Papers')

    import streamlit.components.v1 as components

    # embed streamlit docs in a streamlit app

    components.iframe("https://cosmochemistry-papers.com", width=800, height=1000, scrolling=True)
    

#---------------------------------#
#------ Test  --------------------#
#---------------------------------#
def test():
    from bokeh.layouts import column, row
    from bokeh.models import CustomJS, Select
    from bokeh.plotting import ColumnDataSource, figure
    import numpy as np
    import altair as alt
    import pandas as pd

    dfData = pd.read_table('data/2022-01-27 B JB MC AG_20220128-104636/001_A.exp', header=22).loc[21:199][:]
    dfData

    
    chart_data = dfData['Time']

    st.line_chart(dfData['10B'])
    
    
          

    dfData.iloc[21][:]
    #indexgroup
    #dfplotdata = dfData.loc[21:220][:]
    #dfplotdata
    #index1 = dfplotdata.iloc[0][:]
    #index1
    #indexgroup
    #dfplotdata.set_index(index1) 
    #dfplotdata.columns('Time')
    #dfplotdata1 = dfplotdata.str.split(' ')
     
    #dfplotdata1[20]
    #columns[27:]
    
#---------------------------------#
#------ Main Page Sidebar --------#
#---------------------------------#  

st.sidebar.image('https://raw.githubusercontent.com/Hezel2000/GeoROC/main/images/Goethe-Logo.jpg', width=150)

page_names_to_funcs = {
    'Welcome': welcome,
    'Data Reading': scatterplots,
    'Baseline Selection': paired_plots,
    'Correction': REE,
    'plot results': d,
    'test': test

}

demo_name = st.sidebar.radio("Select your Visualisation", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()


link = '[Back to Geoplatform](http://www.geoplatform.de)'
st.sidebar.markdown(link, unsafe_allow_html=True)