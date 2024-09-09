import streamlit as st
import textstat
import pandas as pd
import markdown
import re
import spacy
import matplotlib.pyplot as plt
from statistics import mean

# Download spaCy model
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def calcular_indices_legibilidade(texto):
    resultados = {
        "Flesch-Kincaid Grade": textstat.flesch_kincaid_grade(texto),
        "Gunning Fog": textstat.gunning_fog(texto),
        "Coleman-Liau Index": textstat.coleman_liau_index(texto),
        "SMOG Index": textstat.smog_index(texto),
        "LIX": textstat.lix(texto),
        "Flesch Reading Ease": textstat.flesch_reading_ease(texto),
        "Dale-Chall Readability Score": textstat.dale_chall_readability_score(texto),
    }
    return pd.DataFrame(list(resultados.items()), columns=['Índice', 'Valor'])

def amostras_de_cem_palavras(texto):
    palavras = re.findall(r'\w+', texto)
    return [palavras[i:i+100] for i in range(0, len(palavras), 100) if i+100 <= len(palavras)]

def calcular_frases_e_silabas_por_cem_palavras(amostra):
    texto_amostra = ' '.join(amostra)
    doc = nlp(texto_amostra)
    numero_de_frases = len(list(doc.sents))
    numero_de_silabas = sum(textstat.syllable_count(token.text) for token in doc)
    return numero_de_frases, numero_de_silabas

def calcular_indice_fry(texto):
    amostras = amostras_de_cem_palavras(texto)
    if len(amostras) < 3:
        raise ValueError("O texto precisa ter pelo menos 300 palavras para uma análise adequada.")
    
    frases_por_cem = []
    silabas_por_cem = []
    
    for amostra in amostras[:3]:
        frases, silabas = calcular_frases_e_silabas_por_cem_palavras(amostra)
        frases_por_cem.append(frases)
        silabas_por_cem.append(silabas)
    
    media_frases = mean(frases_por_cem)
    media_silabas = mean(silabas_por_cem)
    
    return media_frases, media_silabas

def plotar_grafico_fry(silabas_por_100_palavras, frases_por_100_palavras):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    
    niveis_de_leitura = [(4, '4º-5º ano'), (6, '6º-8º ano'), (8, '8º-9º ano'), (10, 'Ensino Médio'), (14, 'Universitário')]
    for nivel, descricao in niveis_de_leitura:
        ax.axhline(y=nivel, color='gray', linestyle='--')
        ax.axvline(x=nivel, color='gray', linestyle='--')
        ax.text(20.5, nivel, descricao, va='center', ha='left', backgroundcolor='w')
        ax.text(nivel, 20.5, descricao, va='bottom', ha='center', backgroundcolor='w', rotation=90)
    
    ax.scatter(silabas_por_100_palavras, frases_por_100_palavras, color='red')
    ax.set_xlabel('Sílabas por 100 palavras')
    ax.set_ylabel('Frases por 100 palavras')
    ax.grid(True)
    
    return fig

st.title('Análise de Legibilidade de Texto')

uploaded_file = st.file_uploader("Escolha um arquivo Markdown", type="md")

if uploaded_file is not None:
    content = uploaded_file.read().decode('utf-8')
    texto = markdown.markdown(content)
    
    st.header('Índices de Legibilidade')
    indices = calcular_indices_legibilidade(texto)
    st.table(indices)
    
    st.header('Gráfico de Fry')
    try:
        media_frases, media_silabas = calcular_indice_fry(texto)
        st.write(f"Média de frases por 100 palavras: {media_frases:.2f}")
        st.write(f"Média de sílabas por 100 palavras: {media_silabas:.2f}")
        
        fig = plotar_grafico_fry(media_silabas, media_frases)
        st.pyplot(fig)
    except ValueError as e:
        st.error(str(e))

st.sidebar.header('Sobre')
st.sidebar.info('Esta aplicação analisa a legibilidade de textos em arquivos Markdown.')
