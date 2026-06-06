import streamlit as st
from pathlib import Path


def load_css():
    css_path = Path(__file__).parent.parent / "styles" / "main.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <div style="
            font-size: 1.8rem;
            font-weight: 800;
            color: #e2e8f0;
            letter-spacing: -0.03em;
            line-height: 1.2;
        ">{icon} {title}</div>
        {f'<div style="font-size:0.95rem; color:#64748b; margin-top:4px;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <hr style="border-color:#2d3154; margin: 0 0 1.5rem 0;">
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: str = "", color: str = "#4C9BE8"):
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase;
                    letter-spacing:0.08em; font-weight:600; margin-bottom:8px;">
            {label}
        </div>
        <div style="font-size:2rem; font-weight:800; color:{color}; line-height:1;">
            {value}
        </div>
        {f'<div style="font-size:0.8rem; color:#64748b; margin-top:6px;">{delta}</div>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str, border_color: str = "#4C9BE8"):
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a1d2e, #1e2235);
        border: 1px solid #2d3154;
        border-left: 4px solid {border_color};
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
    ">
        <div style="font-weight:700; color:#e2e8f0; margin-bottom:6px;">{title}</div>
        <div style="font-size:0.9rem; color:#94a3b8; line-height:1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def tag(text: str, color: str = "blue"):
    color_map = {
        "blue": "tag",
        "green": "tag tag-green",
        "amber": "tag tag-amber",
    }
    css_class = color_map.get(color, "tag")
    return f'<span class="{css_class}">{text}</span>'


def tags_row(items: list, color: str = "blue"):
    if not items:
        return
    html = " ".join([tag(item, color) for item in items])
    st.markdown(html, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="margin: 1.5rem 0 1rem 0;">
        <div class="section-header">{title}</div>
        {f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def divider():
    st.markdown(
        '<hr style="border-color:#2d3154; margin: 1rem 0;">',
        unsafe_allow_html=True
    )


def success_banner(message: str):
    st.markdown(f"""
    <div style="
        background: rgba(0, 212, 170, 0.1);
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-left: 4px solid #00d4aa;
        border-radius: 10px;
        padding: 14px 20px;
        color: #00d4aa;
        font-weight: 600;
        margin: 12px 0;
    ">✅ {message}</div>
    """, unsafe_allow_html=True)


def error_banner(message: str):
    st.markdown(f"""
    <div style="
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 14px 20px;
        color: #ef4444;
        font-weight: 600;
        margin: 12px 0;
    ">❌ {message}</div>
    """, unsafe_allow_html=True)


def plotly_dark_layout(fig, title: str = "", height: int = 400):
    fig.update_layout(
        title=dict(text=title, font=dict(color="#e2e8f0", size=14)),
        paper_bgcolor="#1a1d2e",
        plot_bgcolor="#1a1d2e",
        font=dict(color="#94a3b8", family="Inter"),
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            gridcolor="#2d3154",
            linecolor="#2d3154",
            tickfont=dict(color="#94a3b8"),
        ),
        yaxis=dict(
            gridcolor="#2d3154",
            linecolor="#2d3154",
            tickfont=dict(color="#94a3b8"),
        ),
        legend=dict(
            bgcolor="#1a1d2e",
            bordercolor="#2d3154",
            font=dict(color="#94a3b8")
        ),
    )
    return fig