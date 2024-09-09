import streamlit as st
import textstat
import io

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

else:
    st.info("Por favor, faça o upload de um arquivo Markdown para iniciar a análise.")

st.sidebar.header('Sobre')
st.sidebar.info('Esta aplicação realiza uma análise avançada de legibilidade de arquivos Markdown usando a biblioteca textstat.')
st.sidebar.warning('Nota: Certifique-se de que o arquivo Markdown não contém informações sensíveis antes de fazer o upload.')
