import streamlit as st
from audio_recorder_streamlit import audio_recorder
import requests

st.set_page_config(page_title="مساعد مستشفى التحرير الذكي", page_icon="🏥")
st.title("🏥 نظام الرد الصوتي للمستشفى")

# 1. فتح المايك وتسجيل الصوت
audio_bytes = audio_recorder(
    text="اضغط على المايك وابدأ الكلام",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_size="3x",
)

if audio_bytes:
    with st.spinner("جاري معالجة صوتك..."):
        # 2. إرسال الصوت فوراً للـ Webhook بتاعك في n8n
        # استخدم الـ Production URL اللي في صورة n8n
        WEBHOOK_URL = (
            "https://client1.tashghil.pro/webhook/9ffef3de-a05a-4120-8e44-37c053ce392d"
        )

        files = {"file": ("query.wav", audio_bytes, "audio/wav")}
        response = requests.post(WEBHOOK_URL, files=files)

        if response.status_code == 200:
            res = response.json()
            st.success("تم الرد!")
            # 3. عرض النص وتشغيل الرد الصوتي
            st.write(f"**الرد:** {res.get('output_text')}")
            st.audio(res.get("audio_url"))
        else:
            st.error("فشل الاتصال بالسيستم، تأكد من تشغيل الـ Workflow")
