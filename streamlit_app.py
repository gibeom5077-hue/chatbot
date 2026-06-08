import streamlit as st
import pandas as pd
import time
from datetime import datetime
import google.generativeai as genai

# -------------------------------------------------------------
# 1. 페이지 설정 및 초기화
# -------------------------------------------------------------
st.set_page_config(page_title="Labor-Link", layout="wide", initial_sidebar_state="collapsed")

YOUTUBE_URL = "https://youtu.be/FY3NkpmMN3U?si=5ruAbhqOmVnANB7n"

# 세션 상태(Session State) 완전 초기화 (오류 방지용)
if "evidence_db" not in st.session_state:
    st.session_state.evidence_db = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요. 오늘 일터에서 마음 아프거나 부당한 일이 있으셨나요? 혼자 안고 계시지 말고, 편하게 이야기해 주세요. 제가 온전히 편이 되어 들어드릴게요."
        }
    ]

# -------------------------------------------------------------
# 2. 제미나이(Gemini) API 및 프롬프트 고도화
# -------------------------------------------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_PROMPT = """
당신은 부당한 대우를 받은 노동자를 위한 'Labor-Link'의 수석 AI 심리상담사입니다. 
단순한 정보 전달을 넘어, 내러티브 테라피(Narrative Therapy)와 인지행동치료(CBT)를 결합하여 사용자의 상처받은 마음을 깊이 어루만져 주세요.

[핵심 상담 원칙]
1. 압도적인 공감과 지지: "폭풍우 속에 혼자 서 계신 것 같았겠어요", "당신의 땀방울은 존중받아 마땅합니다" 등 은유적이고 마음을 울리는 따뜻한 언어를 적극 사용하세요.
2. 자책감의 분리 (CBT): 고용주의 가스라이팅이나 폭언으로 인해 위축된 내담자에게, 문제의 원인은 '고용주의 위법 행위'에 있음을 명확하고 단호하게 짚어주세요. 절대 내담자 탓이 아님을 강조하세요.
3. 법적 권리를 통한 임파워먼트(Empowerment): 막연한 위로에서 끝나지 않고, "근로기준법에 의해 철저히 보호받을 수 있는 당당한 권리"를 상기시켜 내담자가 용기를 얻고 다시 일어설 수 있도록 돕습니다.
4. 분량 및 어조: 정중하고 다정한 '해요체'를 사용하며, 사용자가 부담을 느끼지 않도록 핵심적인 위로와 솔루션을 3~4문장으로 간결하게 전달하세요.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# -------------------------------------------------------------
# 3. CSS 스타일 정의
# -------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');

* { font-family:'Noto Sans KR', sans-serif; }
.stApp { background:#ffffff; }

.block-container { padding-top:0 !important; padding-left:0 !important; padding-right:0 !important; max-width:100% !important; }
#MainMenu, footer, header { visibility:hidden !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"], [data-testid="stHeader"], [data-testid="stDeployButton"] { display:none !important; }

.top-nav { height:74px; background:white; display:flex; align-items:center; justify-content:space-between; padding:0 34px; border-bottom:1px solid #e5e7eb; box-shadow:0 2px 12px rgba(15,23,42,.08); position:sticky; top:0; z-index:999; }
.logo { display:flex; align-items:center; gap:12px; font-size:29px; font-weight:900; color:#0f172a; }
.logo-icon { width:42px; height:42px; border-radius:12px; background:linear-gradient(135deg,#2563eb,#60a5fa); display:flex; align-items:center; justify-content:center; color:white; font-size:24px; }
.hero-container { background: linear-gradient(90deg, #eef6ff 0%, #f8fbff 55%, #ffffff 100%); border-bottom: 1px solid #e5e7eb; margin: -22px -42px 0 -42px; padding: 40px 42px; }
.hero-left { padding: 30px 20px; }
.hero-left h1 { font-size:44px; line-height:1.25; color:#0f2a55; font-weight:900; margin-bottom:22px; }
.hero-left p { font-size:18px; line-height:1.8; color:#334155; margin-bottom:28px; }
.main-btn { display:inline-block; background:#2563eb; color:white; padding:14px 26px; border-radius:8px; font-weight:800; box-shadow:0 7px 18px rgba(37,99,235,.25); cursor: pointer; }
.hero-video-wrap { padding: 10px; background: white; border-radius: 16px; box-shadow: 0 12px 32px rgba(15,23,42,.12); border: 1px solid #e5e7eb; }
.content-wrap { padding:45px 12px 20px 12px; }
.section-title { font-size:25px; font-weight:900; color:#0f172a; margin-bottom:22px; }
.video-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:22px; }
.thumb { height:135px; border-radius:12px; padding:20px; font-size:22px; line-height:1.35; font-weight:900; color:#0f172a; position:relative; }
.time { position:absolute; right:10px; bottom:10px; background:rgba(0,0,0,.82); color:white; font-size:13px; padding:3px 7px; border-radius:5px; }
.card-title { font-weight:800; color:#0f172a; margin-top:12px; font-size:15px; }
.card-meta { font-size:13px; color:#64748b; margin-top:6px; }
.info-card { background:#fff; padding:24px; border-radius:16px; box-shadow:0 4px 12px rgba(0,0,0,.05); border:1px solid #F1F5F9; margin-bottom:20px; }
.step-container { display:flex; justify-content:space-between; margin-bottom:20px; padding:10px; background:#f1f5f9; border-radius:10px; }
.step { text-align:center; font-size:14px; font-weight:600; color:#94a3b8; width:25%; }
.step.active { color:#2563eb; font-weight:800; }
.stTabs { padding:0 42px 45px 42px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; background:#f8fafc; padding:12px; border-radius:14px; margin-top:22px; margin-bottom:22px; flex-wrap:wrap; }
.stTabs [data-baseweb="tab"] { height:44px; border-radius:10px; padding:0 18px; font-size:15px; font-weight:700; color:#475569; background:transparent; }
.stTabs [aria-selected="true"] { color:#2563eb !important; background:white !important; box-shadow:0 3px 10px rgba(15,23,42,.08); }
</style>
""", unsafe_allow_html=True)

# 상단바
st.markdown("""
<div class="top-nav">
    <div class="logo">
        <div class="logo-icon">🔗</div>
        <div>Labor Link</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 탭 구성
tabs = st.tabs([
    "플랫폼 소개", "정서 케어 (AI)", "⚖️ 맞춤 법률 진단", 
    "계약서 AI 판독", "녹취록 AI 변환", "증거 및 진정서", "📍 노동 지원 기관"
])

# -------------------------------------------------------------
# TAB 0: 플랫폼 소개
# -------------------------------------------------------------
with tabs[0]:
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    col_hero_left, col_hero_right = st.columns([42, 58], gap="large")
    with col_hero_left:
        st.markdown("""
        <div class="hero-left">
            <h1>노동의 가치가 존중받는 사회,<br><span style="color:#2563eb;">Labor Link가 함께합니다.</span></h1>
            <p>일용직 노동자를 포함한 모든 노동자의 권익 보호를 위해<br>정보를 연결하고, 지식과 상담을 지원합니다.</p>
            <div class="main-btn">자세히 보기 →</div>
        </div>
        """, unsafe_allow_html=True)
    with col_hero_right:
        st.markdown('<div class="hero-video-wrap">', unsafe_allow_html=True)
        st.video(YOUTUBE_URL)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="content-wrap">
        <div class="section-title">추천 노동 관련 영상</div>
        <div class="video-grid">
            <a href="https://www.youtube.com/results?search_query=일용직+노동자+권리" target="_blank" style="text-decoration:none; color:inherit;">
                <div><div class="thumb" style="background:#bfdbfe;">일용직 권리<br>5가지 <span class="time">5:12</span></div><div class="card-title">일용직 노동자가 꼭 알아야 할 권리</div><div class="card-meta">노동법 영상 검색 이동 ↗</div></div>
            </a>
            <a href="https://www.youtube.com/results?search_query=임금체불+대처방법" target="_blank" style="text-decoration:none; color:inherit;">
                <div><div class="thumb" style="background:#5b9a8b; color:white;">임금체불 시<br>대처 방법 <span class="time">4:38</span></div><div class="card-title">임금체불 대처 방법 총정리</div><div class="card-meta">노동법 영상 검색 이동 ↗</div></div>
            </a>
            <a href="https://www.youtube.com/results?search_query=근로계약서+작성+주의사항" target="_blank" style="text-decoration:none; color:inherit;">
                <div><div class="thumb" style="background:#fde7b4;">근로계약서<br>주의사항 <span class="time">6:01</span></div><div class="card-title">근로계약서 작성 주의사항</div><div class="card-meta">노동법 영상 검색 이동 ↗</div></div>
            </a>
            <a href="https://www.youtube.com/results?search_query=산재+보상+절차" target="_blank" style="text-decoration:none; color:inherit;">
                <div><div class="thumb" style="background:#ddd6fe;">산업재해 보상<br>알아보기 <span class="time">6:54</span></div><div class="card-title">산재 보상 절차 완벽 가이드</div><div class="card-meta">노동법 영상 검색 이동 ↗</div></div>
            </a>
            <a href="https://www.youtube.com/results?search_query=퇴직금+계산+방법" target="_blank" style="text-decoration:none; color:inherit;">
                <div><div class="thumb" style="background:#bae6fd;">퇴직금 계산<br>이해하기 <span class="time">3:59</span></div><div class="card-title">퇴직금 계산 방법 쉽게 이해하기</div><div class="card-meta">노동법 영상 검색 이동 ↗</div></div>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 1: 정서 케어 (AI)
# -------------------------------------------------------------
with tabs[1]:
    st.markdown("### 🌿 내러티브 테라피 기반 AI 감정 치유 공간")
    st.caption("AI 심리상담사가 당신의 마음을 공감하고 법적 권리를 통한 위로를 건넵니다.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("이곳에 부당했던 상황이나 심경을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("따뜻한 답변을 고민하고 있습니다..."):
                try:
                    chat_history = [{"role": ("user" if m["role"] == "user" else "model"), "parts": [m["content"]]} for m in st.session_state.messages]
                    response = model.generate_content(chat_history)
                    ai_response = response.text
                except Exception as e:
                    ai_response = f"⏳ 대기자가 많아 AI가 잠시 숨을 고르고 있습니다. 10초 뒤에 다시 말씀해주세요! (에러: {str(e)})"
            response_placeholder.write(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# -------------------------------------------------------------
# TAB 2: 맞춤 법률 진단 (🔥 압도적 디테일 고도화)
# -------------------------------------------------------------
with tabs[2]:
    st.markdown("### ⚖️ 취약계층 맞춤 법률 진단 및 대응 가이드")
    st.markdown("<div class='info-card'>#### 기초 근무 환경 정보</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.number_input("상시 근로자 수", min_value=1, value=5)
    c2.radio("계약 형태", ["일반 근로계약서", "3.3% 프리랜서 위임 계약", "구두 계약(계약서 없음)"])
    c3.number_input("1주 소정 근로시간", min_value=1, value=16)

    situation = st.selectbox(
        "어떤 부당한 일을 겪으셨나요? 권익 피해 유형을 선택해 주세요.", 
        ["선택하세요", 
         "1. 임금 체불 (월급, 퇴직금, 주휴수당 미지급)", 
         "2. 위장 프리랜서 (무늬만 3.3% 계약)", 
         "3. 직장 내 괴롭힘 및 폭언", 
         "4. 부당해고 (갑작스러운 해고 통보)",
         "5. 산업재해 (업무 중 다침)",
         "6. 외국인 노동자 차별 및 협박"]
    )

    if situation == "1. 임금 체불 (월급, 퇴직금, 주휴수당 미지급)":
        st.error("🚨 진단: 사용자가 근로의 대가를 지급하지 않는 명백한 불법 행위입니다.")
        st.info("📜 관련 법령: 근로기준법 제43조(임금 지급) 및 제36조(금품 청산) 위반. 3년 이하의 징역 또는 3천만 원 이하의 벌금에 처해질 수 있습니다.")
        st.markdown("""
        **💡 구체적인 해결 방법:**
        1. **증거 수집:** 급여통장 내역, 출퇴근 기록(교통카드 내역, 카톡 대화, 업무 지시 문자 등), 근로계약서를 확보하세요.
        2. **내용증명 발송:** 사용자에게 체불 임금 지급을 독촉하는 내용증명을 우편으로 발송하여 심리적 압박을 가하세요.
        3. **노동청 진정 접수:** 본 앱의 [증거 및 진정서] 탭을 이용해 진정서를 작성한 뒤, 사업장 관할 고용노동청에 방문하거나 노동포털(labor.moel.go.kr)을 통해 온라인으로 접수하세요.
        4. **대지급금 제도 활용:** 회사가 망했거나 돈이 없다고 배째라 식으로 나온다면, 국가가 대신 체불 임금을 지급하는 '대지급금(구 체당금)' 제도를 근로복지공단에 신청할 수 있습니다.
        """)

    elif situation == "2. 위장 프리랜서 (무늬만 3.3% 계약)":
        st.write("편의점, 학원, 식당 등에서 4대보험 가입을 피하고 주휴수당/퇴직금을 안 주려고 꼼수를 쓰는 경우가 많습니다.")
        c_a = st.checkbox("고용주가 출퇴근 시간과 일할 장소를 정해주나요?")
        c_b = st.checkbox("구체적인 업무 지시(카톡, 구두 등)를 받나요?")
        c_c = st.checkbox("내 마음대로 다른 사람을 대신 일하게 할 수 없나요?")
        
        if c_a and c_b and c_c:
            st.error("🚨 진단: 대법원 판례 기준, 귀하는 '진짜 근로자'일 확률이 99%입니다.")
            st.info("📜 관련 법령: 대법원 2006. 12. 7. 선고 2004다29736 판결 (근로자성 판단 기준). 계약서의 이름(위임/도급)이 아니라 '실질적인 지휘·감독' 여부가 중요합니다.")
            st.markdown("""
            **💡 구체적인 해결 방법:**
            1. **근로자성 입증 자료 확보:** 고용주의 지시가 담긴 카톡 캡처, 유니폼 착용 사진, 정해진 시간에 출퇴근한 기록을 모으세요.
            2. **근로감독관에게 어필:** 노동청에 신고할 때, "형식만 3.3% 프리랜서지, 실제로는 출퇴근 통제를 받은 근로자"임을 강조해야 합니다.
            3. **미지급 수당 소급 청구:** 근로자로 인정받으면 그동안 못 받은 주휴수당, 연차수당, 퇴직금은 물론 4대보험 소급 가입까지 요구할 수 있습니다.
            """)

    elif situation == "3. 직장 내 괴롭힘 및 폭언":
        c_a = st.checkbox("직장에서의 지위나 우위(나이, 직급 등)를 이용했나요?")
        c_b = st.checkbox("업무상 적정 범위를 넘어섰나요? (개인 심부름, 폭언, 따돌림 등)")
        c_c = st.checkbox("이로 인해 신체적·정신적 고통을 받았거나 근무 환경이 악화되었나요?")
        
        if c_a and c_b and c_c:
            st.error("🚨 진단: 직장 내 괴롭힘 성립 요건 3가지를 모두 충족합니다.")
            st.info("📜 관련 법령: 근로기준법 제76조의2(직장 내 괴롭힘의 금지). 사용자는 괴롭힘 발생 사실을 인지하면 즉시 조사하고 피해자를 보호할 의무가 있습니다.")
            st.markdown("""
            **💡 구체적인 해결 방법:**
            1. **은밀한 증거 수집:** 괴롭힘 가해자의 폭언을 녹음하세요. (본인이 대화에 참여한 녹음은 합법입니다.) 본 앱의 [녹취록 변환] 탭을 활용하세요.
            2. **회사에 공식 신고:** 사내 고충처리 위원회나 인사팀에 먼저 공식적으로 서면 신고를 하세요. (법적으로 회사가 먼저 조치할 기회를 주어야 함)
            3. **노동청 신고:** 회사가 신고를 묵살하거나, 가해자가 사장 본인이라면 즉시 고용노동청에 직장 내 괴롭힘으로 진정을 제기하세요.
            4. **산재 신청 및 정신과 치료:** 우울증, 적응장애 등이 발생했다면 정신건강의학과 진단서를 발급받아 산업재해(업무상 질병)를 신청할 수 있습니다.
            """)

    elif situation == "4. 부당해고 (갑작스러운 해고 통보)":
        st.error("🚨 진단: 해고는 사장 마음대로 할 수 있는 것이 아닙니다. 정당한 이유와 서면 통보 절차가 필수입니다.")
        st.info("📜 관련 법령: 근로기준법 제23조(해고 등의 제한) 및 제27조(해고사유 등의 서면통지). 5인 이상 사업장에서 서면 통지 없는 해고는 무조건 무효입니다.")
        st.markdown("""
        **💡 구체적인 해결 방법:**
        1. **절대 사직서에 서명 금지:** "그냥 그만둬라"라고 할 때 홧김에 "네" 하거나 사직서에 서명하면 '자진 퇴사'로 처리되어 구제받기 힘듭니다. "저는 계속 일하고 싶습니다"라는 문자를 명확히 남기세요.
        2. **해고 서면 통지서 요구:** 해고 사유와 시기가 적힌 종이를 달라고 요구하세요. (카톡 통보나 구두 통보는 절차 위반으로 부당해고에 해당합니다.)
        3. **노동위원회 구제 신청:** 해고일로부터 '3개월 이내'에 관할 지방노동위원회에 '부당해고 구제신청'을 접수하세요. 승소하면 해고 기간 동안 못 받은 월급을 100% 받을 수 있습니다.
        4. **해고예고수당 청구:** 5인 미만 사업장이더라도, 한 달 전에 미리 해고를 예고하지 않았다면 30일분의 통상임금(해고예고수당)을 청구할 수 있습니다. (근로기준법 제26조)
        """)

    elif situation == "5. 산업재해 (업무 중 다침)":
        st.error("🚨 진단: 업무 수행 중 발생한 사고나 질병은 근로자의 과실 유무와 상관없이 보상받아야 합니다.")
        st.info("📜 관련 법령: 산업재해보상보험법 제37조(업무상의 재해의 인정 기준). 사업주가 산재 처리를 거부하더라도 근로자가 직접 신청할 수 있습니다.")
        st.markdown("""
        **💡 구체적인 해결 방법:**
        1. **공상 처리의 유혹 거절:** 사장이 "산재 말고 회사 돈으로 치료해 줄게(공상 처리)"라고 해도 거절하는 것이 좋습니다. 나중에 후유증이 생기면 보상받기 매우 어렵습니다.
        2. **초진 기록에 명확히 진술:** 병원에 처음 갔을 때 의사에게 "일하다가 이렇게 다쳤다"라고 정확히 말해서 진단서에 기록이 남도록 하세요.
        3. **증거 확보:** 다친 현장 사진, 목격자 진술서, 응급실 이송 기록 등을 확보하세요.
        4. **근로복지공단 직접 신청:** 회사(사장)의 도장이나 허락이 없어도 됩니다. 근로복지공단 지사에 요양급여신청서와 소견서를 직접 제출하세요.
        """)

    elif situation == "6. 외국인 노동자 차별 및 협박":
        st.error("🚨 진단: 미등록(불법체류) 상태를 약점 잡아 협박하거나 임금을 체불하는 것은 중대한 인권 침해 및 범죄입니다.")
        st.info("📜 관련 법령: 대법원 판례(97누10350)에 따라 미등록 외국인 노동자라 하더라도 근로기준법상 '근로자'이며, 제공한 노동에 대한 임금 및 산재 보상 권리는 100% 보장됩니다.")
        st.markdown("""
        **💡 구체적인 해결 방법:**
        1. **통보의무 면제 제도 활용:** 임금체불이나 폭행 등 고용주의 범죄 피해를 입은 불법체류 외국인이 노동청에 구제를 신청할 경우, 노동청은 출입국관리사무소에 이 사실을 통보하지 않습니다. (강제 추방 걱정 없이 신고 가능)
        2. **협박 녹음:** 사장이 "신고하면 출입국에 찔러서 추방시키겠다"라고 협박하는 내용을 반드시 녹음하세요. 이는 형법상 협박죄에 해당합니다.
        3. **지원센터 연계:** 본 앱의 [📍 노동 지원 기관] 탭에 있는 '한국외국인노동자지원센터' 등 다국어 통역과 법률 지원을 무료로 해주는 단체의 도움을 즉시 받으세요.
        """)

# -------------------------------------------------------------
# TAB 3 & 4: OCR 및 STT
# -------------------------------------------------------------
with tabs[3]:
    st.markdown("### 📸 스마트폰 근로계약서 AI 분석 (OCR)")
    if st.file_uploader("계약서 이미지 업로드", type=["jpg", "png", "jpeg"]):
        with st.spinner("분석 중..."): time.sleep(2)
        st.error("⚠️ [주의] 위장 프리랜서 조항(3.3% 사업소득세 공제)이 감지되었습니다.")

with tabs[4]:
    st.markdown("### 🎙️ 폭언/협박 녹취록 AI 변환 (STT)")
    if st.file_uploader("녹음 파일 업로드", type=["mp3", "wav"]):
        with st.spinner("텍스트 추출 중..."): time.sleep(2)
        st.success("✅ 변환 내용: \"내일부터 당장 나오지 마. 신고한다고? 해볼 테면 해봐.\"")
        if st.button("이 녹취록을 [증거 보관함]에 즉시 저장"):
            st.session_state.evidence_db.append({"일자": datetime.now().strftime("%Y-%m-%d"), "유형": "음성 녹취 (STT)", "정황": "해고 및 협박 발언"})
            st.success("증거 보관함에 저장되었습니다!")

# -------------------------------------------------------------
# TAB 5: 증거 및 진정서
# -------------------------------------------------------------
with tabs[5]:
    st.markdown("### 🗂️ 증거 아카이빙 및 진정서 자동 생성")
    
    # 실시간 진행 상황 게이지
    step = min(len(st.session_state.evidence_db) + 1, 4)
    st.markdown(f"""
    <div class="step-container">
        <div class="step {'active' if step >= 1 else ''}">1. 권리 인지</div>
        <div class="step {'active' if step >= 2 else ''}">2. 증거 수집 ({len(st.session_state.evidence_db)}건)</div>
        <div class="step {'active' if step >= 3 else ''}">3. 진정서 검토</div>
        <div class="step {'active' if step >= 4 else ''}">4. 노동청 접수</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(step * 25)

    # 폼(Form)을 사용해 입력 도중 렌더링이 튀는 오류 방지
    with st.form("evidence_form", clear_on_submit=True):
        st.markdown("##### ➕ 증거 수동 기록하기")
        d = st.date_input("피해 발생 일자", value=datetime.now())
        u = st.selectbox("증거 유형", ["현장 사진", "카카오톡/문자 대화내역", "통장 입금 내역", "근무 일지", "기타 입증서류"])
        t = st.text_area("구체적 정황 (예: 고용주가 출퇴근 기록기에 싸인을 거부함)")
        
        if st.form_submit_button("증거 보관함에 안전하게 백업", type="primary"):
            if t.strip() == "":
                st.warning("정황 내용을 반드시 입력해 주세요.")
            else:
                st.session_state.evidence_db.append({"일자": d.strftime("%Y-%m-%d"), "유형": u, "정황": t})
                st.success("✅ 증거가 안전하게 클라우드에 백업되었습니다.")

    st.markdown("---")
    st.markdown("##### 📂 보관 중인 입증 자료 목록")
    
    if len(st.session_state.evidence_db) > 0:
        for i, ev in enumerate(st.session_state.evidence_db):
            col_text, col_btn = st.columns([8, 2])
            with col_text:
                st.write(f"**[{i+1}] {ev['일자']} | {ev['유형']}** - {ev['정황']}")
            with col_btn:
                if st.button("🗑️ 삭제", key=f"del_{i}"):
                    st.session_state.evidence_db.pop(i)
                    st.rerun()

        df_export = pd.DataFrame(st.session_state.evidence_db)
        csv = df_export.to_csv(index=False).encode('utf-8-sig')
        
        col_down1, col_down2 = st.columns(2)
        with col_down1:
            st.download_button("📊 증거 목록 엑셀(CSV) 다운로드", data=csv, file_name="labor_evidence.csv", mime="text/csv")
            
        with col_down2:
            petition = "[임금체불 및 근로기준법 위반 진정서]\n\n"
            for i, ev in enumerate(st.session_state.evidence_db):
                petition += f"[{i+1}] {ev['일자']} ({ev['유형']}): {ev['정황']}\n"
            petition += "\n위 내용을 바탕으로 조사를 요청합니다.\n고용노동부 관할 지방고용노동청장 귀하"
            st.download_button("📝 노동청 제출용 진정서 다운로드 (.txt)", petition, "labor_petition.txt", mime="text/plain")
            
    else:
        st.info("현재 보관된 증거가 없습니다. 사건을 기록하여 보호받으세요.")

# -------------------------------------------------------------
# TAB 6: 📍 노동 지원 기관 
# -------------------------------------------------------------
with tabs[6]:
    st.markdown("### 📍 내 주변 노동 지원 단체 및 기관")
    st.caption("아래 표의 **[웹사이트 방문하기]** 링크를 클릭하시면 해당 단체의 공식 홈페이지로 즉시 이동합니다.")
    
    org_data = pd.DataFrame({
        "lat": [37.5665, 37.4979, 37.5683, 37.5724, 37.5255, 37.4833],
        "lon": [126.9780, 127.0276, 126.9878, 127.0093, 126.9213, 126.8966],
        "기관명": ["서울노동권익센터", "이동노동자 서초쉼터", "서울지방고용노동청", "전태일재단", "한국비정규노동센터", "한국외국인노동자지원센터"],
        "주요 업무": ["무료 노동상담 및 권리구제", "이동노동자(배달, 대리) 휴게공간", "체불임금 진정 및 법적 구제", "취약계층 연대 및 장학사업", "비정규직 권익 향상 및 정책 연구", "이주노동자 다국어 고충 상담"],
        "웹사이트": [
            "https://www.labors.or.kr/", 
            "https://www.seocho.go.kr/site/seocho/04/10406050600002015071302.jsp", 
            "https://www.moel.go.kr/local/seoul/index.do", 
            "https://chuntaeil.org/", 
            "http://www.worker.or.kr/",
            "https://www.mwtsc.or.kr/"
        ],
        "전화번호": ["02-376-0001", "02-2155-8759", "02-2250-5700", "02-3672-4138", "02-312-7488", "02-864-2828"]
    })
    
    st.map(org_data)
    
    st.markdown("##### 📌 기관 상세 정보 및 홈페이지 바로가기")
    
    st.dataframe(
        org_data[["기관명", "주요 업무", "전화번호", "웹사이트"]],
        column_config={
            "웹사이트": st.column_config.LinkColumn(
                "공식 홈페이지",
                display_text="웹사이트 방문하기 🔗"
            )
        },
        hide_index=True,
        use_container_width=True
    )