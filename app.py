import streamlit as st
import time
import language_tool_python

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="المصحح اللغوي والنحوي الشامل",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. الواجهة المخصصة (CSS)
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

.card-title { font-size: 1.2rem; font-weight: 700; color: var(--gold); margin-bottom: 1rem; }

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

/* تصميم الكلمات الخاطئة */
mark.error-word {
    background-color: rgba(231, 76, 60, 0.3);
    color: #ff6b6b;
    border-bottom: 2px dashed #e74c3c;
    padding: 0 4px;
    border-radius: 3px;
    font-weight: bold;
    cursor: help;
}

/* تصميم النص المصحح */
.corrected-text {
    color: #2ecc71;
    font-weight: 500;
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
# 3. إعداد مكتبة التدقيق الشامل
# ==========================================
@st.cache_resource
def init_language_tool():
    return language_tool_python.LanguageTool('en-US')

try:
    tool = init_language_tool()
    tool_status = "✅ المكتبة جاهزة"
except Exception as e:
    tool = None
    tool_status = f"❌ حدث خطأ في التهيئة: {e}"

# ==========================================
# 4. قسم الهيدر
# ==========================================
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">✨ المصحح النحوي والإملائي الشامل</h1>
    <p class="hero-subtitle">يكتشف الأخطاء الإملائية، القواعد النحوية، والكلمات المتشابهة بدقة عالية</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. منطقة العمل
# ==========================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown(f'<div class="card-title">✍️ أدخل النص الإنجليزي ({tool_status})</div>', unsafe_allow_html=True)

default_text = "Their are many speling errrs here. He go to the market everyday."

user_text = st.text_area(
    label="النص",
    value=default_text,
    height=150,
    label_visibility="collapsed"
)

col1, col2 = st.columns([4, 1])
with col1:
    check_btn = st.button("🔍 فحص وتصحيح النص", type="primary", use_container_width=True)
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
    elif tool is None:
        st.error("المكتبة غير متوفرة. تأكد من إعدادات الجافا (ملف packages.txt).")
    else:
        with st.spinner("⏳ يتم تحليل القواعد والإملاء..."):
            t0 = time.time()
            
            # فحص النص بالكامل
            matches = tool.check(user_text)
            
            # التصحيح التلقائي
            corrected_text = language_tool_python.utils.correct(user_text, matches)
            
            html_original = ""
            last_end = 0
            
            # ترتيب الأخطاء
            matches.sort(key=lambda m: m.offset)
            
            for m in matches:
                # [إصلاح الخطأ هنا]: استخراج طول الخطأ بشكل آمن يدعم جميع إصدارات المكتبة
                err_len = getattr(m, 'errorLength', getattr(m, 'length', getattr(m, 'error_length', 0)))
                
                # إضافة النص السليم
                html_original += user_text[last_end:m.offset]
                
                # الكلمة الخاطئة
                bad_word = user_text[m.offset:m.offset + err_len]
                
                # رسالة التوضيح
                tooltip_msg = f"{m.message}"
                if m.replacements:
                    tooltip_msg += f" (Suggestions: {', '.join(m.replacements[:3])})"
                
                html_original += f'<mark class="error-word" title="{tooltip_msg}">{bad_word}</mark>'
                
                last_end = m.offset + err_len
            
            # باقي النص
            html_original += user_text[last_end:]
            html_original = html_original.replace('\n', '<br>')
            
            corrected_text_html = corrected_text.replace('\n', '<br>')
            
            elapsed = round(time.time() - t0, 2)

            # عرض النتائج
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            st.markdown('<div class="card-title">🔍 الأخطاء المكتشفة (مرر الماوس فوق الكلمة لمعرفة السبب):</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-display">{html_original}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown('<div class="card-title">✅ النص بعد التصحيح:</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-display corrected-text">{corrected_text_html}</div>', unsafe_allow_html=True)

            # الإحصائيات
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-value">{len(user_text.split())}</div>
                    <div class="stat-label">إجمالي الكلمات</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #ff6b6b;">{len(matches)}</div>
                    <div class="stat-label">أخطاء إملائية/نحوية</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #2ecc71;">{elapsed}s</div>
                    <div class="stat-label">وقت التحليل</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
