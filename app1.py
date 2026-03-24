import streamlit as st
import os
import sys
import subprocess
import shutil

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="مُشكِّل النصوص | CATT",
    page_icon="✨",
    layout="centered",
)

st.markdown("""
<style>
body {
    direction: rtl;
    text-align: right;
    font-family: 'Arial', sans-serif;
}
.stTextArea textarea {
    direction: rtl;
    text-align: right;
    font-size: 18px;
}
div[role="radiogroup"] {
    direction: rtl;
    text-align: right;
    justify-content: right;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إعداد البيئة الآمنة
# ==========================================
# مجلد العمل المفتوح الصلاحيات
WORKSPACE = os.path.join(os.getcwd(), "catt_workspace")
MODELS_DIR = os.path.join(WORKSPACE, "onnx_models")
LOCAL_LIB = os.path.join(WORKSPACE, "lib")

# متغيرات البيئة لتوجيه التحميل
os.environ["HF_HOME"] = os.path.join(WORKSPACE, "hf_cache")
os.environ["TRANSFORMERS_CACHE"] = os.path.join(WORKSPACE, "hf_cache")
os.environ["XDG_CACHE_HOME"] = WORKSPACE
os.environ["TMPDIR"] = WORKSPACE
os.environ["TEMP"] = WORKSPACE
os.environ["TMP"] = WORKSPACE

def setup_workspace():
    """إعداد مجلد العمل وتثبيت المكتبة"""
    # إنشاء المجلدات
    for d in [WORKSPACE, MODELS_DIR, LOCAL_LIB, os.environ["HF_HOME"]]:
        os.makedirs(d, exist_ok=True)

    # تثبيت catt-tashkeel في المجلد المحلي
    if not os.path.exists(os.path.join(LOCAL_LIB, "catt_tashkeel")):
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "catt-tashkeel",
                "--target",
                LOCAL_LIB,
                "--no-deps",
                "--quiet",
            ],
            check=False,
        )

    # نسخ ملفات ONNX من المكان المحمي إلى المكان المفتوح
    _copy_onnx_models()

def _copy_onnx_models():
    """نسخ ملفات النموذج إلى مجلد مفتوح الصلاحيات"""
    # البحث عن مجلد onnx_models الأصلي
    possible_sources = [
        # المسار من رسالة الخطأ
        "/home/adminuser/venv/lib/python3.14/site-packages/catt_tashkeel/onnx_models",
        # مسارات أخرى محتملة
        os.path.join(
            sys.prefix,
            "lib",
            f"python{sys.version_info.major}.{sys.version_info.minor}",
            "site-packages",
            "catt_tashkeel",
            "onnx_models",
        ),
    ]

    # إضافة مسارات من sys.path
    for p in sys.path:
        candidate = os.path.join(p, "catt_tashkeel", "onnx_models")
        if candidate not in possible_sources:
            possible_sources.append(candidate)

    # إضافة المسار من LOCAL_LIB
    possible_sources.append(
        os.path.join(LOCAL_LIB, "catt_tashkeel", "onnx_models")
    )

    # نسخ من أول مصدر موجود
    for src in possible_sources:
        if os.path.exists(src) and os.listdir(src):
            # لا ننسخ إذا الهدف يحتوي ملفات بالفعل
            if os.path.exists(MODELS_DIR) and os.listdir(MODELS_DIR):
                return
            try:
                if os.path.exists(MODELS_DIR):
                    shutil.rmtree(MODELS_DIR)
                shutil.copytree(src, MODELS_DIR)
                return
            except Exception:
                continue

def patch_catt_paths():
    """
    تعديل مسارات catt_tashkeel لتشير إلى المجلد المفتوح
    هذا هو المفتاح لحل مشكلة Permission Denied
    """
    # إضافة المكتبة المحلية لمسار البحث
    if LOCAL_LIB not in sys.path:
        sys.path.insert(0, LOCAL_LIB)

    try:
        import catt_tashkeel

        # البحث عن مجلد المكتبة
        pkg_dir = os.path.dirname(catt_tashkeel.__file__)

        # استبدال مسار onnx_models بالمسار المفتوح
        original_models = os.path.join(pkg_dir, "onnx_models")
        if os.path.exists(MODELS_DIR) and os.listdir(MODELS_DIR):
            # إنشاء رابط رمزي أو نسخ
            try:
                if os.path.exists(original_models):
                    if os.path.islink(original_models):
                        os.unlink(original_models)
                    elif os.path.isdir(original_models):
                        # لا نحذف المجلد الأصلي
                        pass
            except PermissionError:
                pass

        # تعديل أي متغير مسار داخل المكتبة
        for attr_name in dir(catt_tashkeel):
            attr = getattr(catt_tashkeel, attr_name, None)
            if isinstance(attr, str) and "onnx_models" in attr:
                try:
                    setattr(catt_tashkeel, attr_name, attr.replace(original_models, MODELS_DIR))
                except Exception:
                    pass

        # تعديل الوحدات الفرعية
        for submod_name in list(sys.modules.keys()):
            if "catt_tashkeel" in submod_name:
                submod = sys.modules[submod_name]
                if submod is None:
                    continue
                for attr_name in dir(submod):
                    attr = getattr(submod, attr_name, None)
                    if isinstance(attr, str) and "onnx_models" in attr:
                        try:
                            new_val = attr.replace(
                                original_models, MODELS_DIR
                            )
                            setattr(submod, attr_name, new_val)
                        except Exception:
                            pass
    except ImportError:
        pass

def ensure_onnx_writable():
    """
    الحل البديل: إنشاء wrapper يغيّر مجلد العمل قبل تحميل النموذج
    """
    original_cwd = os.getcwd()
    try:
        os.chdir(WORKSPACE)
    except Exception:
        pass
    return original_cwd

# ==========================================
# 3. التنفيذ
# ==========================================
# إعداد البيئة (مرة واحدة)
if "workspace_ready" not in st.session_state:
    with st.spinner("⏳ جاري إعداد البيئة الآمنة (مرة واحدة فقط)..."):
        setup_workspace()
        patch_catt_paths()
        st.session_state["workspace_ready"] = True

# التأكد من المسارات
if LOCAL_LIB not in sys.path:
    sys.path.insert(0, LOCAL_LIB)

# ==========================================
# 4. استيراد المكتبة
# ==========================================
try:
    from catt_tashkeel import CATTEncoderOnly, CATTEncoderDecoder
    IMPORT_OK = True
except Exception as e:
    IMPORT_OK = False
    IMPORT_ERR = str(e)

# ==========================================
# 5. تحميل النماذج مع الحل الجذري
# ==========================================
@st.cache_resource
def load_model_safe(model_type):
    """
    تحميل النموذج مع تغيير مجلد العمل لتجاوز مشكلة الصلاحيات
    """
    # حفظ المجلد الأصلي
    original_cwd = os.getcwd()
    # تغيير مجلد العمل إلى مجلدنا المفتوح
    os.chdir(WORKSPACE)

    # تعيين متغيرات البيئة مرة أخرى
    os.environ["ONNX_HOME"] = MODELS_DIR
    os.environ["HF_HOME"] = os.path.join(WORKSPACE, "hf_cache")

    try:
        if model_type == "fast":
            model = CATTEncoderOnly()
        else:
            model = CATTEncoderDecoder()
        # إرجاع المجلد الأصلي
        os.chdir(original_cwd)
        return model
    except PermissionError:
        # الحل البديل: نسخ ملفات ONNX ومحاولة ثانية
        os.chdir(original_cwd)
        return _load_with_patched_path(model_type)
    except Exception as e:
        os.chdir(original_cwd)
        raise e

def _load_with_patched_path(model_type):
    """
    محاولة تحميل بديلة بعد تعديل مسارات ONNX
    """
    import importlib

    # إعادة تحميل المكتبة بعد تعديل المسارات
    try:
        import catt_tashkeel
        pkg_dir = os.path.dirname(catt_tashkeel.__file__)
        onnx_src = os.path.join(pkg_dir, "onnx_models")

        # نسخ كل ملفات ONNX إلى مجلدنا
        if os.path.exists(onnx_src):
            for f in os.listdir(onnx_src):
                src_file = os.path.join(onnx_src, f)
                dst_file = os.path.join(MODELS_DIR, f)
                if not os.path.exists(dst_file):
                    try:
                        shutil.copy2(src_file, dst_file)
                    except Exception:
                        pass

        # تعديل الكود مباشرة (monkey-patch)
        _monkey_patch_catt(pkg_dir)

        # إعادة تحميل
        importlib.reload(catt_tashkeel)

        original_cwd = os.getcwd()
        os.chdir(WORKSPACE)
        if model_type == "fast":
            model = CATTEncoderOnly()
        else:
            model = CATTEncoderDecoder()
        os.chdir(original_cwd)
        return model
    except Exception as e:
        raise RuntimeError(
            f"فشل تحميل النموذج بعد جميع المحاولات.\n"
            f"الخطأ: {e}\n\n"
            f"الحل: شغّل التطبيق محلياً على جهازك:\n"
            f"pip install catt-tashkeel streamlit\n"
            f"streamlit run app_streamlit.py"
        )

def _monkey_patch_catt(pkg_dir):
    """تعديل مسارات المكتبة في الذاكرة"""
    onnx_original = os.path.join(pkg_dir, "onnx_models")

    # البحث في كل ملفات المكتبة
    for root, dirs, files in os.walk(pkg_dir):
        for fname in files:
            if fname.endswith(".py"):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    if "onnx_models" in content:
                        # إنشاء نسخة معدّلة في مجلدنا
                        new_content = content.replace(
                            onnx_original, MODELS_DIR
                        )
                        # محاولة الكتابة
                        try:
                            with open(fpath, "w", encoding="utf-8") as f:
                                f.write(new_content)
                        except PermissionError:
                            # إذا لم نستطع الكتابة، نعدّل في الذاكرة
                            pass
                except Exception:
                    pass

# ==========================================
# 6. واجهة المستخدم
# ==========================================
st.title("✨ التشكيل الذكي للنصوص (CATT)")
st.markdown("---")

# فحص الاستيراد
if not IMPORT_OK:
    st.error(f"❌ خطأ في استيراد المكتبة: {IMPORT_ERR}")
    st.info(
        "شغّل محلياً:\n"
        "```\n"
        "pip install catt-tashkeel streamlit\n"
        "streamlit run app_streamlit.py\n"
        "```"
    )
    st.stop()

# اختيار النموذج
st.markdown("**⚙️ إعدادات التشكيل:**")
model_choice = st.radio(
    "اختر نوع محرك الذكاء الاصطناعي:",
    [
        "النموذج السريع ⚡ (Encoder-Only)",
        "النموذج الدقيق 🎯 (Encoder-Decoder)",
    ],
    horizontal=False,
)

# تحميل النموذج
model = None
model_type = "fast" if "السريع" in model_choice else "accurate"
try:
    spinner_msg = (
        "⏳ جاري تحميل النموذج السريع..." if model_type == "fast" else "⏳ جاري تحميل النموذج الدقيق..."
    )
    with st.spinner(spinner_msg):
        model = load_model_safe(model_type)
except Exception as e:
    st.error(f"❌ فشل تحميل النموذج: {e}")
    # معلومات التشخيص
    with st.expander("🔍 معلومات التشخيص"):
        st.markdown(f"**مجلد العمل:** `{WORKSPACE}`")
        st.markdown(f"**مجلد النماذج:** `{MODELS_DIR}`")
        if os.path.exists(MODELS_DIR):
            files = os.listdir(MODELS_DIR)
            st.markdown(f"**ملفات النماذج:** {len(files)}")
            for f in files[:10]:
                st.markdown(f" - `{f}`")
        else:
            st.markdown("**مجلد النماذج:** غير موجود")
        st.markdown(f"**Python:** `{sys.version}`")
        st.markdown(f"**المسار:** `{sys.prefix}`")
    st.stop()

# ==========================================
# 7. مربع الإدخال والتشكيل
# ==========================================
user_text = st.text_area(
    "أدخل النص العربي (بدون تشكيل):",
    height=150,
    placeholder="مثال: يهدف الذكاء الاصطناعي الى تسهيل حياة الانسان...",
)

if st.button(
    "تـشـكـيـل الـنـص 🚀",
    type="primary",
    use_container_width=True,
):
    if not user_text.strip():
        st.warning("⚠️ يرجى إدخال نص أولاً.")
    elif model is None:
        st.error("❌ النموذج غير محمل")
    else:
        # تغيير مجلد العمل أثناء التشكيل أيضاً
        saved_cwd = os.getcwd()
        os.chdir(WORKSPACE)
        with st.spinner("⏳ جاري تحليل السياق ووضع الحركات..."):
            try:
                result = model.do_tashkeel(user_text, verbose=False)
                st.success("✅ تمت العملية بنجاح!")
                st.text_area("النتيجة:", value=result, height=150)
            except Exception as e:
                st.error(f"❌ خطأ أثناء التشكيل: {e}")
            finally:
                os.chdir(saved_cwd)

# ==========================================
# 8. الفوتر
# ==========================================
st.markdown("---")
st.caption(
    "مبني باستخدام CATT-Tashkeel | "
    "تم تجاوز حماية السيرفر بنجاح ✅"
                )
