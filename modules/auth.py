import bcrypt
from sqlalchemy.orm import Session
from .database import SessionLocal, User

def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against a hash."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def login_user(email, password):
    """
    Authenticates a user.
    Returns the user object if successful, None otherwise.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user and user.active and verify_password(password, user.password_hash):
            return user
        return None
    finally:
        db.close()

def register_user(name, email, password, mother_name, favorite_color):
    """
    Registers a new user.
    Returns (True, message) or (False, error_message).
    """
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return False, "E-mail já cadastrado."

        hashed = get_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            password_hash=hashed,
            mother_name=mother_name,
            favorite_color=favorite_color,
            role="user",
            active=True
        )
        db.add(new_user)
        db.commit()
        return True, "Usuário cadastrado com sucesso!"
    except Exception as e:
        db.rollback()
        return False, f"Erro ao cadastrar: {str(e)}"
    finally:
        db.close()

def recover_password(email, mother_name, favorite_color, new_password):
    """
    Resets password if security questions match.
    Returns (True, message) or (False, error_message).
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False, "Usuário não encontrado."

        # Case insensitive check for security questions
        if (user.mother_name.strip().lower() != mother_name.strip().lower() or
            user.favorite_color.strip().lower() != favorite_color.strip().lower()):
            return False, "Respostas de segurança incorretas."

        user.password_hash = get_password_hash(new_password)
        db.commit()
        return True, "Senha redefinida com sucesso!"
    except Exception as e:
        db.rollback()
        return False, f"Erro ao redefinir senha: {str(e)}"
    finally:
        db.close()
