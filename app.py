import streamlit as st
from modules.database import init_db
from modules.auth import login_user, register_user, recover_password
from modules.utils import set_ui_style, show_header, show_error, show_success
from modules.admin import admin_dashboard
from modules.quiz import quiz_flow

# 1. Configuration
st.set_page_config(
    page_title="Quiz Educativo",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Initialization
if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

set_ui_style()

# 3. Session State Management
if 'user' not in st.session_state:
    st.session_state.user = None

if 'current_view' not in st.session_state:
    st.session_state.current_view = "Login"

def logout():
    st.session_state.user = None
    st.session_state.current_view = "Login"
    st.rerun()

# 4. Auth Views
def show_auth_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🎓 Quiz Educativo")

        tab_login, tab_register, tab_recovery = st.tabs(["Login", "Registrar", "Recuperar Senha"])

        with tab_login:
            with st.form("login_form"):
                email = st.text_input("E-mail")
                password = st.text_input("Senha", type="password")
                submit = st.form_submit_button("Entrar")

                if submit:
                    user = login_user(email, password)
                    if user:
                        st.session_state.user = user
                        st.success(f"Bem-vindo, {user.name}!")
                        st.rerun()
                    else:
                        show_error("E-mail ou senha incorretos.")

        with tab_register:
            with st.form("register_form"):
                name = st.text_input("Nome Completo")
                email = st.text_input("E-mail (único)")
                password = st.text_input("Senha", type="password")

                st.markdown("**Perguntas de Segurança (para recuperação)**")
                mother_name = st.text_input("Nome da mãe")
                fav_color = st.text_input("Cor preferida")

                submit = st.form_submit_button("Criar Conta")

                if submit:
                    if name and email and password and mother_name and fav_color:
                        success, msg = register_user(name, email, password, mother_name, fav_color)
                        if success:
                            show_success(msg)
                        else:
                            show_error(msg)
                    else:
                        show_error("Preencha todos os campos!")

        with tab_recovery:
            st.write("Esqueceu sua senha? Preencha os dados abaixo.")
            with st.form("recovery_form"):
                email = st.text_input("E-mail cadastrado")
                mother_name = st.text_input("Nome da mãe")
                fav_color = st.text_input("Cor preferida")
                new_password = st.text_input("Nova Senha", type="password")

                submit = st.form_submit_button("Redefinir Senha")

                if submit:
                    success, msg = recover_password(email, mother_name, fav_color, new_password)
                    if success:
                        show_success(msg)
                    else:
                        show_error(msg)

# 5. Main Application Logic
if st.session_state.user is None:
    show_auth_screen()

else:
    # Sidebar
    with st.sidebar:
        st.write(f"👤 **{st.session_state.user.name}**")
        st.write(f"📧 {st.session_state.user.email}")
        role = "Administrador" if st.session_state.user.role == "master" else "Jogador"
        st.caption(f"Perfil: {role}")

        # Calculate Points on Sidebar
        from modules.database import SessionLocal, Answer, Question
        db = SessionLocal()
        # Join query for speed
        total_points = 0
        try:
            # We can't easily join in raw SQL without aliasing in SQLAlchemy core properly,
            # but let's do python side for simplicity as user base is small.
            answers = db.query(Answer).filter(Answer.user_id == st.session_state.user.id, Answer.is_correct == True).all()
            if answers:
                q_ids = [a.question_id for a in answers]
                questions = db.query(Question).filter(Question.id.in_(q_ids)).all()
                phase_weights = {1: 10, 2: 20, 3: 30, 4: 50}
                for q in questions:
                    total_points += phase_weights.get(q.phase, 10)
        except Exception:
            pass
        finally:
            db.close()

        st.metric("Pontos Totais", total_points)
        st.markdown("---")

        menu_options = ["🏠 Início / Quiz"]
        if st.session_state.user.role == "master":
            menu_options.append("🛠️ Painel Master")

        selection = st.radio("Navegação", menu_options)

        st.markdown("---")
        if st.button("Sair"):
            logout()

    # Router
    if selection == "🏠 Início / Quiz":
        quiz_flow()

    elif selection == "🛠️ Painel Master" and st.session_state.user.role == "master":
        admin_dashboard()
