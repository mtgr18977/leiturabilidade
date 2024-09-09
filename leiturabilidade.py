import streamlit as st
import re
import string
from collections import Counter
import io

def count_sentences(text):
    return len(re.findall(r'\w+[.!?][\s\n]', text)) + 1

def count_words(text):
    words = re.findall(r'\w+', text.lower())
    return len(words)

def count_syllables(word):
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

def interpret_fk_grade(fk_grade):
    if fk_grade < 6:
        return "Muito fácil", "Adequado para estudantes do ensino fundamental."
    elif 6 <= fk_grade < 10:
        return "Fácil", "Adequado para estudantes do ensino médio."
    elif 10 <= fk_grade < 14:
        return "Moderado", "Adequado para estudantes universitários."
    else:
        return "Difícil", "Adequado para leitores com nível universitário ou profissional."

st.set_page_config(page_title="Análise de Legibilidade Markdown", layout="wide")

st.title('Análise de Legibilidade de Arquivo Markdown')

uploaded_file = st.file_uploader("Escolha um arquivo Markdown", type="md")

if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Conteúdo do Arquivo")
        st.text_area("", value=content, height=300, disabled=True)
    
    with col2:
        st.subheader("Resultados da Análise")
        results = analyze_text(content)
        
        metrics = ["Número de sentenças", "Número de palavras", "Número de sílabas"]
        averages = ["Média de palavras por sentença", "Média de sílabas por palavra"]
        
        for metric in metrics:
            st.metric(label=metric, value=f"{results[metric]:.0f}")
        
        st.markdown("---")
        
        for avg in averages:
            st.metric(label=avg, value=f"{results[avg]:.2f}")
        
        st.markdown("---")
        
        fk_grade = results["Índice Flesch-Kincaid simplificado"]
        difficulty, explanation = interpret_fk_grade(fk_grade)
        
        st.metric(label="Índice Flesch-Kincaid simplificado", value=f"{fk_grade:.2f}")
        st.markdown(f"**Dificuldade:** {difficulty}")
        st.markdown(f"**Interpretação:** {explanation}")

else:
    st.info("Por favor, faça o upload de um arquivo Markdown para iniciar a análise.")

st.sidebar.header('Sobre')
st.sidebar.info('Esta aplicação realiza uma análise simplificada de legibilidade de arquivos Markdown.')
st.sidebar.warning('Nota: Esta é uma versão simplificada e pode não ser tão precisa quanto ferramentas mais avançadas.')
