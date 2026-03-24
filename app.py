import streamlit as st
import re
import time
from spellchecker import SpellChecker

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="المصحح الإملائي الذكي",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. الواجهة المخصصة (CSS الاحترافي المُنقّح)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@200;300;400;500;700;800;900&display=swap');

:root {
    --gold: #e9c46a;
    --orange: #f4a261;
    --dark-1: #050510;
    --text-primary: #f0f0f0;
    --text-secondary: #b0b0b0;
    --glass: rgba(255, 255, 255, 0.03);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-hover: rgba(255, 255, 255, 0.06);
}

* { font-family: 'Tajawal', sans-serif !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark-1) !important;
    color: var(--text-primary) !important;
}

#MainMenu, footer, header { display: none !important; }

.hero-section { text-align: center; padding: 3rem 2rem 2rem; }
.hero-title { font-size: 3rem; font-weight: 900; color: var(--gold); margin-bottom: 0.5rem; }
.hero-subtitle { font-size: 1.2rem; color: var(--text-secondary); margin-bottom: 2rem; }

.glass-card {
    background: var(--glass);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}

.card-title { font-size: 1.2rem; font-weight: 700; color: var(--gold); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;}

/* تعديل مربع النص ليدعم الإنجليزية من اليسار لليمين */
.stTextArea textarea {
    font-family: monospace !important;
    font-size: 1.2rem !important;
    line-height: 1.8 !important;
    direction: ltr !important; 
    text-align: left !important;
    background: rgba(0, 0, 0, 0.3) !important;
    border: 2px solid var(--glass-border) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    color: var(--text-primary) !important;
}

.stTextArea textarea:focus { border-color: var(--gold) !important; }

.output-display {
    background: linear-gradient(135deg, rgba(233, 196, 106, 0.06), rgba(244, 162, 97, 0.03));
    border: 2px solid rgba(233, 196, 106, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    direction: ltr;
    text-align: left;
    font-size: 1.2rem;
    line-height: 2;
    color: var(--text-primary);
    min-height: 150px;
}

mark.error-word {
    background-color: rgba(231, 76, 60, 0.3);
    color: #ff6b6b;
    border-bottom: 2px solid #e74c3c;
    padding: 0 4px;
    border-radius: 3px;
    font-weight: bold;
}

mark.corrected-word {
    background-color: rgba(46, 204, 113, 0.2);
    color: #2ecc71;
    font-weight: bold;
    padding: 0 4px;
    border-radius: 3px;
}

.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.5rem; }
.stat-card {
    background: rgba(26, 26, 62, 0.8);
    border: 1px solid var(--glass-border);
    border-radius: 18px;
    padding: 1.5rem;
    text-align: center;
}
.stat-value { font-size: 2rem; font-weight: 900; color: var(--gold); }
.stat-label { font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.5rem; }

.stButton > button {
    border-radius: 14px !important;
    padding: 0.8rem !important;
    font-weight: bold !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold), var(--orange)) !important;
    color: var(--dark-1) !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. إعداد مكتبة التدقيق الإملائي
# ==========================================
@st.cache_resource
def init_spellchecker():
    # تعمل أوفلاين وتدعم الإنجليزية افتراضياً
    return SpellChecker(language='en')

spell = init_spellchecker()

# ==========================================
# 4. قسم الهيدر (Hero)
# ==========================================
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">📝 المصحح الإملائي الذكي</h1>
    <p class="hero-subtitle">اكتشف الأخطاء الإملائية وصححها فوراً وبدون اتصال بالإنترنت</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. منطقة العمل
# ==========================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">✍️ أدخل النص (باللغة الإنجليزية)</div>', unsafe_allow_html=True)

# مربع الإدخال
user_text = st.text_area(
    label="النص",
    value="Type some text with speling errrs here to test the aplication...",
    height=150,
    label_visibility="collapsed"
)

# الأزرار
col1, col2 = st.columns([4, 1])
with col1:
    check_btn = st.button("🔍 فحص وتصحيح الأخطاء", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ مسح", use_container_width=True)

if clear_btn:
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. المعالجة وعرض النتائج
# ==========================================
if check_btn:
    if not user_text.strip():
        st.warning("⚠️ الرجاء كتابة نص أولاً!")
    else:
        with st.spinner("⏳ جاري فحص النص..."):
            t0 = time.time()
            
            # استخراج الكلمات
            words_only = [m.group(0) for m in re.finditer(r'\b[A-Za-z]+\b', user_text)]
            misspelled = spell.unknown(words_only)
            
            errors_count = len(misspelled)
            
            # دوال فرعية للتلوين والتصحيح (HTML)
            def highlight_errors(match):
                word = match.group(0)
                if word.lower() in misspelled:
                    return f'<mark class="error-word">{word}</mark>'
                return word

            def apply_corrections(match):
                word = match.group(0)
                if word.lower() in misspelled:
                    corr = spell.correction(word)
                    if corr:
                        return f'<mark class="corrected-word">{corr}</mark>'
                return word

            # توليد النصوص
            html_original = re.sub(r'\b[A-Za-z]+\b', highlight_errors, user_text).replace('\n', '<br>')
            html_corrected = re.sub(r'\b[A-Za-z]+\b', apply_corrections, user_text).replace('\n', '<br>')
            
            elapsed = round(time.time() - t0, 3)

            # عرض النتائج في بطاقات زجاجية
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            st.markdown('<div class="card-title">❌ الأخطاء المكتشفة:</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-display">{html_original}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown('<div class="card-title">✅ النص المصحح:</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-display">{html_corrected}</div>', unsafe_allow_html=True)

            # الإحصائيات
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-value">{len(words_only)}</div>
                    <div class="stat-label">إجمالي الكلمات</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #ff6b6b;">{errors_count}</div>
                    <div class="stat-label">أخطاء إملائية</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #2ecc71;">{elapsed}s</div>
                    <div class="stat-label">وقت الفحص</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
