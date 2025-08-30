import bcrypt
import streamlit as st

def generate_hash(password: str) -> bytes:
    """
    Gera um hash seguro para uma senha usando bcrypt.
    """
    # Adiciona um "sal" aleatório e gera o hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password

def main():
    """
    Interface Streamlit para gerar hashes de senhas.
    """
    st.set_page_config(
        page_title="Gerador de Hash de Senha",
        layout="centered"
    )

    st.title("🔐 Gerador de Hash de Senha")
    st.warning(
        "Esta é uma ferramenta de utilidade para o administrador. "
        "Use-a para gerar hashes seguros para as senhas dos usuários. "
        "**Nunca armazene senhas em texto plano!**"
    )

    st.markdown(
        """
        **Como usar:**
        1.  Digite a senha que deseja 'hashear' no campo abaixo.
        2.  Clique no botão 'Gerar Hash'.
        3.  Copie o hash gerado.
        4.  Armazene este hash em suas variáveis de ambiente ou segredos do Streamlit
            (por exemplo, `SENHA_ADMIN`, `SENHA_GESTOR`).
        """
    )

    password = st.text_input("Digite a senha para gerar o hash", type="password")

    if st.button("Gerar Hash"):
        if password:
            hashed_password = generate_hash(password)
            st.success("Hash gerado com sucesso!")
            # O hash é uma sequência de bytes, então decodificamos para exibição
            st.code(hashed_password.decode("utf-8"), language="text")
            st.info("Copie este hash e atualize suas variáveis de ambiente ou segredos.")
        else:
            st.error("Por favor, digite uma senha.")

if __name__ == "__main__":
    main()
