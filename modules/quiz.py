import streamlit as st
import random
import time
from .database import SessionLocal, Question, Answer, Phase

def quiz_flow():
    user = st.session_state.user

    # 1. Determine Global Phase Status
    db = SessionLocal()
    phases_config = {p.phase_number: p.is_unlocked for p in db.query(Phase).all()}

    # 2. Determine User Progress
    # Get all answers for this user
    user_answers = db.query(Answer).filter(Answer.user_id == user.id).all()
    answered_ids = [a.question_id for a in user_answers]

    # Check progress per phase
    current_phase = 1
    phase_score = 0
    phase_total_qs = 0

    # Logic: Iterate phases 1 to 4.
    # If phase is not completed (some questions remain) -> This is current phase.
    # If phase completed -> Check if passed -> Go to next.
    # If locked globally -> Stop.

    # Fetch all questions to map them
    all_questions = db.query(Question).all()
    qs_by_phase = {1: [], 2: [], 3: [], 4: []}
    for q in all_questions:
        qs_by_phase[q.phase].append(q)

    db.close()

    active_phase = None

    for p in range(1, 5):
        if not phases_config.get(p, False):
            # Phase locked globally
            if active_phase is None:
                st.info(f"A Fase {p} está bloqueada temporariamente pelo administrador.")
                return
            break

        phase_qs = qs_by_phase[p]
        phase_qs_ids = [q.id for q in phase_qs]

        # Answers for this phase
        answered_in_phase = [aid for aid in answered_ids if aid in phase_qs_ids]

        if len(answered_in_phase) < len(phase_qs):
            # User hasn't finished this phase
            active_phase = p
            break
        else:
            # User finished this phase. Check score?
            # For now, let's assume if finished, they move on.
            # Calculate score just for display?
            pass

    if active_phase is None:
        st.success("🎉 Parabéns! Você completou todas as fases disponíveis!")
        st.balloons()
        return

    # Show Quiz for Active Phase
    play_phase(active_phase, qs_by_phase[active_phase], answered_ids)

def play_phase(phase_num, questions, answered_ids):
    st.header(f"🚀 Fase {phase_num}")

    # Filter remaining
    remaining = [q for q in questions if q.id not in answered_ids]

    total = len(questions)
    completed = total - len(remaining)
    progress = completed / total if total > 0 else 0

    st.progress(progress)
    st.caption(f"Progresso: {completed}/{total}")

    if not remaining:
        st.write("Fase concluída!")
        return

    # Pick next question (random or sequential?)
    # Random is better for variety
    # But Streamlit reruns. We need to stabilize the current question.
    # We can use session_state to store the 'current_question_id' until answered.

    if 'current_q_id' not in st.session_state or st.session_state.current_q_id not in [q.id for q in remaining]:
        st.session_state.current_q_id = random.choice(remaining).id
        st.session_state.q_start_time = time.time()

    # Get the question object
    current_q = next(q for q in remaining if q.id == st.session_state.current_q_id)

    with st.container():
        st.subheader(f"Questão: {current_q.question}")
        st.write(f"Dificuldade: {current_q.difficulty}")

        # Form to hold state
        with st.form("quiz_form"):
            # Options shuffle
            # To persist shuffle we might need state, but let's just show them in order A-D or fixed list
            # The DB has opt_a...opt_d.
            options = [
                ("A", current_q.option_a),
                ("B", current_q.option_b),
                ("C", current_q.option_c),
                ("D", current_q.option_d)
            ]
            # If we want to shuffle presentation, we can, but we need to map back to the 'option_a' text or key.
            # For simplicity, let's present them as is.

            choice = st.radio("Escolha a alternativa correta:", options, format_func=lambda x: f"{x[0]}) {x[1]}")

            submit = st.form_submit_button("Responder")

            if submit:
                duration = int(time.time() - st.session_state.get('q_start_time', time.time()))

                # choice is tuple ('A', 'Text')
                selected_text = choice[1]
                # Check correctness
                # correct_option stored in DB could be 'A' or the text. In admin.py I stored the TEXT.

                is_correct = (selected_text == current_q.correct_option)

                if is_correct:
                    st.success("✅ Resposta Correta!")
                    time.sleep(1)
                else:
                    st.error(f"❌ Incorreto! A resposta era: {current_q.correct_option}")
                    time.sleep(2)

                # Save to DB
                db = SessionLocal()
                try:
                    ans = Answer(
                        user_id=st.session_state.user.id,
                        question_id=current_q.id,
                        selected_option=selected_text,
                        is_correct=is_correct,
                        duration_seconds=duration
                    )
                    db.add(ans)
                    db.commit()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
                finally:
                    db.close()

                # Clear current q from state to pick new one
                del st.session_state.current_q_id
                if 'q_start_time' in st.session_state:
                    del st.session_state.q_start_time
                st.rerun()
