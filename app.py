import math

import pandas as pd
import streamlit as st

# =====================================================================
# CẤU HÌNH
# =====================================================================
st.set_page_config(page_title="Thẩm định tín dụng", page_icon="🏦", layout="centered")

TIEU_DE = "Phần mềm thẩm định tín dụng_Nguyễn Viết Minh Khánh"
TRIEU = 1_000_000
PT_GOC_DEU = "Gốc đều + lãi tính trên số tiền vay"
PT_TRA_DEU = "Trả góp đều hàng tháng (niên kim)"

# =====================================================================
# GIAO DIỆN (CSS)
# =====================================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
.stApp, .stApp p, .stApp label, .stApp input, .stApp textarea, .stApp h1, .stApp h2, .stApp h3,
.stApp h4, .stApp li, .stApp button p, .stApp td, .stApp th {font-family:'Be Vietnam Pro',sans-serif !important;}
.stApp {background:#F4F6FB;}
header[data-testid="stHeader"] {background:transparent;}
.block-container {padding-top:2rem; padding-bottom:3rem; max-width:860px;}

.hero {background:linear-gradient(135deg,#0B3C74 0%,#1565C0 60%,#1E88E5 100%); border-radius:18px;
       padding:26px 28px; color:#fff; box-shadow:0 10px 30px rgba(11,60,116,.25); margin-bottom:18px;}
.hero-badge {display:inline-block; background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.25);
       padding:4px 12px; border-radius:999px; font-size:.75rem; letter-spacing:.08em; font-weight:600;}
.hero-title {font-size:1.65rem; font-weight:800; line-height:1.3; margin:12px 0 6px;}
.hero-sub {opacity:.85; font-size:.95rem;}

.sec {font-weight:700; color:#0B3C74; font-size:1.02rem; margin:4px 0 2px; display:flex; gap:8px; align-items:center;}
.sec small {font-weight:500; color:#6B7280; font-size:.8rem;}

div[data-testid="stForm"] {background:#fff; border:1px solid #E5E9F2; border-radius:16px;
       padding:20px 22px; box-shadow:0 4px 16px rgba(15,23,42,.05);}

.result {border-radius:16px; padding:20px 24px; display:flex; justify-content:space-between; align-items:center;
       gap:16px; flex-wrap:wrap; color:#fff; margin:6px 0 14px;}
.result.ok {background:linear-gradient(135deg,#0F9D58,#16A34A);}
.result.fail {background:linear-gradient(135deg,#C62828,#E53935);}
.r-label {font-size:.82rem; opacity:.9; text-transform:uppercase; letter-spacing:.06em;}
.r-value {font-size:2.6rem; font-weight:800; line-height:1.1;}
.r-status {font-size:1.25rem; font-weight:800; text-align:right;}
.r-sub {font-size:.88rem; opacity:.9; text-align:right;}

.gauge {background:#fff; border:1px solid #E5E9F2; border-radius:14px; padding:16px 18px 10px; margin-bottom:14px;}
.g-head {display:flex; justify-content:space-between; font-size:.85rem; color:#475569; margin-bottom:10px;}
.g-track {position:relative; height:14px; border-radius:999px;
       background:linear-gradient(90deg,#DCFCE7 0%,#DCFCE7 var(--a),#FEF3C7 var(--a),#FEF3C7 var(--t),#FEE2E2 var(--t),#FEE2E2 100%);}
.g-fill {position:absolute; left:0; top:0; height:100%; border-radius:999px;}
.g-thr {position:absolute; top:-6px; width:2px; height:26px; background:#0F172A;}
.g-thr span {position:absolute; top:-20px; left:50%; transform:translateX(-50%); font-size:.72rem;
       font-weight:700; color:#0F172A; white-space:nowrap;}
.g-scale {display:flex; justify-content:space-between; font-size:.72rem; color:#94A3B8; margin-top:6px;}

.kpis {display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:8px;}
.kpi {background:#fff; border:1px solid #E5E9F2; border-radius:14px; padding:14px 16px;}
.kpi-l {font-size:.78rem; color:#64748B;}
.kpi-v {font-size:1.15rem; font-weight:700; color:#0F172A; margin-top:2px;}
.kpi-s {font-size:.75rem; margin-top:2px;}
@media (max-width:640px){ .kpis{grid-template-columns:1fr;} .r-status,.r-sub{text-align:left;} }

.sol {background:#fff; border:1px solid #E5E9F2; border-radius:14px; padding:16px 18px; margin-bottom:12px;
       border-left:5px solid #CBD5E1; min-height:190px;}
.sol.ok {border-left-color:#16A34A;} .sol.warn {border-left-color:#F59E0B;} .sol.na {border-left-color:#94A3B8;}
.sol-h {display:flex; justify-content:space-between; align-items:center; gap:8px;}
.sol-t {font-weight:700; color:#0F172A;}
.badge {font-size:.72rem; font-weight:700; padding:3px 10px; border-radius:999px; white-space:nowrap;}
.b-ok {background:#DCFCE7; color:#166534;} .b-warn {background:#FEF3C7; color:#92400E;} .b-na {background:#F1F5F9; color:#475569;}
.sol-v {font-size:1.25rem; font-weight:800; color:#0B3C74; margin:8px 0 2px;}
.sol-d {font-size:.86rem; color:#334155;}
.sol-tip {font-size:.8rem; color:#64748B; margin-top:8px; padding-top:8px; border-top:1px dashed #E2E8F0;}

.hint {background:#fff; border:1px dashed #CBD5E1; border-radius:14px; padding:22px; text-align:center; color:#64748B;}
.plan {background:#EFF6FF; border:1px solid #BFDBFE; border-radius:14px; padding:14px 16px; color:#1E3A8A; font-size:.92rem;}
.foot {text-align:center; color:#94A3B8; font-size:.78rem; margin-top:28px;}
button[data-baseweb="tab"] p {font-weight:600;}
</style>
""",
    unsafe_allow_html=True,
)


# =====================================================================
# HÀM TÍNH TOÁN
# =====================================================================
def vnd(x: float) -> str:
    return f"{x:,.0f} đ".replace(",", ".")


def trieu(x: float) -> str:
    """Hiển thị gọn theo triệu đồng."""
    v = round(x / TRIEU, 2)
    nguyen, le = f"{v:,.2f}".split(".")
    le = le.rstrip("0")
    return nguyen.replace(",", ".") + ("," + le if le else "") + " triệu"


def pct(x) -> str:
    return "—" if x is None else f"{x * 100:.2f}%"


def tra_hang_thang(stv, nam, LS, pt):
    if stv <= 0:
        return 0.0
    n, r = nam * 12, LS / 12
    if pt == PT_TRA_DEU:
        return stv * r / (1 - (1 + r) ** (-n)) if r > 0 else stv / n
    return stv / n + stv * r


def tinh_dti(stv, nam, LS, nc, tn, cpsh, sn, pt):
    con_lai = tn - cpsh * sn
    if con_lai <= 0:
        return None
    return (tra_hang_thang(stv, nam, LS, pt) + nc) / con_lai


def html(s: str):
    st.markdown(s, unsafe_allow_html=True)


# =====================================================================
# HEADER
# =====================================================================
html(
    f'<div class="hero"><span class="hero-badge">THẨM ĐỊNH TÍN DỤNG · CHỈ SỐ DTI</span>'
    f'<div class="hero-title">🏦 {TIEU_DE}</div>'
    f'<div class="hero-sub">Đánh giá khả năng trả nợ của khách hàng và đề xuất giải pháp để đủ điều kiện vay</div></div>'
)

with st.expander("⚙️ Cài đặt chính sách ngân hàng"):
    a1, a2, a3 = st.columns(3)
    nguong_pct = a1.number_input("Ngưỡng DTI tối đa (%)", 10.0, 100.0, 70.0, 1.0, format="%.0f")
    muc_tieu = a2.number_input(
        "DTI mục tiêu khi tư vấn (%)", 1.0, nguong_pct, nguong_pct, 1.0, format="%.0f",
        help="Giải pháp sẽ đưa DTI xuống dưới mức này.",
    )
    THOI_HAN_TOI_DA = a3.number_input("Thời hạn vay tối đa (năm)", 1, 50, 20, 1)
    PT = st.radio("Phương thức trả nợ", [PT_GOC_DEU, PT_TRA_DEU], horizontal=True)
NGUONG = nguong_pct / 100

# =====================================================================
# FORM NHẬP LIỆU
# =====================================================================
with st.form("ho_so"):
    html('<div class="sec">👤 Thông tin khách hàng</div>')
    ten_kh = st.text_input("Họ tên khách hàng", placeholder="VD: Nguyễn Văn A")
    c1, c2 = st.columns(2)
    tn_tr = c1.number_input("Thu nhập hàng tháng (triệu đ)", 0.0, value=45.0, step=1.0, format="%.1f")
    nc_tr = c2.number_input("Nợ cũ phải trả / tháng (triệu đ)", 0.0, value=10.0, step=0.5, format="%.1f")
    sn = c1.number_input("Số người trong gia đình", 1, value=3, step=1)
    cpsh_tr = c2.number_input("Chi phí sinh hoạt / người / tháng (triệu đ)", 0.0, value=4.0, step=0.5, format="%.1f")

    st.write("")
    html('<div class="sec">💳 Khoản vay đề nghị</div>')
    d1, d2, d3 = st.columns(3)
    stv_tr = d1.number_input("Số tiền vay (triệu đ)", 0.0, value=800.0, step=10.0, format="%.0f")
    thv = d2.number_input("Thời hạn vay (năm)", 1, 50, 5, 1)
    ls = d3.number_input("Lãi suất (%/năm)", 0.0, value=12.0, step=0.1, format="%.2f")

    submitted = st.form_submit_button("🔍  Thẩm định hồ sơ", type="primary", width="stretch")

if submitted:
    st.session_state["da_tinh"] = True
    st.session_state["lan"] = st.session_state.get("lan", 0) + 1

if not st.session_state.get("da_tinh"):
    html('<div class="hint">📝 Nhập thông tin khách hàng và khoản vay, sau đó bấm <b>Thẩm định hồ sơ</b>.</div>')
    html('<div class="foot">© 2026 · Nguyễn Viết Minh Khánh · Công cụ hỗ trợ học tập, kết quả mang tính tham khảo</div>')
    st.stop()

# =====================================================================
# TÍNH TOÁN
# =====================================================================
stv, tn, nc, cpsh = stv_tr * TRIEU, tn_tr * TRIEU, nc_tr * TRIEU, cpsh_tr * TRIEU
LS = ls / 100
ten = ten_kh.strip() or "Khách hàng"

tra_moi = tra_hang_thang(stv, thv, LS, PT)
lai_1 = stv * LS / 12
goc_1 = tra_moi - lai_1
tong_no = tra_moi + nc
chi_phi = cpsh * sn
con_lai = tn - chi_phi
DTI = tong_no / con_lai if con_lai > 0 else None
DAT = DTI is not None and DTI < NGUONG and thv <= THOI_HAN_TOI_DA

# =====================================================================
# KẾT QUẢ
# =====================================================================
st.write("")
html(f'<div class="sec">📊 Kết quả thẩm định <small>— {ten}</small></div>')

if DTI is None:
    html(
        '<div class="result fail"><div><div class="r-label">Chỉ số DTI</div><div class="r-value">—</div></div>'
        '<div><div class="r-status">✖ KHÔNG ĐỦ ĐIỀU KIỆN</div>'
        f'<div class="r-sub">Thu nhập không đủ chi phí sinh hoạt (thiếu {vnd(-con_lai)}/tháng)</div></div></div>'
    )
else:
    cls = "ok" if DAT else "fail"
    trang_thai = "✔ ĐỦ ĐIỀU KIỆN VAY" if DAT else "✖ KHÔNG ĐỦ ĐIỀU KIỆN"
    ly_do = f"Ngưỡng ngân hàng: DTI &lt; {nguong_pct:g}%"
    if DTI < NGUONG and thv > THOI_HAN_TOI_DA:
        ly_do = f"Thời hạn {thv} năm vượt mức tối đa {THOI_HAN_TOI_DA} năm"
    html(
        f'<div class="result {cls}"><div><div class="r-label">Chỉ số DTI</div>'
        f'<div class="r-value">{DTI * 100:.2f}%</div></div>'
        f'<div><div class="r-status">{trang_thai}</div><div class="r-sub">{ly_do}</div></div></div>'
    )

    # Thanh đo DTI (thang 0 – 120%)
    THANG = 1.2
    vi_tri = min(DTI, THANG) / THANG * 100
    nguong_vt = NGUONG / THANG * 100
    canh_bao_vt = max(NGUONG - 0.1, 0) / THANG * 100
    mau = "#16A34A" if DTI < NGUONG - 0.1 else ("#F59E0B" if DTI < NGUONG else "#DC2626")
    html(
        f'<div class="gauge"><div class="g-head"><span>Mức độ an toàn</span>'
        f'<span><b style="color:{mau}">{DTI * 100:.2f}%</b></span></div>'
        f'<div class="g-track" style="--a:{canh_bao_vt}%;--t:{nguong_vt}%">'
        f'<div class="g-fill" style="width:{vi_tri}%;background:{mau}"></div>'
        f'<div class="g-thr" style="left:{nguong_vt}%"><span>Ngưỡng {nguong_pct:g}%</span></div></div>'
        f'<div class="g-scale"><span>0%</span><span>🟢 An toàn · 🟡 Cảnh báo · 🔴 Vượt ngưỡng</span><span>120%</span></div></div>'
    )

du_dia = NGUONG * con_lai - tong_no
html(
    '<div class="kpis">'
    f'<div class="kpi"><div class="kpi-l">Tổng trả nợ / tháng</div><div class="kpi-v">{trieu(tong_no)}</div>'
    f'<div class="kpi-s" style="color:#64748B">Vay mới {trieu(tra_moi)} + nợ cũ {trieu(nc)}</div></div>'
    f'<div class="kpi"><div class="kpi-l">Thu nhập còn lại / tháng</div><div class="kpi-v">{trieu(con_lai)}</div>'
    f'<div class="kpi-s" style="color:#64748B">Sau chi phí sinh hoạt {trieu(chi_phi)}</div></div>'
    f'<div class="kpi"><div class="kpi-l">{"Dư địa trả nợ" if du_dia >= 0 else "Vượt khả năng trả"}</div>'
    f'<div class="kpi-v" style="color:{"#16A34A" if du_dia >= 0 else "#DC2626"}">{trieu(abs(du_dia))}</div>'
    f'<div class="kpi-s" style="color:#64748B">so với ngưỡng {nguong_pct:g}%</div></div>'
    '</div>'
)

# =====================================================================
# GIẢI PHÁP
# =====================================================================
T = min(muc_tieu / 100, NGUONG) - 0.0005  # chừa biên nhỏ để luôn dưới mục tiêu
giai_phap = []  # mỗi phần tử: dict(icon, title, value, detail, dti, status, tip)

# 1. Giảm số tiền vay
if con_lai <= 0:
    giai_phap.append(dict(icon="💰", title="Giảm số tiền vay", value="Không áp dụng",
                          detail="Thu nhập còn lại ≤ 0, cần tăng thu nhập trước.", dti="—", status="na", tip=""))
else:
    dd = T * con_lai - nc
    if dd <= 0:
        giai_phap.append(dict(icon="💰", title="Giảm số tiền vay", value="Không khả thi",
                              detail=f"Riêng nợ cũ {trieu(nc)}/tháng đã vượt mức cho phép.",
                              dti="—", status="na", tip=""))
    else:
        stv_max = min(stv, math.floor(dd / tra_hang_thang(1, thv, LS, PT) / TRIEU) * TRIEU)
        d = tinh_dti(stv_max, thv, LS, nc, tn, cpsh, sn, PT)
        them = ""
        if thv < THOI_HAN_TOI_DA:
            stv_max2 = math.floor(dd / tra_hang_thang(1, THOI_HAN_TOI_DA, LS, PT) / TRIEU) * TRIEU
            them = f" Nếu vay {THOI_HAN_TOI_DA} năm: tối đa {trieu(stv_max2)}."
        giai_phap.append(dict(
            icon="💰", title="Giảm số tiền vay", value=f"Tối đa {trieu(stv_max)}",
            detail=f"Giảm {trieu(stv - stv_max)} so với đề nghị, giữ thời hạn {thv} năm.{them}",
            dti=pct(d), status="ok",
            tip="Bổ sung phần thiếu bằng vốn tự có hoặc chọn phương án/tài sản giá trị thấp hơn."))

# 2. Kéo dài thời hạn
if con_lai <= 0 or stv == 0:
    giai_phap.append(dict(icon="⏳", title="Kéo dài thời hạn vay", value="Không áp dụng",
                          detail="Thu nhập còn lại ≤ 0 hoặc không có khoản vay.", dti="—", status="na", tip=""))
else:
    n_min = next((n for n in range(thv, 101)
                  if (tinh_dti(stv, n, LS, nc, tn, cpsh, sn, PT) or 9) < T), None)
    if n_min is None:
        giai_phap.append(dict(icon="⏳", title="Kéo dài thời hạn vay", value="Không khả thi",
                              detail="Tiền lãi và nợ cũ đã vượt mức cho phép.", dti="—", status="na", tip=""))
    elif n_min > THOI_HAN_TOI_DA:
        d = tinh_dti(stv, THOI_HAN_TOI_DA, LS, nc, tn, cpsh, sn, PT)
        giai_phap.append(dict(
            icon="⏳", title="Kéo dài thời hạn vay", value=f"Cần {n_min} năm",
            detail=f"Vượt mức tối đa {THOI_HAN_TOI_DA} năm. Vay {THOI_HAN_TOI_DA} năm thì DTI còn {pct(d)}.",
            dti=pct(d), status="warn", tip="Cần kết hợp với giải pháp khác (xem tab Mô phỏng)."))
    else:
        d = tinh_dti(stv, n_min, LS, nc, tn, cpsh, sn, PT)
        giai_phap.append(dict(
            icon="⏳", title="Kéo dài thời hạn vay", value=f"{n_min} năm",
            detail=f"Từ {thv} lên {n_min} năm, trả {trieu(tra_hang_thang(stv, n_min, LS, PT))}/tháng.",
            dti=pct(d), status="ok",
            tip="Trả hàng tháng giảm nhưng tổng lãi cả kỳ tăng; có thể trả trước hạn khi có điều kiện."))

# 3. Trả bớt nợ cũ
if con_lai <= 0:
    giai_phap.append(dict(icon="📉", title="Trả bớt nợ cũ", value="Không áp dụng",
                          detail="Thu nhập còn lại ≤ 0, cần tăng thu nhập trước.", dti="—", status="na", tip=""))
elif nc == 0:
    giai_phap.append(dict(icon="📉", title="Trả bớt nợ cũ", value="Không có nợ cũ",
                          detail="Khách hàng không có khoản nợ cũ.", dti="—", status="na", tip=""))
else:
    nc_max = T * con_lai - tra_moi
    if nc_max < 0:
        d = tinh_dti(stv, thv, LS, 0, tn, cpsh, sn, PT)
        giai_phap.append(dict(
            icon="📉", title="Trả bớt nợ cũ", value="Chưa đủ",
            detail=f"Tất toán toàn bộ nợ cũ thì DTI vẫn còn {pct(d)}.",
            dti=pct(d), status="warn", tip="Cần kết hợp với giải pháp khác (xem tab Mô phỏng)."))
    else:
        nc_max = math.floor(nc_max / 1000) * 1000
        d = tinh_dti(stv, thv, LS, nc_max, tn, cpsh, sn, PT)
        giai_phap.append(dict(
            icon="📉", title="Trả bớt nợ cũ", value=f"Còn ≤ {trieu(nc_max)}/tháng",
            detail=f"Giảm {trieu(nc - nc_max)}/tháng so với hiện tại ({trieu(nc)}).",
            dti=pct(d), status="ok",
            tip="Tất toán trước khoản vay nhỏ / thẻ tín dụng hoặc cơ cấu lại nợ cũ."))

# 4. Tăng thu nhập
tn_min = math.ceil((tong_no / T + chi_phi) / 100_000) * 100_000
d = tinh_dti(stv, thv, LS, nc, tn_min, cpsh, sn, PT)
giai_phap.append(dict(
    icon="👥", title="Tăng thu nhập / người đồng vay", value=f"Thu nhập ≥ {trieu(tn_min)}",
    detail=f"Cần tăng thêm {trieu(tn_min - tn)}/tháng so với hiện tại.",
    dti=pct(d), status="ok",
    tip="Bổ sung người đồng vay (vợ/chồng, người thân) hoặc chứng minh thêm nguồn thu."))

# =====================================================================
# TABS
# =====================================================================
st.write("")
tab1, tab2, tab3 = st.tabs(["💡 Giải pháp đề xuất", "🎛️ Mô phỏng kết hợp", "📋 Chi tiết tính toán"])

with tab1:
    can_tu_van = DTI is None or DTI >= T
    if not can_tu_van:
        html(f'<div class="plan">✅ <b>{ten}</b> đã đạt DTI mục tiêu ({muc_tieu:g}%), không cần điều chỉnh.</div>')
        st.write("")
        dd = T * con_lai - nc
        if dd > 0:
            han_muc = math.floor(dd / tra_hang_thang(1, thv, LS, PT) / TRIEU) * TRIEU
            han_muc2 = math.floor(dd / tra_hang_thang(1, THOI_HAN_TOI_DA, LS, PT) / TRIEU) * TRIEU
            html(
                f'<div class="sol ok" style="min-height:0"><div class="sol-h"><span class="sol-t">💰 Hạn mức vay tối đa</span>'
                f'<span class="badge b-ok">Tham khảo</span></div><div class="sol-v">{trieu(han_muc)}</div>'
                f'<div class="sol-d">Với thời hạn {thv} năm, lãi suất {ls:g}%/năm. '
                f'Nếu vay {THOI_HAN_TOI_DA} năm: tối đa {trieu(han_muc2)}.</div></div>'
            )
    else:
        st.caption(f"Mỗi giải pháp chỉ thay đổi **một** yếu tố để đưa DTI xuống dưới **{muc_tieu:g}%**.")

    BADGE = {"ok": ("Đạt mục tiêu", "b-ok"), "warn": ("Chưa đủ", "b-warn"), "na": ("Không khả thi", "b-na")}
    cols = st.columns(2)
    for i, g in enumerate(giai_phap):
        nhan, lop = BADGE[g["status"]]
        if not can_tu_van:
            break
        with cols[i % 2]:
            html(
                f'<div class="sol {g["status"]}"><div class="sol-h"><span class="sol-t">{g["icon"]} {g["title"]}</span>'
                f'<span class="badge {lop}">{nhan}</span></div>'
                f'<div class="sol-v">{g["value"]}</div><div class="sol-d">{g["detail"]}</div>'
                f'<div class="sol-d" style="margin-top:4px">DTI sau điều chỉnh: <b>{g["dti"]}</b></div>'
                + (f'<div class="sol-tip">💬 {g["tip"]}</div>' if g["tip"] else "")
                + '</div>'
            )

with tab2:
    st.caption("Kéo các thanh trượt để kết hợp nhiều giải pháp cùng lúc. Bấm lại **Thẩm định hồ sơ** để đặt lại.")
    v = st.session_state.get("lan", 0)
    s1, s2 = st.columns(2)
    with s1:
        stv_s = st.slider("Số tiền vay (triệu đ)", 0.0, float(max(stv_tr, 10.0)), float(stv_tr),
                          step=10.0 if stv_tr >= 100 else 1.0, format="%.0f", key=f"a{v}")
        thv_s = st.slider("Thời hạn vay (năm)", 1, int(max(THOI_HAN_TOI_DA, thv)), int(thv), key=f"b{v}")
        ls_s = st.slider("Lãi suất (%/năm)", 0.0, float(max(ls * 2, 20.0)), float(ls), step=0.1,
                         format="%.1f", key=f"c{v}")
    with s2:
        nc_s = st.slider("Nợ cũ / tháng (triệu đ)", 0.0, float(max(nc_tr, 1.0)), float(nc_tr), step=0.5,
                         format="%.1f", key=f"d{v}")
        tn_s = st.slider("Thu nhập / tháng (triệu đ)", float(tn_tr), float(max(tn_tr * 3, tn_tr + 50)),
                         float(tn_tr), step=0.5, format="%.1f", key=f"e{v}")
        sn_s = st.slider("Số người phụ thuộc chi phí", 1, int(max(sn, 10)), int(sn), key=f"f{v}")

    dti_s = tinh_dti(stv_s * TRIEU, thv_s, ls_s / 100, nc_s * TRIEU, tn_s * TRIEU, cpsh, sn_s, PT)
    tra_s = tra_hang_thang(stv_s * TRIEU, thv_s, ls_s / 100, PT)
    dat_s = dti_s is not None and dti_s < NGUONG and thv_s <= THOI_HAN_TOI_DA

    if dti_s is None:
        html('<div class="result fail"><div><div class="r-label">DTI mô phỏng</div><div class="r-value">—</div></div>'
             '<div><div class="r-status">✖ CHƯA ĐẠT</div><div class="r-sub">Thu nhập chưa đủ chi phí sinh hoạt</div></div></div>')
    else:
        thay = "" if DTI is None else f"{(dti_s - DTI) * 100:+.2f}% so với ban đầu"
        html(
            f'<div class="result {"ok" if dat_s else "fail"}"><div><div class="r-label">DTI mô phỏng</div>'
            f'<div class="r-value">{dti_s * 100:.2f}%</div></div>'
            f'<div><div class="r-status">{"✔ ĐỦ ĐIỀU KIỆN" if dat_s else "✖ CHƯA ĐẠT"}</div>'
            f'<div class="r-sub">{thay} · Trả {trieu(tra_s + nc_s * TRIEU)}/tháng</div></div></div>'
        )

    thay_doi = []
    if stv_s != stv_tr:
        thay_doi.append(f"số tiền vay <b>{trieu(stv_s * TRIEU)}</b>")
    if thv_s != thv:
        thay_doi.append(f"thời hạn <b>{thv_s} năm</b>")
    if abs(ls_s - ls) > 1e-9:
        thay_doi.append(f"lãi suất <b>{ls_s:.1f}%/năm</b>")
    if nc_s != nc_tr:
        thay_doi.append(f"nợ cũ còn <b>{trieu(nc_s * TRIEU)}/tháng</b>")
    if tn_s != tn_tr:
        thay_doi.append(f"thu nhập <b>{trieu(tn_s * TRIEU)}/tháng</b>")
    if sn_s != sn:
        thay_doi.append(f"<b>{sn_s}</b> người phụ thuộc")
    if thay_doi:
        html(f'<div class="plan">📝 <b>Phương án tư vấn cho {ten}:</b> ' + "; ".join(thay_doi) + ".</div>")

with tab3:
    bang = pd.DataFrame(
        [
            ["Phương thức trả nợ", PT],
            ["Gốc trả " + ("hàng tháng" if PT == PT_GOC_DEU else "tháng đầu"), vnd(goc_1)],
            ["Lãi trả " + ("hàng tháng" if PT == PT_GOC_DEU else "tháng đầu"), vnd(lai_1)],
            ["Khoản vay mới / tháng", vnd(tra_moi)],
            ["Nợ cũ / tháng", vnd(nc)],
            ["Tổng nợ phải trả / tháng", vnd(tong_no)],
            ["Thu nhập hàng tháng", vnd(tn)],
            [f"Chi phí sinh hoạt ({sn} người)", vnd(chi_phi)],
            ["Thu nhập còn lại", vnd(con_lai)],
            ["Chỉ số DTI", pct(DTI)],
        ],
        columns=["Khoản mục", "Giá trị"],
    )
    st.dataframe(bang, hide_index=True, width="stretch")
    st.caption("DTI = Tổng nợ phải trả hàng tháng / (Thu nhập − Chi phí sinh hoạt × Số người)")

html('<div class="foot">© 2026 · Nguyễn Viết Minh Khánh · Công cụ hỗ trợ học tập, kết quả mang tính tham khảo</div>')
