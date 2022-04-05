import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
import spacy
from spacy.lang.pt import Portuguese
from collections import Counter
import re
from PIL import Image


st.set_page_config(page_title="My App",layout='wide')
st.title("Reviews Positivas e Negativas ao Longo do Tempo")

df = pd.read_csv("ReviewsAlongTime.csv")

x = list(df["Date"])
y1 = list(df["Count_Pos_Reviews"])
y2 = list(df["Count_Neg_Reviews"])
y = np.array(list(zip(y1,y2)))


def update_data(x, y1, y2, a_date):
  if (len(a_date) == 1):
    a_date = list((a_date[0], datetime.date(2023,1,1)))
  if (len(a_date) == 2):
    new_x, new_y1, new_y2 = [], [], []
    for index, element in enumerate(x):
      if (np.datetime64(element) >= np.datetime64(a_date[0]) and np.datetime64(element) <= np.datetime64(a_date[1])):
        new_x.append(element)
        new_y1.append(y1[index])
        new_y2.append(y2[index])
    x = new_x
    y1 = new_y1
    y2 = new_y2
  return (x, y1, y2)
    

min_date = datetime.datetime(2019,10,8)
max_date = datetime.date(2023,1,1)
a_date = list(st.date_input("Selecione um intervalo:", (min_date, max_date)))


source = pd.DataFrame({
  'Datas': update_data(x, y1, y2, a_date)[0],
  'Contagem de Reviews Positivas': update_data(x, y1, y2, a_date)[1]
})

source2 = pd.DataFrame({
  'Datas': update_data(x, y1, y2, a_date)[0],
  'Contagem de Reviews Negativas': update_data(x, y1, y2, a_date)[2]
})

graphic1 = alt.Chart(source).mark_line(color="green").encode(
    x='Datas',
    y='Contagem de Reviews Positivas'
)

graphic2 = alt.Chart(source2).mark_line(color="red").encode(
    x='Datas',
    y='Contagem de Reviews Negativas',
)


st.header("Contagem de Reviews Positivas no Tempo")
st.altair_chart(graphic1 , use_container_width=False)
st.header("Contagem de Reviews Negativas no Tempo")
st.altair_chart(graphic2 , use_container_width=False)

st.title("Review Positiva Mais Representativa")
st.write('A Echo Dot é ótima pra quem busca uma “facilidade” no seu dia-a-dia, como por exemplo ligar a luz do quarto, claro se você tiver a lâmpada inteligente ou então usa-la para saber clima, despertador ou para ouvir música. Recomendo bastante, ainda mais se tiver com um preço bem interessante.')

st.title("Review Negativa Mais Representativa")
st.write('Muitas das vezes ela diz que não entende o que quero dizer, mesmo pedindo uma coisa muito simples.A parte de configurar rotinas é interessante.A integração com spotify não consegui fazer funcionar, então não tenho como pedir músicas pra ela.Precisa melhorar muito ainda.')

st.title("Word Cloud")
image = Image.open('word_cloud.png')
st.image(image, caption='Word Cloud')