import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 기본 설정 및 사이드바 제거를 위한 와이드 레이아웃
st.set_page_config(page_title="Labor-Link", layout="wide")

# 미학적 개선을 위한 미니멀 폰트 및 스타일 적용
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 깔끔하게 정돈 */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Pretendard', -apple-system, sans-serif;
    }
    /* 탭 메뉴 디자인 커스텀 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre;
        font-size: 16px;
        font-weight: 500;
        color: #64748b;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        color: #1e293b !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #2563eb !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Labor-Link")
st.text("플랫폼 및 일용직 노동 권익 보호 플랫폼")
st.markdown("<br>", unsafe_allow_html=True)

# 상단 탭 내비게이션으로 전환 (사이드바 완전 대체)
tab1, tab2, tab3, tab4 = st.tabs([
    "프로젝트 소개", 
    "상황별 맞춤 법률 지식", 
    "근로 권익 자가진단", 
    "디지털 증거 보관함"
])

# ------------------------------------------------------------------
# TAB 1: 프로젝트 소개 (서연수 분석 자료 기반 정돈)
# ------------------------------------------------------------------
with tab1:
    st.subheader("거대한 시스템 앞에 침묵하는 이들을 위한 안전망")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 현대 노동 현장의 권력 구조와 노동 소외")
        st.write(
            "대학생 및 생계형 일용직 노동자들이 현장에서 경험하는 구조적 문제를 식별하고, "
            "법적 무지와 심리적 위축으로 인해 권리를 포기하는 침묵의 악순환을 끊어내고자 합니다."
        )
        st.write(
            "부당한 처우 앞에서도 대처 방법을 몰라 고개 숙여야 했던 노동자들이 "
            "명확한 법적 지식을 바탕으로 당당하게 자기 권리를 선언할 수 있도록 돕는 실무적 복구 플랫폼입니다."
        )
        
        st.markdown("<br>### 핵심 연구 키워드", unsafe_allow_html=True)
        st.write("1. 도구적 신체: 인간이 주체가 아닌 생산수단으로서 소모되는 현상")
        st.write("2. 구조적 침묵: 불이익에 대한 두려움으로 인해 목소리를 내지 못하는 상태")
        st.write("3. 심리적 재기: 위축 상태에서 벗어나 능동적인 법적 대처를 시작할 수 있는 정서적 회복")
        
    with col2:
        st.markdown("### 플랫폼 운영 목표")
        st.info(
            "구체성\n"
            "실질적 권리 구제 가이드 및 맞춤형 정서 케어 인터페이스 제공\n\n"
            "측정 가능성\n"
            "권익 구제 및 법률 상담 진입 장벽 50% 이상 완화\n\n"
            "달성 가능성\n"
            "기존 구인구직 플랫폼의 정보 비대칭 및 보호 부재 보완\n\n"
            "목적 연관성\n"
            "노동 인권 보호 및 노동자의 주체성 회복\n\n"
            "기한성\n"
            "키스톤 디자인 프로젝트 기간 내 구현 완료"
        )

# ------------------------------------------------------------------
# TAB 2: 상황별 맞춤 법률 지식 (커뮤니티 대체 신규 연계 시스템)
# ------------------------------------------------------------------
with tab2:
    st.subheader("상황별 맞춤 법률 지식 매뉴얼")
    st.text("현재 직면한 현장 문제를 선택하시면 근로기준법 조항에 따른 대응 방향을 안내합니다.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 사용자 상황 선택 인터페이스
    situation = st.selectbox(
        "겪고 계신 부당 처우 유형을 선택해 주세요.",
        [
            "선택하세요",
            "임금 체불 (급여 미지급, 퇴직금 정산 지연)",
            "부당 해고 (기습 해고, 서면 통지 미이행)",
            "직장 내 괴롭힘 및 폭언 (업무 위계에 의한 처우)",
            "휴게시간 및 근로시간 미보장"
        ]
    )
    
    st.markdown("---")
    
    if situation == "임금 체불 (급여 미지급, 퇴직금 정산 지연)":
        st.markdown("### 임금 지급 조항 및 대응 가이드 (근로기준법 제43조, 제36조)")
        st.write("- 법적 기준: 임금은 매월 1회 이상 일정한 날짜를 정하여 전액 지급되어야 합니다. 또한 퇴직 시 14일 이내에 모든 금품 청산이 완료되어야 합니다.")
        st.write("- 권리 구제 안내: 명백한 고용주의 고의성 체불이 입증될 경우 법원에 체불 임금의 3배 이내 금액 손해배상 청구가 가능하도록 법이 개정되었습니다.")
        st.warning("실전 액션 플랜: 즉시 통장 입금 내역 데이터와 가감 없는 출퇴근 기록 수치를 보관함 탭에 기록하세요.")
        
    elif situation == "부당 해고 (기습 해고, 서면 통지 미이행)":
        st.markdown("### 해고의 제한 및 서면 통지 규정 (근로기준법 제23조, 제26조, 제27조)")
        st.write("- 법적 기준: 사용자는 정당한 이유 없이 근로자를 해고할 수 없으며, 적어도 30일 전에 예고해야 합니다. 예고하지 않았을 시에는 30일분 이상의 통상임금을 지급해야 합니다.")
        st.write("- 5인 미만 사업장 특례: 상시 5인 미만 사업장의 경우 부당해고 구제신청 자체는 제한될 수 있으나, 30일 전 해고 예고 조항 및 업무상 부상 기간 내 해고 금지 조항은 동일하게 보호받습니다.")
        st.warning("실전 액션 플랜: 해고 사유와 시기가 명시된 서면 통지서를 요구하시고, 관련 대화나 문자 메시지를 백업해 두세요.")
        
    elif situation == "직장 내 괴롭힘 및 폭언 (업무 위계에 의한 처우)":
        st.markdown("### 직장 내 괴롭힘 금지법 (근로기준법 제76조의2)")
        st.write("- 법적 기준: 직장에서의 지위나 관계 우위를 이용해 업무상 적정 범위를 넘어 신체적, 정신적 고통을 주거나 근무 환경을 악화시키는 행위는 전면 금지되어 있습니다.")
        st.write("- 판례 가이드: 업무상 위계에 의한 폭언 및 모욕은 법적 처벌 및 정서적 위자료 청구의 근거가 됩니다.")
        st.warning("실전 액션 플랜: 폭언이 발생한 일시, 장소, 목격자를 기록하고 현장 녹취록 파일을 확보하는 것이 가장 강력합니다.")
        
    elif situation == "휴게시간 및 근로시간 미보장":
        st.markdown("### 법정 휴게시간 및 대기시간 규정 (근로기준법 제50조, 제54조)")
        st.write("- 법적 기준: 근로시간이 4시간인 경우 30분 이상, 8시간인 경우 1시간 이상의 휴게시간이 근무 도중에 보장되어야 합니다.")
        st.write("- 대기시간 인정: 작업을 위해 고용주의 지휘 및 감독 아래에 있는 대기시간은 휴게시간이 아니라 명백한 근로시간에 포함됩니다.")
        st.warning("실전 액션 플랜: 휴게시간에도 실질적으로 업무 지시를 받았거나 대기 상태였다면, 해당 시간 기록을 증거 보관함에 작성해 두세요.")

# ------------------------------------------------------------------
# TAB 3: 근로 권익 자가진단 (강정훈 법률 기준 가이드 기반 수치 연산 로직)
# ------------------------------------------------------------------
with tab3:
    st.subheader("법정 근로 조건 기준 자가진단")
    st.text("현재 근무 환경 수치를 입력하시면 표준 가이드라인 위반 여부를 연산합니다.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("diagnosis_form"):
        col1, col2 = st.columns(2)
        with col1:
            emp_count = st.number_input("상시 근로자 수 (본인 제외 현장 인원)", min_value=1, value=5)
            weekly_hours = st.number_input("1주일 총 소정 근로시간", min_value=1, value=16)
            daily_hours = st.number_input("하루 평균 근무 시간", min_value=1, value=8)
        with col2:
            has_contract = st.radio("근로계약서를 서면이나 전자문서로 교부받으셨습니까?", ["예", "아니오"])
            has_pay_stub = st.radio("임금명세서를 교부받으셨습니까?", ["예", "아니오"])
            rest_time = st.number_input("보장받은 총 휴게시간 (분 단위)", min_value=0, value=60)
            
        submitted = st.form_submit_button("진단 결과 분석")
        
    if submitted:
        st.markdown("### 분석 보고서")
        violation_detected = False
        
        if emp_count < 5:
            st.warning(
                "상시 5인 미만 사업장 안내\n"
                "해당 사업장은 상시 근로자 수가 5인 미만으로 파악되어 해고구제신청이나 휴업수당 일부 조항이 제외될 수 있습니다. "
                "단, 30일 전 해고 예고 의무는 동일하게 적용됩니다."
            )
        
        if weekly_hours < 15:
            st.info(
                "단시간 근로자 규정 안내\n"
                "주 소정근로시간이 15시간 미만인 경우 주휴수당 및 연차유급휴가 지급 대상에서 제외됩니다."
            )
        else:
            st.success("주휴수당 지급 기준 충족: 주 15시간 이상 근무자이므로 법정 주휴수당 청구 권리가 발생합니다.")
            
        required_rest = 30 if daily_hours >= 4 and daily_hours < 8 else (60 if daily_hours >= 8 else 0)
        if rest_time < required_rest:
            st.error(f"휴게시간 미달 (근로기준법 제54조 위반 의심): 하루 {daily_hours}시간 근무 시 법정 최저 휴게시간은 {required_rest}분입니다.")
            violation_detected = True
            
        if has_contract == "아니오":
            st.error("근로조건 서면 명시 의무 위반 (근로기준법 제17조 위반 의심): 근로계약서 미교부는 명백한 위법입니다.")
            violation_detected = True
        if has_pay_stub == "아니오":
            st.error("임금명세서 교부 의무 위반 (근로기준법 제48조 위반 의심): 상세 계산 방법이 적힌 명세서 미교부는 위법입니다.")
            violation_detected = True
            
        if not violation_detected and emp_count >= 5:
            st.success("입력된 기초 법정 근로 조건이 표준 가이드라인에 부합합니다.")

# ------------------------------------------------------------------
# TAB 4: 디지털 증거 보관함 (실전 입증 자료 구조화 기능)
# ------------------------------------------------------------------
with tab4:
    st.subheader("디지털 증거 보관함")
    st.text("부당 처우에 대처하기 위해 법원에서 요구하는 객관적 증거 수치를 기록해 두는 공간입니다.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if "evidence_db" not in st.session_state:
        st.session_state.evidence_db = []
        
    with st.expander("기록 추가하기"):
        ev_date = st.date_input("기록 일자", datetime.now())
        ev_type = st.selectbox("증거 유형", ["출퇴근 기록 수치", "대화 녹취 데이터", "임금 입금 내역역", "부당 지시 카카오톡 문자"])
        ev_detail = st.text_area("구체적 상황 기술 (인물 명, 시간, 금액 수치 명시)")
        
        if st.button("보관함 저장"):
            st.session_state.evidence_db.append({
                "일자": ev_date,
                "유형": ev_type,
                "상세 정황": ev_detail
            })
            st.success("데이터가 안전하게 레코드에 등록되었습니다.")
            
    if st.session_state.evidence_db:
        df = pd.DataFrame(st.session_state.evidence_db)
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="진정서 복구 제출용 CSV 파일 다운로드",
            data=csv,
            file_name="labor_evidence_archive.csv",
            mime="text/csv"
        )
    else:
        st.info("저장된 증거 레코드가 없습니다.")