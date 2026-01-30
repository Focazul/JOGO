import streamlit as st

def set_ui_style():
    """Sets custom CSS styles for the application."""
    st.markdown("""
        <style>
        /* Main Background */
        .stApp {
            background-color: #f4f5f7;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #2c3e50;
            color: white;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #ecf0f1;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {
            color: #bdc3c7;
        }

        /* Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            font-weight: bold;
            background-color: #4b49ac;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #3f3d91;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        /* Secondary/Action Buttons (if any specific class, otherwise generic override) */

        /* Metric Cards */
        [data-testid="stMetric"] {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-left: 5px solid #ff7f50;
        }
        [data-testid="stMetricLabel"] {
            color: #7f8c8d;
        }
        [data-testid="stMetricValue"] {
            color: #2c3e50;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #e0e0e0;
            border-radius: 5px 5px 0 0;
            color: #555;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: white;
            color: #4b49ac;
            border-top: 3px solid #4b49ac;
        }

        /* Inputs */
        .stTextInput>div>div>input {
            border-radius: 5px;
            border: 1px solid #ddd;
        }

        /* Progress Bar */
        .stProgress > div > div > div > div {
            background-color: #ff7f50;
        }

        /* Custom Boxes */
        .success-box {
            padding: 15px;
            background-color: #d1e7dd;
            color: #0f5132;
            border-radius: 8px;
            border-left: 5px solid #198754;
            margin-bottom: 15px;
        }
        .error-box {
            padding: 15px;
            background-color: #f8d7da;
            color: #842029;
            border-radius: 8px;
            border-left: 5px solid #dc3545;
            margin-bottom: 15px;
        }

        /* Headings */
        h1, h2, h3 {
            color: #2c3e50;
        }
        h1 {
            border-bottom: 2px solid #ff7f50;
            padding-bottom: 10px;
            display: inline-block;
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
