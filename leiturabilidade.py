import streamlit as st
import textstat
import io
from collections import Counter
import matplotlib.pyplot as plt
import re

# Lista de stop words em inglês
STOP_WORDS = set([
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were',
    'will', 'with', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
    'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
    'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',
    'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
    'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
    'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
    'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
    "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
])

def analyze_readability(content):
    # Função de análise de legibilidade (mantida como estava)
    ...

def interpret_flesch_reading_ease(score):
    # Função de interpretação do Flesch Reading Ease (mantida como estava)
    ...

def get_word_frequency(content, top_n=10):
    words = re.findall(r'\b\w+\b', content.lower())
    # Filtra as stop words
    words = [word for word in words if word not in STOP_WORDS]
    return Counter(words).most_common(top_n)

def plot_word_frequency(word_freq):
    words, counts = zip(*word_freq)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(words, counts)
    plt.xticks(rotation=45, ha='right')
    plt.title("Palavras mais comuns (excluindo stop words)")
    plt.xlabel("Palavras")
    plt.ylabel("Frequência")
    plt.tight_layout()
    return fig

def generate_report(results, word_freq):
    # Atualizar o relatório para mencionar a exclusão de stop words
    report = f"""
    # Relatório de Análise de Legibilidade

    ## Resumo
    O texto analisado tem um nível de legibilidade {interpret_flesch_reading_ease(results['Flesch Reading Ease'])[0].lower()}, 
    com uma pontuação Flesch Reading Ease de {results['Flesch Reading Ease']:.2f}. 
    Isso significa que o texto é mais adequado para {interpret_flesch_reading_ease(results['Flesch Reading Ease'])[1]}

    ## Métricas Detalhadas
    - Flesch-Kincaid Grade: {results['Flesch-Kincaid Grade']:.2f}
    - SMOG Index: {results['SMOG Index']:.2f}
    - Coleman-Liau Index: {results['Coleman-Liau Index']:.2f}
    - Automated Readability Index: {results['Automated Readability Index']:.2f}
    - Dale-Chall Readability Score: {results['Dale-Chall Readability Score']:.2f}
    - Gunning Fog: {results['Gunning Fog']:.2f}

    ## Complexidade do Vocabulário
    - Número de palavras difíceis: {results['Difficult Words']}
    - Padrão de texto: {results['Text Standard']}

    ## Palavras mais comuns (excluindo stop words)
    {', '.join([f"{word} ({count})" for word, count in word_freq])}

    ## Recomendações
    Baseado nestes resultados, considere:
    1. {
    "Simplificar o vocabulário e a estrutura das frases" if results['Flesch Reading Ease'] < 60 else 
    "Manter o atual nível de complexidade, que é adequado para o público-alvo" if 60 <= results['Flesch Reading Ease'] < 80 else
    "Possivelmente aumentar a complexidade se o público-alvo for mais avançado"
    }
    2. {
    "Reduzir o comprimento das frases para melhorar a clareza" if results['Gunning Fog'] > 12 else
    "Manter o atual comprimento das frases, que está em um bom nível" if 10 <= results['Gunning Fog'] <= 12 else
    "Considerar frases um pouco mais longas ou complexas se apropriado para o público"
    }
    3. Revisar o uso frequente das palavras mais comuns (excluindo stop words) e considerar variações para enriquecer o vocabulário, se apropriado.
    """
    return report

# O resto do código Streamlit permanece o mesmo
...
