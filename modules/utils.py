import streamlit as st

def set_ui_style():
    """Sets custom CSS styles for the application."""
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            font-weight: bold;
        }
        .success-box {
            padding: 10px;
            background-color: #d4edda;
            color: #155724;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .error-box {
            padding: 10px;
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def show_header(title, subtitle=None):
    """Displays a consistent header."""
    st.title(title)
    if subtitle:
        st.subheader(subtitle)
    st.markdown("---")

def show_success(message):
    st.markdown(f'<div class="success-box">{message}</div>', unsafe_allow_html=True)

def show_error(message):
    st.markdown(f'<div class="error-box">{message}</div>', unsafe_allow_html=True)
