#(c) Nickolai Knyazev 2021
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import SessionState
from datetime import datetime
from datetime import timedelta
import os
import math
import random
import streamlit as st
import json
import geopandas as gpd
import pydeck as pdk

import pyproj
import plotly.graph_objs as go
st.set_page_config(layout="wide")
import pickle
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

state = SessionState.get(x=0)

#@st.cache(allow_output_mutation=True)
def load_pandas_df(file):
    df = pd.read_csv(file)
    if "df_gr_all" in file:
        df.set_index(pd.to_datetime(df["Date"]), inplace=True)
    if "whole_table" in file:
        df.set_index(pd.to_datetime(df["Time"]), inplace=True)
    return df


#@st.cache(allow_output_mutation=True)
def load_pickle(file):
    with open(file,"rb") as f:
        return pickle.load(f)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
pogoda = load_pickle("pogoda.pkl")
pogoda["lng"] = pogoda.lon

tcol1, _, tcol2 = st.beta_columns([10,1,10])

st.header("Анализ")
def_date= pd.to_datetime('2020-07-01 00:00:00')
hcol1, hcol2 = st.beta_columns([1,1])
with hcol1:
    def_date = st.date_input("Выберете дату", value=def_date, min_value= pd.to_datetime('2020-06-01 00:00:00'), max_value= pd.to_datetime('2020-12-15 00:00:00'))
    treshold = st.slider('Минимальная вероятность ',value=30,min_value=0, max_value=100, step=1)#, format="DD HH")
    treshold /=100
def_date=pd.to_datetime(def_date)
pogoda["check"] = pogoda["winddirection"].apply(lambda x: random.randint(0,255))

DATA_URL = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/housing.csv"
#df = pd.read_csv(DATA_URL)
#df = check_df[:10]

# tooltip = {
#     "html": "<b>{mrt_distance}</b> meters away from an MRT station, costs <b>{price_per_unit_area}</b> NTD/sqm",
#     "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
# }


#st.text( r.to_html().data)
#st.write(r.to_html().data, unsafe_allow_html=False)
         #"column_layer.html")

    
# you can select which traitlets keys it observes
import streamlit.components.v1 as components




# >>> import plotly.express as px
# >>> fig = px.box(range(10))
# >>> fig.write_html('test.html')

HtmlFile = open("column_layer.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
#print(source_code)
#components.html(r.to_html(filename=None, open_browser=False, notebook_display=None, iframe_width='100%', iframe_height=1500, as_string=True, offline=False),               height=350)import streamlit as st

features_dict = load_pickle("features_dict.pkl")
ft_ids = {v:k for k,v in features_dict.items()}


ft_len = len(features_dict)

    
import colorsys


colors = load_pickle("colors.pkl")# _get_colors(ft_len)
color_dict={}
#st.write("<font bgcolor=rgb(249, 201, 16)>THIS TEXT WILL BE RED</font>", unsafe_allow_html=True)
oblast_list = load_pickle("oblast_list.pkl")


    
with hcol2:

    risks = st.multiselect(
     'Выберите риски',
    list(ft_ids.values()),
 list(ft_ids.values())[-5:])
layers = []


cont = st.beta_container()
oblast = st.selectbox(
     'Выберете область',
    sorted(oblast_list),
    index=3
)

col1, _,col2 = st.beta_columns([15,1,15])
#st.text(check_df.loc[oblast])



avarii1 = load_pickle("avarii1.pkl")
with col1:
    st.header("       Текущая ситуация                                   ")
    hist_range = st.slider('За сколько дней выводить данные ',value=5,min_value=0, max_value=30, step=1)#, format="DD HH")
  
    st.write( avarii1[(avarii1.date_dt<def_date)&(avarii1.date_dt>def_date-timedelta(days=hist_range))&(avarii1.oblast==oblast)][["причина","why","data"]].rename(
    
    columns={"why":"описание"}
    ).reset_index(drop=True))
with col2:
    st.header("                      Прогноз")
    forecast = st.slider('На сколько дней строить прогноз ',value=5,min_value=0, max_value=30, step=1)#, format="DD HH")
    predictor = load_pickle("predictor.pkl")
    pred_datset= predictor.got_dataset(def_date,forecast,where=oblast_list)
    cont_col2 = st.beta_container()


    with cont:
        test_df = load_pickle("test_df.pkl")
        #check_df = pogoda[(pogoda.datetime_d == def_date)&(pogoda.lon<60)&(pogoda.lat<60)&(pogoda.lon>40)&(pogoda.lat>40)]
        check_df= pred_datset #test_df
        check_df = check_df[(check_df.lon<90)&(check_df.lat<90)&(check_df.lon>20)&(check_df.lat>20)]
        df=check_df

        df["lng"] = df["lon"]
        df["tmplng"] = df.lng
        df["tmplat"] = df.lat
        # for i in ft_ids.keys():
        #     check_df["risk"+str(i)].loc[check_df["risk"+str(i)]<0.5] =0

        check_df["text"] = check_df.index + "\n"
        for k in ft_ids.keys():
            color_dict[k] = colors[k]

            old_text =  check_df["text"].copy()
            check_df["text"]+=" ".join(ft_ids[k].split(" ")[:2])
            str_col = (check_df["risk"+str(k)]*100).astype(int).astype(str)
            check_df["text"]+=" "+str_col
           # str((check_df["risk"+str(k)]*100).astype(int))
            check_df["text"]+="% \n "
            check_df.loc[check_df["risk"+str(k)]<treshold,"text"]=old_text.loc[check_df["risk"+str(k)]<treshold]

with tcol1:
    st.markdown('<p style="background-color:#FF0000;color:#00000;font-weight:bold;font-size:26px;font-family:"IBM Plex Sans", sans-serif;border-radius:2%;">Происходит сейчас</style> </p>',
         unsafe_allow_html=True)
    ex = st.beta_expander(label=check_df.index[8], expanded=False)
    with ex:
        
        k=5
        st.markdown('<p style="background-color:RGB({},{},{});color:#000000;font-weight:bold;font-size:14px;font-family:"IBM Plex Sans", sans-serif;border-radius:2%;"> {}</style> Источник: внутренний, телефон +79161234567 </p>'.format( color_dict[k][0]*255,color_dict[k][1]*255,color_dict[k][2]*255, ft_ids[k]),
         unsafe_allow_html=True)
        if st.button("Перейти",key=0):
            oblast=check_df.index[8]
        
    ex = st.beta_expander(label=check_df.index[17], expanded=False)
    with ex:
        
        k=3
        st.markdown('<p style="background-color:RGB({},{},{});color:#000000;font-weight:bold;font-size:14px;font-family:"IBM Plex Sans", sans-serif;border-radius:2%;"> {}</style> Источник: внутренний, телефон +79161234567 </p>'.format( color_dict[k][0]*255,color_dict[k][1]*255,color_dict[k][2]*255, ft_ids[k]),
         unsafe_allow_html=True)
        if st.button("Перейти",key=1):
            oblast=check_df.index[17]
                
with tcol2:
    st.markdown('<p style="background-color:#FFDD00;color:#00000;font-weight:bold;font-size:26px;font-family:"IBM Plex Sans", sans-serif;border-radius:2%;">Прогноз на ближайшие 3 дня</style> </p>',
         unsafe_allow_html=True)
    ex = st.beta_expander(label=check_df.index[16], expanded=False)
    with ex:
        
        k=2
        st.markdown('<p style="background-color:RGB({},{},{});color:#000000;font-weight:bold;font-size:14px;font-family:"IBM Plex Sans", sans-serif;border-radius:2%;"> {}</style> Источник: внутренний, телефон +79161234567 </p>'.format( color_dict[k][0]*255,color_dict[k][1]*255,color_dict[k][2]*255, ft_ids[k]),
         unsafe_allow_html=True)
        if st.button("Перейти",key=2):
            oblast=check_df.index[16]
        
    ex = st.beta_expander(label=check_df.index[2], expanded=False)
    with ex:
        
        k=4
        st.markdown('<p style="background-color:RGB({},{},{});color:#000000;font-weight:bold;font-size:14px;font-family:"IBM Plex Sans", sans-serif;border-radius:2%;"> {}</style> Источник: внутренний, телефон +79161234567 </p>'.format( color_dict[k][0]*255,color_dict[k][1]*255,color_dict[k][2]*255, ft_ids[k]),
         unsafe_allow_html=True)
        if st.button("Перейти",key=3):
            oblast=check_df.index[2]
                

            
#with tcol2:
   # k = 7
    #st.markdown('''div.stButton > button:first-child {background-color: red;color:green;font-size:20px;height:3em;width:30em;border-radius:10px 10px 10px 10px;}''', unsafe_allow_html=True)
    
    #if st.button(oblast_list[3]):
    #    oblast_to_view = oblast_list[5]
        #st.write(“content you want to show”)
            
            #st.write(df)
layers=[]
for i,risk in enumerate(risks):
    df["tmp_view"+str(i)] = df["risk"+str(features_dict[risk])]*150000 + 1000
    
    st.write(str(features_dict[risk])+" "+str(risk)+str(df["tmp_view"+str(i)]) ) #str([c*255 for c in color_dict[int(features_dict[risk])]]))#,df["risk"+str(i)])
    shv = 0.125
    if i==1:
        df["tmplng"] = df.lng + shv*2
    elif i==2:
        df["tmplng"] = df.lng - shv*2
    elif i==3:
        df["tmplat"] = df.lat + shv*2
    elif i==4:
        df["tmplat"] = df.lat - shv*2
    elif i==5:
        df["tmplng"] = df.lng + shv
        df["tmplat"] = df.lat - shv

    elif i==6:
        df["tmplng"] = df.lng - shv
        df["tmplat"] = df.lat + shv        
    elif i==7:
        df["tmplng"] = df.lng + shv
        df["tmplat"] = df.lat + shv         
    elif i==8:
        df["tmplng"] = df.lng - shv
        df["tmplat"] = df.lat - shv            
    layers.append(pdk.Layer(
    "ColumnLayer",
    data=df.loc[df["risk"+str(i)]>treshold].copy(),
    get_position=["tmplng", "tmplat"],
    get_elevation= ["tmp_view"+str(i)],#["risk"+str(features_dict[risk])],
    elevation_scale=1,
    get_fill_color=[c*255 for c in color_dict[int(features_dict[risk])]],
        extrudet = False,
        stroke=True,

    radius=8000,
    pickable=True
     )#,
   # auto_highlight=True,
    )
with cont:
    view = pdk.data_utils.compute_view(df[["lng", "lat"]])
    view.pitch = 75
    view.bearing = 60
    
    view_state = pdk.ViewState(
        longitude=check_df.loc[oblast].lon,
        latitude=check_df.loc[oblast].lat,
        zoom=4,
        min_zoom=2,
        max_zoom=15,
        pitch=40.5,
        bearing=0)

    r = pdk.Deck(
        layers,
        initial_view_state=view_state,
        #tooltip=tooltip,
        #map_provider="mapbox",
        map_style=pdk.map_styles.LIGHT,
        #pdk.map_styles.SATELLITE,
        tooltip={"text": "{text}"},
        height=100
    )
    st.pydeck_chart(r)
with cont_col2:
    for i,k in enumerate(list(ft_ids.keys())[::-1]):

        st.markdown('<p style="background-color:RGB({},{},{});color:#000000;font-weight:bold;font-size:14px;font-family:"IBM Plex Sans", sans-serif;border-radius:2%;">{}</style> вероятность {}% </p>'.format( color_dict[k][0]*255,color_dict[k][1]*255,color_dict[k][2]*255, ft_ids[k],
        int(check_df.loc[oblast]["risk"+str(k)]*100)), unsafe_allow_html=True)
        
        
        


