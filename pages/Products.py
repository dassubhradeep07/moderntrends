import streamlit as st
import pandas as pd
from utils import calculate_price, get_text

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

df = pd.read_excel("jewellery_catalog.xlsx")

lang = st.sidebar.selectbox("🌐 Language",["English","Hindi","Bengali"])
T = get_text(lang)

if st.sidebar.button("🏠 "+T["home"]):
    st.switch_page("app.py")

cat = st.session_state.get("category", df["type"].iloc[0])

st.title(cat)

search = st.text_input(T["search"])

if st.button("🎤 "+T["voice"]):
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source)
    try:
        search=r.recognize_google(audio)
    except:
        pass

st.subheader(T["filters"])

types = st.multiselect("Type", df["type"].unique(), default=[cat])
min_w,max_w = st.slider(T["weight"],0,100,(0,100))
min_m,max_m = st.slider(T["making"],0,50000,(0,50000))

data=df[df["type"].isin(types)]

if search:
    data=data[data["name"].str.contains(search,case=False)]

data=data[(data["weight"]>=min_w)&(data["weight"]<=max_w)]
data=data[(data["making_charge"]>=min_m)&(data["making_charge"]<=max_m)]

cols=st.columns(3)

for i,row in data.iterrows():
    price=calculate_price(row["weight"],6000,row["making_charge"])

    with cols[i%3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.image(row["img1"],use_container_width=True)
        st.write(row["name"])
        st.success(f"₹ {price:,.0f}")

        if st.button("View",key=row["code"]):
            st.session_state["product"]=row["code"]
            st.switch_page("/workspaces/moderntrends/pages/Product_Details.py")
            #st.switch_page("pages/Product_Details")

        st.markdown('</div>', unsafe_allow_html=True)




