import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import util
import pickle
import requests
from sklearn.feature_extraction.text import CountVectorizer

# streamlit run app.py

df = pd.read_csv('data.csv')
df.dropna(inplace=True)

lines = df['line']
labels = df['class']

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(lines)

print("Abriu a pagina")

if not util.check_password():
    print("Usuario nao logado")
    st.stop()
    

print("Carregou a pagina")

model = pickle.load(open('./models/DecisionTreeClassifier.pkl', 'rb'))   

st.title('Secret Finder')

url = st.text_input('URL Github')

submit = st.button('Identificar segredos')

#https://raw.githubusercontent.com/LacunaSoftware/PkiSuiteSamples/refs/heads/master/java/springmvc/src/main/resources/application.yml
#https://raw.githubusercontent.com/Lifan1998/GPSHelp-Server/refs/heads/master/src/main/resources/application.yml

if submit:
    response = requests.get(url)
    secrets = False
    for line in list(response.text.split('\n')):
        test = vectorizer.transform([line])
        result = model.predict(test)


        if result[0] == 1:
            if not secrets:
                st.header('Secrets')
            st.code(line)
            secrets = True

    st.header('Code')
    st.code(response.text)

