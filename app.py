import streamlit as st
import os
import sys
import subprocess

# ==========================================
# 1. إعدادات الصفحة (يجب أن تكون أول سطر دائماً)
# ==========================================
st.set_page_config(page_title="مُشكِّل النصوص | CATT", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    body { direction: rtl; text-align: right; font-family: 'Arial', sans-serif;}
    .stTextArea textarea { direction: rtl; text-align: right; font-size: 18px;}
    div[role="radiogroup"] { direction: rtl; text-align: right; justify-content: right;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🚀 2. الحل الجذري النهائي (البيئة المعزولة)
# ==========================================
# إنشاء مجلد محلي داخل المشروع (حيث يُسمح لنا بالكتابة والتحميل)
LOCAL_LIB_DIR = os.path.join(os.getcwd(), "catt_workspace")

if not os.path.exists(LOCAL_LIB_DIR):
    with st.spinner("⏳ جاري بناء بيئة عمل آمنة لتجاوز حماية السيرفر (يحدث مرة واحدة فقط)..."):
        os.makedirs(LOCAL_LIB_DIR, exist_ok=True)
        # تثبيت المكتبة حصرياً داخل هذا المجلد المفتوح
        subprocess.run([sys.executable, "-m", "pip", "install", "catt-tashkeel", "--target", LOCAL_LIB_DIR, "--no-deps"])

# إجبار بايثون على إعطاء الأولوية القصوى لهذا المجلد المفتوح بدلاً من مجلد النظام المغلق
if LOCAL_LIB_DIR not in sys.path:
    sys.path.insert(0, LOCAL_LIB_DIR)

# الآن نستدعي المكتبة بأمان، وأي ملفات ستحملها ستذهب لمجلدنا المفتوح!
try:
    from catt_tashkeel import CATTEncoderOnly, CATTEncoderDecoder
except Exception as e:
    st.error(f"❌ خطأ في استدعاء المكتبة: {e}")
    st.stop()

# ==========================================
# 3. وظائف تحميل النماذج (مع تخزين مؤقت)
# ==========================================
@st.cache_resource
def load_eo_model():
    return CATTEncoderOnly()

@st.cache_resource
def load_ed_model():
    return CATTEncoderDecoder()

# ==========================================
# 4. واجهة المستخدم
# ==========================================
st.title("✨ التشكيل الذكي للنصوص (CATT)")
st.markdown("---")

st.markdown("**⚙️ إعدادات التشكيل:**")
model_choice = st.radio(
    "اختر نوع محرك الذكاء الاصطناعي:",
    ["النموذج السريع ⚡ (Encoder-Only)", "النموذج الدقيق 🎯 (Encoder-Decoder)"],
    horizontal=False
)

try:
    if "السريع" in model_choice:
        with st.spinner("⏳ جاري تحميل أوزان النموذج السريع في بيئتنا الآمنة..."):
            model = load_eo_model()
    else:
        with st.spinner("⏳ جاري تحميل أوزان النموذج الدقيق (قد يستغرق وقتاً أطول للتحميل)..."):
            model = load_ed_model()
except Exception as e:
    st.error(f"❌ فشل تحميل أوزان النموذج: {e}")
    st.stop()

# ==========================================
# 5. مربع الإدخال والتشغيل
# ==========================================
user_text = st.text_area("أدخل النص العربي (بدون تشكيل):", height=150, placeholder="مثال: يهدف الذكاء الاصطناعي الى تسهيل حياة الانسان...")

if st.button("تـشـكـيـل الـنـص 🚀", type="primary", use_container_width=True):
    if not user_text.strip():
        st.warning("⚠️ يرجى إدخال نص أولاً.")
    else:
        with st.spinner("⏳ جاري تحليل السياق ووضع الحركات..."):
            try:
                result = model.do_tashkeel(user_text, verbose=False)
                st.success("✅ تمت العملية بنجاح!")
                st.text_area("النتيجة:", value=result, height=150)
            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء التشكيل: {e}")

st.markdown("---")
st.caption("مبني باستخدام CATT-Tashkeel. تم تجاوز حماية السيرفر بنجاح.")
