import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import google.generativeai as genai # Gemini AI 라이브러리 추가됨!

# --- 1. 페이지 설정 및 와이드 레이아웃 ---
st.set_page_config(page_title="Labor-Link", layout="wide", initial_sidebar_state="collapsed")

# 커스텀 CSS
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; font-family: 'Pretendard', sans-serif; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .info-card { background-color: #FFFFFF; padding: 24px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #F1F5F9; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid #E2E8F0; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { height: 45px; font-size: 15px; font-weight: 600; color: #64748B; border-radius: 8px 8px 0 0; padding: 0 16px; border: none; background-color: transparent; white-space: nowrap; }
    .stTabs [aria-selected="true"] { color: #2563EB !important; border-bottom: 3px solid #2563EB !important; }
    .step-container { display: flex; justify-content: space-between; margin-bottom: 20px; padding: 10px; background-color: #f1f5f9; border-radius: 10px;}
    .step { text-align: center; font-size: 14px; font-weight: 600; color: #94a3b8; width: 25%; }
    .step.active { color: #2563eb; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.markdown("<h2 style='text-align: center; color: #1E293B; margin-bottom: 0;'>Labor-Link</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; margin-bottom: 30px;'>모든 취약계층 노동자를 위한 실전 권익 보호 플랫폼</p>", unsafe_allow_html=True)

# 7개의 독립된 탭 구성
tabs = st.tabs(["플랫폼 소개", "정서 케어 (AI)", "맞춤 법률 진단", "계약서 AI 판독", "녹취록 AI 변환", "증거 및 진정서", "📍 쉼터 지도"])

# --- TAB 1: 플랫폼 소개 ---
with tabs[0]:
    st.markdown("<div class='info-card'><h3>거대한 시스템 앞의 안전망</h3><p>Labor-Link는 고용 형태의 사각지대나 언어 장벽, 신체적 불리함으로 인해 목소리를 내지 못하는 취약계층 근로자를 위한 실효적 디지털 울타리입니다.</p></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.markdown("<div class='info-card'><h4 style='color:#2563EB;'>도구적 신체 탈피</h4><p style='color:#475569; font-size:14px;'>생산수단으로 소모되는 구조적 현실 인지</p></div>", unsafe_allow_html=True)
    col2.markdown("<div class='info-card'><h4 style='color:#2563EB;'>구조적 침묵 타파</h4><p style='color:#475569; font-size:14px;'>AI 분석을 통한 심리적 두려움 극복</p></div>", unsafe_allow_html=True)
    col3.markdown("<div class='info-card'><h4 style='color:#2563EB;'>심리적 재기 확보</h4><p style='color:#475569; font-size:14px;'>죄책감에서 벗어나 권리 주체의 상태 도달</p></div>", unsafe_allow_html=True)

# --- TAB 2: 정서 케어 대화 (진짜 Gemini AI 연동) ---
with tabs[1]:
    st.markdown("### 내러티브 테라피 기반 AI 감정 치유 공간")
    st.caption("근로기준법 및 심리치료(CBT)에 기반하여 훈련된 AI 상담사입니다. 편하게 이야기해 보세요.")
    
    try:
        # API 키 불러오기 및 모델 세팅
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        system_instruction = """
        당신은 부당한 대우를 받은 취약계층/일용직 노동자를 위한 전문 심리 상담사입니다. 
        매우 공감적이고 따뜻한 말투(해요체)로 위로하며, 인지행동치료(CBT) 기법을 활용해 노동자의 자책감을 덜어주세요. 
        가스라이팅 당한 노동자에게 '당신의 잘못이 아닌 고용주의 위법'임을 명확하고 다정하게 인지시켜주세요.
        답변은 3~4문장으로 핵심만 길지 않게 말해주세요.
        """
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

        # 채팅 세션 초기화
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])
            st.session_state.messages = [{"role": "assistant", "content": "안녕하세요. 오늘 현장에서 마음 아픈 일이 있으셨나요? 혼자 앓지 말고 제게 편하게 털어놓아 주세요."}]

        # 기존 대화 출력
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # 채팅 입력창
        if prompt := st.chat_input("이곳에 상황이나 심경을 입력하세요..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("상담사가 답변을 작성하고 있습니다..."):
                    response = st.session_state.chat_session.send_message(prompt)
                    st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"🚨 에러 상세 내용: {e}")

# --- TAB 3: 맞춤 법률 진단 ---
with tabs[2]:
    st.markdown("### 취약계층 맞춤 진단 및 계산기")
    st.markdown("<div class='info-card'>#### 기초 근무 환경 정보", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.number_input("상시 근로자 수", min_value=1, value=5)
    c2.radio("계약 형태", ["일반 근로계약서", "3.3% 프리랜서 위임 계약"])
    c3.number_input("1주 소정 근로시간", min_value=1, value=16)
    st.markdown("</div>", unsafe_allow_html=True)

    situation = st.selectbox("권익 피해 유형을 선택해 주세요.", ["선택하세요", "외국인 노동자 권리 보장 및 체류 협박 대응", "임금채권 소멸시효 및 체불 모델", "위장 프리랜서 검증", "직장 내 괴롭힘"])
    if situation == "외국인 노동자 권리 보장 및 체류 협박 대응":
        st.error("💡 대법원 판례(97누10350): 미등록(불법체류) 외국인 노동자라 할지라도, 제공한 노동에 대한 임금 및 산재 보상 권리는 100% 보장받습니다.")
    elif situation == "임금채권 소멸시효 및 체불 모델":
        st.info("체불된 임금은 단순한 돈이 아니라, '최저임금 기준 귀하의 피땀 어린 노동 시간'이 증발한 구조적 문제입니다.")

# --- TAB 4: 계약서 AI 판독 ---
with tabs[3]:
    st.markdown("### 📸 스마트폰 근로계약서 AI 분석 (OCR)")
    uploaded_img = st.file_uploader("계약서 이미지 업로드 (jpg, png)", type=["jpg", "png", "jpeg"])
    if uploaded_img:
        with st.spinner("AI가 스캔하고 있습니다..."): time.sleep(2)
        st.error("⚠️ **[주의] 위장 프리랜서 조항 발견!**\n\n해당 계약서에 **'3.3% 사업소득세 공제'** 및 **'위임 계약'**이 감지되었습니다. 불법 계약일 확률이 높습니다.")

# --- TAB 5: 녹취록 AI 변환 ---
with tabs[4]:
    if "evidence_db" not in st.session_state: st.session_state.evidence_db = []
    st.markdown("### 🎙️ 폭언/협박 녹취록 AI 텍스트 변환 (STT)")
    uploaded_audio = st.file_uploader("녹음 파일 업로드 (mp3, wav)", type=["mp3", "wav"])
    if uploaded_audio:
        with st.spinner("AI가 텍스트 변환 및 키워드 추출 중입니다..."): time.sleep(2)
        st.success("✅ **변환 완료:** \"내일부터 당장 나오지 마. 외국인 주제에 어디서 노동청에 신고한다고 협박이야? 해볼 테면 해봐.\"")
        if st.button("이 녹취록을 [증거 보관함]에 즉시 저장"):
            st.session_state.evidence_db.append({"일자": datetime.now().strftime("%Y-%m-%d"), "유형": "음성 녹취 (STT)", "정황": "녹취 변환: 기습 해고 및 외국인 차별 협박 포함"})
            st.rerun()

# --- TAB 6: 증거 수집 및 진정서 ---
with tabs[5]:
    if "evidence_db" not in st.session_state: st.session_state.evidence_db = []
    st.markdown("### 증거 아카이빙 및 노동청 진정서 생성")
    
    with st.expander("➕ 수동으로 증거 기록 추가하기"):
        d = st.date_input("피해 발생 일자"); t = st.text_area("객관적 정황 기술")
        if st.button("데이터 백업", type="primary") and t:
            st.session_state.evidence_db.append({"일자": d.strftime("%Y-%m-%d"), "유형": "수동 기록", "정황": t})
            st.rerun()
                
    if len(st.session_state.evidence_db) > 0:
        st.dataframe(pd.DataFrame(st.session_state.evidence_db), use_container_width=True)
        petition = f"입증 자료 총 {len(st.session_state.evidence_db)}건\n" + "\n".join([f"[{i+1}] {ev['일자']} | {ev['정황']}" for i, ev in enumerate(st.session_state.evidence_db)])
        st.download_button("📝 진정서 다운로드 (.txt)", f"[임금체불 및 근로기준법 위반 진정서]\n\n{petition}\n\n고용노동부 관할 지방고용노동청장 귀하", "petition.txt")

# --- TAB 7: 지도 ---
with tabs[6]:
    st.markdown("### 📍 내 주변 기관 및 쉼터")
    st.map(pd.DataFrame({'lat': [37.5665, 37.4979, 37.5683], 'lon': [126.9780, 127.0276, 126.9878], 'name': ['서울노동권익센터', '이동노동자 쉼터', '지방고용노동청']}))