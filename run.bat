@echo off
echo Iniciando o Jogo Philipe...
start "" "http://localhost:8501"
.venv\Scripts\python.exe -m streamlit run app_streamlit.py --server.headless false