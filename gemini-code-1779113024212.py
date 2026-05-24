import streamlit as st
import pandas as pd
from datetime import datetime

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Labor-Link 플랫폼",
    page_icon="⚖️",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 스타일링 (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; font-family: 'Pretendard', sans-serif; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E0E0E0; }
    h1, h2, h3 { color: #1A1A1A; font-weight: 700; }
    /* 카드 형태 UI 스타일 */
    .info-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #4F46E5; color: white; border-radius: 8px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 사이드바 구성 ---
with st.sidebar:
    st.markdown("## ⚖️ Labor-Link")
    st.caption("플랫폼·일용직 노동자 안전망")
    st.markdown("---")
    
    menu = st.radio(
        "메뉴를 선택하세요",
        ["🏠 홈 (Home)", "🧠 심리적 재기 (정서 케어)", "⚖️ 상황별 맞춤 법률 지식", "📁 디지털 증거 보관함"]
    )
    st.markdown("---")
    st.caption("서울시 노동권익센터 연계망 지향")
    st.caption(f"Today: {datetime.now().strftime('%Y-%m-%d')}")

# --- 1. 홈 (Home) ---
if menu == "🏠 홈 (Home)":
    st.title("노동 존엄성 회복을 위한 첫걸음")
    st.markdown("<div class='info-card'>현대 노동 현장의 거대한 권력 구조 속에서 침묵을 강요받던 노동자들이 당당하게 자기 권리를 선언할 수 있도록 돕는 실무적·심리적 복구 플랫폼입니다.</div>", unsafe_allow_html=True)
    
    st.subheader("💡 우리의 핵심 가치")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color:#4F46E5;'>1. 도구적 신체 탈피</h3>
            <p>인간이 주체가 아닌 생산수단으로서 소모되는 '노동 소외' 현상을 식별하고 존엄성을 회복합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color:#4F46E5;'>2. 구조적 침묵 타파</h3>
            <p>고용주의 책임 전가와 인사 불이익에 대한 두려움으로 목소리를 내지 못하는 상태를 타파합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='info-card'>
            <h3 style='color:#4F46E5;'>3. 심리적 재기</h3>
            <p>위축 상태에서 벗어나 능동적인 법적 대처를 시작할 수 있는 정서적 회복탄력성을 제공합니다.</p>
        </div>
        """, unsafe_allow_html=True)

# --- 2. 심리적 재기 (인지행동/이야기 치료 기반) ---
elif menu == "🧠 심리적 재기 (정서 케어)":
    st.title("심리적 재기 및 정서적 복구")
    st.write("부당한 대우로 인한 상처를 치유하고, 자존감을 회복하는 공간입니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("🗣️ 내러티브 테라피 (이야기 치료)")
        st.write("피해 경험을 혼자 삭히지 않고 겉으로 꺼내어 객관화해 보세요. 당신의 잘못이 아닙니다.")
        
        user_feeling = st.text_area("그때 사장님이 그렇게 말했을 때 기분이 어떠셨나요? 견디기 힘들었던 부분을 편하게 적어주세요.")
        if st.button("감정 털어놓기"):
            if user_feeling:
                st.success("이야기를 들려주셔서 감사합니다. 부당한 대우는 명백한 고용주의 위법 행위이며, 당신이 위축될 이유가 없습니다. 우리는 연대할 수 있습니다.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("🧠 인지재구성 (CBT 기반)")
        st.write("부당 처우 직후 흔히 빠지는 왜곡된 인지를 바로잡습니다.")
        st.info(
            "❌ **왜곡된 인지:** '내가 일을 못 해서 화가 나신 걸까? 나만 조용히 그만두면 돼.'\n\n"
            "⭕ **객관적 인지:** '이것은 내 업무 능력의 문제가 아니라, 권력을 이용한 고용주의 명백한 폭력이자 근로기준법 위반이다.'"
        )
        st.markdown("</div>", unsafe_allow_html=True)

# --- 3. 상황별 맞춤 법률 지식 ---
elif menu == "⚖️ 상황별 맞춤 법률 지식":
    st.title("상황별 맞춤 법률 매뉴얼")
    
    situation = st.selectbox(
        "겪고 계신 부당 처우 유형을 선택해 주세요.",
        ["선택하세요", "임금 체불 및 퇴직금 지연", "직장 내 괴롭힘 및 폭언", "부당 해고 (기습 해고)", "휴게시간 미보장"]
    )
    
    if situation == "직장 내 괴롭힘 및 폭언":
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("🚨 직장 내 괴롭힘 금지법 (제76조의2) 자가진단")
        st.write("고용노동청에 진정을 넣기 위한 **엄격한 3대 성립 요건**을 확인해 보세요.")
        
        c1 = st.checkbox("1. 직장에서의 지위나 관계 등의 우위를 이용했는가?")
        c2 = st.checkbox("2. 업무상 적정범위를 넘었는가? (사적인 심부름, 폭언 등)")
        c3 = st.checkbox("3. 신체적·정신적 고통을 주거나 근무환경을 악화시켰는가?")
        
        if c1 and c2 and c3:
            st.error("⚠️ 3가지 요건이 모두 충족되었습니다. 명백한 '직장 내 괴롭힘'에 해당하며 노동청 진정 대상입니다. 즉시 [디지털 증거 보관함]에 당시 상황을 육하원칙으로 기록하세요.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    elif situation == "임금 체불 및 퇴직금 지연":
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("💰 임금 지급 조항 (제43조, 제36조)")
        st.write("- **원칙:** 임금은 매월 1회 이상 전액 지급되어야 하며, 퇴직 시 14일 이내에 모든 금품이 청산되어야 합니다.")
        st.write("- **알바몬 권익센터 연계:** 체불 금액이 크거나 대응이 막막하다면, 알바몬 전문노무상담 게시판을 통해 무료 자문을 구할 수 있습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif situation == "부당 해고 (기습 해고)":
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("🚫 해고 예고 및 제한 (제23조, 제26조, 제27조)")
        st.write("- **30일 전 예고 의무:** 사용자는 적어도 30일 전에 해고를 예고해야 하며, 지키지 않을 시 30일분 이상의 통상임금(해고예고수당)을 지급해야 합니다.")
        st.write("- **서면 통지:** 해고 사유와 시기를 서면으로 통지하지 않은 해고는 효력이 없습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 4. 디지털 증거 보관함 ---
elif menu == "📁 디지털 증거 보관함":
    st.title("디지털 증거 아카이빙")
    st.write("법적 구제를 위해 가장 중요한 '객관적 증거'를 수집하고 저장하는 공간입니다.")
    
    if "evidence_db" not in st.session_state:
        st.session_state.evidence_db = []
        
    with st.expander("➕ 법적 효력이 있는 증거 기록하기", expanded=True):
        st.info("💡 **증거 수집 팁:** 폭언 당시의 상황을 날짜/시간/참석자와 함께 육하원칙 일지 양식으로 기록하세요.")
        
        ev_date = st.date_input("발생 일자", datetime.now())
        ev_type = st.selectbox("증거 유형", ["업무지시 카톡/문자 캡처", "출퇴근 기록 및 임금 내역", "폭언 현장 녹취 (합법 기준 충족)", "육하원칙 일지"])
        ev_detail = st.text_area("육하원칙(누가, 언제, 어디서, 무엇을, 어떻게, 왜)에 기반한 상세 정황 기술")
        
        if st.button("보관함에 저장하기"):
            if ev_detail:
                st.session_state.evidence_db.append({
                    "발생 일자": ev_date,
                    "증거 유형": ev_type,
                    "상세 정황 (육하원칙)": ev_detail
                })
                st.success("증거가 안전하게 저장되었습니다.")
            else:
                st.warning("상세 정황을 입력해 주세요.")
                
    if st.session_state.evidence_db:
        df = pd.DataFrame(st.session_state.evidence_db)
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 고용노동청 진정 제출용 증거 일지 다운로드 (CSV)",
            data=csv,
            file_name="labor_evidence_log.csv",
            mime="text/csv"
        )