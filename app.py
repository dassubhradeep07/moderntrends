import base64
import io
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from PIL import Image, ImageOps
from utils import get_text

try:
    from utils import resolve_image_path
except ImportError:
    def resolve_image_path(image_path):
        return image_path

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


    /* ---------- CAROUSEL FIT ---------- */
    /* Force carousel images to fill and crop to the container */
    .carousel-item img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
    }
    /* Bootstrap override used by streamlit-carousel */
    .carousel-inner img {
        width: 100% !important;
        height: auto !important;
        object-fit: cover !important;
        object-position: center center !important;
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


def get_fitted_image(image_path, size=(700, 700)):
    """Return a center-cropped image with consistent dimensions for card rendering."""
    try:
        resolved = resolve_image_path(image_path)
        if not resolved:
            return None
        img = Image.open(resolved).convert("RGB")
        resample = getattr(Image, "Resampling", Image).LANCZOS
        return ImageOps.fit(img, size, method=resample)
    except Exception:
        return None


def image_to_data_url(image_path, max_width=1800):
    """Preserve aspect ratio and return image as base64 data URL for HTML slider."""
    try:
        resolved = resolve_image_path(image_path)
        if not resolved:
            return ""
        img = Image.open(resolved).convert("RGB")
        w, h = img.size
        if w > max_width:
            new_h = int((max_width / w) * h)
            resample = getattr(Image, "Resampling", Image).LANCZOS
            img = img.resize((max_width, new_h), resample)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=88)
        encoded = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        return ""


def get_slider_height(image_paths, target_width=1200, min_height=260, max_height=540):
    """Derive a good slider height from the first valid banner aspect ratio."""
    for path in image_paths:
        try:
            with Image.open(path) as img:
                w, h = img.size
                if w > 0 and h > 0:
                    ratio = w / h
                    derived = int(target_width / ratio)
                    return max(min_height, min(max_height, derived))
        except Exception:
            continue
    return 360


def render_auto_banner_slider(image_paths):
        """Render auto-playing slider where banner size auto-fits source aspect ratio."""
        data_urls = [image_to_data_url(p) for p in image_paths]
        data_urls = [u for u in data_urls if u]

        if not data_urls:
                return

        slider_height = get_slider_height(image_paths)

        slides_html = "\n".join(
                [
                        f'<div class="banner-slide" style="display:{"block" if i == 0 else "none"};">'
                        f'<img src="{url}" alt="Banner {i+1}" />'
                        '</div>'
                        for i, url in enumerate(data_urls)
                ]
        )

        html = f"""
        <div class="banner-slider-wrap">
            <div id="banner-slider" class="banner-slider">
                {slides_html}
            </div>
        </div>

        <style>
            .banner-slider-wrap {{
                width: 100%;
                background: transparent;
            }}
            .banner-slider {{
                width: 100%;
                border-radius: 12px;
                overflow: hidden;
            }}
            .banner-slide {{
                width: 100%;
                animation: fadeIn 0.5s ease;
            }}
            .banner-slide img {{
                width: 100%;
                height: {slider_height}px;
                object-fit: cover;
                object-position: center center;
                display: block;
                background: #ffffff;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0.25; }}
                to {{ opacity: 1; }}
            }}
        </style>

        <script>
            (function() {{
                const slides = document.querySelectorAll('#banner-slider .banner-slide');
                if (!slides || slides.length <= 1) return;
                let idx = 0;
                setInterval(() => {{
                    slides[idx].style.display = 'none';
                    idx = (idx + 1) % slides.length;
                    slides[idx].style.display = 'block';
                }}, 3200);
            }})();
        </script>
        """

        components.html(html, height=slider_height + 20, scrolling=False)




st.set_page_config(layout="wide")
apply_style()

df = pd.read_excel("jewellery_catalog.xlsx")

lang = st.sidebar.selectbox("🌐 Language",["English","Hindi","Bengali"])
T = get_text(lang)

if st.sidebar.button("📦 "+T["products"]):
    st.switch_page("pages/Products.py")

#st.image("images/banner.jpg", use_container_width=True, caption="Discover the Art of Elegance: Exquisite Jewelry for Every Occasion")

# st.markdown('<div class="banner-container">', unsafe_allow_html=True)
# st.image("images/banner-trends-1.jpg", use_container_width=True)
# st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="banner-container">', unsafe_allow_html=True)
#st.image("images/banner-trends-1.jpg", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

banner_files = [
    "images/1_banner.JPG",
    "images/2_banner.JPG",
    "images/3_banner.JPG",
]

render_auto_banner_slider(banner_files)



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
        fitted = get_fitted_image(item["img1"])
        if fitted is not None:
            st.image(fitted, use_container_width=True)
        else:
            st.markdown(
                '<div style="height:220px;display:flex;align-items:center;justify-content:center;'
                'background:#f3f4f6;border-radius:10px;color:#9aa0a6;font-weight:600;">Image not available</div>',
                unsafe_allow_html=True,
            )
        st.subheader(t)
        st.write(item["name"])

        if st.button("Explore", key=t):
            st.session_state["category"]=t
            st.switch_page("pages/Products.py")

        st.markdown('</div>', unsafe_allow_html=True)
