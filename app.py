import streamlit as st
import os
import stat

# ==========================================
# 🚀 الإصلاح السحري لمشكلة الصلاحيات (Permission Denied)
# ==========================================
import catt_tashkeel

# جلب المسار الذي تم تثبيت المكتبة فيه داخل السيرفر
catt_dir = os.path.dirname(catt_tashkeel.__file__)

try:
    # منح صلاحيات كاملة (قراءة وكتابة وتعديل) للمجلد الرئيسي للمكتبة
    os.chmod(catt_dir, 0o777)
    
    # إذا كان مجلد onnx_models موجوداً ولكن مغلقاً، سنفتحه أيضاً
    onnx_dir = os.path.join(catt_dir, "onnx_models")
    if os.path.exists(onnx_dir):
        os.chmod(onnx_dir, 0o777)
except Exception as e:
    # في حال فشل تغيير الصلاحيات، سيتم طباعة السبب دون إيقاف التطبيق
    st.warning(f"ملاحظة نظام: تعذر تغيير بعض الصلاحيات ({e})")

# الآن يمكننا استدعاء النماذج بأمان بعد أن فتحنا الأبواب
from catt_tashkeel import CATTEncoderOnly, CATTEncoderDecoder

# ==========================================
# 1. إعدادات الصفحة والتصميم
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
# 2. وظائف التحميل
# ==========================================
@st.cache_resource
def load_eo_model():
    return CATTEncoderOnly()

@st.cache_resource
def load_ed_model():
    return CATTEncoderDecoder()

# ==========================================
# 3. الواجهة الرسومية
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
        with st.spinner("⏳ جاري تهيئة النموذج السريع (يحتاج بضع ثوانٍ للتحميل في المرة الأولى)..."):
            model = load_eo_model()
    else:
        with st.spinner("⏳ جاري تهيئة النموذج الدقيق (ملف كبير، قد يستغرق دقيقة للتحميل)..."):
            model = load_ed_model()
except Exception as e:
    st.error(f"❌ فشل تحميل النموذج: {e}")
    st.stop()

# ==========================================
# 4. مربع الإدخال والتشغيل
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
st.caption("مبني باستخدام CATT-Tashkeel. تطوير الواجهة بواسطة Streamlit.")
