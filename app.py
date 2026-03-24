import streamlit as st
import time
import re
import difflib

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="المصحح اللغوي بالذكاء الاصطناعي (Gramformer)",
    page_icon="🤖",
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

/* تصميم التعديلات (الأحمر للمحذوف، والأخضر للمضاف) */
mark.error-word {
    background-color: rgba(231, 76, 60, 0.3);
    color: #ff6b6b;
    border-radius: 3px;
    padding: 0 4px;
    font-weight: bold;
}

mark.corrected-word {
    background-color: rgba(46, 204, 113, 0.2);
    color: #2ecc71;
    font-weight: bold;
    padding: 0 4px;
    border-radius: 3px;
    border-bottom: 2px solid #2ecc71;
}

.corrected-text { color: #2ecc71; font-weight: 500; }

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
# 3. تحميل نموذج Gramformer الثقيل
# ==========================================
@st.cache_resource
def load_model():
    # استيراد المكتبة هنا حتى لا تعطل الواجهة عند بدء التشغيل
    from gramformer import Gramformer
    import torch
    
    # تثبيت البذور العشوائية لضمان استقرار النتائج
    def set_seed(seed):
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    
    set_seed(1212)
    # تحميل نموذج المصحح النحوي (models=1)
    gf = Gramformer(models=1, use_gpu=False)
    return gf

try:
    with st.spinner("⏳ جاري تحميل نموذج الذكاء الاصطناعي (قد يستغرق وقتاً في المرة الأولى)..."):
        gf = load_model()
        model_status = "✅ الذكاء الاصطناعي جاهز"
except Exception as e:
    gf = None
    model_status = f"❌ فشل التحميل: {e}"

# ==========================================
# 4. دوال فرعية للمقارنة واستخراج الجمل
# ==========================================
def get_diff_html(original, corrected):
    """تقارن بين النصين وتنتج كود HTML يبرز المحذوف بالاحمر والمضاف بالاخضر"""
    diff = difflib.ndiff(original.split(), corrected.split())
    result = []
    for token in diff:
        if token.startswith('- '):
            result.append(f'<mark class="error-word" style="text-decoration: line-through;" title="خطأ تم حذفه">{token[2:]}</mark>')
        elif token.startswith('+ '):
            result.append(f'<mark class="corrected-word" title="تصحيح مضاف">{token[2:]}</mark>')
        elif token.startswith('  '):
            result.append(token[2:])
    return ' '.join(result)

# ==========================================
# 5. الواجهة الرئيسية
# ==========================================
st.markdown(f"""
<div class="hero-section">
    <h1 class="hero-title">🤖 مصحح Gramformer العميق</h1>
    <p class="hero-subtitle">يستخدم نماذج Hugging Face لفهم السياق وتصحيح أعقد الأخطاء</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown(f'<div class="card-title">✍️ أدخل النص الإنجليزي ({model_status})</div>', unsafe_allow_html=True)

# النص التجريبي المليء بالأخطاء السياقية
test_text = "Last weak, me and my freind goed to the librery to studdy for our finalle examms."

user_text = st.text_area(
    label="النص",
    value=test_text,
    height=150,
    label_visibility="collapsed"
)

col1, col2 = st.columns([4, 1])
with col1:
    check_btn = st.button("🚀 فحص بالذكاء الاصطناعي", type="primary", use_container_width=True)
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
    elif gf is None:
        st.error("❌ النموذج غير متوفر بسبب خطأ في التحميل.")
    else:
        with st.spinner("🧠 يتم تحليل النص وإعادة صياغته..."):
            t0 = time.time()
            
            # تقطيع النص إلى جمل قصيرة لتخفيف الضغط على الـ RAM وزيادة الدقة
            # نقسم بناءً على علامات الترقيم (. ! ?)
            sentences = re.split(r'(?<=[.!?]) +', user_text.strip())
            
            corrected_sentences = []
            
            for sent in sentences:
                if sent.strip():
                    # تصحيح كل جملة على حدة باستخدام Gramformer
                    # max_candidates=1 نطلب منه أفضل اقتراح فقط
                    res = gf.correct(sent, max_candidates=1)
                    corrected_sentences.append(list(res)[0])
            
            # إعادة دمج النص
            final_corrected_text = " ".join(corrected_sentences)
            
            # استخراج الفروقات للتلوين
            diff_html = get_diff_html(user_text, final_corrected_text)
            
            elapsed = round(time.time() - t0, 2)

            # عرض النتائج
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            st.markdown('<div class="card-title">🔍 خريطة التعديلات (الأحمر: محذوف، الأخضر: مصحح):</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-display">{diff_html}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown('<div class="card-title">✅ النص النظيف النهائي:</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-display corrected-text">{final_corrected_text}</div>', unsafe_allow_html=True)

            # الإحصائيات
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-value">{len(user_text.split())}</div>
                    <div class="stat-label">كلمة مفحوصة</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #ff6b6b;">{len(sentences)}</div>
                    <div class="stat-label">جملة تمت معالجتها</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #2ecc71;">{elapsed}s</div>
                    <div class="stat-label">وقت المعالجة</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
