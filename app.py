import streamlit as st
import pandas as pd
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
    # .card img {
    #     width: 100%;
    #     height: 150px;
    #     object-fit: cover;
    #     border-radius: 10px;
    # }

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
                
    /* ---------- SQUARE IMAGE BOX ---------- */
    .card img {
        width: 100%;
        aspect-ratio: 1 / 1;   /* ⭐ perfect square */
        object-fit: cover;     /* crop nicely */
        border-radius: 10px;
    }

    /* ---------- BANNER IMAGE SMALLER ---------- */
    .banner-container img {
        width: 100%;
        height: 100px;      /* 🔥 Adjust this value (200–300px) */
        object-fit: cover;  /* keeps it clean and cropped */
        border-radius: 12px;
    }


    /* ---------- LUXURY CAPTION ---------- */
    .luxury-caption {
        text-align: center;
        font-size: 18px;
        font-weight: 500;
        color: #b48a2c;              /* soft gold */
        margin-top: 8px;
        margin-bottom: 25px;
        letter-spacing: 1px;
        font-style: italic;
    }



    </style>
    """, unsafe_allow_html=True)




st.set_page_config(layout="wide")
apply_style()

df = pd.read_excel("jewellery_catalog.xlsx")

lang = st.sidebar.selectbox("🌐 Language",["English","Hindi","Bengali"])
T = get_text(lang)

if st.sidebar.button("📦 "+T["products"]):
    st.switch_page("pages/Products.py")

#st.image("images/banner.jpg", use_container_width=True, caption="Discover the Art of Elegance: Exquisite Jewelry for Every Occasion")

st.markdown('<div class="banner-container">', unsafe_allow_html=True)
st.image("images/banner-trends-1.jpg", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("""
<div class="luxury-caption">
    Discover the Art of Elegance: Exquisite Jewelry for Every Occasion
</div>
""", unsafe_allow_html=True)


st.title("💎 "+T["title"])

types = df["type"].unique()

cols = st.columns(3)

for i,t in enumerate(types):
    item = df[df["type"]==t].iloc[0]

    with cols[i%3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.image(item["img1"], use_container_width=True)
        st.subheader(t)
        st.write(item["name"])

        if st.button("Explore", key=t):
            st.session_state["category"]=t
            #st.switch_page("pages/Products.py")
            st.switch_page("pages/Products")

        st.markdown('</div>', unsafe_allow_html=True)


