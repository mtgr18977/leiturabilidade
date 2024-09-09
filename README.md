# Análise de Legibilidade de Arquivos Markdown

## Descrição
Este projeto é uma aplicação Streamlit que realiza uma análise avançada de legibilidade em arquivos Markdown. Ele fornece várias métricas de legibilidade, análise de frequência de palavras e recomendações para melhorar a clareza do texto.

## Funcionalidades
- Upload de arquivos Markdown
- Análise de legibilidade usando múltiplas métricas:
  - Flesch Reading Ease
  - Flesch-Kincaid Grade
  - SMOG Index
  - Coleman-Liau Index
  - Automated Readability Index
  - Dale-Chall Readability Score
  - Gunning Fog
  - Linsear Write Formula
- Análise de frequência de palavras (excluindo stop words)
- Visualização gráfica das palavras mais comuns
- Relatório detalhado com interpretações e recomendações
- Valores de referência para cada métrica de legibilidade

## Requisitos
- Python 3.7+
- Streamlit
- textstat
- matplotlib

## Instalação
1. Clone este repositório:
   ```
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso
Para executar a aplicação localmente:

```
streamlit run app.py
```

Acesse a aplicação em seu navegador, geralmente em `http://localhost:8501`.

## Uso no Streamlit Cloud
1. Faça fork deste repositório para sua conta do GitHub.
2. Acesse [Streamlit Cloud](https://streamlit.io/cloud).
3. Crie um novo aplicativo e selecione o repositório forkado.
4. Escolha o arquivo `app.py` como o arquivo principal.
5. Implante o aplicativo.

## Estrutura do Projeto
- `app.py`: O código principal da aplicação Streamlit
- `requirements.txt`: Lista de dependências do projeto
- `README.md`: Este arquivo

## Contribuições
Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests ou abrir issues para sugerir melhorias ou reportar bugs.

## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato
Se você tiver alguma dúvida ou sugestão, por favor, abra uma issue neste repositório.
