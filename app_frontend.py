import streamlit as st
import requests

st.set_page_config(page_title="WEG RAG Assistant", page_icon="⚙️")

st.title("⚙️ WEG Technical Assistant")
st.markdown("---")

API_URL = "http://localhost:8000"

with st.sidebar:
    st.header("Upload de Manuais")
    uploaded_files = st.file_uploader(
        "Selecione os manuais (PDF)", type="pdf", accept_multiple_files=True
    )

    if st.button("Indexar Documentos"):
        if uploaded_files:
            files = [
                ("files", (f.name, f.getvalue(), "application/pdf"))
                for f in uploaded_files
            ]
            with st.spinner("Processando..."):
                res = requests.post(f"{API_URL}/documents", files=files)
                if res.status_code == 200:
                    st.success(f"Indexado: {res.json()['total_chunks']} chunks.")
        else:
            st.error("Selecione um arquivo!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ex: Qual a potência do motor?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando manuais..."):
            response = requests.post(f"{API_URL}/question", json={"question": prompt})
            if response.status_code == 200:
                data = response.json()
                answer = data["answer"]
                refs = "\n\n**Fontes:**\n" + "\n".join(
                    [f"- {r}" for r in data["references"]]
                )

                full_res = f"{answer}{refs}"
                st.markdown(full_res)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_res}
                )
