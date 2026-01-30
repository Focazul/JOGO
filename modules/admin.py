import streamlit as st
import pandas as pd
from .database import SessionLocal, User, KnowledgeBase, Question, Phase, Answer
from .utils import show_success, show_error

def admin_dashboard():
    st.title("👑 Painel Administrativo")

    tabs = st.tabs([
        "📚 Banco de Conhecimento",
        "❓ Gerenciamento de Perguntas",
        "🔓 Controle de Fases",
        "📊 Estatísticas",
        "🗑️ Gerenciamento de Usuários"
    ])

    with tabs[0]:
        manage_knowledge_base()

    with tabs[1]:
        manage_questions()

    with tabs[2]:
        manage_phases()

    with tabs[3]:
        show_statistics()

    with tabs[4]:
        manage_users()

# --- Tab 1: Banco de Conhecimento ---
def manage_knowledge_base():
    st.header("Banco de Conhecimento")

    db = SessionLocal()
    kb_list = db.query(KnowledgeBase).all()

    mode = st.radio("Modo", ["Adicionar Novo", "Editar/Excluir Existente"], horizontal=True, key="kb_mode")

    if mode == "Adicionar Novo":
        with st.form("add_kb_form"):
            theme = st.text_input("Tema")
            content = st.text_area("Conteúdo (Texto Base)")
            phase = st.number_input("Fase", min_value=1, max_value=4, step=1)
            difficulty = st.selectbox("Dificuldade", ["Fácil", "Médio", "Difícil", "Muito Difícil"])
            submitted = st.form_submit_button("Salvar")

            if submitted:
                if theme and content:
                    try:
                        kb = KnowledgeBase(theme=theme, content=content, phase=phase, difficulty=difficulty)
                        db.add(kb)
                        db.commit()
                        show_success("Conteúdo adicionado!")
                    except Exception as e:
                        show_error(f"Erro: {e}")
                else:
                    show_error("Preencha todos os campos obrigatórios.")

    else: # Edit Mode
        if not kb_list:
            st.info("Nenhum conteúdo cadastrado.")
        else:
            kb_options = {f"{kb.theme} (Fase {kb.phase}) - ID {kb.id}": kb.id for kb in kb_list}
            selected_label = st.selectbox("Selecione o Conteúdo", list(kb_options.keys()))
            selected_id = kb_options[selected_label]

            kb_to_edit = db.query(KnowledgeBase).filter(KnowledgeBase.id == selected_id).first()

            if kb_to_edit:
                with st.form("edit_kb_form"):
                    theme = st.text_input("Tema", value=kb_to_edit.theme)
                    content = st.text_area("Conteúdo (Texto Base)", value=kb_to_edit.content)
                    phase = st.number_input("Fase", min_value=1, max_value=4, step=1, value=kb_to_edit.phase)

                    diff_opts = ["Fácil", "Médio", "Difícil", "Muito Difícil"]
                    try:
                        diff_index = diff_opts.index(kb_to_edit.difficulty)
                    except:
                        diff_index = 0
                    difficulty = st.selectbox("Dificuldade", diff_opts, index=diff_index)

                    col1, col2 = st.columns(2)
                    with col1:
                        update = st.form_submit_button("Atualizar")
                    with col2:
                        delete = st.form_submit_button("Excluir", type="primary")

                    if update:
                        kb_to_edit.theme = theme
                        kb_to_edit.content = content
                        kb_to_edit.phase = phase
                        kb_to_edit.difficulty = difficulty
                        db.commit()
                        show_success("Conteúdo atualizado!")
                        st.rerun()

                    if delete:
                        db.delete(kb_to_edit)
                        db.commit()
                        show_success("Conteúdo excluído!")
                        st.rerun()

    db.close()

# --- Tab 2: Gerenciamento de Perguntas ---
def manage_questions():
    st.header("Gerenciamento de Perguntas")

    db = SessionLocal()
    questions = db.query(Question).all()

    # Validation Display
    counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for q in questions:
        if q.phase in counts:
            counts[q.phase] += 1

    st.subheader("Validação de Fases")
    cols = st.columns(4)
    for i in range(1, 5):
        count = counts[i]
        with cols[i-1]:
            st.metric(f"Fase {i}", f"{count}/15")
            if count == 15:
                st.caption("✅ Completa")
            elif count < 15:
                st.caption(f"⚠️ Faltam {15 - count}")
            else:
                st.caption(f"🚫 Excesso ({count})")

    st.markdown("---")

    mode = st.radio("Modo", ["Adicionar Nova", "Editar/Excluir Existente"], horizontal=True, key="q_mode")

    if mode == "Adicionar Nova":
        with st.form("add_q_form"):
            question_text = st.text_area("Enunciado")
            col1, col2 = st.columns(2)
            with col1:
                opt_a = st.text_input("Alternativa A")
                opt_b = st.text_input("Alternativa B")
            with col2:
                opt_c = st.text_input("Alternativa C")
                opt_d = st.text_input("Alternativa D")

            correct = st.selectbox("Correta", ["A", "B", "C", "D"])
            phase = st.number_input("Fase", min_value=1, max_value=4, step=1, key="add_q_phase")
            difficulty = st.selectbox("Dificuldade", ["Fácil", "Médio", "Difícil", "Muito Difícil"], key="add_q_diff")

            submitted = st.form_submit_button("Salvar Pergunta")

            if submitted:
                if question_text and opt_a and opt_b and opt_c and opt_d:
                    options_map = {"A": opt_a, "B": opt_b, "C": opt_c, "D": opt_d}
                    correct_text = options_map[correct]

                    try:
                        q = Question(
                            question=question_text,
                            option_a=opt_a,
                            option_b=opt_b,
                            option_c=opt_c,
                            option_d=opt_d,
                            correct_option=correct_text,
                            phase=phase,
                            difficulty=difficulty
                        )
                        db.add(q)
                        db.commit()
                        show_success("Pergunta adicionada!")
                        st.rerun()
                    except Exception as e:
                        show_error(f"Erro: {e}")
                else:
                    show_error("Preencha todos os campos.")

    else: # Edit Mode
        # Filter logic to help find question
        filter_phase = st.selectbox("Filtrar por Fase", [1, 2, 3, 4, "Todas"], key="q_filter")

        filtered_qs = [q for q in questions if filter_phase == "Todas" or q.phase == filter_phase]

        if not filtered_qs:
            st.info("Nenhuma pergunta encontrada.")
        else:
            q_options = {f"[F{q.phase}] {q.question[:50]}... (ID: {q.id})": q.id for q in filtered_qs}
            selected_label = st.selectbox("Selecione a Pergunta", list(q_options.keys()))
            selected_id = q_options[selected_label]

            q_to_edit = db.query(Question).filter(Question.id == selected_id).first()

            if q_to_edit:
                with st.form("edit_q_form"):
                    question_text = st.text_area("Enunciado", value=q_to_edit.question)
                    col1, col2 = st.columns(2)
                    with col1:
                        opt_a = st.text_input("Alternativa A", value=q_to_edit.option_a)
                        opt_b = st.text_input("Alternativa B", value=q_to_edit.option_b)
                    with col2:
                        opt_c = st.text_input("Alternativa C", value=q_to_edit.option_c)
                        opt_d = st.text_input("Alternativa D", value=q_to_edit.option_d)

                    # Reverse engineer 'correct' selection (A, B, C or D)
                    current_correct_char = "A" # default
                    if q_to_edit.correct_option == q_to_edit.option_a: current_correct_char = "A"
                    elif q_to_edit.correct_option == q_to_edit.option_b: current_correct_char = "B"
                    elif q_to_edit.correct_option == q_to_edit.option_c: current_correct_char = "C"
                    elif q_to_edit.correct_option == q_to_edit.option_d: current_correct_char = "D"

                    correct = st.selectbox("Correta", ["A", "B", "C", "D"], index=["A","B","C","D"].index(current_correct_char))

                    phase = st.number_input("Fase", min_value=1, max_value=4, step=1, value=q_to_edit.phase)

                    diff_opts = ["Fácil", "Médio", "Difícil", "Muito Difícil"]
                    try:
                        diff_index = diff_opts.index(q_to_edit.difficulty)
                    except:
                        diff_index = 0
                    difficulty = st.selectbox("Dificuldade", diff_opts, index=diff_index)

                    col1, col2 = st.columns(2)
                    with col1:
                        update = st.form_submit_button("Atualizar")
                    with col2:
                        delete = st.form_submit_button("Excluir", type="primary")

                    if update:
                        options_map = {"A": opt_a, "B": opt_b, "C": opt_c, "D": opt_d}
                        correct_text = options_map[correct]

                        q_to_edit.question = question_text
                        q_to_edit.option_a = opt_a
                        q_to_edit.option_b = opt_b
                        q_to_edit.option_c = opt_c
                        q_to_edit.option_d = opt_d
                        q_to_edit.correct_option = correct_text
                        q_to_edit.phase = phase
                        q_to_edit.difficulty = difficulty

                        db.commit()
                        show_success("Pergunta atualizada!")
                        st.rerun()

                    if delete:
                        db.delete(q_to_edit)
                        db.commit()
                        show_success("Pergunta excluída!")
                        st.rerun()

    db.close()

# --- Tab 3: Controle de Fases ---
def manage_phases():
    st.header("Controle de Fases")
    st.info("Aqui você pode liberar ou bloquear o acesso às fases para todos os usuários.")

    db = SessionLocal()
    phases = db.query(Phase).all()

    for p in phases:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Fase {p.phase_number}")
        with col2:
            status = "🔓 Liberada" if p.is_unlocked else "🔒 Bloqueada"
            if st.button(f"Alternar ({status})", key=f"phase_{p.phase_number}"):
                p.is_unlocked = not p.is_unlocked
                db.commit()
                st.rerun()
    db.close()

# --- Tab 4: Estatísticas ---
def show_statistics():
    st.header("Estatísticas Gerais")

    db = SessionLocal()

    # Load data into Pandas
    users_df = pd.read_sql(db.query(User).statement, db.bind)
    answers_df = pd.read_sql(db.query(Answer).statement, db.bind)
    db.close()

    # KPI 1: Total Users
    total_users = len(users_df[users_df['role'] != 'master'])
    st.metric("Total de Usuários (Comuns)", total_users)

    if answers_df.empty:
        st.warning("Sem dados de respostas ainda.")
        return

    col1, col2 = st.columns(2)

    # KPI 2: Global Success Rate
    success_rate = (answers_df['is_correct'].sum() / len(answers_df)) * 100
    with col1:
        st.metric("Taxa de Acerto Global", f"{success_rate:.2f}%")

    # KPI 3: Avg Time
    # Check if column exists (handling legacy schema just in case, though we updated it)
    if 'duration_seconds' in answers_df.columns:
        avg_time = answers_df['duration_seconds'].mean()
        with col2:
            st.metric("Tempo Médio de Resposta", f"{avg_time:.1f} segundos")

    # Chart 1: Answers per User (Top 10)
    st.subheader("Top 10 Usuários Mais Ativos")
    if not users_df.empty:
        # Merge to get names
        merged = answers_df.merge(users_df, left_on='user_id', right_on='id', suffixes=('_ans', '_usr'))
        active_users = merged['name'].value_counts().head(10)
        st.bar_chart(active_users)

    # Chart 2: Correct vs Incorrect
    st.subheader("Acertos vs Erros")
    correct_counts = answers_df['is_correct'].value_counts()
    correct_counts.index = ['Incorreto', 'Correto']
    st.bar_chart(correct_counts)

    # Ranking Logic (Points Weighted)
    st.subheader("Ranking (Pontos Acumulados)")

    # We need to calculate points, which requires joining Question table to get phases
    # Let's do a more complex query or dataframe merge
    if not answers_df.empty:
        # Load Questions to get phases
        questions_df = pd.read_sql(db.query(Question).statement, db.bind)

        # Merge Answers with Questions
        # answers_df has 'question_id', questions_df has 'id'
        full_df = answers_df.merge(questions_df, left_on='question_id', right_on='id', suffixes=('_ans', '_q'))

        # Merge with Users
        full_df = full_df.merge(users_df, left_on='user_id', right_on='id', suffixes=('_x', '_user'))

        # Filter correct only
        correct_df = full_df[full_df['is_correct'] == True].copy()

        # Apply weights
        phase_weights = {1: 10, 2: 20, 3: 30, 4: 50}
        correct_df['points'] = correct_df['phase'].map(phase_weights).fillna(10)

        # Group by User Name
        ranking = correct_df.groupby('name')['points'].sum().sort_values(ascending=False).head(10)
        st.table(ranking)

# --- Tab 5: Usuários ---
def manage_users():
    st.header("Gerenciamento de Usuários")

    db = SessionLocal()
    users = db.query(User).filter(User.role != 'master').all()

    for u in users:
        with st.expander(f"{u.name} ({u.email})"):
            st.write(f"Status: {'Ativo' if u.active else 'Bloqueado'}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Bloquear/Desbloquear", key=f"block_{u.id}"):
                    u.active = not u.active
                    db.commit()
                    st.rerun()
            with col2:
                if st.button("🗑️ Excluir Usuário", key=f"del_user_{u.id}"):
                    # Delete answers first
                    db.query(Answer).filter(Answer.user_id == u.id).delete()
                    db.delete(u)
                    db.commit()
                    st.rerun()

            # Show progress
            user_answers = db.query(Answer).filter(Answer.user_id == u.id).count()
            user_correct = db.query(Answer).filter(Answer.user_id == u.id, Answer.is_correct == True).count()
            st.write(f"Respostas: {user_answers} | Acertos: {user_correct}")

    db.close()
