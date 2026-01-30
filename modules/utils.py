import streamlit as st

def set_ui_style():
    """Sets custom CSS styles for the application."""
    st.markdown("""
        <style>
        /* Main Background - Dark Mode */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #262730;
            color: white;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #ffffff;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {
            color: #e0e0e0;
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
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        /* Metric Cards */
        [data-testid="stMetric"] {
            background-color: #1f2937;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            border-left: 5px solid #ff7f50;
        }
        [data-testid="stMetricLabel"] {
            color: #d1d5db;
        }
        [data-testid="stMetricValue"] {
            color: #ffffff;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #2d3748;
            border-radius: 5px 5px 0 0;
            color: #a0aec0;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #0e1117;
            color: #4b49ac;
            border-top: 3px solid #4b49ac;
        }

        /* Inputs */
        .stTextInput>div>div>input {
            border-radius: 5px;
            border: 1px solid #4a5568;
            background-color: #1a202c;
            color: white;
        }

        /* Text Color Overrides for General Readability */
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: #e0e0e0;
        }

        h1 {
            border-bottom: 2px solid #ff7f50;
            padding-bottom: 10px;
            display: inline-block;
            color: #ffffff;
        }

        /* Progress Bar */
        .stProgress > div > div > div > div {
            background-color: #ff7f50;
        }

        /* Custom Boxes - Darker variants */
        .success-box {
            padding: 15px;
            background-color: #052c1e;
            color: #d1e7dd;
            border-radius: 8px;
            border-left: 5px solid #198754;
            margin-bottom: 15px;
        }
        .error-box {
            padding: 15px;
            background-color: #410b10;
            color: #f8d7da;
            border-radius: 8px;
            border-left: 5px solid #dc3545;
            margin-bottom: 15px;
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
