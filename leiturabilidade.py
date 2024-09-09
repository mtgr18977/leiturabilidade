import streamlit as st
import re
import string
from collections import Counter

def count_sentences(text):
    # Uma aproximação simples para contar sentenças
    return len(re.findall(r'\w+[.!?][\s\n]', text)) + 1

def count_words(text):
    words = re.findall(r'\w+', text.lower())
    return len(words)

def count_syllables(word):
    # Uma aproximação simples para contar sílabas
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count

def analyze_text(text):
    sentences = count_sentences(text)
    words = count_words(text)
    syllables = sum(count_syllables(word) for word in re.findall(r'\w+', text.lower()))
    
    # Calculando o índice de legibilidade Flesch-Kincaid simplificado
    if words > 0 and sentences > 0:
        flesch_kincaid_grade = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
    else:
        flesch_kincaid_grade = 0
    
    return {
        "Número de sentenças": sentences,
        "Número de palavras": words,
        "Número de sílabas": syllables,
        "Média de palavras por sentença": words / sentences if sentences > 0 else 0,
        "Média de sílabas por palavra": syllables / words if words > 0 else 0,
        "Índice Flesch-Kincaid simplificado": flesch_kincaid_grade
    }

st.title('Análise Simplificada de Legibilidade de Texto')

text_input = st.text_area("Cole seu texto aqui:", height=200)

if st.button('Analisar'):
    if text_input:
        results = analyze_text(text_input)
        
        st.header('Resultados da Análise')
        for metric, value in results.items():
            st.write(f"{metric}: {value:.2f}")
        
        # Interpretação simplificada do índice Flesch-Kincaid
        fk_grade = results["Índice Flesch-Kincaid simplificado"]
        st.header('Interpretação')
        if fk_grade < 6:
            st.write("O texto é muito fácil de ler, adequado para estudantes do ensino fundamental.")
        elif 6 <= fk_grade < 10:
            st.write("O texto é fácil de ler, adequado para estudantes do ensino médio.")
        elif 10 <= fk_grade < 14:
            st.write("O texto é de dificuldade moderada, adequado para estudantes universitários.")
        else:
            st.write("O texto é difícil de ler, adequado para leitores com nível universitário ou profissional.")
    else:
        st.error("Por favor, insira algum texto para análise.")

st.sidebar.header('Sobre')
st.sidebar.info('Esta aplicação realiza uma análise simplificada de legibilidade de textos.')
st.sidebar.warning('Nota: Esta é uma versão simplificada e pode não ser tão precisa quanto ferramentas mais avançadas.')
