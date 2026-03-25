import streamlit as st
import os
import sys
import subprocess
import shutil
import time

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="مُشكِّل النصوص العربية | CATT AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. الواجهة المخصصة الكاملة
# ==========================================
st.markdown("""
<style>
/* ══════════════════════════════════ استيراد الخطوط ══════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@200;300;400;500;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap');

/* ══════════════════════════════════ متغيرات الألوان ══════════════════════════════════ */
:root {
    --gold: #e9c46a;
    --gold-light: #f4d58d;
    --gold-dark: #c9a227;
    --cyan: #a8dadc;
    --cyan-light: #d4f0f0;
    --dark-1: #050510;
    --dark-2: #0d0d2b;
    --dark-3: #1a1a3e;
    --dark-4: #252552;
    --orange: #f4a261;
    --coral: #e76f51;
    --green: #2ecc71;
    --red: #e74c3c;
    --purple: #a855f7;
    --text-primary: #f0f0f0;
    --text-secondary: #b0b0b0;
    --glass: rgba(255, 255, 255, 0.03);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-hover: rgba(255, 255, 255, 0.06);
}

/* ══════════════════════════════════ إعدادات عامة ══════════════════════════════════ */
* {
    font-family: 'Tajawal', sans-serif !important;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark-1) !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* إخفاء عناصر Streamlit */
#MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}

/* ══════════════════════════════════ الخلفية المتحركة ══════════════════════════════════ */
.bg-wrapper {
    position: fixed;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}

.bg-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.15;
    animation: orbit 20s ease-in-out infinite;
}

.bg-orb-1 {
    width: 500px;
    height: 500px;
    background: var(--gold);
    top: -150px;
    right: -150px;
    animation-delay: 0s;
}

.bg-orb-2 {
    width: 400px;
    height: 400px;
    background: var(--purple);
    bottom: -100px;
    left: -100px;
    animation-delay: -7s;
}

.bg-orb-3 {
    width: 300px;
    height: 300px;
    background: var(--cyan);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation-delay: -14s;
}

.bg-grid {
    position: absolute;
    inset: 0;
    background-image: linear-gradient(rgba(233,196,106,0.03) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(233,196,106,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
}

@keyframes orbit {
    0%, 100% { transform: translate(0, 0) scale(1); }
    25% { transform: translate(40px, -60px) scale(1.1); }
    50% { transform: translate(-50px, 40px) scale(0.9); }
    75% { transform: translate(30px, 70px) scale(1.05); }
}

/* ══════════════════════════════════ شريط التنقل العلوي ══════════════════════════════════ */
.navbar {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 3rem;
    background: rgba(13, 13, 43, 0.7);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--glass-border);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.nav-logo {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--gold), var(--orange));
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 4px 15px rgba(233, 196, 106, 0.3);
}

.nav-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--gold);
    letter-spacing: -0.5px;
}

.nav-links {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.3s;
    cursor: pointer;
}

.nav-link:hover {
    color: var(--gold);
}

.nav-badge {
    background: linear-gradient(135deg, var(--gold), var(--orange));
    color: var(--dark-1);
    padding: 0.4rem 1rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
}

/* ══════════════════════════════════ القسم الرئيسي (Hero) ══════════════════════════════════ */
.hero-section {
    position: relative;
    z-index: 1;
    text-align: center;
    padding: 4rem 2rem 3rem;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(233, 196, 106, 0.1);
    border: 1px solid rgba(233, 196, 106, 0.2);
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    font-size: 0.85rem;
    color: var(--gold);
    margin-bottom: 1.5rem;
    animation: fadeInDown 0.8s ease;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    line-height: 1.2;
    margin-bottom: 1rem;
    animation: fadeInUp 0.8s ease;
}

.hero-title .gradient-text {
    background: linear-gradient(135deg, var(--gold), var(--orange), var(--gold-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto 2rem;
    line-height: 1.8;
    font-weight: 300;
    animation: fadeInUp 0.8s ease 0.2s both;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    animation: fadeInUp 0.8s ease 0.4s both;
}

.hero-stat {
    text-align: center;
}

.hero-stat-value {
    font-size: 1.8rem;
    font-weight: 900;
    color: var(--gold);
}

.hero-stat-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 0.2rem;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* ══════════════════════════════════ منطقة العمل الرئيسية ══════════════════════════════════ */
.workspace-container {
    position: relative;
    z-index: 1;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 2rem 3rem;
}

/* بطاقة زجاجية */
.glass-card {
    background: var(--glass);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(233, 196, 106, 0.15);
    background: var(--glass-hover);
}

/* عنوان البطاقة */
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.2rem;
}

.card-title {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
}

.card-title-icon {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, var(--gold), var(--orange));
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
}

.card-counter {
    font-size: 0.8rem;
    color: var(--text-secondary);
    background: rgba(255,255,255,0.05);
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    border: 1px solid var(--glass-border);
}

/* ══════════════════════════════════ مربعات النص المخصصة ══════════════════════════════════ */
.stTextArea textarea {
    font-family: 'Noto Naskh Arabic', 'Amiri', serif !important;
    font-size: 1.3rem !important;
    line-height: 2.4 !important;
    direction: rtl !important;
    text-align: right !important;
    background: rgba(0, 0, 0, 0.3) !important;
    border: 2px solid var(--glass-border) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    color: var(--text-primary) !important;
    transition: all 0.3s ease !important;
    resize: none !important;
}

.stTextArea textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 4px rgba(233, 196, 106, 0.1) !important;
    background: rgba(0, 0, 0, 0.4) !important;
}

.stTextArea textarea::placeholder {
    color: rgba(255, 255, 255, 0.2) !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 1rem !important;
}

/* ══════════════════════════════════ مربع النتيجة ══════════════════════════════════ */
.output-display {
    background: linear-gradient(135deg, rgba(233, 196, 106, 0.06), rgba(244, 162, 97, 0.03), rgba(168, 218, 220, 0.03) );
    border: 2px solid rgba(233, 196, 106, 0.2);
    border-radius: 16px;
    padding: 2rem;
    direction: rtl;
    text-align: right;
    font-family: 'Noto Naskh Arabic', 'Amiri', serif;
    font-size: 1.4rem;
    line-height: 2.8;
    color: var(--gold-light);
    min-height: 200px;
    word-wrap: break-word;
    position: relative;
    overflow: hidden;
}

.output-display::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--orange), var(--gold));
    border-radius: 16px 16px 0 0;
}

.output-empty {
    color: rgba(255, 255, 255, 0.15);
    font-family: 'Tajawal', sans-serif;
    font-size: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.8rem;
    min-height: 200px;
}

.output-empty-icon {
    font-size: 2.5rem;
    opacity: 0.3;
}

/* ══════════════════════════════════ الأزرار المخصصة ══════════════════════════════════ */
.stButton > button {
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    padding: 0.8rem 1.5rem !important;
    font-size: 1.1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: none !important;
    position: relative;
    overflow: hidden;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold), var(--orange)) !important;
    color: var(--dark-1) !important;
    box-shadow: 0 4px 20px rgba(233, 196, 106, 0.3) !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(233, 196, 106, 0.4) !important;
}

.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

.stButton > button[kind="secondary"] {
    background: var(--glass) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--glass-border) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: var(--glass-hover) !important;
    border-color: rgba(233, 196, 106, 0.3) !important;
}

/* ══════════════════════════════════ بطاقات الإحصائيات ══════════════════════════════════ */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}

.stat-card {
    background: linear-gradient(135deg, rgba(26, 26, 62, 0.8), rgba(13, 13, 43, 0.9) );
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}

.stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(233, 196, 106, 0.3);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.stat-card:hover::before {
    opacity: 1;
}

.stat-icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    display: block;
}

.stat-value {
    font-size: 2rem;
    font-weight: 900;
    color: var(--gold);
    display: block;
    line-height: 1.2;
}

.stat-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
    font-weight: 500;
}

/* ══════════════════════════════════ شريط التوزيع ══════════════════════════════════ */
.dist-section {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 1.5rem;
    margin-top: 1rem;
}

.dist-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--gold);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.dist-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.6rem;
    direction: rtl;
}

.dist-name {
    min-width: 80px;
    font-size: 0.85rem;
    color: var(--cyan);
    text-align: right;
    font-weight: 500;
}

.dist-bar-bg {
    flex: 1;
    height: 6px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 3px;
    overflow: hidden;
}

.dist-bar-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--gold), var(--orange));
    transition: width 1s ease;
}

.dist-count {
    min-width: 35px;
    text-align: center;
    font-weight: 700;
    color: var(--gold);
    font-size: 0.85rem;
}

/* ══════════════════════════════════ حالة النموذج ══════════════════════════════════ */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1.2rem;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 600;
}

.status-ok {
    background: rgba(46, 204, 113, 0.1);
    border: 1px solid rgba(46, 204, 113, 0.25);
    color: #2ecc71;
}

.status-demo {
    background: rgba(243, 156, 18, 0.1);
    border: 1px solid rgba(243, 156, 18, 0.25);
    color: #f39c12;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    animation: pulse-dot 2s infinite;
}

.status-ok .status-dot {
    background: #2ecc71;
}

.status-demo .status-dot {
    background: #f39c12;
}

@keyframes pulse-dot {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: 0.5;
        transform: scale(0.8);
    }
}

/* ══════════════════════════════════ شريط الأدوات ══════════════════════════════════ */
.toolbar {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}

.tool-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.4rem 1rem;
    background: rgba(233, 196, 106, 0.06);
    border: 1px solid rgba(233, 196, 106, 0.12);
    border-radius: 50px;
    font-size: 0.8rem;
    color: var(--gold);
    cursor: pointer;
    transition: all 0.3s;
}

.tool-chip:hover {
    background: rgba(233, 196, 106, 0.12);
    border-color: rgba(233, 196, 106, 0.3);
    transform: translateY(-1px);
}

/* ══════════════════════════════════ اختيار النموذج ══════════════════════════════════ */
.model-selector {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.model-option {
    flex: 1;
    background: var(--glass);
    border: 2px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
}

.model-option:hover {
    border-color: rgba(233, 196, 106, 0.3);
}

.model-option.active {
    border-color: var(--gold);
    background: rgba(233, 196, 106, 0.08);
}

.model-option-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.model-option-name {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
}

.model-option-desc {
    font-size: 0.8rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}

/* ══════════════════════════════════ الشريط الجانبي ══════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--dark-2), var(--dark-3)) !important;
    border-left: 1px solid var(--glass-border) !important;
}

section[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ══════════════════════════════════ Radio مخصص ══════════════════════════════════ */
div[role="radiogroup"] {
    direction: rtl !important;
    gap: 0.5rem !important;
}

div[role="radiogroup"] label {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.2rem !important;
    transition: all 0.3s !important;
    color: var(--text-primary) !important;
}

div[role="radiogroup"] label:hover {
    border-color: rgba(233, 196, 106, 0.3) !important;
    background: var(--glass-hover) !important;
}

div[role="radiogroup"] label[data-checked="true"] {
    border-color: var(--gold) !important;
    background: rgba(233, 196, 106, 0.1) !important;
}

/* ══════════════════════════════════ نماذج سريعة ══════════════════════════════════ */
.samples-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1rem 0;
    direction: rtl;
}

.sample-chip {
    padding: 0.5rem 1rem;
    background: rgba(168, 218, 220, 0.06);
    border: 1px solid rgba(168, 218, 220, 0.12);
    border-radius: 25px;
    font-size: 0.85rem;
    color: var(--cyan);
    cursor: pointer;
    transition: all 0.3s;
    font-family: 'Tajawal', sans-serif;
}

.sample-chip:hover {
    background: rgba(168, 218, 220, 0.12);
    border-color: rgba(168, 218, 220, 0.3);
    transform: translateY(-2px);
    color: var(--cyan-light);
}

/* ══════════════════════════════════ إشعار النسخ ══════════════════════════════════ */
.copy-toast {
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%) translateY(100px);
    padding: 0.8rem 1.5rem;
    background: var(--dark-3);
    border: 1px solid var(--gold);
    border-radius: 50px;
    color: var(--gold);
    font-weight: 600;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    z-index: 9999;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.copy-toast.show {
    transform: translateX(-50%) translateY(0);
}

/* ══════════════════════════════════ الميزات (Features) ══════════════════════════════════ */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 2rem 0;
}

.feature-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s;
}

.feature-card:hover {
    border-color: rgba(233, 196, 106, 0.2);
    transform: translateY(-3px);
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: 0.8rem;
    display: block;
}

.feature-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.3rem;
}

.feature-desc {
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* ══════════════════════════════════ الفوتر ══════════════════════════════════ */
.site-footer {
    position: relative;
    z-index: 1;
    text-align: center;
    padding: 3rem 2rem;
    border-top: 1px solid var(--glass-border);
    margin-top: 3rem;
}

.footer-brand {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--gold);
    margin-bottom: 0.5rem;
}

.footer-text {
    color: var(--text-secondary);
    font-size: 0.85rem;
    line-height: 1.8;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 1rem;
}

.footer-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.85rem;
    transition: color 0.3s;
}

.footer-link:hover {
    color: var(--gold);
}

/* ══════════════════════════════════ تجاوب الشاشات الصغيرة ══════════════════════════════════ */
@media (max-width: 768px) {
    .navbar {
        padding: 0.8rem 1rem;
    }
    .nav-links {
        display: none;
    }
    .hero-title {
        font-size: 2rem;
    }
    .hero-stats {
        gap: 1.5rem;
    }
    .hero-stat-value {
        font-size: 1.3rem;
    }
    .stats-row {
        grid-template-columns: repeat(2, 1fr);
    }
    .features-grid {
        grid-template-columns: 1fr;
    }
    .workspace-container {
        padding: 0 1rem 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. الخلفية المتحركة + شريط التنقل
# ==========================================
st.markdown("""
<div class="bg-wrapper">
    <div class="bg-orb bg-orb-1"></div>
    <div class="bg-orb bg-orb-2"></div>
    <div class="bg-orb bg-orb-3"></div>
    <div class="bg-grid"></div>
</div>
<div class="navbar">
    <div class="nav-brand">
        <div class="nav-logo">✨</div>
        <span class="nav-title">CATT AI</span>
    </div>
    <div class="nav-links">
        <span class="nav-link">الرئيسية</span>
        <span class="nav-link">المميزات</span>
        <span class="nav-link">حول</span>
        <span class="nav-badge">v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. قسم Hero
# ==========================================
st.markdown("""
<div class="hero-section">
    <div class="hero-badge"> 🚀 مدعوم بالذكاء الاصطناعي </div>
    <h1 class="hero-title">
        <span class="gradient-text">مُشكِّل النصوص العربية</span>
    </h1>
    <p class="hero-subtitle">
        أضف الحركات على النصوص العربية بدقة عالية باستخدام نماذج التعلم العميق المتقدمة — فوري، دقيق، ومجاني
    </p>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">+95%</div>
            <div class="hero-stat-label">دقة التشكيل</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">&lt;1s</div>
            <div class="hero-stat-label">سرعة المعالجة</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">∞</div>
            <div class="hero-stat-label">بدون حدود</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. إعداد البيئة
# ==========================================
WORKSPACE = os.path.join(os.getcwd(), "catt_workspace")
MODELS_DIR = os.path.join(WORKSPACE, "onnx_models")
LOCAL_LIB = os.path.join(WORKSPACE, "lib")

os.environ["HF_HOME"] = os.path.join(WORKSPACE, "hf_cache")
os.environ["TRANSFORMERS_CACHE"] = os.path.join(WORKSPACE, "hf_cache")
os.environ["XDG_CACHE_HOME"] = WORKSPACE
os.environ["TMPDIR"] = WORKSPACE
os.environ["TEMP"] = WORKSPACE
os.environ["TMP"] = WORKSPACE

def setup_environment():
    for d in [WORKSPACE, MODELS_DIR, LOCAL_LIB, os.environ["HF_HOME"]]:
        os.makedirs(d, exist_ok=True)
    catt_in_lib = os.path.join(LOCAL_LIB, "catt_tashkeel")
    if not os.path.exists(catt_in_lib):
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "catt-tashkeel", "--target", LOCAL_LIB, "--no-deps", "--quiet"],
            check=False,
        )
    # نسخ ملفات ONNX
    search_paths = [
        os.path.join(sys.prefix, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages", "catt_tashkeel", "onnx_models"),
        os.path.join(LOCAL_LIB, "catt_tashkeel", "onnx_models"),
    ]
    for p in sys.path:
        search_paths.append(os.path.join(p, "catt_tashkeel", "onnx_models"))
    for src in search_paths:
        if os.path.exists(src) and os.listdir(src):
            if not os.path.exists(MODELS_DIR) or not os.listdir(MODELS_DIR):
                try:
                    if os.path.exists(MODELS_DIR):
                        shutil.rmtree(MODELS_DIR)
                    shutil.copytree(src, MODELS_DIR)
                    break
                except Exception:
                    continue

if "env_ready" not in st.session_state:
    with st.spinner(""):
        setup_environment()
    if LOCAL_LIB not in sys.path:
        sys.path.insert(0, LOCAL_LIB)
    st.session_state["env_ready"] = True

if LOCAL_LIB not in sys.path:
    sys.path.insert(0, LOCAL_LIB)

# ==========================================
# 6. استيراد المكتبة
# ==========================================
try:
    from catt_tashkeel import CATTEncoderOnly, CATTEncoderDecoder
    LIB_OK = True
except Exception as e:
    LIB_OK = False
    LIB_ERR = str(e)

# ==========================================
# 7. تحميل النموذج
# ==========================================
@st.cache_resource
def load_model(mtype):
    original = os.getcwd()
    os.chdir(WORKSPACE)
    os.environ["ONNX_HOME"] = MODELS_DIR
    try:
        if mtype == "fast":
            m = CATTEncoderOnly()
        else:
            m = CATTEncoderDecoder()
        return m
    except PermissionError:
        # نسخ إضافية
        import catt_tashkeel as ct
        src = os.path.join(os.path.dirname(ct.__file__), "onnx_models")
        if os.path.exists(src):
            for f in os.listdir(src):
                sf = os.path.join(src, f)
                df = os.path.join(MODELS_DIR, f)
                if not os.path.exists(df):
                    try:
                        shutil.copy2(sf, df)
                    except Exception:
                        pass
        if mtype == "fast":
            return CATTEncoderOnly()
        else:
            return CATTEncoderDecoder()
    finally:
        os.chdir(original)

# ==========================================
# 8. منطقة العمل الرئيسية
# ==========================================
st.markdown('<div class="workspace-container">', unsafe_allow_html=True)

# فحص المكتبة
if not LIB_OK:
    st.markdown(
        '<div class="status-pill status-demo">'
        '<div class="status-dot"></div>'
        f'خطأ: {LIB_ERR}'
        '</div>',
        unsafe_allow_html=True,
    )

# اختيار النموذج
st.markdown("""
<div class="glass-card">
    <div class="card-header">
        <div class="card-title">
            <div class="card-title-icon">⚙️</div>
            اختيار النموذج
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

model_choice = st.radio(
    "النموذج:",
    ["⚡ سريع (Encoder-Only)", "🎯 دقيق (Encoder-Decoder)"],
    horizontal=True,
    label_visibility="collapsed",
)

mtype = "fast" if "سريع" in model_choice else "accurate"

# تحميل النموذج
model = None
if LIB_OK:
    try:
        with st.spinner("🔄 جاري تحميل النموذج..."):
            model = load_model(mtype)
        st.markdown(
            '<div class="status-pill status-ok">'
            '<div class="status-dot"></div>'
            'النموذج جاهز ✓'
            '</div>',
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.markdown(
            f'<div class="status-pill status-demo">'
            f'<div class="status-dot"></div>'
            f'خطأ: {e}'
            f'</div>',
            unsafe_allow_html=True,
        )

# ==========================================
# 9. النماذج الجاهزة
# ==========================================
SAMPLES = [
    "بسم الله الرحمن الرحيم",
    "انما الاعمال بالنيات",
    "العلم نور والجهل ظلام",
    "من جد وجد ومن زرع حصد",
    "اللغة العربية من اجمل اللغات",
    "الصبر مفتاح الفرج",
]

st.markdown("""
<div class="glass-card">
    <div class="card-header">
        <div class="card-title">
            <div class="card-title-icon">💡</div>
            جرّب نصاً جاهزاً
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

cols = st.columns(3)
for i, sample in enumerate(SAMPLES):
    with cols[i % 3]:
        if st.button(sample, key=f"sample_{i}", use_container_width=True):
            st.session_state["user_input"] = sample

# ==========================================
# 10. الإدخال والإخراج
# ==========================================
# الإدخال
st.markdown("""
<div class="glass-card">
    <div class="card-header">
        <div class="card-title">
            <div class="card-title-icon">📝</div>
            النص الأصلي
        </div>
        <span class="card-counter" id="counter">0 حرف</span>
    </div>
</div>
""", unsafe_allow_html=True)

user_text = st.text_area(
    label="النص",
    value=st.session_state.get("user_input", ""),
    height=180,
    placeholder="اكتب أو الصق النص العربي هنا...",
    label_visibility="collapsed",
    key="input_area",
)

# الأزرار
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    run_btn = st.button(
        "✨ تشكيل النص",
        type="primary",
        use_container_width=True,
        key="btn_run",
    )
with c2:
    clear_btn = st.button(
        "🗑️ مسح",
        use_container_width=True,
        key="btn_clear",
    )
with c3:
    copy_btn = st.button(
        "📋 نسخ",
        use_container_width=True,
        key="btn_copy",
    )

# مسح
if clear_btn:
    st.session_state["user_input"] = ""
    st.session_state["last_result"] = ""
    st.rerun()

# النتيجة
st.markdown("""
<div class="glass-card">
    <div class="card-header">
        <div class="card-title">
            <div class="card-title-icon">✨</div>
            النص المُشكَّل
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

result_holder = st.empty()

if "last_result" in st.session_state and st.session_state["last_result"]:
    result_holder.markdown(
        f'<div class="output-display">{st.session_state["last_result"]}</div>',
        unsafe_allow_html=True,
    )
else:
    result_holder.markdown(
        '<div class="output-display output-empty">'
        '<div class="output-empty-icon">✍️</div>'
        '<div>أدخل نصاً واضغط "تشكيل النص"</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# تشكيل
if run_btn:
    if not user_text.strip():
        st.warning("⚠️ أدخل نصاً أولاً")
    elif model is None:
        st.error("❌ النموذج غير محمّل")
    else:
        saved = os.getcwd()
        os.chdir(WORKSPACE)
        with st.spinner("⏳ جاري التشكيل..."):
            try:
                t0 = time.time()
                result = model.do_tashkeel(user_text, verbose=False)
                elapsed = round(time.time() - t0, 3)
                st.session_state["last_result"] = result
                result_holder.markdown(
                    f'<div class="output-display">{result}</div>',
                    unsafe_allow_html=True,
                )
                st.success("✅ تم التشكيل بنجاح!")

                # إحصائيات
                import re
                words = len(user_text.split())
                chars = len(re.findall(r"[\u0600-\u06FF]", user_text))
                diac = len(re.findall(r"[\u064B-\u0652]", result))

                st.markdown(f"""
                <div class="stats-row">
                    <div class="stat-card">
                        <span class="stat-icon">📝</span>
                        <span class="stat-value">{words}</span>
                        <div class="stat-label">كلمة</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">🔤</span>
                        <span class="stat-value">{chars}</span>
                        <div class="stat-label">حرف عربي</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">✍️</span>
                        <span class="stat-value">{diac}</span>
                        <div class="stat-label">حركة</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-icon">⚡</span>
                        <span class="stat-value">{elapsed}s</span>
                        <div class="stat-label">الوقت</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ خطأ: {e}")
            finally:
                os.chdir(saved)

# نسخ
if copy_btn:
    lr = st.session_state.get("last_result", "")
    if lr:
        st.code(lr, language=None)
        st.info("📋 حدّد النص وانسخه Ctrl+C")
    else:
        st.warning("⚠️ لا نتيجة للنسخ")

# ==========================================
# 11. قسم المميزات
# ==========================================
st.markdown("""
<div class="features-grid">
    <div class="feature-card">
        <span class="feature-icon">🧠</span>
        <div class="feature-title">ذكاء اصطناعي متقدم</div>
        <div class="feature-desc">نموذج CATT مدرّب على ملايين النصوص العربية المشكّلة</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">⚡</span>
        <div class="feature-title">سرعة فائقة</div>
        <div class="feature-desc">تشكيل فوري في أقل من ثانية مع دقة عالية</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <div class="feature-title">دقة عالية</div>
        <div class="feature-desc">نسبة دقة تتجاوز 95% في التشكيل الصحيح</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">📱</span>
        <div class="feature-title">متجاوب</div>
        <div class="feature-desc">يعمل على جميع الأجهزة والشاشات بسلاسة</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🔒</span>
        <div class="feature-title">آمن وخاص</div>
        <div class="feature-desc">النصوص تُعالج فورياً دون تخزين أو مشاركة</div>
    </div>
    <div class="feature-card">
        <span class="feature-icon">🆓</span>
        <div class="feature-title">مجاني بالكامل</div>
        <div class="feature-desc">استخدام غير محدود بدون تسجيل أو اشتراك</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # إغلاق workspace

# ==========================================
# 12. الفوتر
# ==========================================
st.markdown("""
<div class="site-footer">
    <div class="footer-brand">✨ CATT AI — مُشكِّل النصوص العربية</div>
    <div class="footer-text">
        مبني بتقنية التعلم العميق | نموذج CATT<br>
        صُنع بـ ❤️ للغة العربية
    </div>
    <div class="footer-links">
        <a class="footer-link" href="https://github.com/GT-SALT/CATT" target="_blank">GitHub</a>
        <span class="footer-link">الإصدار 2.0</span>
        <span class="footer-link">2025</span>
    </div>
</div>
""", unsafe_allow_html=True)
