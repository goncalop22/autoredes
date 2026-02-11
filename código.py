import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração da Página
st.set_page_config(page_title="OCR de Topologia", layout="wide")
st.title("🖼️ De Foto para Configuração de Rede")
st.markdown("Faça upload de um desenho (quadro branco ou digital) e receba o config inicial.")

# Sidebar para API Key
with st.sidebar:
    api_key = st.text_input("Insira sua Gemini API Key:", type="password")
    st.info("Obtenha sua chave em: https://aistudio.google.com/")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Modelo rápido e eficiente para visão

    uploaded_file = st.file_uploader("Escolha a imagem da topologia...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Topologia Carregada', use_column_width=True)
        
        btn_gerar = st.button("🚀 Gerar Configurações")

        if btn_gerar:
            with st.spinner('Analisando topologia e gerando comandos...'):
                # O Prompt "Mágico" para o Vision
                prompt = """
                Analise esta imagem de topologia de rede. 
                1. Identifique todos os dispositivos (Routers, Switches, PCs).
                2. Identifique as conexões entre eles.
                3. Se houver IPs escritos, use-os. Se não, atribua IPs genéricos (ex: 192.168.1.0/24).
                4. Gere um script de configuração básica de Cisco IOS para cada dispositivo identificado.
                Inclua: Hostname, configuração de interfaces e uma rota estática ou RIP simples para conectividade.
                Formate a saída com títulos claros para cada equipamento.
                """
                
                try:
                    response = model.generate_content([prompt, image])
                    
                    st.success("Configurações Geradas!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
else:
    st.warning("Por favor, insira a API Key no menu lateral para começar.")
