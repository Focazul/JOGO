import streamlit as st
import random
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
import hashlib
import os

# Database setup
default_sqlite = "sqlite:///./educational_app.db"
if os.getenv("VERCEL"):
    default_sqlite = "sqlite:////tmp/educational_app.db"

URL_DATABASE = os.getenv("DATABASE_URL", default_sqlite)

connect_args = {}
if URL_DATABASE.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

if URL_DATABASE.startswith("postgres://"):
    URL_DATABASE = URL_DATABASE.replace("postgres://", "postgresql://", 1)

engine = create_engine(URL_DATABASE, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_master = Column(Boolean, default=False)
    results = relationship("Result", back_populates="user")

class Knowledge(Base):
    __tablename__ = 'knowledge'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    question = Column(String)
    answer = Column(String)
    distractor1 = Column(String)
    distractor2 = Column(String)
    distractor3 = Column(String)

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    score = Column(Integer)
    total_questions = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="results")

# Auth with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        # Fallback to old SHA-256 hash for compatibility
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password):
    return pwd_context.hash(password)

# Create tables
Base.metadata.create_all(bind=engine)

# Create master user if not exists
db = SessionLocal()
master = db.query(User).filter(User.username == "Master").first()
if not master:
    master_hash = get_password_hash("master123")
    master_user = User(username="Master", password_hash=master_hash, is_master=True)
    db.add(master_user)
    db.commit()

# Create test user if not exists
test_user = db.query(User).filter(User.username == "teste").first()
if not test_user:
    test_hash = get_password_hash("teste")
    test_user_obj = User(username="teste", password_hash=test_hash, is_master=False)
    db.add(test_user_obj)
    db.commit()

# Insert sample knowledge if none exists
knowledge_count = db.query(Knowledge).count()
if knowledge_count == 0:
    sample_knowledge = [
        ("Conhecimento sobre: Qual é a capital do Brasil?", "Qual é a capital do Brasil?", "Brasília", "Rio de Janeiro", "São Paulo", "Salvador"),
        ("Conhecimento sobre: Quem escreveu \"Dom Quixote\"?", "Quem escreveu \"Dom Quixote\"?", "Miguel de Cervantes", "William Shakespeare", "Dante Alighieri", "Homero"),
        ("Conhecimento sobre: Qual é o maior planeta do Sistema Solar?", "Qual é o maior planeta do Sistema Solar?", "Júpiter", "Saturno", "Marte", "Terra"),
        ("Conhecimento sobre: Em que ano o homem pisou na Lua?", "Em que ano o homem pisou na Lua?", "1969", "1965", "1972", "1957"),
        ("Conhecimento sobre: Qual é o símbolo químico do ouro?", "Qual é o símbolo químico do ouro?", "Au", "Ag", "Fe", "Cu"),
        ("Conhecimento sobre: Quem pintou a Mona Lisa?", "Quem pintou a Mona Lisa?", "Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Michelangelo"),
        ("Conhecimento sobre: Qual é o rio mais longo do mundo?", "Qual é o rio mais longo do mundo?", "Rio Amazonas", "Rio Nilo", "Rio Yangtze", "Rio Mississipi"),
        ("Conhecimento sobre: Quantos continentes existem?", "Quantos continentes existem?", "7", "5", "6", "8"),
        ("Conhecimento sobre: Qual é a moeda do Japão?", "Qual é a moeda do Japão?", "Iene", "Won", "Yuan", "Dólar"),
        ("Conhecimento sobre: Quem descobriu a penicilina?", "Quem descobriu a penicilina?", "Alexander Fleming", "Louis Pasteur", "Robert Koch", "Edward Jenner"),
        ("Conhecimento sobre: Qual é o maior oceano do mundo?", "Qual é o maior oceano do mundo?", "Oceano Pacífico", "Oceano Atlântico", "Oceano Índico", "Oceano Ártico"),
        ("Conhecimento sobre: Em que país fica a Torre Eiffel?", "Em que país fica a Torre Eiffel?", "França", "Itália", "Espanha", "Reino Unido"),
        ("Conhecimento sobre: Qual é o número atômico do carbono?", "Qual é o número atômico do carbono?", "6", "8", "12", "14"),
        ("Conhecimento sobre: Quem foi o primeiro presidente dos Estados Unidos?", "Quem foi o primeiro presidente dos Estados Unidos?", "George Washington", "Thomas Jefferson", "Abraham Lincoln", "John Adams"),
        ("Conhecimento sobre: Qual é a linguagem de programação mais usada?", "Qual é a linguagem de programação mais usada?", "Python", "Java", "C++", "JavaScript"),
        ("Conhecimento sobre: Qual é o maior deserto do mundo?", "Qual é o maior deserto do mundo?", "Deserto do Saara", "Deserto de Gobi", "Deserto da Arábia", "Deserto da Antártida"),
        ("Conhecimento sobre: Quem escreveu \"1984\"?", "Quem escreveu \"1984\"?", "George Orwell", "Aldous Huxley", "Ray Bradbury", "Isaac Asimov"),
        ("Conhecimento sobre: Qual é a velocidade da luz?", "Qual é a velocidade da luz?", "299.792.458 m/s", "300.000.000 m/s", "150.000.000 m/s", "200.000.000 m/s"),
        ("Conhecimento sobre: Em que ano começou a Primeira Guerra Mundial?", "Em que ano começou a Primeira Guerra Mundial?", "1914", "1912", "1916", "1939"),
        ("Conhecimento sobre: Qual é o metal mais abundante na crosta terrestre?", "Qual é o metal mais abundante na crosta terrestre?", "Alumínio", "Ferro", "Cobre", "Zinco"),
        ("Conhecimento sobre: Quem foi o autor de \"A Origem das Espécies\"?", "Quem foi o autor de \"A Origem das Espécies\"?", "Charles Darwin", "Gregor Mendel", "Carl Linnaeus", "Alfred Wallace"),
        ("Conhecimento sobre: Qual é a capital da Austrália?", "Qual é a capital da Austrália?", "Camberra", "Sydney", "Melbourne", "Perth"),
        ("Conhecimento sobre: Quantos ossos tem o corpo humano adulto?", "Quantos ossos tem o corpo humano adulto?", "206", "208", "210", "204"),
        ("Conhecimento sobre: Qual é o maior mamífero do mundo?", "Qual é o maior mamífero do mundo?", "Baleia Azul", "Elefante", "Girafa", "Hipopótamo"),
        ("Conhecimento sobre: Quem inventou a lâmpada elétrica?", "Quem inventou a lâmpada elétrica?", "Thomas Edison", "Nikola Tesla", "Alexander Graham Bell", "Benjamin Franklin"),
        ("Conhecimento sobre: Qual é o país com mais habitantes?", "Qual é o país com mais habitantes?", "China", "Índia", "Estados Unidos", "Indonésia"),
        ("Conhecimento sobre: Em que ano foi fundada a ONU?", "Em que ano foi fundada a ONU?", "1945", "1942", "1948", "1950"),
        ("Conhecimento sobre: Qual é o gás mais abundante na atmosfera terrestre?", "Qual é o gás mais abundante na atmosfera terrestre?", "Nitrogênio", "Oxigênio", "Argônio", "Dióxido de carbono"),
        ("Conhecimento sobre: Quem foi o primeiro homem a orbitar a Terra?", "Quem foi o primeiro homem a orbitar a Terra?", "Yuri Gagarin", "John Glenn", "Alan Shepard", "Neil Armstrong"),
        ("Conhecimento sobre: Qual é a unidade de medida da energia?", "Qual é a unidade de medida da energia?", "Joule", "Newton", "Watt", "Volt")
    ]
    for content, question, answer, d1, d2, d3 in sample_knowledge:
        k = Knowledge(content=content, question=question, answer=answer, distractor1=d1, distractor2=d2, distractor3=d3)
        db.add(k)
    db.commit()

db.close()

st.set_page_config(page_title="Jogo Philipe", layout="centered")

def login_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and verify_password(password, user.password_hash):
        st.session_state.user = {"id": user.id, "username": user.username, "is_master": user.is_master}
        print(f"Login successful for {username}")
        return True
    print(f"Login failed for {username}")
    return False

def register_user(username, password):
    db = SessionLocal()
    if db.query(User).filter(User.username == username).first():
        db.close()
        return False
    hashed = get_password_hash(password)
    user = User(username=username, password_hash=hashed)
    db.add(user)
    db.commit()
    db.close()
    return True

def logout():
    if 'user' in st.session_state:
        del st.session_state.user

def get_quiz_questions():
    db = SessionLocal()
    questions = db.query(Knowledge).filter(Knowledge.question != None).all()
    db.close()
    random.shuffle(questions)
    questions = questions[:10]  # Limit to 10 random questions
    quiz_data = []
    for q in questions:
        options = [q.answer, q.distractor1, q.distractor2, q.distractor3]
        random.shuffle(options)
        quiz_data.append({
            'id': q.id,
            'question': q.question,
            'options': options,
            'correct': q.answer
        })
    return quiz_data

@st.cache_data
def get_memory_cards():
    db = SessionLocal()
    items = db.query(Knowledge).filter(Knowledge.content != None).all()
    db.close()
    cards = []
    for item in items:
        cards.append({'id': item.id, 'content': item.content, 'match_id': item.id})
        cards.append({'id': item.id, 'content': item.content, 'match_id': item.id})  # Par
    random.shuffle(cards)
    return cards

def save_result(score, total):
    if 'user' not in st.session_state:
        return
    db = SessionLocal()
    result = Result(user_id=st.session_state.user['id'], score=score, total_questions=total)
    db.add(result)
    db.commit()
    db.close()

def add_knowledge(content, question, answer, d1, d2, d3):
    db = SessionLocal()
    k = Knowledge(content=content, question=question, answer=answer, distractor1=d1, distractor2=d2, distractor3=d3)
    db.add(k)
    db.commit()
    db.close()

# Menu
if 'user' in st.session_state:
    menu = ["Logout", "Dashboard", "Quiz", "Jogo da Memória", "Resultados"]
    if st.session_state.user['is_master']:
        menu.append("Admin")
    default_index = 1  # Dashboard
else:
    menu = ["Login", "Registrar"]
    default_index = 0  # Login

escolha = st.sidebar.selectbox("Menu", menu, index=default_index)

# Sidebar user info
if 'user' in st.session_state:
    st.sidebar.write(f"**Usuário:** {st.session_state.user['username']}")
    if st.session_state.user['is_master']:
        st.sidebar.write("**Tipo:** Mestre")
    else:
        st.sidebar.write("**Tipo:** Jogador")

if escolha == "Logout":
    logout()
    st.rerun()

elif escolha == "Dashboard":
    if 'user' not in st.session_state:
        st.error("Faça login primeiro.")
    else:
        st.header(f"Bem-vindo, {st.session_state.user['username']}!")
        st.write("Escolha uma atividade no menu lateral.")
        # Show recent results
        db = SessionLocal()
        recent_results = db.query(Result).filter(Result.user_id == st.session_state.user['id']).order_by(Result.timestamp.desc()).limit(5).all()
        db.close()
        if recent_results:
            st.subheader("Últimos Resultados")
            for r in recent_results:
                st.write(f"Quiz: {r.score}/{r.total_questions} - {r.timestamp.strftime('%d/%m/%Y %H:%M')}")
        else:
            st.write("Nenhum resultado ainda. Jogue um quiz!")

elif escolha == "Login":
    st.header("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        print(f"Tentando login com usuário: {username}")
        if login_user(username, password):
            st.success("Login realizado!")
            print(f"Login realizado para {username}, user in session: {st.session_state.get('user')}")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
            print(f"Login falhou para {username}")

elif escolha == "Registrar":
    st.header("Registrar")
    username = st.text_input("Novo usuário")
    password = st.text_input("Nova senha", type="password")
    if st.button("Registrar"):
        if register_user(username, password):
            st.success("Usuário registrado!")
        else:
            st.error("Usuário já existe.")

elif escolha == "Quiz":
    if 'user' not in st.session_state:
        st.error("Faça login primeiro.")
    else:
        st.header("Quiz")
        if 'quiz_questions' not in st.session_state:
            st.session_state.quiz_questions = get_quiz_questions()
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_selected = None

        questions = st.session_state.quiz_questions
        if st.session_state.quiz_index < len(questions):
            q = questions[st.session_state.quiz_index]
            progress = (st.session_state.quiz_index) / len(questions)
            st.progress(progress)
            st.write(f"Pergunta {st.session_state.quiz_index + 1} de {len(questions)}")
            st.subheader(q['question'])
            
            # Use columns for options
            cols = st.columns(2)
            selected = None
            for i, option in enumerate(q['options']):
                with cols[i % 2]:
                    if st.button(option, key=f"q{st.session_state.quiz_index}_{i}"):
                        selected = option
            
            if selected:
                st.session_state.quiz_selected = selected
                if selected == q['correct']:
                    st.success("Correto!")
                    st.session_state.quiz_score += 1
                else:
                    st.error(f"Incorreto! A resposta certa é: {q['correct']}")
                st.session_state.quiz_index += 1
                st.rerun()
        else:
            st.write(f"Quiz terminado! Pontuação: {st.session_state.quiz_score}/{len(questions)}")
            save_result(st.session_state.quiz_score, len(questions))
            if st.button("Reiniciar"):
                del st.session_state.quiz_questions
                st.rerun()

elif escolha == "Jogo da Memória":
    if 'user' not in st.session_state:
        st.error("Faça login primeiro.")
    else:
        st.header("Jogo da Memória")
        if 'memory_cards' not in st.session_state:
            st.session_state.memory_cards = get_memory_cards()
            st.session_state.flipped = []
            st.session_state.solved = []
            st.session_state.disabled = False

        cards = st.session_state.memory_cards
        cols = st.columns(4)
        for i, card in enumerate(cards):
            with cols[i % 4]:
                if i in st.session_state.solved or i in st.session_state.flipped:
                    st.button(card['content'], disabled=True, key=f"card{i}")
                else:
                    if st.button("?", key=f"card{i}") and not st.session_state.disabled:
                        st.session_state.flipped.append(i)
                        if len(st.session_state.flipped) == 2:
                            st.session_state.disabled = True
                            c1 = cards[st.session_state.flipped[0]]
                            c2 = cards[st.session_state.flipped[1]]
                            if c1['match_id'] == c2['match_id']:
                                st.session_state.solved.extend(st.session_state.flipped)
                                st.session_state.flipped = []
                                st.session_state.disabled = False
                            else:
                                st.session_state.flipped = []
                                st.session_state.disabled = False
                        st.rerun()

        if len(st.session_state.solved) == len(cards):
            st.success("Parabéns! Você venceu!")
            if st.button("Reiniciar"):
                del st.session_state.memory_cards
                st.rerun()

elif escolha == "Resultados":
    if 'user' not in st.session_state:
        st.error("Faça login primeiro.")
    else:
        st.header("Resultados")
        db = SessionLocal()
        results = db.query(Result).filter(Result.user_id == st.session_state.user['id']).all()
        db.close()
        for r in results:
            st.write(f"Score: {r.score}/{r.total_questions} em {r.timestamp}")

elif escolha == "Admin":
    if 'user' not in st.session_state or not st.session_state.user['is_master']:
        st.error("Acesso negado.")
    else:
        st.header("Administração - Adicionar Conhecimentos")
        with st.form("add_knowledge"):
            content = st.text_area("Conteúdo (para Jogo da Memória)")
            question = st.text_input("Pergunta (para Quiz)")
            answer = st.text_input("Resposta correta")
            distractor1 = st.text_input("Opção incorreta 1")
            distractor2 = st.text_input("Opção incorreta 2")
            distractor3 = st.text_input("Opção incorreta 3")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                if content or question:
                    add_knowledge(content, question, answer, distractor1, distractor2, distractor3)
                    st.success("Conhecimento adicionado com sucesso!")
                else:
                    st.error("Preencha pelo menos o conteúdo ou a pergunta.")
