import streamlit as st
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def cadastrar_usuario(nome, cpf, data_nascimento):
    url = f"{BASE_URL}/usuarios"
    payload = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento
    }
    response = requests.post(url, json=payload)
    return response

def listar_bicicletas():
    url = f"{BASE_URL}/bikes"
    response = requests.get(url)
    return response.json().get("bicicletas", [])

def realizar_emprestimo(id_usuario, id_bike):
    url = f"{BASE_URL}/emprestimos/usuarios/{id_usuario}/bikes/{id_bike}"
    response = requests.post(url)
    return response

def main():
    st.title("Cadastro de Usuário e Empréstimo de Bicicletas")

    st.header("Cadastrar Usuário")
    
    if 'id_usuario' not in st.session_state:
        st.session_state.id_usuario = None

    with st.form("cadastro_usuario"):
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        data_nascimento = st.date_input("Data de Nascimento", min_value=datetime(1900, 1, 1))
        submitted = st.form_submit_button("Cadastrar")

        if submitted:
            response = cadastrar_usuario(nome, cpf, data_nascimento.strftime('%Y-%m-%d'))
            if response.status_code == 201:
                st.success("Usuário cadastrado com sucesso!")
                response_data = response.json()
                st.session_state.id_usuario = response_data.get("id") 
            else:
                st.error(f"Erro: {response.json().get('erro', 'Erro desconhecido')}")

    if st.session_state.id_usuario:
        st.header("Escolher Bicicleta para Empréstimo")
        bicicletas = listar_bicicletas()
        if bicicletas:
            ids_bicicletas = [bici['_id'] for bici in bicicletas]
            opcoes_bicicletas = [f"ID: {bici['_id']} | Marca: {bici['marca']} | Modelo: {bici['modelo']}" for bici in bicicletas]
            
            indice_bicicleta = st.selectbox("Escolha uma bicicleta", range(len(opcoes_bicicletas)), format_func=lambda x: opcoes_bicicletas[x])
            
            confirmar_emprestimo = st.button("Realizar Empréstimo")
            
            if confirmar_emprestimo:
                id_bike_selecionada = ids_bicicletas[indice_bicicleta]
                
                st.write(f"ID do usuário: {st.session_state.id_usuario}, ID da bicicleta: {id_bike_selecionada}")

                emprestimo_response = realizar_emprestimo(st.session_state.id_usuario, id_bike_selecionada)
                
                if emprestimo_response.status_code == 201:
                    st.success("Empréstimo realizado com sucesso!")
                else:
                    st.error(f"Erro ao realizar empréstimo: {emprestimo_response.json().get('message', 'Erro desconhecido')}")
                    st.write(emprestimo_response.json())
        else:
            st.info("Nenhuma bicicleta disponível no momento.")

if __name__ == "__main__":
    main()