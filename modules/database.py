from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
import os
import bcrypt

# Database Setup
DB_NAME = "educational_app.db"
# Use absolute path for sqlite to avoid issues
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
URL_DATABASE = f"sqlite:///{DB_PATH}"

engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    mother_name = Column(String, nullable=True) # Used for recovery
    favorite_color = Column(String, nullable=True) # Used for recovery
    role = Column(String, default="user") # 'master' or 'user'
    active = Column(Boolean, default=True)

    answers = relationship("Answer", back_populates="user")

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'

    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    phase = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False) # 'Fácil', 'Médio', 'Difícil', 'Muito Difícil'

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False) # Should match one of the options or be 'A', 'B', etc. Let's store the actual text or 'option_a'.
    # Requirement says "4 alternativas", "Resposta correta".
    # Storing the value is safer if shuffled, but storing the key ('option_a') is easier if fixed layout.
    # Given the requirements don't specify shuffle logic inside the DB, we'll store the text of the correct answer or the column name.
    # Let's assume we store the text of the correct answer to be unambiguous.
    phase = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)

    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    selected_option = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Integer, nullable=True) # Time taken to answer

    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")

class Phase(Base):
    __tablename__ = 'phases'

    phase_number = Column(Integer, primary_key=True) # 1, 2, 3, 4
    is_unlocked = Column(Boolean, default=False)

# Initialization Logic

def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Check/Create Master User
    master = db.query(User).filter(User.role == "master").first()
    if not master:
        # Hash password
        pwd = "master@123".encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd, salt).decode('utf-8')

        master_user = User(
            name="Administrador",
            email="master", # acts as username for master
            password_hash=hashed,
            role="master",
            active=True,
            mother_name="admin", # placeholder
            favorite_color="admin" # placeholder
        )
        db.add(master_user)
        print("Master user created.")

    # Check/Create Phases
    phases_count = db.query(Phase).count()
    if phases_count < 4:
        # Ensure we have phases 1 to 4
        for i in range(1, 5):
            p = db.query(Phase).filter(Phase.phase_number == i).first()
            if not p:
                # Phase 1 unlocked by default? Or all unlocked by master?
                # Requirement: "Usuários comuns: Só acessam fases liberadas"
                # Requirement: "Usuário master pode: Liberar ou bloquear fases"
                # Let's unlock Phase 1 by default so new users can start.
                is_unlocked = (i == 1)
                new_phase = Phase(phase_number=i, is_unlocked=is_unlocked)
                db.add(new_phase)
        print("Phases initialized.")

    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
