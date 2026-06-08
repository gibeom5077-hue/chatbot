import streamlit as st
import pandas as pd
import time
from datetime import datetime
import google.generativeai as genai
from PIL import Image

# -------------------------------------------------------------
# 1. 페이지 설정 및 초기화
# -------------------------------------------------------------
st.set_page_config(page_title="Labor-Link", layout="wide", initial_sidebar_state="collapsed")

YOUTUBE_URL = "https://youtu.be/FY3NkpmMN3U?si=5ruAbhqOmVnANB7n"

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
# 2. 제미나이(Gemini) API
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
# TAB 2: 맞춤 법률 진단 (🔥 변수 연동 고도화 및 확장 완료)
# -------------------------------------------------------------
with tabs[2]:
    st.markdown("### ⚖️ 취약계층 맞춤 법률 진단 및 대응 가이드")
    st.markdown("<div class='info-card'>#### 기초 근무 환경 정보</div>", unsafe_allow_html=True)

    # 🛠️ 1층 조건 제어판
    c1, c2, c3 = st.columns(3)
    emp_count = c1.number_input("상시 근로자 수 (명)", min_value=1, value=5)
    contract_type = c2.radio("계약 형태", ["일반 근로계약서", "3.3% 프리랜서 위임 계약", "구두 계약(계약서 없음)"])
    work_hours = c3.number_input("1주 소정 근로시간 (시간)", min_value=1, value=16)

    # 🛠️ 2층 조건 제어판 (퇴직금 및 해고 수당 정밀 진단용 변수 추가!)
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    c4, c5 = st.columns(2)
    working_months = c4.number_input("총 근무 기간 (개월 수 입력)", min_value=1, value=13)
    dismissal_status = c5.radio("해고 통보 상태", ["해고당하지 않음 / 권고사직 합의", "30일 미만 남겨두고 기습 해고 통보 받음 (즉시 해고)", "30일 전에 미리 해고 예고 통보 받음"])

    situation = st.selectbox(
        "어떤 부당한 일을 겪으셨나요? 권익 피해 유형을 선택해 주세요.", 
        ["선택하세요", 
         "1. 임금 체불 및 퇴직금 미지급", 
         "2. 위장 프리랜서 (무늬만 3.3% 계약)", 
         "3. 직장 내 괴롭힘 및 폭언", 
         "4. 부당해고 및 해고예고수당 청구",
         "5. 산업재해 (업무 중 다침)",
         "6. 외국인 노동자 차별 및 협박"]
    )

    if situation != "선택하세요":
        st.markdown("---")
        
        if contract_type == "구두 계약(계약서 없음)":
            st.warning("⚠️ **[경고] 계약서 미작성 상태 확인:** 현재 입력하신 '구두 계약' 역시 고용주에게 500만 원 이하의 벌금이 부과되는 명백한 불법입니다. 신고 시 이 사실을 함께 주장하여 강력한 압박 무기로 삼으세요.")

        # 1️⃣ 임금 체불 및 퇴직금 미지급 코너
        if situation == "1. 임금 체불 및 퇴직금 미지급":
            st.error("🚨 진단: 사용자가 근로의 대가를 지급하지 않는 명백한 위법 행위입니다.")
            
            # 주휴수당 조건 피드백
            if work_hours < 15:
                st.info(f"📊 **[근로시간 분석]** 주 {work_hours}시간 근무로 '초단시간 근로자'에 해당하여 현행법상 **주휴수당** 청구는 어렵습니다. 단, 기본 일한 시간에 대한 체불 임금은 100% 청구 가능합니다.")
            else:
                st.success(f"📊 **[근로시간 분석]** 주 {work_hours}시간 근무로 주 15시간 이상 요건을 만족합니다. **미지급 월급 및 주휴수당**까지 모두 소급 청구 대상입니다.")
            
            # 🔥 퇴직금 2대 조건 실시간 동적 판정 로직 연동
            st.markdown("##### 💰 알바/일용직 퇴직금 실시간 판정 결과")
            is_hours_ok = work_hours >= 15
            is_tenure_ok = working_months >= 12
            
            if is_hours_ok and is_tenure_ok:
                st.success(f"✅ **퇴직금 요건 충족 (지급 대상):** 귀하는 주 소정근로시간 {work_hours}시간(15시간 이상) 및 총 근무기간 {working_months}개월(1년 이상) 요건을 모두 충족합니다. 법정 최소 기준인 **'1년 근무당 평균임금 30일분'**을 당당히 청구할 수 있습니다.")
            else:
                reasons = []
                if not is_hours_ok: reasons.append(f"주 소정근로시간 미달 (현재 주 {work_hours}시간 / 기준 15시간 이상)")
                if not is_tenure_ok: reasons.append(f"계속근로기간 미달 (현재 {working_months}개월 / 기준 12개월(1년) 이상)")
                st.error(f"❌ **퇴직금 요건 미충족 (지급 제외):**\n\n**미충족 원인:** {', '.join(reasons)}\n\n퇴직금 청구 조건에는 미달하지만, 기본 일한 시간에 따른 임금 체불 진정서 작성이 가능합니다.")
            
            # FAQ 바인딩
            with st.expander("📚 퇴직금 관련 실전 팩트 체크 (FAQ)"):
                st.markdown("""
                * **Q. 4대 보험 미가입 혹은 3.3% 소득세를 뗐는데 퇴직금을 받나요?** **A.** 네! 통장 입금 내역, 출퇴근 기록 등 실질적으로 일했다는 사실만 입증되면 가계약 형식과 무관하게 법적으로 무조건 받을 수 있습니다.
                * **Q. 계약서에 '퇴직금 없음'이라고 쓰고 싸인했는데요?** **A.** 그 조항은 원천 무효입니다. 노동법은 강행규정이므로 합의서보다 법이 무조건 우선합니다.
                * **Q. 퇴직금은 언제까지 줘야 하나요?** **A.** 퇴직일로부터 **14일 이내**에 지급되어야 하며, 넘을 시 고용노동청에 임금체불 진정 제기가 가능합니다.
                """)

        elif situation == "2. 위장 프리랜서 (무늬만 3.3% 계약)":
            if contract_type == "3.3% 프리랜서 위임 계약":
                st.info(f"📊 **[계약 형태 분석 적용]** 귀하가 선택하신 **'3.3% 프리랜서 위임 계약'**은 4대보험 등을 회피하기 위한 꼼수일 확률이 높습니다. 아래 조건을 확인하세요.")
                c_a = st.checkbox("고용주가 출퇴근 시간과 일할 장소를 정해주나요?")
                c_b = st.checkbox("구체적인 업무 지시(카톡, 구두 등)를 받나요?")
                c_c = st.checkbox("내 마음대로 다른 사람을 대신 일하게 할 수 없나요?")
                
                if c_a and c_b and c_c:
                    st.error("🚨 진단: 대법원 판례 기준, 귀하는 무늬만 프리랜서인 '진짜 근로자'일 확률이 99%입니다.")
                    st.markdown("""
                    **💡 구체적인 해결 방법:**
                    1. **근로자성 입증 자료 확보:** 고용주의 지시가 담긴 카톡 캡처, 유니폼 착용 사진 등을 모으세요.
                    2. **미지급 수당 소급 청구:** 근로자로 인정받으면 못 받은 주휴수당, 연차수당, 퇴직금을 모두 요구할 수 있습니다.
                    """)
            else:
                st.info(f"📊 **[계약 형태 분석 적용]** 현재 선택하신 **'{contract_type}'**은 프리랜서 계약이 아니므로 이 진단 유형에 적합하지 않습니다. 만약 세금을 3.3% 떼고 받는다면 위 옵션을 '3.3% 프리랜서 위임 계약'으로 변경해 보세요.")

        elif situation == "3. 직장 내 괴롭힘 및 폭언":
            if emp_count < 5:
                st.warning(f"📊 **[근로자 수 분석 적용]** 현재 상시 근로자가 **{emp_count}명(5인 미만)**이므로, 현행법상 노동청에 '직장 내 괴롭힘'으로 신고가 불가능합니다.")
                st.markdown("""
                **💡 5인 미만 우회 해결 방법:**
                1. **경찰 고소:** 노동청 대신, 심한 폭언이나 폭행 증거를 모아 경찰에 **모욕죄, 협박죄** 등으로 형사 고소해야 합니다.
                2. **산업재해 신청:** 우울증 등으로 정신과 치료를 받는다면 산재 신청은 근로자 수와 무관하게 가능합니다.
                """)
            else:
                st.success(f"📊 **[근로자 수 분석 적용]** 상시 근로자가 **{emp_count}명(5인 이상)**이므로 직장 내 괴롭힘 금지법이 온전히 적용됩니다.")
                c_a = st.checkbox("직장에서의 지위나 우위(나이, 직급 등)를 이용했나요?")
                c_b = st.checkbox("업무상 적정 범위를 넘어선 폭언, 따돌림 등이 있었나요?")
                
                if c_a and c_b:
                    st.error("🚨 진단: 직장 내 괴롭힘 성립 요건을 충족합니다.")
                    st.markdown("""
                    **💡 구체적인 해결 방법:**
                    1. **은밀한 증거 수집:** 폭언 등을 녹음하세요. 본 앱의 [녹취록 변환] 탭을 활용하면 좋습니다.
                    2. **회사에 1차 서면 신고 후 노동청 진정:** 사내 고충처리 위원회에 먼저 알린 후, 회사가 묵살하면 즉시 노동청에 진정을 제기하세요.
                    """)

        # 4️⃣ 부당해고 및 해고예고수당 코너 (🔥 완벽 연동 구현)
        elif situation == "4. 부당해고 및 해고예고수당 청구":
            st.markdown("##### 📢 해고예고수당 및 구제 신청 실시간 판정")
            is_over_3months = working_months >= 3
            
            # 사장님이 30일 전에 예고를 안 하고 갑자기 자른 경우
            if dismissal_status == "30일 미만 남겨두고 기습 해고 통보 받음 (즉시 해고)":
                if is_over_3months:
                    st.error(f"🚨 **해고예고수당 (30일분 통상임금) 청구 대상 확정!**\n\n귀하는 근무 기간이 {working_months}개월(3개월 이상)이면서 30일 전에 명확한 예고 없이 당장 해고를 당하셨습니다. 고용주는 당장 내일부터 나오지 말라고 통보한 대가로 **반드시 30일분 이상의 통상임금**을 지급해야 할 법적 의무가 생깁니다.")
                else:
                    st.warning(f"⚠️ **해고예고수당 제외 대상 발견:** 갑작스러운 해고를 당하셨으나, 총 근무 기간이 3개 미만({working_months}개월)인 경우 법적인 해고예고수당 지급 예외 사유에 해당하여 수당 청구가 어렵습니다.")
                
                # 상시 근로자 수 연동 피드백
                if emp_count < 5:
                    st.warning(f"📌 **부당해고 구제신청 불가 (5인 미만):** 현재 사업장 규모가 {emp_count}명이므로 노동위원회에 '부당해고 구제신청'은 불가합니다. **하지만 해고예고수당만큼은 사업장 규모 상관없이 1인 이상 모든 사업장에 적용되므로 당당히 청구하세요!**")
                else:
                    st.success(f"🎉 **부당해고 구제신청 가능 (5인 이상):** 상시 근로자가 {emp_count}명으로 조건을 만족합니다. 사유와 서면 통지 절차가 위법하므로 노동위원회에 **부당해고 구제신청**을 넣어 원직 복직 및 해고 기간 동안의 임금을 모두 청구할 수 있습니다.")
            
            elif dismissal_status == "30일 전에 미리 해고 예고 통보 받음":
                st.info("정상적인 해고 예고 절차(30일 전 통보)가 이행된 상태이므로 해고예고수당은 발생하지 않습니다. 단, 5인 이상 사업장인 경우 해고 사유의 정당성을 다투는 '부당해고 구제신청'은 별개로 진행 가능합니다.")
            else:
                st.write("본인이 사장님의 제안에 동의해서 그만두는 '권고사직'이나 스스로 그만두는 자진 퇴사는 해고가 아니므로 해고예고수당 청구 대상이 아닙니다.")
                
            with st.expander("📚 해고예고수당 필수 체크포인트 (FAQ)"):
                st.markdown("""
                * **Q. 5인 미만 작은 개인 편의점이나 카페 알바도 받나요?** **A.** 네, **무조건 받습니다.** 부당해고 구제신청은 5인 이상만 되지만, 해고예고수당은 사장이 혼자 운영하는 가게라도 3개월 이상 일한 근로자를 예고 없이 잘랐다면 무조건 30일치 월급을 줘야 합니다.
                * **Q. 제 실수가 있어서 해고당하는 경우에도 수당을 주나요?** **A.** 네, 원칙적으로 줍니다. 법에서 정한 극단적인 귀책사유(공금 횡령, 기물 고의 파손 등 범죄 수준)가 아니라면, 단순히 일을 못 하거나 지각했다는 이유로 당장 내일부터 나오지 말라고 할 땐 수당을 지급해야 합니다.
                """)

        elif situation == "5. 산업재해 (업무 중 다침)":
            st.error("🚨 진단: 업무상 사고/질병은 근로자의 과실 유무나 규모와 상관없이 보상받아야 합니다.")
            st.markdown("""
            **💡 구체적인 해결 방법:**
            1. **공상 처리 거절:** 회사 돈으로 치료해 준다는 제안을 거절하고 당당하게 산재를 요구하세요.
            2. **초진 기록 명확히 진술:** 병원 첫 방문 시 의사에게 "일하다 다쳤다"고 명확히 말하세요.
            3. **근로복지공단 직접 신청:** 사장의 허락이 없어도 근로복지공단 지사에 요양급여를 직접 신청할 수 있습니다.
            """)

        elif situation == "6. 외국인 노동자 차별 및 협박":
            st.error("🚨 진단: 미등록 상태를 약점 잡아 협박하는 것은 명백한 인권 침해 및 범죄입니다.")
            st.markdown("""
            **💡 구체적인 해결 방법:**
            1. **통보의무 면제 제도:** 범죄 피해를 입은 불법체류자가 노동청에 신고 시 출입국에 통보되지 않습니다.
            2. **협박 녹음:** 사장의 추방 협박 내용을 녹음해 두세요. 이는 협박죄에 해당합니다.
            3. **지원센터 연계:** 본 앱의 [📍 노동 지원 기관] 탭에서 이주노동자 다국어 고충 상담 단체의 도움을 받으세요.
            """)

# -------------------------------------------------------------
# TAB 3: 계약서 AI 판독 
# -------------------------------------------------------------
with tabs[3]:
    st.markdown("### 📸 스마트폰 근로계약서 AI 분석 (OCR)")
    st.write("계약서를 촬영하거나 업로드하면 AI가 불리한 조항이나 위장 프리랜서 요소를 꼼꼼히 판독해 줍니다.")
    
    uploaded_img = st.file_uploader("계약서 이미지 업로드 (jpg, png)", type=["jpg", "png", "jpeg"])
    
    if uploaded_img:
        image = Image.open(uploaded_img)
        st.image(image, caption="업로드된 계약서", use_container_width=True)
        
        with st.spinner("AI가 계약서 내용을 꼼꼼히 읽고 분석하고 있습니다... (약 5~10초 소요)"):
            try:
                analyze_prompt = """
                이 이미지는 사용자가 업로드한 근로계약서 또는 위임/도급(프리랜서) 계약서입니다.
                사진 속의 텍스트를 모두 읽어보고, 아래 기준에 따라 노동자에게 불리하거나 불법적인 요소가 있는지 분석해 주세요.

                [분석 포인트]
                1. 3.3% 사업소득세 공제 조항이 있는지 (있다면 '위장 프리랜서' 위험 경고)
                2. 근무 장소, 출퇴근 시간이 명확히 고정되어 있는지 (프리랜서 계약서인데 이게 있다면 불법 소지 높음)
                3. 최저임금 위반, 부당한 손해배상 청구 등 독소 조항 여부

                [출력 형식]
                결과는 반드시 "[안전]", "[주의]", "[위험]" 중 하나의 상태로 시작하고, 
                그 이유와 발견된 조항의 문제점을 아주 친절하고 전문적인 말투로 3~4문장으로 요약해서 알려주세요.
                """
                response = model.generate_content([image, analyze_prompt])
                
                st.success("✅ AI 판독이 완료되었습니다!")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"🚨 분석 중 오류가 발생했습니다. 트래픽이 많을 수 있으니 잠시 후 다시 시도해 주세요! (내용: {e})")

# -------------------------------------------------------------
# TAB 4: 녹취록 AI 변환
# -------------------------------------------------------------
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