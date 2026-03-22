import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image, ImageOps
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
        height: 220px;
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

    /* ---------- DETAIL HERO ---------- */
    .detail-hero {
        background: white;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        margin-bottom: 24px;
    }
    .detail-hero img {
        width: 100%;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        border-radius: 12px;
    }
    .detail-info h1 {
        font-size: 26px;
        font-weight: 700;
        color: #2b2b2b;
        margin-bottom: 6px;
    }
    .detail-info .badge {
        display: inline-block;
        background: #fdf3d8;
        color: #b48a2c;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .detail-info .desc {
        color: #555;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 16px;
    }
    .detail-info .meta-row {
        display: flex;
        gap: 24px;
        flex-wrap: wrap;
        margin-top: 10px;
    }
    .detail-info .meta-item {
        background: #f6f7f9;
        border-radius: 10px;
        padding: 10px 18px;
        text-align: center;
        min-width: 110px;
    }
    .detail-info .meta-item .label {
        font-size: 11px;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .detail-info .meta-item .value {
        font-size: 18px;
        font-weight: 700;
        color: #2b2b2b;
        margin-top: 2px;
    }
    /* ---------- SIDEBAR CLEAN ---------- */
    section[data-testid="stSidebar"] {
        background: #ffffff;
    }

    </style>
    """, unsafe_allow_html=True)


def get_fitted_image(image_path, size=(900, 900)):
    """Return a center-cropped image with consistent dimensions for card rendering."""
    try:
        img = Image.open(image_path).convert("RGB")
        resample = getattr(Image, "Resampling", Image).LANCZOS
        return ImageOps.fit(img, size, method=resample)
    except Exception:
        return None



st.set_page_config(layout="wide")
apply_style()

if st.session_state.pop("scroll_to_top", False):
    components.html(
        """
        <script>
            window.parent.scrollTo({top: 0, behavior: 'smooth'});
        </script>
        """,
        height=0,
    )

df=pd.read_excel("jewellery_catalog.xlsx")

lang = st.sidebar.selectbox("🌐 Language",["English","Hindi","Bengali"])
T = get_text(lang)

if st.sidebar.button("⬅ Products"):
    st.switch_page("pages/Products.py")

row=df[df["code"]==st.session_state["product"]].iloc[0]

# ── HERO: single image + info side by side ──────────────────────────────────
hero_img_col, hero_info_col = st.columns([1, 1], gap="large")

with hero_img_col:
    st.markdown('<div class="detail-hero" style="padding:12px;">', unsafe_allow_html=True)
    hero_img = get_fitted_image(row["img1"], size=(1000, 1000))
    if hero_img is not None:
        st.image(hero_img, use_container_width=True)
    else:
        st.markdown(
            '<div style="height:320px;display:flex;align-items:center;justify-content:center;'
            'background:#f3f4f6;border-radius:10px;color:#9aa0a6;font-weight:600;">Image not available</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

with hero_info_col:
    desc = str(row.get("description", "") or "")
    weight_val = row["weight"]
    making_val = row["making_charge"]
    st.markdown(f"""
    <div class="detail-hero detail-info">
        <h1>{row['name']}</h1>
        <span class="badge">{row['type']}</span>
        <p class="desc">{desc if desc else "A beautiful piece from our exclusive collection."}</p>
        <div class="meta-row">
            <div class="meta-item">
                <div class="label">Weight</div>
                <div class="value">{weight_val} gm</div>
            </div>
            <div class="meta-item">
                <div class="label">Making Charge</div>
                <div class="value">₹{making_val}</div>
            </div>
            <div class="meta-item">
                <div class="label">Code</div>
                <div class="value" style="font-size:14px;">{row['code']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =================== ADVANCED CALCULATOR ===================
st.subheader("💰 Price Calculator")

col1, col2, col3 = st.columns(3)

with col1:
    gm_weight = st.number_input("Gold Weight (gm)", min_value=0.1, value=3.0, step=0.1, key="gm_weight")

with col2:
    mc_per_gm = st.number_input("Making Charge per gm (₹)", min_value=0.0, value=1200.0, step=100.0, key="mc_per_gm")

with col3:
    gold_rate = st.number_input("Gold Rate per gm (₹)", min_value=0.0, value=7500.0, step=100.0, key="gold_rate")

# === SIMPLE CALCULATION ===
# Formula: (gold_weight * rate_per_gm + mc_per_gm * 3) * (1 + 3% GST)
# Where 3% GST = 1.5% + 1.5%

gold_cost = gm_weight * gold_rate
making_charge = mc_per_gm * 3.0
subtotal = gold_cost + making_charge

# 3% GST (1.5% + 1.5%)
gst_rate = 0.03
gst_amount = subtotal * gst_rate
final_total = subtotal + gst_amount

# Display calculation breakdown
st.markdown("---")
st.markdown("### 📊 Price Breakdown")

breakdown_col1, breakdown_col2 = st.columns(2)

with breakdown_col1:
    st.write(f"🥇 Gold Cost ({gm_weight} gm × ₹{gold_rate:,.0f})", f"₹ {gold_cost:,.2f}")
    st.write(f"🔨 Making Charge (₹{mc_per_gm:,.0f} × 3)", f"₹ {making_charge:,.2f}")
    st.write(f"**Subtotal**", f"**₹ {subtotal:,.2f}**")

with breakdown_col2:
    st.write(f"💳 GST (1.5% + 1.5% = 3%)", f"₹ {gst_amount:,.2f}")
    st.success(f"### **💎 TOTAL PRICE: ₹ {final_total:,.2f}**")

st.markdown("---")
st.subheader("💎 Suggested Designs")

all_designs = df.copy()
all_designs["weight_num"] = pd.to_numeric(all_designs["weight"], errors="coerce")
current_weight = pd.to_numeric(pd.Series([row["weight"]]), errors="coerce").iloc[0]

same_category = all_designs[
    (all_designs["type"] == row["type"]) &
    (all_designs["code"] != st.session_state["product"])
]

if pd.notna(current_weight):
    similar_weight = same_category[
        (same_category["weight_num"].notna()) &
        ((same_category["weight_num"] - current_weight).abs() <= 0.5)
    ]
else:
    similar_weight = same_category.iloc[0:0]

suggestions = similar_weight.head(3).copy()

if len(suggestions) < 3:
    remaining_from_category = same_category[
        ~same_category["code"].isin(suggestions["code"])
    ]
    needed = 3 - len(suggestions)
    if len(remaining_from_category) > 0:
        suggestions = pd.concat(
            [suggestions, remaining_from_category.sample(min(needed, len(remaining_from_category)))],
            ignore_index=True,
        )

if len(suggestions) < 3:
    remaining_overall = all_designs[
        (~all_designs["code"].isin(suggestions["code"])) &
        (all_designs["code"] != st.session_state["product"])
    ]
    needed = 3 - len(suggestions)
    if len(remaining_overall) > 0:
        suggestions = pd.concat(
            [suggestions, remaining_overall.sample(min(needed, len(remaining_overall)))],
            ignore_index=True,
        )

if len(suggestions) == 0:
    st.info("No suggestions available right now")
else:
    card_cols = st.columns(min(3, len(suggestions)))
    for idx, (_, design) in enumerate(suggestions.iterrows()):
        with card_cols[idx]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            suggestion_img = get_fitted_image(design["img1"], size=(700, 700))
            if suggestion_img is not None:
                st.image(suggestion_img, use_container_width=True)
            else:
                st.markdown(
                    '<div style="height:220px;display:flex;align-items:center;justify-content:center;'
                    'background:#f3f4f6;border-radius:10px;color:#9aa0a6;font-weight:600;">Image not available</div>',
                    unsafe_allow_html=True,
                )
            st.subheader(str(design["name"]))
            st.write(f"**Type:** {design['type']}")
            st.write(f"**Weight:** {design['weight']} gm")
            st.write(f"**Making:** ₹{design['making_charge']}")
            if st.button("View Details", key=f"suggest_{design['code']}"):
                st.session_state["scroll_to_top"] = True
                st.session_state["product"] = design["code"]
                st.switch_page("pages/Product_Details.py")
            st.markdown('</div>', unsafe_allow_html=True)
