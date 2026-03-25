import streamlit as st
import os
import sys
import subprocess
import shutil
import time
import json
import re
from datetime import datetime

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
# 2. إعدادات المكتبات و API Keys (Groq, OpenAI, Gemini)
# ==========================================
# تهيئة Groq
try:
    from groq import Groq
    groq_api_key = st.secrets["GROQ_API_KEY"]
    groq_client = Groq(api_key=groq_api_key)
    groq_status = True
except Exception:
    groq_client = None
    groq_status = False

# تهيئة OpenAI (ChatGPT)
try:
    import openai
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    openai_status = True
except Exception:
    openai_status = False

# تهيئة Gemini
try:
    import google.generativeai as genai
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    gemini_status = True
except Exception:
    gemini_status = False

# ==========================================
# 3. الواجهة المخصصة الكاملة (CSS)
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

.bg-orb-1 { width: 500px; height: 500px; background: var(--gold); top: -150px; right: -150px; animation-delay: 0s; }
.bg-orb-2 { width: 400px; height: 400px; background: var(--purple); bottom: -100px; left: -100px; animation-delay: -7s; }
.bg-orb-3 { width: 300px; height: 300px; background: var(--cyan); top: 50%; left: 50%; transform: translate(-50%, -50%); animation-delay: -14s; }

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

.nav-brand { display: flex; align-items: center; gap: 0.8rem; }
.nav-logo { width: 40px; height: 40px; background: linear-gradient(135deg, var(--gold), var(--orange)); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; box-shadow: 0 4px 15px rgba(233, 196, 106, 0.3); }
.nav-title { font-size: 1.2rem; font-weight: 700; color: var(--gold); letter-spacing: -0.5px; }
.nav-links { display: flex; gap: 2rem; align-items: center; }
.nav-link { color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; font-weight: 500; transition: color 0.3s; cursor: pointer; }
.nav-link:hover { color: var(--gold); }
.nav-badge { background: linear-gradient(135deg, var(--gold), var(--orange)); color: var(--dark-1); padding: 0.4rem 1rem; border-radius: 50px; font-size: 0.85rem; font-weight: 700; }

/* ══════════════════════════════════ القسم الرئيسي (Hero) ══════════════════════════════════ */
.hero-section { position: relative; z-index: 1; text-align: center; padding: 4rem 2rem 3rem; }
.hero-badge { display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(233, 196, 106, 0.1); border: 1px solid rgba(233, 196, 106, 0.2); padding: 0.4rem 1.2rem; border-radius: 50px; font-size: 0.85rem; color: var(--gold); margin-bottom: 1.5rem; }
.hero-title { font-size: 3.5rem; font-weight: 900; line-height: 1.2; margin-bottom: 1rem; }
.hero-title .gradient-text { background: linear-gradient(135deg, var(--gold), var(--orange), var(--gold-light)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-subtitle { font-size: 1.2rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto 2rem; line-height: 1.8; font-weight: 300; }
.hero-stats { display: flex; justify-content: center; gap: 3rem; }
.hero-stat { text-align: center; }
.hero-stat-value { font-size: 1.8rem; font-weight: 900; color: var(--gold); }
.hero-stat-label { font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.2rem; }

/* ══════════════════════════════════ منطقة العمل ══════════════════════════════════ */
.workspace-container { position: relative; z-index: 1; max-width: 1100px; margin: 0 auto; padding: 0 2rem 3rem; }
.glass-card { background: var(--glass); backdrop-filter: blur(20px); border: 1px solid var(--glass-border); border-radius: 24px; padding: 2rem; margin-bottom: 1.5rem; transition: all 0.3s ease; }
.glass-card:hover { border-color: rgba(233, 196, 106, 0.15); background: var(--glass-hover); }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2rem; }
.card-title { display: flex; align-items: center; gap: 0.6rem; font-size: 1.05rem; font-weight: 700; color: var(--text-primary); }
.card-title-icon { width: 32px; height: 32px; background: linear-gradient(135deg, var(--gold), var(--orange)); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; }

/* ══════════════════════════════════ مربعات النص والأزرار ══════════════════════════════════ */
.stTextArea textarea { font-family: 'Noto Naskh Arabic', 'Amiri', serif !important; font-size: 1.3rem !important; line-height: 2.4 !important; direction: rtl !important; text-align: right !important; background: rgba(0, 0, 0, 0.3) !important; border: 2px solid var(--glass-border) !important; border-radius: 16px !important; padding: 1.5rem !important; color: var(--text-primary) !important; transition: all 0.3s ease !important; resize: none !important; }
.stTextArea textarea:focus { border-color: var(--gold) !important; box-shadow: 0 0 0 4px rgba(233, 196, 106, 0.1) !important; background: rgba(0, 0, 0, 0.4) !important; }

.output-display { background: linear-gradient(135deg, rgba(233, 196, 106, 0.06), rgba(244, 162, 97, 0.03), rgba(168, 218, 220, 0.03) ); border: 2px solid rgba(233, 196, 106, 0.2); border-radius: 16px; padding: 2rem; direction: rtl; text-align: right; font-family: 'Noto Naskh Arabic', 'Amiri', serif; font-size: 1.4rem; line-height: 2.8; color: var(--gold-light); min-height: 200px; word-wrap: break-word; position: relative; overflow: hidden; }
.output-display::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--gold), var(--orange), var(--gold)); border-radius: 16px 16px 0 0; }
.output-empty { color: rgba(255, 255, 255, 0.15); font-family: 'Tajawal', sans-serif; font-size: 1rem; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.8rem; min-height: 200px; }
.output-empty-icon { font-size: 2.5rem; opacity: 0.3; }

.stButton > button { font-family: 'Tajawal', sans-serif !important; font-weight: 700 !important; border-radius: 14px !important; padding: 0.8rem 1.5rem !important; font-size: 1.1rem !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; border: none !important; position: relative; overflow: hidden; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, var(--gold), var(--orange)) !important; color: var(--dark-1) !important; box-shadow: 0 4px 20px rgba(233, 196, 106, 0.3) !important; }
.stButton > button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 30px rgba(233, 196, 106, 0.4) !important; }

.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.5rem 0; }
.stat-card { background: linear-gradient(135deg, rgba(26, 26, 62, 0.8), rgba(13, 13, 43, 0.9) ); border: 1px solid var(--glass-border); border-radius: 18px; padding: 1.5rem; text-align: center; transition: all 0.3s ease; position: relative; overflow: hidden; }
.stat-card:hover { transform: translateY(-5px); border-color: rgba(233, 196, 106, 0.3); }
.stat-icon { font-size: 1.5rem; margin-bottom: 0.5rem; display: block; }
.stat-value { font-size: 1.6rem; font-weight: 900; color: var(--gold); display: block; line-height: 1.2; }
.stat-label { font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.3rem; font-weight: 500; }

.status-pill { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1.2rem; border-radius: 50px; font-size: 0.9rem; font-weight: 600; }
.status-ok { background: rgba(46, 204, 113, 0.1); border: 1px solid rgba(46, 204, 113, 0.25); color: #2ecc71; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: #2ecc71; animation: pulse-dot 2s infinite; }
@keyframes pulse-dot { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(0.8); } }

div[role="radiogroup"] { direction: rtl !important; gap: 0.5rem !important; margin-bottom: 1rem; }
div[role="radiogroup"] label { background: var(--glass) !important; border: 1px solid var(--glass-border) !important; border-radius: 12px !important; padding: 0.8rem 1.2rem !important; transition: all 0.3s !important; color: var(--text-primary) !important; }
div[role="radiogroup"] label:hover { border-color: rgba(233, 196, 106, 0.3) !important; background: var(--glass-hover) !important; }
div[role="radiogroup"] label[data-checked="true"] { border-color: var(--gold) !important; background: rgba(233, 196, 106, 0.1) !important; }

.history-item { background: var(--glass); border: 1px solid var(--glass-border); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem; direction: rtl; text-align: right; transition: all 0.3s; }
.history-item:hover { border-color: rgba(233, 196, 106, 0.2); }
.history-feature { color: var(--gold); font-weight: 700; font-size: 0.85rem; }
.history-time { color: var(--text-secondary); font-size: 0.75rem; float: left; }
.history-preview { color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.3rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.live-counter { display: flex; gap: 1.5rem; justify-content: flex-end; direction: rtl; padding: 0.5rem 0; font-size: 0.8rem; color: var(--text-secondary); }
.live-counter-value { color: var(--gold); font-weight: 700; }

.stSelectbox > div > div { background: rgba(0, 0, 0, 0.3) !important; border: 1px solid var(--glass-border) !important; border-radius: 12px !important; color: var(--text-primary) !important; direction: rtl !important; }
.stSelectbox label { color: var(--text-secondary) !important; direction: rtl !important; text-align: right !important; }
.stExpander { background: var(--glass) !important; border: 1px solid var(--glass-border) !important; border-radius: 16px !important; }
.stExpander header { color: var(--text-primary) !important; }

.site-footer { position: relative; z-index: 1; text-align: center; padding: 3rem 2rem; border-top: 1px solid var(--glass-border); margin-top: 3rem; }
.footer-brand { font-size: 1.2rem; font-weight: 700; color: var(--gold); margin-bottom: 0.5rem; }
.footer-text { color: var(--text-secondary); font-size: 0.85rem; line-height: 1.8; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. البرومبت الأكاديمي الصارم (المهام الثلاث)
# ==========================================
ACADEMIC_TASKS = ["الإعراب التفاعلي", "مختبر الشعر (العروض)", "التشكيل الذكي"]

ACADEMIC_SYSTEM_PROMPT = """أنت "سيبويه الذكاء الاصطناعي"، خبير أكاديمي متخصص في علوم النحو والصرف والعروض للغة العربية الفصحى. مهمتك هي أداء واحدة من ثلاث مهام بصرامة أكاديمية مطلقة، دون أي إضافات أو شروحات جانبية، ودون المساس بالنص الأصلي.

عندما يطلب منك المستخدم مهمة، يجب أن تلتزم بالقواعد التالية التزاماً تاماً:

1. إذا كانت المهمة [الإعراب]:
- قم بإعراب النص كلمة بكلمة أو جملة بجملة بشكل تفصيلي.
- التزم بالمصطلحات النحوية الكلاسيكية المعتمدة (مبتدأ، خبر، فاعل، مفعول به، مجرور، مجزوم، إلخ).
- إياك واختراع أي مصطلحات نحوية غير موجودة في المراجع العربية المعتمدة.
- نسّق النتيجة في جدول أو نقاط واضحة (الكلمة: إعرابها).

2. إذا كانت المهمة [مختبر العروض والتقطيع]:
- قم بتفكيك البيت الشعري بخطوات رياضية دقيقة:
  أولاً: الكتابة العروضية (ما يُنطق يُكتب، وما لا يُنطق يُحذف).
  ثانياً: الرموز العروضية (حركة /، سكون 0).
  ثالثاً: التفعيلات (مثل: فاعلن، مستفعلن، مفاعيلن).
  رابعاً: البحر الشعري (تحديد اسم البحر بدقة بناءً على التفعيلات).
- لا تقم بوزن كل كلمة على حدة، بل زِن الشطر كاملاً ككتلة صوتية واحدة.

3. إذا كانت المهمة [التشكيل الآلي]:
- قم بتشكيل النص المُدخل تشكيلاً كاملاً (بنية الكلمة وأواخرها) بناءً على موقعها الإعرابي الدقيق.
- [شرط حرج]: إياك أن تغير، تبدل، تضيف، أو تحذف أي كلمة أو حرف من النص الأصلي. مهمتك إضافة الحركات فقط.

[توجيهات الإخراج]:
أعطني النتيجة مباشرة ومنسقة بشكل جميل باستخدام Markdown. لا تبدأ بعبارات مثل "بالتأكيد" أو "إليك الإعراب"، ولا تختم بنصائح. أعطني النتيجة العلمية فقط."""

# ==========================================
# 5. البروبتات الثورية (Groq) للمهام الأخرى
# ==========================================
AI_FEATURES = {
    # المهام الأكاديمية (البرومبت الخاص بها موجود في ACADEMIC_SYSTEM_PROMPT أعلاه، هذا فقط لإظهارها في القائمة)
    "التشكيل الذكي": {"icon": "✏️", "category": "أكاديمي", "temp": 0.0, "prompt": "هذا البرومبت موجه داخلياً للأكاديمي"},
    "الإعراب التفاعلي": {"icon": "🔬", "category": "أكاديمي", "temp": 0.0, "prompt": "هذا البرومبت موجه داخلياً للأكاديمي"},
    "مختبر الشعر (العروض)": {"icon": "🎵", "category": "أكاديمي", "temp": 0.0, "prompt": "هذا البرومبت موجه داخلياً للأكاديمي"},

    # ━━━━━━━━━━━━━━━━━ باقي المهام الصاروخية لـ Groq ━━━━━━━━━━━━━━━━━
    "التفقيط النحوي": {
        "icon": "🔢", "category": "أساسيات", "temp": 0.1,
        "prompt": "أنت متخصص في قاعدة العدد والمعدود. حوّل كل رقم في النص إلى كلمات عربية فصيحة مشكّلة مع تطبيق قواعد العدد والمعدود بصرامة واستخرج جدولاً يوضح كل رقم وتحويله."
    },
    "التقويم البلاغي والأسلوبي": {
        "icon": "💎", "category": "تحسين", "temp": 0.4,
        "prompt": "أنت كاتب بليغ. ارتقِ بالنص المُدخل ليصبح فصيحاً وبليغاً مع الحفاظ الكامل على المعنى، وأضف لمسات جمالية وأدوات ربط منطقية، ثم اعرض النص المحسن وأبرز التعديلات."
    },
    "التحليل الصرفي واستخراج الجذور": {
        "icon": "🌳", "category": "أساسيات", "temp": 0.1,
        "prompt": "أنت عالم صرف عربي دقيق. حلل الكلمات الرئيسية في النص تحليلاً صرفياً شاملاً مستخرجاً الجذر والوزن والنوع والمعنى الصرفي في جدول دقيق."
    },
    "التنقيط الذكي وهندسة الفقرات": {
        "icon": "📐", "category": "تحسين", "temp": 0.15,
        "prompt": "أنت منسق نصوص. أعد تنظيم النص بإضافة علامات الترقيم الصحيحة وتقسيمه إلى فقرات منطقية دون تغيير أي كلمة."
    },
    "مترجم اللهجات إلى الفصحى": {
        "icon": "🗣️", "category": "ترجمة", "temp": 0.3,
        "prompt": "أنت مترجم لهجات. اقرأ النص العامي، حدد اللهجة، ثم ترجمه إلى فصحى بليغة معاصرة مع إدراج مسرد للمفردات العامية ومعناها."
    },
    "استخراج الصور البيانية": {
        "icon": "🎨", "category": "بلاغة", "temp": 0.2,
        "prompt": "أنت ناقد بلاغي. استخرج كل صورة بيانية (تشبيه، استعارة، كناية، مجاز مرسل) مع شرحها وبيان سر جمالها. لا تخترع صوراً غير موجودة."
    },
    "تصفية النص (التعريب)": {
        "icon": "🧹", "category": "تحسين", "temp": 0.2,
        "prompt": "أنت حارس اللغة. نقّ النص من التراكيب المترجمة حرفياً والأخطاء الشائعة والكلمات الأجنبية، وقدم النص المنقى مع جدول يوضح التصحيحات."
    },
    "إعادة الصياغة الموجهة": {
        "icon": "🔄", "category": "تحسين", "temp": 0.5,
        "prompt": "أعد صياغة النص بثلاثة أساليب: أسلوب رسمي رصين، أسلوب أدبي عاطفي، وأسلوب مبسط جداً للأطفال والعوام."
    },
    "كاشف الحشو والإطالة": {
        "icon": "✂️", "category": "تحسين", "temp": 0.2,
        "prompt": "أنت محرر صارم. احذف كل حشو لغوي أو تكرار مترادف من النص، وقدم النص الموجز مع تقرير تخفيض يوضح نسبة الكلمات المحذوفة والسبب."
    },
    "مستشعر اللهجات": {
        "icon": "🌍", "category": "تحليل", "temp": 0.2,
        "prompt": "أنت عالم لسانيات اجتماعية. حلل النص العامي لتحديد مصدره الجغرافي (الدولة/المنطقة) واذكر الكلمات الدالة التي قادتك لهذا الاستنتاج."
    },
    "كاشف المزاج والمشاعر": {
        "icon": "💭", "category": "تحليل", "temp": 0.25,
        "prompt": "أنت محلل نفسي لغوي. حلل المشاعر المهيمنة في النص والنبرة النفسية للكاتب، واستخرج الكلمات الدالة على تلك الحالة."
    },
    "تصحيح الأخطاء الإملائية والنحوية": {
        "icon": "🔧", "category": "أساسيات", "temp": 0.1,
        "prompt": "أنت مصحح لغوي دقيق. صحح جميع الأخطاء الإملائية والنحوية، وضع جدولاً يوضح الخطأ، والتصحيح، والقاعدة المنطبقة."
    },
    "تلخيص النصوص": {
        "icon": "📄", "category": "تحليل", "temp": 0.2,
        "prompt": "لخص النص بثلاثة مستويات: تلخيص فائق (جملة واحدة)، تلخيص مكثف (فقرة)، وتلخيص نقطي للأفكار الرئيسية."
    },
    "مولّد المرادفات والأضداد": {
        "icon": "🔀", "category": "معجم", "temp": 0.3,
        "prompt": "لكل كلمة رئيسية في النص، وفر شبكة معجمية تتضمن: المرادفات، الأضداد، الكلمات ذات الصلة، واستخدامها في جملة قصيرة."
    },
    "توليد أسئلة اختبارية من النص": {
        "icon": "❓", "category": "تعليم", "temp": 0.4,
        "prompt": "أنشئ أسئلة اختبارية من النص تتضمن: أسئلة فهم مباشر، أسئلة استنتاج، أسئلة اختيار من متعدد، وأسئلة صح أم خطأ مع الإجابات."
    },
    "الترجمة الاحترافية (إنجليزي ↔ عربي)": {
        "icon": "🌐", "category": "ترجمة", "temp": 0.2,
        "prompt": "أنت مترجم محترف. ترجم النص بين الإنجليزية والعربية باحترافية وتصرف لغوي طبيعي دون ترجمة حرفية ركيكة."
    },
    "محلل بنية النص": {
        "icon": "🏗️", "category": "تحليل", "temp": 0.2,
        "prompt": "أنت محلل نصوص. تفكك النص هيكلياً مبدياً نوعه، بنيته الكلية، أدوات الربط، تماسك الفقرات، ومستوى اللغة المستخدمة."
    }
}

SAMPLE_TEXTS = {
    "نثر أدبي": "ان الذين يحسنون الظن بالحياة لا يخسرون شيئا حتى لو اكتشفوا في النهاية ان الحياة لم تكن بالجمال الذي تصوروه فقد عاشوا اجمل اللحظات وهم يحلمون",
    "شعر عربي": "قِفَا نَبكِ مِن ذِكرى حَبيبٍ وَمَنزِلِ    بِسِقطِ اللِّوى بَينَ الدَّخولِ فَحَومَلِ",
    "نص عامي مصري": "انا رحت السوق امبارح واشتريت حاجات كتير بس الاسعار كانت غالية اوي والحر كان مش طبيعي",
    "نص عامي خليجي": "هالحين انا بالبيت وابي اروح السوق بس الجو حار واجد والله ما ابي اطلع",
    "نص به أخطاء": "ذهبو الطلاب الى المدرسه وكانو سعداء بالعوده إلي الدراسه لاكن بعض الطلاب لم يأتو",
    "نص للتلخيص": "تعتبر القراءة من أهم الوسائل التي يستخدمها الإنسان لاكتساب المعرفة والثقافة والعلوم المختلفة فهي تفتح آفاقا واسعة أمام القارئ وتجعله يتعرف على ثقافات وحضارات مختلفة كما أنها تنمي مهارات التفكير النقدي والتحليلي وتساعد على تطوير اللغة وزيادة المفردات وتحسين مهارات الكتابة والتعبير",
    "نص بأرقام": "حضر 15 طالب و7 طالبة الى المحاضرة التي استمرت 3 ساعات وناقشوا 12 موضوع مختلف",
    "نص للترجمة (EN)": "Artificial intelligence is transforming the way we interact with technology, making our lives more efficient and connected than ever before.",
}

# ==========================================
# 6. الخلفية المتحركة + شريط التنقل + Hero
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
        <span class="nav-badge">v4.0 (Pro+ Hybrid)</span>
    </div>
</div>
""", unsafe_allow_html=True)

feature_count = len(AI_FEATURES)
st.markdown(f"""
<div class="hero-section">
    <div class="hero-badge"> 🚀 مدعوم بالتوجيه الذكي (CATT Offline, Groq, GPT-4o, Gemini 2.5) </div>
    <h1 class="hero-title">
        <span class="gradient-text">المساعد اللغوي العربي الهجين</span>
    </h1>
    <p class="hero-subtitle">
        {feature_count} أداة ذكية بمسارات توجيه تلقائية تضمن أعلى دقة للمهام الأكاديمية وأعلى سرعة للمهام الإبداعية.
    </p>
    <div class="hero-stats">
        <div class="hero-stat"><div class="hero-stat-value">{feature_count}</div><div class="hero-stat-label">أداة ذكية</div></div>
        <div class="hero-stat"><div class="hero-stat-value">4</div><div class="hero-stat-label">محركات (AI & Local)</div></div>
        <div class="hero-stat"><div class="hero-stat-value">∞</div><div class="hero-stat-label">دقة أكاديمية</div></div>
        <div class="hero-stat"><div class="hero-stat-value">&lt;3s</div><div class="hero-stat-label">للمسار السريع</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. إعداد البيئة لـ CATT (للتشغيل بدون إنترنت)
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
        subprocess.run([sys.executable, "-m", "pip", "install", "catt-tashkeel", "--target", LOCAL_LIB, "--no-deps", "--quiet"], check=False)
    search_paths = [
        os.path.join(sys.prefix, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages", "catt_tashkeel", "onnx_models"),
        os.path.join(LOCAL_LIB, "catt_tashkeel", "onnx_models"),
    ]
    for src in search_paths:
        if os.path.exists(src) and os.listdir(src):
            if not os.path.exists(MODELS_DIR) or not os.listdir(MODELS_DIR):
                try:
                    shutil.copytree(src, MODELS_DIR)
                    break
                except Exception:
                    continue

if "env_ready" not in st.session_state:
    with st.spinner(""):
        setup_environment()
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
        return CATTEncoderOnly() if mtype == "fast" else CATTEncoderDecoder()
    except Exception:
        import catt_tashkeel as ct
        src = os.path.join(os.path.dirname(ct.__file__), "onnx_models")
        if os.path.exists(src):
            for f in os.listdir(src):
                sf = os.path.join(src, f)
                df = os.path.join(MODELS_DIR, f)
                if not os.path.exists(df):
                    try: shutil.copy2(sf, df)
                    except: pass
        return CATTEncoderOnly() if mtype == "fast" else CATTEncoderDecoder()
    finally:
        os.chdir(original)

# Session State Init
if "history" not in st.session_state: st.session_state["history"] = []
if "last_result" not in st.session_state: st.session_state["last_result"] = ""
if "last_result_raw" not in st.session_state: st.session_state["last_result_raw"] = ""
if "user_input" not in st.session_state: st.session_state["user_input"] = ""

# ==========================================
# 8. منطقة العمل الرئيسية (التوجيه الذكي)
# ==========================================
st.markdown('<div class="workspace-container">', unsafe_allow_html=True)
st.markdown("""
<div class="glass-card">
    <div class="card-header">
        <div class="card-title">
            <div class="card-title-icon">⚙️</div>
            محرك المعالجة والتوجيه الذكي
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

engine_choice = st.radio(
    "المحرك:",
    ["💻 نموذج CATT المحلي (للتشكيل السريع وبدون إنترنت)", "🧠 الذكاء الاصطناعي السحابي (توجيه ذكي عبر API)"],
    horizontal=False,
    label_visibility="collapsed"
)

selected_feature = None
academic_model_choice = None
groq_model_name = None

if "CATT" in engine_choice:
    if not LIB_OK:
        st.error(f"خطأ في مكتبة CATT: {LIB_ERR}")
    else:
        mtype_choice = st.radio("النموذج المحلي:", ["⚡ سريع (Encoder-Only)", "🎯 دقيق (Encoder-Decoder)"], horizontal=True)
        mtype = "fast" if "سريع" in mtype_choice else "accurate"
        model = load_model(mtype)
        st.markdown('<div class="status-pill status-ok"><div class="status-dot"></div>نموذج CATT المحلي جاهز للعمل ✓</div>', unsafe_allow_html=True)
else:
    # واجهة الذكاء الاصطناعي
    feature_display_list = [f"{AI_FEATURES[f]['icon']} {f}" for f in AI_FEATURES.keys()]
    selected_display = st.selectbox("اختر الأداة اللغوية:", feature_display_list)
    selected_feature = selected_display.split(" ", 1)[1] if selected_display else None

    # التوجيه الذكي
    if selected_feature in ACADEMIC_TASKS:
        st.info("🎯 **المسار الأكاديمي الصارم:** هذه المهمة تتطلب دقة رياضية وقواعد صارمة، تم توجيهها للنماذج الكبرى لمنع الهلوسة.")
        academic_model_choice = st.selectbox("اختر المحرك الأكاديمي:", ["🤖 ChatGPT (GPT-4o)", "✨ Gemini (2.5 Pro)"])
        
        if "ChatGPT" in academic_model_choice and not openai_status:
            st.error("❌ مفتاح OpenAI غير متوفر في st.secrets.")
        if "Gemini" in academic_model_choice and not gemini_status:
            st.error("❌ مفتاح Gemini غير متوفر في st.secrets.")
    else:
        st.success("⚡ **المسار الإبداعي السريع:** هذه المهمة تتطلب إبداعاً وسرعة، تم توجيهها لنماذج Groq الصاروخية.")
        if not groq_status:
            st.error("❌ مفتاح Groq غير متوفر في st.secrets.")
        else:
            groq_model_name = st.selectbox(
                "اختر نموذج Groq:", 
                ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"]
            )

# ──────── النصوص التجريبية ────────
st.markdown('<div class="glass-card"><div class="card-header"><div class="card-title"><div class="card-title-icon">🧪</div>نصوص تجريبية جاهزة</div></div></div>', unsafe_allow_html=True)
sample_cols = st.columns(4)
sample_keys = list(SAMPLE_TEXTS.keys())
for i, col in enumerate(sample_cols):
    start = i * 2
    for j in range(2):
        idx = start + j
        if idx < len(sample_keys):
            key = sample_keys[idx]
            with col:
                if st.button(f"📎 {key}", key=f"sample_{idx}", use_container_width=True):
                    st.session_state["user_input"] = SAMPLE_TEXTS[key]
                    st.rerun()

# ──────── الإدخال ────────
st.markdown('<div class="glass-card"><div class="card-header"><div class="card-title"><div class="card-title-icon">📝</div>النص الأصلي</div></div></div>', unsafe_allow_html=True)
user_text = st.text_area(label="النص", value=st.session_state.get("user_input", ""), height=180, placeholder="اكتب أو الصق النص هنا...", label_visibility="collapsed")

if user_text:
    word_count = len(user_text.split())
    char_count = len(user_text)
    arabic_chars = len(re.findall(r"[\u0600-\u06FF]", user_text))
    st.markdown(f"""
    <div class="live-counter">
        <div class="live-counter-item">📝 كلمات: <span class="live-counter-value">{word_count}</span></div>
        <div class="live-counter-item">🔤 أحرف: <span class="live-counter-value">{char_count}</span></div>
        <div class="live-counter-item">🔠 عربي: <span class="live-counter-value">{arabic_chars}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ──────── أزرار التحكم ────────
c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
with c1: run_btn = st.button("🚀 تنفيذ المهمة", type="primary", use_container_width=True)
with c2: clear_btn = st.button("🗑️ مسح", use_container_width=True)
with c3: copy_btn = st.button("📋 نسخ", use_container_width=True)
with c4: export_btn = st.button("💾 تصدير", use_container_width=True)

if clear_btn:
    st.session_state["user_input"] = ""; st.session_state["last_result"] = ""; st.session_state["last_result_raw"] = ""; st.rerun()

# ──────── النتيجة ────────
st.markdown('<div class="glass-card"><div class="card-header"><div class="card-title"><div class="card-title-icon">✨</div>النتيجة والتحليل</div></div></div>', unsafe_allow_html=True)
result_holder = st.empty()

if "last_result" in st.session_state and st.session_state["last_result"]:
    result_holder.markdown(f'<div class="output-display">{st.session_state["last_result"]}</div>', unsafe_allow_html=True)
else:
    result_holder.markdown('<div class="output-display output-empty"><div class="output-empty-icon">✍️</div><div>النتيجة ستظهر هنا بعد التنفيذ</div></div>', unsafe_allow_html=True)

# ==========================================
# 9. محرك التنفيذ والتوجيه (Execution & Routing Logic)
# ==========================================
if run_btn:
    if not user_text.strip():
        st.warning("⚠️ أدخل نصاً أولاً أو اختر نصاً تجريبياً")
    else:
        t0 = time.time()
        result_text = ""
        used_model = ""

        # ──── المسار الأول: CATT (محلي) ────
        if "CATT" in engine_choice:
            saved = os.getcwd()
            os.chdir(WORKSPACE)
            with st.spinner("⏳ جاري التشكيل بنموذج CATT المحلي..."):
                try:
                    result_text = model.do_tashkeel(user_text, verbose=False)
                    used_model = "CATT Offline"
                except Exception as e: st.error(f"❌ خطأ: {e}")
                finally: os.chdir(saved)

        # ──── المسار الثاني: الذكاء الاصطناعي السحابي ────
        else:
            # مسار 2-أ: المهام الأكاديمية الصارمة (GPT-4o أو Gemini 2.5)
            if selected_feature in ACADEMIC_TASKS:
                task_instruction = f"المهمة المطلوبة: [{selected_feature}]\n\nالنص المُراد تحليله:\n{user_text}"
                
                if "ChatGPT" in academic_model_choice and openai_status:
                    with st.spinner("⏳ جاري التحليل الأكاديمي الصارم عبر GPT-4o..."):
                        try:
                            response = openai.chat.completions.create(
                                model="gpt-4o",
                                messages=[
                                    {"role": "system", "content": ACADEMIC_SYSTEM_PROMPT},
                                    {"role": "user", "content": task_instruction}
                                ],
                                temperature=0.0
                            )
                            result_text = response.choices[0].message.content
                            used_model = "GPT-4o"
                        except Exception as e: st.error(f"❌ خطأ في اتصال OpenAI: {e}")
                
                elif "Gemini" in academic_model_choice and gemini_status:
                    with st.spinner("⏳ جاري التحليل الأكاديمي الصارم عبر Gemini 2.5 Pro..."):
                        try:
                            model_g = genai.GenerativeModel(
                                "gemini-2.5-pro",
                                system_instruction=ACADEMIC_SYSTEM_PROMPT
                            )
                            response = model_g.generate_content(
                                task_instruction,
                                generation_config=genai.types.GenerationConfig(temperature=0.0)
                            )
                            result_text = response.text
                            used_model = "Gemini 2.5 Pro"
                        except Exception as e: st.error(f"❌ خطأ في اتصال Gemini: {e}")

            # مسار 2-ب: المهام الإبداعية الصاروخية (Groq)
            else:
                if groq_status:
                    feature_temp = AI_FEATURES.get(selected_feature, {}).get("temp", 0.2)
                    feature_prompt = AI_FEATURES.get(selected_feature, {}).get("prompt", "")
                    with st.spinner(f"⏳ جاري التنفيذ السريع عبر Groq ({groq_model_name})..."):
                        try:
                            completion = groq_client.chat.completions.create(
                                model=groq_model_name,
                                messages=[
                                    {"role": "system", "content": feature_prompt},
                                    {"role": "user", "content": f"النص المطلوب معالجته:\n\n{user_text}"}
                                ],
                                temperature=feature_temp,
                                max_tokens=4096,
                            )
                            result_text = completion.choices[0].message.content
                            used_model = groq_model_name
                        except Exception as e: st.error(f"❌ خطأ في اتصال Groq: {e}")

        # ──── عرض النتيجة وتحديث السجل ────
        if result_text:
            elapsed = round(time.time() - t0, 2)
            formatted_result = result_text.replace('\n', '<br>')
            st.session_state["last_result"] = formatted_result
            st.session_state["last_result_raw"] = result_text
            result_holder.markdown(f'<div class="output-display">{formatted_result}</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-card"><span class="stat-icon">🤖</span><span class="stat-value" style="font-size: 1.2rem;">{used_model.split('-')[0].upper()}</span><div class="stat-label">المحرك</div></div>
                <div class="stat-card"><span class="stat-icon">⚡</span><span class="stat-value">{elapsed}s</span><div class="stat-label">زمن الاستجابة</div></div>
                <div class="stat-card"><span class="stat-icon">📝</span><span class="stat-value">{len(user_text.split())}</span><div class="stat-label">كلمة عولجت</div></div>
            </div>
            """, unsafe_allow_html=True)

            feature_name = selected_feature if not "CATT" in engine_choice else "التشكيل المحلي (CATT)"
            st.session_state["history"].insert(0, {
                "feature": feature_name,
                "input_preview": user_text[:60] + "..." if len(user_text) > 60 else user_text,
                "time": datetime.now().strftime("%H:%M:%S"),
                "elapsed": f"{elapsed}s",
                "model": used_model
            })

# ──── النسخ والتصدير ────
if copy_btn:
    lr = st.session_state.get("last_result_raw", "")
    if lr:
        st.code(lr, language=None)
        st.info("📋 تم تجهيز النص أعلاه. حدده وانسخه (Ctrl+C).")

if export_btn:
    lr = st.session_state.get("last_result_raw", "")
    if lr:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(label="⬇️ تحميل كملف نصي", data=lr, file_name=f"catt_result_{timestamp}.txt", mime="text/plain", use_container_width=True)

# ==========================================
# 10. سجل العمليات & الفوتر
# ==========================================
if st.session_state.get("history"):
    st.markdown('<div class="glass-card"><div class="card-header"><div class="card-title"><div class="card-title-icon">📜</div>سجل العمليات</div></div></div>', unsafe_allow_html=True)
    with st.expander(f"📜 عرض السجل ({len(st.session_state['history'])} عملية)", expanded=False):
        for item in st.session_state["history"][:10]:
            st.markdown(f"""
            <div class="history-item">
                <span class="history-time">{item.get('time', '')} <b>({item.get('model', '')})</b></span>
                <span class="history-feature">🔹 {item.get('feature', '')}</span>
                <span style="color: var(--text-secondary); font-size: 0.75rem; margin-right: 1rem;">⏱️ {item.get('elapsed', '')}</span>
                <div class="history-preview">{item.get('input_preview', '')}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ مسح السجل"): st.session_state["history"] = []; st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="site-footer">
    <div class="footer-brand">✨ CATT & AI — المساعد اللغوي الهجين</div>
    <div class="footer-text">
        توجيه ذكي بين CATT (للتشغيل محلياً)، Groq (للسرعة والإبداع)، و GPT-4o / Gemini 2.5 (للدقة الأكاديمية).<br>
        الإصدار 4.0 Pro+ Hybrid
    </div>
</div>
""", unsafe_allow_html=True)
