# streamlit_app: Personal Data Portfolio
# -------------------------------------------------
# How to run locally:
#   1) pip install -r requirements.txt  (or: pip install streamlit plotly pandas numpy pillow)
#   2) streamlit run app.py
# How to deploy (free):
#   • Push this file to a public GitHub repo.
#   • Go to https://streamlit.io/cloud → "New app" → select your repo/branch/file (app.py) → Deploy.
#   • Your app will be available at https://<your-name>.streamlit.app
# -------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
from datetime import datetime

# ---------- Page config ----------
st.set_page_config(
    page_title="Emanuel Gomes — Data Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Small style refresh ----------
custom_css = """
<style>
/***** Typography *****/
:root { --text: #101418; --muted:#6b7280; --card:#ffffff; --bg:#0b1220; }
html, body, [class^="css" ]  { font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, 'Noto Sans', 'Apple Color Emoji', 'Segoe UI Emoji'; }

/***** Headings *****/
h1, h2 { letter-spacing: -0.02em; }

/***** Cards *****/
.block-container { padding-top: 1.2rem; }
.card { background: var(--card); border-radius: 18px; padding: 18px 18px; box-shadow: 0 10px 20px rgba(2,12,27,0.08); border: 1px solid rgba(2,12,27,0.06); }
.badge { display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; background:#EEF2FF; color:#3730A3; margin-right:6px; margin-bottom:6px; }
.kpi { font-size:28px; font-weight:700; }
.subtle { color: var(--muted); }
.footer { color:#6b7280; font-size:12px; margin-top: 24px; }

/***** Sidebar avatar *****/
.sidebar-avatar { border-radius: 50%; border: 2px solid rgba(2,12,27,0.08); }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    import os
    img_path = "assets/profile.jpg"
    # Display profile photo if it exists
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning("Oops... no photo here yet! Imagine a very professional and friendly face.")

    # Personal details and links
    st.markdown("""
**Emanuel Gomes**  
Data Analyst · Data Scientist  
Porto, PT

[LinkedIn](https://linkedin.com/in/emanuel-gomes-001b16108) · [GitHub](https://github.com/E-man85) · [Email](mailto:eman-gomes@hotmail.com)
""")

    st.markdown("—")
    st.write("Quick filters")

    # Technology stack filter for projects
    show_tech = st.multiselect(
        "Tech stack",
        ["Python", "Pandas", "Plotly", "Power BI", "SQL", "Scikit-learn", "Streamlit", "GeoPandas", "Linguagem M"],
        default=["Python", "Pandas", "Plotly"],
        help="Use this to tag projects you want to highlight.",
    )

    st.markdown("—")
    st.caption("Theme: light/dark follows your browser.")


# ---------- Router ----------
PAGES = {
    "Home": "home",
    "Projects": "projects",
    "Resume": "resume",
    "Contact": "contact",
}

page = st.sidebar.radio("Navigate", list(PAGES.keys()), index=0)

# ---------- Demo data helpers ----------
def make_demo_df(n=200, seed=7):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=n, freq="D"),
        "region": rng.choice(["Lisboa", "Porto", "Matosinhos", "Setúbal"], n),
        "impressions": rng.integers(1_000, 50_000, n),
        "uniques": rng.integers(500, 20_000, n),
        "format": rng.choice(["Mupi", "Abrigo", "Digital"], n),
    })
    df["freq"] = (df["impressions"] / df["uniques"]).round(2)
    return df

@st.cache_data
def load_data():
    return make_demo_df()

# ---------- Home ----------
def render_home():
    st.title("Hi, I'm Emanuel Gomes")
    st.write(
        """
        I transform data into actionable insights and automated solutions that empower businesses to decide faster and work smarter.
        """
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Years of experience", 5)
    with col2:
        st.metric("Projects shipped", 12)
    with col3:
        st.metric("Tech I use", "Python · SQL · Power BI")

    st.markdown("\n")
    st.subheader("Featured projects")

    df = load_data()
    # KPI chart: daily impressions (demo)
    daily = df.groupby("date")["impressions"].sum().reset_index()
    fig = px.line(daily, x="date", y="impressions", title="Daily Impressions (demo)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        **What you'll find here**
        - Short case studies with *problem → approach → impact*.
        - Reproducible code on GitHub.
        - Interactive visuals you can explore.
        """
    )

# ---------- Projects ----------
def render_projects():
    st.header("Projects")
    st.caption("Filter by tags in the left sidebar to focus the list.")

    # Project 1
    with st.expander("Optimising OOH placement with POIs and reach modelling", expanded=True):
        st.markdown("""
        **Role:** Lead Data Analyst  
        **Stack:** Python, Pandas, GeoPandas, scikit‑learn, Streamlit  
        **Summary:** Scored locations by proximity to business POIs (SME decision‑makers) and modelled reach vs. cost to propose an optimal network.
        """)
        df = load_data()
        agg = (
            df.groupby(["region", "format"], as_index=False)[["impressions", "uniques"]]
            .sum()
        )
        fig = px.bar(agg, x="region", y="impressions", color="format", barmode="group",
                     title="Impressions by region & format (demo)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Impact:** -12% cost for the same reach; faster planning cycle.")
        st.markdown("[View code](https://github.com) · [Open notebook](https://github.com)")

    # Project 2
    with st.expander("Mobility insights with TomTom Traffic Stats", expanded=False):
        st.markdown("""
        **Role:** Data Analyst  
        **Stack:** Python, Pandas, Plotly, GeoJSON  
        **Summary:** Analysed peak times and corridors in Matosinhos to inform placement decisions and campaign pacing.
        """)
        df = load_data()
        hourly = df.assign(hour=lambda d: (d.index % 24)).groupby("hour")["uniques"].mean().reset_index()
        fig2 = px.area(hourly, x="hour", y="uniques", title="Average uniques by hour (demo)")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Impact:** Identified 3 prime corridors; +8% uplift in uniques.")

    # Project 3
    with st.expander("Forecasting inventory occupancy (OOH)"):
        st.markdown("""
        **Role:** Data Scientist (post‑grad)  
        **Stack:** Python, scikit‑learn, pandas  
        **Summary:** Built a simple baseline model to forecast weekly occupancy and guide pricing.
        """)
        df = load_data()
        wk = df.copy()
        wk["week"] = wk["date"].dt.isocalendar().week
        wk = wk.groupby("week")["impressions"].sum().reset_index()
        wk["forecast"] = wk["impressions"].rolling(4, min_periods=1).mean().round()
        fig3 = px.line(wk, x="week", y=["impressions", "forecast"], title="Weekly demand vs simple forecast (demo)")
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Replace the demo calculation with your actual model outputs.")

# ---------- Resume ----------
def render_resume():
    import os, base64
    st.header("Resume / CV")
    st.write("Get a detailed look at my professional experience:")

    # Path to local CV file
    cv_path = "assets/Emanuel_Gomes_CV.pdf"

    # Public CV link (fallback or external viewing)
    resume_url = "https://raw.githubusercontent.com/E-man85/portfolio_streamlit/main/assets/Emanuel_Gomes_CV.pdf"

    # Show preview and download if file exists locally
    if os.path.exists(cv_path):
        with open(cv_path, "rb") as f:
            cv_bytes = f.read()

        # Download button for CV
        st.download_button(
            label="⬇️ Download my CV (PDF)",
            data=cv_bytes,
            file_name="Emanuel_Gomes_CV.pdf",
            mime="application/pdf"
        )

        # Inline preview (iframe using base64 encoding)
        b64 = base64.b64encode(cv_bytes).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="720"></iframe>',
            unsafe_allow_html=True,
        )
        st.caption("Preview generated from local assets/Emanuel_Gomes_CV.pdf.")
    else:
        st.warning("Local CV not found at assets/Emanuel_Gomes_CV.pdf. Please add the file or use the public link below.")

    # Public link option to CV
    if resume_url:
        st.markdown(f"[📄 Open CV in browser]({resume_url})")

    # --- Skills & Certs ---
    st.subheader("Skills & certs")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        **Data**  
        • Python (pandas, numpy)  
        • SQL  
        • Power BI / DAX  
        • Linguagem M
        """)
    with cols[1]:
        st.markdown("""
        **ML**  
        • scikit-learn  
        • Forecasting  
        • Model evaluation
        """)
    with cols[2]:
        st.markdown("""
        **Other**  
        • Git & GitHub  
        • Streamlit  
        • Geospatial (GeoPandas)
        """)
   
# ---------- Contact ----------
def render_contact():
    st.header("Contact")
    st.write("Happy to chat about roles, freelance or collaborations.")

    # Functional HTML form via FormSubmit (posts directly to your email)
    form_html = """
    <form action="https://formsubmit.co/eman-gomes@hotmail.com" method="POST" target="_blank">
      <!-- FormSubmit options -->
      <input type="hidden" name="_subject" value="Portfolio contact — Emanuel Gomes">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_template" value="table">
      <!-- Optional: redirect after send (replace with your thanks page if you have one) -->
      <!-- <input type="hidden" name="_next" value="https://your-site/thanks"> -->

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;">
        <input type="text" name="name" placeholder="Name" required style="padding:10px;border-radius:10px;border:1px solid #ddd;">
        <input type="email" name="email" placeholder="Email" required style="padding:10px;border-radius:10px;border:1px solid #ddd;">
      </div>
      <textarea name="message" placeholder="Message" rows="6" required style="width:100%;padding:10px;border-radius:10px;border:1px solid #ddd;"></textarea>
      <div style="margin-top:12px;">
        <button type="submit" style="padding:10px 16px;border-radius:10px;border:1px solid #ddd;cursor:pointer;">Send</button>
      </div>
      <p style="font-size:12px;color:#6b7280;margin-top:8px;">
        By sending, you agree that your message will be emailed to Emanuel. No data is stored on this site.
      </p>
    </form>
    """
    st.markdown(form_html, unsafe_allow_html=True)

    # Mailto fallback (opens user's email client)
    st.markdown(
        "[Or email me directly](mailto:eman-gomes@hotmail.com?subject=Portfolio%20contact%20—%20Emanuel%20Gomes)",
        help="Opens your default email client."
    )

    st.markdown("""
**Find me online**  
- LinkedIn — https://linkedin.com/in/emanuel-gomes-001b16108 
- GitHub — https://github.com/E-man85
- Email — eman-gomes@hotmail.com
""")


# ---------- Router switch ----------
if page == "Home":
    render_home()
elif page == "Projects":
    render_projects()
elif page == "Resume":
    render_resume()
else:
    render_contact()

# ---------- Footer ----------
st.markdown(
    f"<div class='footer'>Last updated: {datetime.now().strftime('%Y-%m-%d')} · Built with Streamlit · © You</div>",
    unsafe_allow_html=True,
)
