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
        WEBHOOK_URL = "https://client1.tashghil.pro/webhook/9ffef3de-a05a-4120-8e44-37c053ce392d"
        
        # تعديل: نبعت الـ bytes مباشرة مع تحديد اسم الملف
        files = {'file': ('audio.wav', audio_bytes, 'audio/wav')}
        
        try:
            response = requests.post(WEBHOOK_URL, files=files, timeout=30)
            if response.status_code == 200:
                # تأكد إن n8n بيرجع JSON فيه مفتاح اسمه output_text
                res = response.json()
                st.success("تم الرد!")
                if 'output_text' in res:
                    st.write(f"**الرد:** {res['output_text']}")
                if 'audio_url' in res:
                    st.audio(res['audio_url'])
            else:
                st.error(f"خطأ من السيرفر: {response.status_code}")
        except Exception as e:
            st.error(f"فشل الاتصال: {e}")
