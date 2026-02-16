import streamlit as st
import pandas as pd
import requests
from utils import get_text

def apply_style():
    import streamlit as st
    st.markdown("""
    <style>

    /* ---------- APP BACKGROUND ---------- */
    .stApp {
        background: #f6f7f9;
        font-family: 'Segoe UI', sans-serif;
    }

    /* ---------- HEADINGS ---------- */
    h1 {
        font-size: 34px;
        font-weight: 600;
        color: #2b2b2b;
    }

    h2, h3 {
        color: #3a3a3a;
    }

    /* ---------- CARD ---------- */
    .card {
        background: white;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        text-align: center;
        margin-bottom: 18px;
    }

    /* ---------- IMAGE (ONLY FIX HEIGHT) ---------- */
    .card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
    }

    /* remove Streamlit extra spacing around images */
    [data-testid="stImage"] {
        padding: 0 !important;
    }

    /* ---------- BUTTON ---------- */
    .stButton>button {
        background: white;
        border: 1px solid #e6e6e6;
        border-radius: 8px;
        font-weight: 500;
    }

    /* gold hover touch */
    .stButton>button:hover {
        border-color: #c9a33c;
        color: #c9a33c;
    }

    /* ---------- SIDEBAR CLEAN ---------- */
    section[data-testid="stSidebar"] {
        background: #ffffff;
    }

    </style>
    """, unsafe_allow_html=True)



st.set_page_config(layout="wide")
apply_style()

df=pd.read_excel("jewellery_catalog.xlsx")

lang = st.sidebar.selectbox("🌐 Language",["English","Hindi","Bengali"])
T = get_text(lang)

if st.sidebar.button("⬅ Products"):
    #st.switch_page("pages/Products.py")
    st.switch_page("pages/Products")

row=df[df["code"]==st.session_state["product"]].iloc[0]

st.title(row["name"])

cols=st.columns(3)

for i,img in enumerate([row["img1"],row["img2"],row["img3"]]):
    with cols[i]:
        st.image(img, use_container_width=True)

st.write("Weight:",row["weight"])
st.write("Making:",row["making_charge"])

st.subheader("🤖 "+T["suggest"])

def suggest():
    prompt=f"Suggest similar jewellery designs for {row['name']} {row['type']}"
    r=requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization":f"Bearer {st.secrets['GROQ_API_KEY']}"},
        json={"model":"llama3-70b-8192","messages":[{"role":"user","content":prompt}]}
    )
    return r.json()["choices"][0]["message"]["content"]

if st.button(T["suggest"]):
    st.write(suggest())


