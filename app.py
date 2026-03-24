import streamlit as st
from catt_tashkeel import CATTEncoderOnly, CATTEncoderDecoder

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="مُشكِّل النصوص | CATT", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    body { direction: rtl; text-align: right; font-family: 'Arial', sans-serif;}
    .stTextArea textarea { direction: rtl; text-align: right; font-size: 18px;}
    div[role="radiogroup"] { direction: rtl; text-align: right; justify-content: right;}
    </style>
""", unsafe_allow_html=True)

# 2. وظائف تحميل النماذج (مع التخزين المؤقت لتسريع الأداء)
@st.cache_resource
def load_eo_model():
    return CATTEncoderOnly()

@st.cache_resource
def load_ed_model():
    return CATTEncoderDecoder()

# 3. واجهة المستخدم
st.title("✨ التشكيل الذكي للنصوص (CATT)")
st.markdown("---")

# 4. خيارات النموذج
st.markdown("**⚙️ إعدادات التشكيل:**")
model_choice = st.radio(
    "اختر نوع محرك الذكاء الاصطناعي:",
    ["النموذج السريع ⚡ (Encoder-Only)", "النموذج الدقيق 🎯 (Encoder-Decoder)"],
    horizontal=False
)

# تحميل النموذج المختار في الخلفية
try:
    if "السريع" in model_choice:
        with st.spinner("⏳ جاري تهيئة النموذج السريع..."):
            model = load_eo_model()
    else:
        with st.spinner("⏳ جاري تهيئة النموذج الدقيق (قد يستغرق وقتاً أطول في المرة الأولى)..."):
            model = load_ed_model()
except Exception as e:
    st.error(f"❌ فشل تحميل النموذج: {e}")
    st.stop()

# 5. مربع الإدخال والتشغيل
user_text = st.text_area("أدخل النص العربي (بدون تشكيل):", height=150, placeholder="مثال: يهدف الذكاء الاصطناعي الى تسهيل حياة الانسان...")

if st.button("تـشـكـيـل الـنـص 🚀", type="primary", use_container_width=True):
    if not user_text.strip():
        st.warning("⚠️ يرجى إدخال نص أولاً.")
    else:
        with st.spinner("⏳ جاري تحليل السياق ووضع الحركات..."):
            try:
                # عملية التشكيل
                result = model.do_tashkeel(user_text, verbose=False)
                
                st.success("✅ تمت العملية بنجاح!")
                st.text_area("النتيجة:", value=result, height=150)
            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء التشكيل: {e}")

st.markdown("---")
st.caption("مبني باستخدام CATT-Tashkeel. تطوير الواجهة بواسطة Streamlit.")
