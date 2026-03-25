import streamlit as st
import os
import sys
import subprocess
import shutil
import time
from groq import Groq  # [إضافة]: استدعاء مكتبة Groq

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="المساعد اللغوي الشامل | CATT & AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. الواجهة المخصصة الكاملة (لم يتم المساس بها)
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

.stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(233, 196, 106, 0.3);
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
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ══════════════════════════════════ Radio مخصص ══════════════════════════════════ */
div[role="radiogroup"] {
    direction: rtl !important;
    gap: 0.5rem !important;
    margin-bottom: 1rem;
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
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. إعداد Groq و المزايا الـ 14 (جديد)
# ==========================================
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    groq_client = Groq(api_key=groq_api_key)
    groq_status = True
except Exception:
    groq_client = None
    groq_status = False

AI_FEATURES = {
    "التشكيل الذكي": "قم بتشكيل النص العربي التالي تشكيلاً دقيقاً مع مراعاة القواعد النحوية والصرفية. أعد النص المشكل فقط.",
    "الإعراب التفاعلي": "قم بإعراب الجملة التالية إعراباً تفصيلياً كاملاً كلمة بكلمة. قدم النتيجة بشكل واضح ومنسق.",
    "التفقيط النحوي": "حول جميع الأرقام في النص التالي إلى كلمات عربية فصحى مضبوطة بالشكل مع مراعاة قواعد العدد والمعدود والإعراب. أعد النص كاملاً.",
    "مختبر الشعر (العروض)": """أنت عالم لغوي وخبير مرجعي في "علم العروض" العربي. مهمتك هي التحليل العروضي الدقيق والصارم للأبيات الشعرية بناءً على منهج الخليل بن أحمد الفراهيدي.
تحذير صارم: إياك أن تقوم بوزن كل كلمة على حدة. التقطيع العروضي يعتمد على المقطع الصوتي والنطق المستمر، وقد تنقسم الكلمة الواحدة بين تفعيلتين، أو تندمج كلمتان في تفعيلة واحدة.

قم بتحليل البيت المرفق باتباع هذه الخطوات التسلسلية بدقة متناهية:
1. التشكيل الكامل: اكتب البيت مضبوطاً بالشكل التام للتأكد من مواضع الحركات والسكنات.
2. الكتابة العروضية: طبق القاعدة الذهبية "كل ما يُنطق يُكتب، وما لا يُنطق يُحذف". (قم بفك التضعيف إلى ساكن فمتحرك، حول التنوين إلى نون ساكنة، احذف همزات الوصل واللام الشمسية، وأشبع حركة الحرف الأخير). اكتب البيت بالصيغة العروضية.
3. الترميز الصوتي (حركات وسكنات): ضع تحت كل حرف متحرك الرمز (/)، وتحت كل حرف ساكن أو حرف مد الرمز (o).
4. استخراج التفعيلات: قسّم الرموز السابقة إلى التفعيلات الخليلية المعروفة (مثل: فاعلاتن، مستفعلن، مفاعيلن، فعولن، متفاعلن). لا تخترع أي تفعيلة غير موجودة في دوائر الخليل. اذكر الزحافات والعلل إن وُجدت.
5. تحديد البحر الشعري: استناداً إلى التفعيلات التي استخرجتها، حدد اسم البحر الشعري بكل ثقة ويقين. 
قدم إجابتك بشكل منهجي، مرتب، وبدون أي حشو لغوي زائد."""
,
    "التقويم البلاغي والأسلوبي": "أعد صياغة النص التالي ليكون أكثر بلاغة وفصاحة وقوة أدبية، مع الحفاظ على المعنى الأصلي.",
    "التحليل الصرفي واستخراج الجذور": "استخرج جذور كل كلمة في النص، ووزنها الصرفي، ونوعها (اسم، فعل، مصدر..). قدم النتيجة في قائمة منظمة.",
    "التنقيط الذكي وهندسة الفقرات": "أضف علامات الترقيم المناسبة (فواصل، نقاط، علامات تعجب/استفهام) وهندس الفقرات ليصبح النص مقروءاً بشكل سليم. أعد النص فقط.",
    "مترجم اللهجات العامية إلى الفصحى": "قم بترجمة النص العامي التالي إلى لغة عربية فصحى سليمة وبليغة.",
    "استخراج الصور البيانية": "استخرج جميع الصور البيانية (استعارة، تشبيه، كناية) من النص التالي واشرح سر جمالها بالتفصيل.",
    "تصفية النص (التعريب)": "صحح التراكيب المترجمة حرفياً والكلمات الدخيلة في النص، واستبدلها ببدائل عربية فصيحة وأصيلة. أعد النص المصحح.",
    "إعادة الصياغة الموجهة": "أعد صياغة النص التالي بثلاثة أساليب مختلفة: 1. أسلوب رسمي (للتقارير) 2. أسلوب أدبي 3. أسلوب مبسط وواضح.",
    "كاشف الحشو والإطالة": "قم بتنقيح النص التالي بحذف الكلمات الزائدة والحشو المكرر دون الإخلال بالمعنى، ليكون النص موجزاً ومباشراً.",
    "مستشعر اللهجات": "حدد اللهجة العربية المستخدمة في النص (البلد والمنطقة) مع ذكر الكلمات الدلالية التي بنيت عليها استنتاجك.",
    "كاشف المزاج والمشاعر": "حلل المشاعر في النص التالي (إيجابي، سلبي، غاضب، حزين، سعيد، متحمس..) واشرح النبرة العاطفية للكاتب."
}

# ==========================================
# 3. الخلفية المتحركة + شريط التنقل (كما هي)
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
        <span class="nav-badge">v3.0 (Pro)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. قسم Hero (كما هو)
# ==========================================
st.markdown("""
<div class="hero-section">
    <div class="hero-badge"> 🚀 مدعوم بنماذج CATT و ذكاء Groq </div>
    <h1 class="hero-title">
        <span class="gradient-text">المساعد اللغوي العربي الشامل</span>
    </h1>
    <p class="hero-subtitle">
        أضف الحركات، أعرب الكلمات، اكتشف اللهجات، وحلل المشاعر بدقة عالية باستخدام أحدث تقنيات الذكاء الاصطناعي
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. إعداد البيئة لـ CATT (كما هي تماماً)
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

try:
    from catt_tashkeel import CATTEncoderOnly, CATTEncoderDecoder
    LIB_OK = True
except Exception as e:
    LIB_OK = False
    LIB_ERR = str(e)

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
# 6. منطقة العمل الرئيسية (المدمجة)
# ==========================================
st.markdown('<div class="workspace-container">', unsafe_allow_html=True)

# اختيار المحرك (CATT أم Groq)
st.markdown("""
<div class="glass-card">
    <div class="card-header">
        <div class="card-title">
            <div class="card-title-icon">⚙️</div>
            محرك المعالجة والأدوات
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

engine_choice = st.radio(
    "المحرك:",
    ["💻 نموذج CATT المحلي (للتشكيل السريع)", "🧠 ذكاء Groq الاصطناعي (للتحليل الشامل و 14 ميزة)"],
    horizontal=False,
    label_visibility="collapsed"
)

# عرض أدوات المحرك المختار
selected_feature = None
mtype = "fast"
model = None

if "CATT" in engine_choice:
    if not LIB_OK:
        st.error(f"خطأ في مكتبة CATT: {LIB_ERR}")
    else:
        mtype_choice = st.radio("نوع النموذج المحلي:", ["⚡ سريع (Encoder-Only)", "🎯 دقيق (Encoder-Decoder)"], horizontal=True)
        mtype = "fast" if "سريع" in mtype_choice else "accurate"
        with st.spinner("🔄 جاري تحميل نموذج CATT..."):
            model = load_model(mtype)
        st.markdown('<div class="status-pill status-ok"><div class="status-dot"></div>نموذج CATT جاهز ✓</div>', unsafe_allow_html=True)
else:
    if not groq_status:
        st.error("❌ مفتاح Groq غير متوفر في st.secrets. الرجاء إضافته لتعمل المزايا الإضافية.")
    else:
        st.markdown('<div class="status-pill status-ok"><div class="status-dot"></div>ذكاء Groq جاهز ومفعل ✓</div>', unsafe_allow_html=True)
        # هنا قائمة المزايا الـ 14
        selected_feature = st.selectbox(
            "اختر الأداة اللغوية التي تريد تطبيقها على النص:",
            list(AI_FEATURES.keys())
        )

# ==========================================
# 7. الإدخال والإخراج
# ==========================================
st.markdown("""
<div class="glass-card">
    <div class="card-header">
        <div class="card-title">
            <div class="card-title-icon">📝</div>
            النص الأصلي
        </div>
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

c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    btn_label = "✨ تشكيل النص" if "CATT" in engine_choice else f"🚀 تنفيذ: {selected_feature}"
    run_btn = st.button(btn_label, type="primary", use_container_width=True)
with c2:
    clear_btn = st.button("🗑️ مسح", use_container_width=True)
with c3:
    copy_btn = st.button("📋 نسخ", use_container_width=True)

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
            النتيجة والتحليل
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
        '<div class="output-display output-empty"><div class="output-empty-icon">✍️</div><div>النتيجة ستظهر هنا</div></div>',
        unsafe_allow_html=True,
    )

# ==========================================
# 8. تنفيذ المعالجة (CATT أو Groq)
# ==========================================
if run_btn:
    if not user_text.strip():
        st.warning("⚠️ أدخل نصاً أولاً")
    else:
        # ---- المسار الأول: المعالجة المحلية (CATT) ----
        if "CATT" in engine_choice:
            if model is None:
                st.error("❌ النموذج المحلي غير محمّل")
            else:
                saved = os.getcwd()
                os.chdir(WORKSPACE)
                with st.spinner("⏳ جاري التشكيل..."):
                    try:
                        t0 = time.time()
                        result = model.do_tashkeel(user_text, verbose=False)
                        elapsed = round(time.time() - t0, 3)
                        st.session_state["last_result"] = result
                        result_holder.markdown(f'<div class="output-display">{result}</div>', unsafe_allow_html=True)
                        st.success("✅ تم التشكيل بنجاح!")
                        
                        import re
                        words = len(user_text.split())
                        chars = len(re.findall(r"[\u0600-\u06FF]", user_text))
                        
                        st.markdown(f"""
                        <div class="stats-row">
                            <div class="stat-card"><span class="stat-icon">📝</span><span class="stat-value">{words}</span><div class="stat-label">كلمة</div></div>
                            <div class="stat-card"><span class="stat-icon">🔤</span><span class="stat-value">{chars}</span><div class="stat-label">حرف</div></div>
                            <div class="stat-card"><span class="stat-icon">⚡</span><span class="stat-value">{elapsed}s</span><div class="stat-label">الوقت</div></div>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")
                    finally:
                        os.chdir(saved)
                        
        # ---- المسار الثاني: الذكاء الاصطناعي (Groq) ----
        else:
            if not groq_status:
                st.error("❌ لا يمكن تنفيذ العملية لغياب مفتاح Groq.")
            else:
                with st.spinner(f"⏳ جاري تحليل النص باستخدام (Groq) للقيام بـ: {selected_feature}..."):
                    t0 = time.time()
                    try:
                        prompt_system = AI_FEATURES[selected_feature]
                        completion = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": prompt_system},
                                {"role": "user", "content": user_text}
                            ],
                            temperature=0.2,
                        )
                        
                        result_groq = completion.choices[0].message.content.strip()
                        # تنسيق النتيجة للحفاظ على المسافات والأسطر
                        formatted_result = result_groq.replace('\n', '<br>')
                        elapsed = round(time.time() - t0, 2)
                        
                        st.session_state["last_result"] = formatted_result
                        result_holder.markdown(f'<div class="output-display">{formatted_result}</div>', unsafe_allow_html=True)
                        st.success(f"✅ تمت عملية ({selected_feature}) بنجاح!")
                        
                        st.markdown(f"""
                        <div class="stats-row">
                            <div class="stat-card"><span class="stat-icon">🧠</span><span class="stat-value">Groq</span><div class="stat-label">المحرك</div></div>
                            <div class="stat-card"><span class="stat-icon">🎯</span><span class="stat-value">Llama3</span><div class="stat-label">النموذج</div></div>
                            <div class="stat-card"><span class="stat-icon">⚡</span><span class="stat-value">{elapsed}s</span><div class="stat-label">سرعة الاستجابة</div></div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ حدث خطأ في اتصال Groq: {e}")

if copy_btn:
    lr = st.session_state.get("last_result", "")
    if lr:
        st.code(lr.replace('<br>', '\n'), language=None)
        st.info("📋 تم تجهيز النص، يمكنك نسخه الآن.")

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 9. الفوتر
# ==========================================
st.markdown("""
<div class="site-footer">
    <div class="footer-brand">✨ CATT & AI — المساعد اللغوي الشامل</div>
    <div class="footer-text">
        يجمع بين النماذج المحلية للتشكيل وذكاء Groq للتحليل اللغوي العميق<br>
        الإصدار 3.0 المطور
    </div>
</div>
""", unsafe_allow_html=True)
