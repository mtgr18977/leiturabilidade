import streamlit as st
import textstat
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

@st.cache_data
def analyze_readability(content):
    # Remover formatação Markdown
    content = content.replace('#', '').replace('*', '').replace('-', '').replace('`', '')
    
    return {
        "Flesch Reading Ease": textstat.flesch_reading_ease(content),
        "Flesch-Kincaid Grade": textstat.flesch_kincaid_grade(content),
        "SMOG Index": textstat.smog_index(content),
        "Coleman-Liau Index": textstat.coleman_liau_index(content),
        "Automated Readability Index": textstat.automated_readability_index(content),
        "Dale-Chall Readability Score": textstat.dale_chall_readability_score(content),
        "Difficult Words": textstat.difficult_words(content),
        "Linsear Write Formula": textstat.linsear_write_formula(content),
        "Gunning Fog": textstat.gunning_fog(content),
        "Text Standard": textstat.text_standard(content)
    }

def interpret_flesch_reading_ease(score):
    if score < 30:
        return "Muito difícil", "Melhor entendido por graduados universitários."
    elif 30 <= score < 50:
        return "Difícil", "Nível universitário."
    elif 50 <= score < 60:
        return "Razoavelmente difícil", "10º a 12º ano."
    elif 60 <= score < 70:
        return "Padrão", "8º e 9º ano."
    elif 70 <= score < 80:
        return "Razoavelmente fácil", "7º ano."
    elif 80 <= score < 90:
        return "Fácil", "6º ano."
    else:
        return "Muito fácil", "5º ano."

@st.cache_data
def get_word_frequency(content):
    words = re.findall(r'\b\w+\b', content.lower())
    # Filtra as stop words
    words = [word for word in words if word not in STOP_WORDS]
    return Counter(words)

def create_word_frequency_chart(word_freq):
    top_words = dict(word_freq.most_common(10))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_words.keys(), top_words.values())
    plt.xticks(rotation=45, ha='right')
    plt.title("Palavras mais comuns (excluindo stop words)")
    plt.xlabel("Palavras")
    plt.ylabel("Frequência")
    plt.tight_layout()
    return fig

def generate_report(results, word_freq):
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
    {', '.join([f"{word} ({count})" for word, count in word_freq.most_common(10)])}

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

def main():
    st.set_page_config(page_title="Análise Avançada de Legibilidade Markdown", layout="wide")

    st.title('Análise Avançada de Legibilidade de Arquivo Markdown')

    uploaded_file = st.file_uploader("Escolha um arquivo Markdown", type="md")

    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Conteúdo do Arquivo")
            st.text_area("", value=content, height=300, disabled=True)
        
        with col2:
            st.subheader("Resultados da Análise")
            results = analyze_readability(content)
            
            col2a, col2b = st.columns(2)
            
            with col2a:
                fre_score = results["Flesch Reading Ease"]
                difficulty, explanation = interpret_flesch_reading_ease(fre_score)
                st.metric("Flesch Reading Ease", f"{fre_score:.2f}")
                st.markdown(f"**Dificuldade:** {difficulty}")
                st.markdown(f"**Interpretação:** {explanation}")
                
                st.metric("Flesch-Kincaid Grade", f"{results['Flesch-Kincaid Grade']:.2f}")
                st.metric("SMOG Index", f"{results['SMOG Index']:.2f}")
                st.metric("Coleman-Liau Index", f"{results['Coleman-Liau Index']:.2f}")
                st.metric("Automated Readability Index", f"{results['Automated Readability Index']:.2f}")
            
            with col2b:
                st.metric("Dale-Chall Readability Score", f"{results['Dale-Chall Readability Score']:.2f}")
                st.metric("Difficult Words", f"{results['Difficult Words']}")
                st.metric("Linsear Write Formula", f"{results['Linsear Write Formula']:.2f}")
                st.metric("Gunning Fog", f"{results['Gunning Fog']:.2f}")
                st.metric("Text Standard", results['Text Standard'])

        st.subheader("Análise de Frequência de Palavras")
        word_freq = get_word_frequency(content)
        
        fig = create_word_frequency_chart(word_freq)
        st.pyplot(fig)

        st.subheader("Palavras mais frequentes")
        top_words = word_freq.most_common(10)
        st.write(", ".join([f"{word} ({count})" for word, count in top_words]))

        st.subheader("Relatório de Análise")
        report = generate_report(results, word_freq)
        st.markdown(report)

    else:
        st.info("Por favor, faça o upload de um arquivo Markdown para iniciar a análise.")

    st.sidebar.header('Sobre')
    st.sidebar.info('Esta aplicação realiza uma análise avançada de legibilidade de arquivos Markdown usando a biblioteca textstat.')
    st.sidebar.warning('Nota: Certifique-se de que o arquivo Markdown não contém informações sensíveis antes de fazer o upload.')

    st.sidebar.header('Valores de Referência')
    st.sidebar.markdown("""
    ### Flesch Reading Ease
    * 90-100: Muito fácil
    * 80-89: Fácil
    * 70-79: Razoavelmente fácil
    * 60-69: Padrão
    * 50-59: Razoavelmente difícil
    * 30-49: Difícil
    * 0-29: Muito difícil

    ### Flesch-Kincaid Grade
    * 1-6: Ensino Fundamental
    * 7-12: Ensino Médio
    * 13-16: Ensino Superior
    * >16: Pós-graduação

    ### SMOG Index
    * 0-6: Ensino Fundamental
    * 7-12: Ensino Médio
    * 13-16: Ensino Superior
    * >16: Pós-graduação

    ### Coleman-Liau Index
    * Similar ao Flesch-Kincaid Grade

    ### Automated Readability Index
    * Similar ao Flesch-Kincaid Grade

    ### Dale-Chall Readability Score
    * 4.9 ou menor: 4º ano ou abaixo
    * 5.0–6.9: 5º-6º ano
    * 7.0–8.9: 7º-8º ano
    * 9.0–9.9: 9º-10º ano
    * 10.0 ou maior: Universitário

    ### Gunning Fog
    * 6: Fácil
    * 8-10: Ideal
    * 12: Aceitável
    * 14-18: Difícil
    * 20+: Muito difícil

    ### Linsear Write Formula
    * 0-5: Ensino Fundamental
    * 6-12: Ensino Médio
    * 13-16: Ensino Superior
    * >16: Pós-graduação
    """)

if __name__ == "__main__":
    main()
