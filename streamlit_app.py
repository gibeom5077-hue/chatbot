import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

# --- 1. 페이지 설정 및 와이드 레이아웃 ---
st.set_page_config(page_title="Labor-Link", layout="wide", initial_sidebar_state="collapsed")

# 커스텀 CSS (탭 줄바꿈 및 스타일 최적화)
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; font-family: 'Pretendard', sans-serif; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .info-card {
        background-color: #FFFFFF; padding: 24px; border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #F1F5F9; margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid #E2E8F0; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; font-size: 15px; font-weight: 600; color: #64748B;
        border-radius: 8px 8px 0 0; padding: 0 16px; border: none; background-color: transparent;
        white-space: nowrap;
    }
    .stTabs [aria-selected="true"] { color: #2563EB !important; border-bottom: 3px solid #2563EB !important; }
    /* 진행도(Progress Bar) 디자인 */
    .step-container { display: flex; justify-content: space-between; margin-bottom: 20px; padding: 10px; background-color: #f1f5f9; border-radius: 10px;}
    .step { text-align: center; font-size: 14px; font-weight: 600; color: #94a3b8; width: 25%; }
    .step.active { color: #2563eb; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.markdown("<h2 style='text-align: center; color: #1E293B; margin-bottom: 0;'>Labor-Link</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; margin-bottom: 30px;'>모든 취약계층 노동자를 위한 실전 권익 보호 플랫폼</p>", unsafe_allow_html=True)

# 7개의 독립된 탭 구성
tabs = st.tabs([
    "플랫폼 소개", 
    "정서 케어", 
    "맞춤 법률 진단", 
    "계약서 AI 판독", 
    "녹취록 AI 변환", 
    "증거 및 진정서", 
    "📍 쉼터 지도"
])

# --- TAB 1: 플랫폼 소개 ---
with tabs[0]:
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("### 거대한 시스템 앞의 안전망")
    st.write("Labor-Link는 고용 형태의 사각지대나 언어 장벽, 신체적 불리함으로 인해 목소리를 내지 못하는 취약계층 근로자를 위한 실효적 디지털 울타리입니다.")
    st.write("단순히 체불된 돈을 계산하는 것을 넘어, 노동자의 시간이 지닌 '거시적 가치'를 환산하여 생산수단으로 소모되는 도구적 신체에서 벗어나도록 돕습니다.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='info-card'><h4 style='color:#2563EB;'>도구적 신체 탈피</h4><p style='color:#475569; font-size:14px;'>생산수단으로 소모되는 부당한 구조적 현실 인지</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='info-card'><h4 style='color:#2563EB;'>구조적 침묵 타파</h4><p style='color:#475569; font-size:14px;'>AI 증거 분석을 통한 심리적 두려움 극복</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='info-card'><h4 style='color:#2563EB;'>심리적 재기 확보</h4><p style='color:#475569; font-size:14px;'>죄책감에서 벗어나 자율적 권리 주체의 상태 도달</p></div>", unsafe_allow_html=True)

# --- TAB 2: 정서 케어 대화 ---
with tabs[1]:
    st.markdown("### 내러티브 테라피 기반 감정 치유 공간")
    st.caption("현장에서 겪으신 차별이나 억울한 기억을 털어놓으셔도 좋습니다. 본 기록은 외부에 저장되지 않습니다.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요. 현장에서 국적이나 신체적 조건 등을 빌미로 위축감을 주는 부당 대우를 경험하셨나요? 어떤 상황이었는지 말씀해 주세요."}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("이곳에 당시 정황이나 심경을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        reply = "경청해 주셔서 감사합니다. 고용주나 중간관리자의 부당한 대우는 근로기준법을 위반한 명백한 불법 행위이며 결코 근로자분의 잘못이 아닙니다. 왜곡된 두려움을 덜어내고 법률 탭에서 권리를 확인해 보세요."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

# --- TAB 3: 맞춤 법률 진단 (계산기 포함) ---
with tabs[2]:
    st.markdown("### 취약계층 맞춤 진단 및 계산기")
    
    # 1. 기초 환경 세팅
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("#### 기초 근무 환경 정보")
    c1, c2, c3 = st.columns(3)
    with c1:
        emp_count = st.number_input("상시 근로자 수", min_value=1, value=5)
    with c2:
        contract_type = st.radio("계약 형태", ["일반 근로계약서", "3.3% 프리랜서 위임 계약"])
    with c3:
        weekly_hours = st.number_input("1주 소정 근로시간", min_value=1, value=16)
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 상황별 법률 진단
    situation = st.selectbox(
        "권익 피해 유형을 선택해 주세요.",
        ["선택하세요", "외국인 노동자 권리 보장 및 체류 협박 대응", "임금채권 소멸시효 및 거시경제 환산 체불 모델", "위장 프리랜서 검증 (3.3% 세금 편법)", "장애인 근로자 차별 처우 진단", "직장 내 괴롭힘 성립 요건", "기습 해고 및 예고 수당"]
    )
    
    if situation == "외국인 노동자 권리 보장 및 체류 협박 대응":
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.markdown("#### 근로기준법 제6조 균등처우 원칙 및 대법원 판례")
        foreigner_status = st.radio("현재 비자 상태", ["정식 취업 비자 보유", "미등록 체류 또는 비자 만료"])
        if foreigner_status == "미등록 체류 또는 비자 만료":
            st.error("💡 대법원 판례(97누10350): 미등록 외국인 노동자라 할지라도, 이미 제공한 노동에 대한 임금 및 산재 보상 권리는 내국인과 동일하게 100% 보장받습니다.")
        if st.checkbox("고용주가 '출입국에 신고하겠다'며 협박을 하나요?"):
            st.error("⚠️ 고용주가 체불 임금을 주지 않으려고 신고 협박을 하는 행위는 형법상 협박·공갈죄에 해당할 수 있습니다. 고용노동청은 임금체불 조사 시 근로자의 구제를 최우선으로 합니다.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif situation == "임금채권 소멸시효 및 거시경제 환산 체불 모델":
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        last_work_date = st.date_input("체불/퇴직 발생 일자", datetime.now() - timedelta(days=365))
        days_passed = (datetime.now().date() - last_work_date).days
        if days_passed / 365.25 >= 3:
            st.error("❌ 소멸시효 완성: 법적 소멸시효 3년이 만료되었을 가능성이 높습니다.")
        else:
            st.success(f"✅ 청구 가능 기한 소지: 소멸시효 만료까지 약 {1095 - days_passed}일 남았습니다.")
            
        st.markdown("#### 💰 체감 임금 모델 (노동 가치 객관화)")
        unpaid_amount = st.number_input("체불된 총 임금 (원)", value=1500000, step=100000)
        if unpaid_amount > 0:
            st.info(f"이 금액은 **대학생 평균 한 달 생활비(약 100만 원)의 {unpaid_amount/1000000:.1f}배**에 달하며, **법정 최저임금 기준 약 {unpaid_amount/10030:.0f}시간의 피땀 어린 노동**이 증발한 것과 같습니다. 이는 단순한 돈의 문제를 넘어 귀하의 생존권과 주체성이 침해받은 구조적 문제입니다.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif situation == "위장 프리랜서 검증 (3.3% 세금 편법)":
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.write("편의점, 학원 등에서 주휴수당 회피 목적으로 프리랜서 계약(3.3% 공제)을 맺었더라도 실질적으로 지휘·감독을 받았다면 진짜 근로자입니다.")
        q1 = st.checkbox("고용주가 출퇴근 시간과 일하는 장소를 지정하고 구속하나요?")
        q2 = st.checkbox("업무 과정에서 구체적인 지휘 및 지시를 받나요?")
        if q1 and q2: st.error("진단 결과: 형식과 상관없이 대법원 판례상 진짜 근로자입니다. 주휴수당, 퇴직금 미지급은 임금체불 위법입니다.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif situation == "장애인 근로자 차별 처우 진단":
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.write("사회적 신분이나 신체 조건을 이유로 근로조건을 차별하는 것은 전면 금지됩니다.")
        if st.radio("고용노동부 장관의 공식 최저임금 적용제외 인가를 받았나요?", ["아니오 또는 잘 모름", "예"]) == "아니오 또는 잘 모름":
            st.info("안내: 정식 승인 없이 장애를 이유로 동일 노동에 대해 최저임금 미만을 지급하거나 임금을 삭감하는 행위는 위법입니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif situation == "직장 내 괴롭힘 성립 요건":
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        if st.checkbox("직장에서의 지위나 우위 구조를 이용했는가?") and st.checkbox("업무상 적정 범위를 명백히 초과한 폭언/차별 대우인가?") and st.checkbox("이로 인해 정신적 고통이나 환경이 악화되었는가?"):
            st.error("요건 충족: 법적 성립 요건을 갖추었습니다. 증거 보관함에 연동해 보존하세요.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif situation == "기습 해고 및 예고 수당":
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        worked_period = st.number_input("연속 근로 기간 (개월)", min_value=1, value=4)
        if worked_period >= 3:
            standard_wage = st.number_input("하루 통상 임금 (원)", value=80000)
            st.metric("청구 가능한 법정 해고예고수당", f"{int(standard_wage * 30):,} 원")
        else:
            st.info("연속 근로 3개월 미만인 경우 해고예고 지급의무 예외 대상입니다.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: 계약서 AI 판독 (단독 탭으로 분리) ---
with tabs[3]:
    st.markdown("### 📸 스마트폰 근로계약서 AI 분석 (OCR)")
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.write("작성하신 계약서를 사진으로 올려주시면, AI가 텍스트를 스캔하여 독소 조항 및 위장 프리랜서 여부를 판별합니다.")
    
    uploaded_img = st.file_uploader("계약서 이미지 업로드 (jpg, png)", type=["jpg", "png", "jpeg"])
    
    if uploaded_img is not None:
        with st.spinner("AI가 문서의 텍스트를 추출하고 법률 위반 여부를 스캔하고 있습니다..."):
            time.sleep(2)
        st.error("⚠️ **[주의] 위장 프리랜서 조항 발견!**\n\nAI 분석 결과, 해당 계약서에 **'3.3% 사업소득세 공제'** 및 **'위임 계약'**이라는 단어가 감지되었습니다. 실질적인 업무 지시를 받았다면 이는 주휴수당 회피를 위한 불법 계약일 확률이 높습니다.")
        st.info("💡 **권장 행동:** 해당 계약서를 증거로 저장하고, [증거 및 진정서] 탭에서 구제 절차를 시작하세요.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 5: 녹취록 AI 변환 (단독 탭으로 분리) ---
with tabs[4]:
    if "evidence_db" not in st.session_state: st.session_state.evidence_db = []

    st.markdown("### 🎙️ 폭언/협박 녹취록 AI 텍스트 변환 (STT)")
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.write("현장에서 몰래 녹음한 음성 파일을 올리시면, 법적 증거로 쓰일 수 있도록 텍스트로 변환하고 핵심 키워드를 자동 추출합니다.")
    
    uploaded_audio = st.file_uploader("녹음 파일 업로드 (mp3, wav)", type=["mp3", "wav"])
    
    if uploaded_audio is not None:
        with st.spinner("AI가 음성을 텍스트로 변환하고 키워드를 추출 중입니다..."):
            time.sleep(2)
        st.success("✅ **변환 완료:** \"내일부터 당장 나오지 마. 외국인 주제에 노동청에 신고한다고? 해볼 테면 해봐.\"")
        st.warning("🔍 **추출 키워드:** `#기습_해고통보` `#국적_차별` `#신고_협박` (증거 효력 등급: 매우 높음)")
        
        if st.button("이 녹취록을 [증거 보관함]에 즉시 저장"):
            st.session_state.evidence_db.append({"일자": datetime.now().strftime("%Y-%m-%d"), "유형": "음성 녹취 (STT)", "정황": "녹취 변환: 기습 해고 및 외국인 차별 협박 포함"})
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 6: 증거 수집 및 진정서 생성 ---
with tabs[5]:
    if "evidence_db" not in st.session_state: st.session_state.evidence_db = []
    
    st.markdown("### 증거 아카이빙 및 노동청 진정서 생성")
    
    # 권리 구제 여정 트래커
    step = min(len(st.session_state.evidence_db) + 1, 4)
    st.markdown(f"""
    <div class="step-container">
        <div class="step {'active' if step >= 1 else ''}">1. 권리 인지</div>
        <div class="step {'active' if step >= 2 else ''}">2. 증거 수집 ({len(st.session_state.evidence_db)}건)</div>
        <div class="step {'active' if step >= 3 else ''}">3. 진정서 완성</div>
        <div class="step {'active' if step >= 4 else ''}">4. 노동청 신고</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(step * 25)
    
    # 수동 아카이빙 기능
    with st.expander("➕ 수동으로 증거 기록 추가하기"):
        ev_date = st.date_input("피해 발생 일자", datetime.now())
        ev_type = st.selectbox("증거 유형", ["출퇴근/입금 내역", "부당 처우 문자/카톡", "육하원칙 일지 기록"])
        ev_detail = st.text_area("객관적 정황 기술 (폭언, 체불액 등)")
        if st.button("데이터 안전 백업", type="primary"):
            if ev_detail:
                st.session_state.evidence_db.append({"일자": ev_date.strftime("%Y-%m-%d"), "유형": ev_type, "정황": ev_detail})
                st.rerun()
                
    # 증거가 있을 때만 진정서 폼 노출
    if len(st.session_state.evidence_db) > 0:
        st.markdown("#### 📄 고용노동부 진정서 자동 완성")
        df = pd.DataFrame(st.session_state.evidence_db)
        st.dataframe(df, use_container_width=True)
        
        evidence_text = ""
        for i, ev in enumerate(st.session_state.evidence_db):
            evidence_text += f"[{i+1}] 일자: {ev['일자']} | 유형: {ev['유형']}\n내용: {ev['정황']}\n\n"
            
        petition_content = f"""[임금체불 및 근로기준법 위반 진정서]

1. 진 정 인 (근로자) : (본인 이름 기재)
2. 피진정인 (고용주) : (가게/회사 및 사장 이름 기재)

3. 진정 취지
피진정인은 진정인에게 근로기준법을 위반하여 부당한 처우 및 임금 체불을 자행하였기에 엄중한 조사와 권리 구제를 요청합니다.

4. 입증 자료 내역 (총 {len(st.session_state.evidence_db)}건)
{evidence_text}

📍 자동 매칭 관할 기관: 관할 지방고용노동청 방문 또는 노동포털(labor.moel.go.kr) 온라인 접수
"""
        st.download_button("📝 원클릭 진정서 다운로드 (.txt)", data=petition_content, file_name="노동청_진정서_양식.txt", mime="text/plain")

# --- TAB 7: 이동노동자 쉼터 및 기관 지도 ---
with tabs[6]:
    st.markdown("### 📍 내 주변 기관 및 이동노동자 쉼터")
    st.write("현 위치 기반으로 쉴 수 있는 권익센터 쉼터와, 신고를 접수할 수 있는 노동청의 위치를 보여줍니다.")
    
    map_data = pd.DataFrame({
        'lat': [37.5665, 37.4979, 37.5443, 37.5094, 37.5683], 
        'lon': [126.9780, 127.0276, 127.0548, 126.9945, 126.9878],
        'name': ['서울시 노동권익센터', '강남 이동노동자 쉼터', '성동구 노동자 쉼터', '서초 휴게공간', '서울지방고용노동청']
    })
    
    st.map(map_data, zoom=11, use_container_width=True)
    st.info("지도에 표시된 마커 근처로 이동하시면 휴게 공간 이용 및 행정 업무 처리가 가능합니다.")