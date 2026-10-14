import calendar
import io
import math
from datetime import date, timedelta
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

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
# LẬP BẢNG KẾ HOẠCH TRẢ NỢ
# =====================================================================
PTL_GOC_DEU = "Gốc đều, lãi tính trên dư nợ giảm dần"
PTL_NIEN_KIM = "Trả góp đều (niên kim)"
PTL_GOC_CUOI = "Trả lãi hằng tháng, gốc cuối kỳ"
PTL_GOC_DINH_KY = "Lãi hằng tháng, gốc trả định kỳ (quý / 6 tháng...)"
LT_CAT = "Cắt bớt số lẻ (như đáp án slide)"
LT_TRON = "Làm tròn"
LT_GIU = "Giữ nguyên, không làm tròn"
DK_CA_HAI_DAU = "Tính cả ngày giải ngân (như đáp án slide)"
DK_THUC_TE = "Số ngày thực tế (không tính ngày giải ngân)"
DLS_THEO_KY = "Theo số kỳ: kỳ thứ N trở đi (như đáp án slide)"
DLS_THEO_NGAY = "Theo ngày: đủ N−1 tháng kể từ ngày giải ngân"
COT_LS = ["Từ kỳ", "Lãi suất cơ sở (%/năm)", "Biên độ (%/năm)", "Ghi chú"]

MAU_DE_BAI = {
    "Bài trang 197 (vay 700 triệu, GN 22/10/2023)": dict(
        stv=700.0, han=5, dv="năm", gn=date(2023, 10, 22), ngay_lai=10, ngay_thu=15,
        ls=[[1, 9.0, 0.0, "Cố định 3 tháng đầu"], [4, 10.0, 4.0, "LS huy động + biên độ"]]),
    "Bài trang 193 (vay 800 triệu, GN 28/03/2024)": dict(
        stv=800.0, han=5, dv="năm", gn=date(2024, 3, 28), ngay_lai=5, ngay_thu=10,
        ls=[[1, 9.0, 0.0, "Cố định 3 tháng đầu"], [4, 8.0, 4.0, "LS huy động + biên độ"]]),
}


def ngay_hop_le(nam: int, thang: int, ngay: int) -> date:
    """Ngày `ngay` của tháng; nếu tháng không có ngày đó (VD 31/02) thì lấy ngày cuối tháng."""
    return date(nam, thang, min(ngay, calendar.monthrange(nam, thang)[1]))


def cong_thang(goc: date, k: int, ngay: int) -> date:
    m = goc.month - 1 + k
    return ngay_hop_le(goc.year + m // 12, m % 12 + 1, ngay)


def lam_tron(x: float, cach: str, so_le: int) -> float:
    if cach == LT_GIU:
        return x
    q = Decimal(1).scaleb(-so_le)
    mode = ROUND_DOWN if cach == LT_CAT else ROUND_HALF_UP
    # str(round(x, 9)) loại sai số dấu phẩy động (VD 7.2675 lưu thành 7.26749999)
    return float(Decimal(str(round(x, 9))).quantize(q, rounding=mode))


def so_vn(x: float, so_le: int = 2, bo_so_0: bool = True) -> str:
    s = f"{x:,.{so_le}f}".replace(",", " ").replace(".", ",").replace(" ", ".")
    if bo_so_0 and "," in s:
        s = s.rstrip("0").rstrip(",")
    return s


def doc_giai_doan(df: pd.DataFrame):
    """Đọc bảng lãi suất → danh sách (từ kỳ, lãi suất/năm), bỏ dòng trống."""
    ds, loi = [], []
    for _, r in df.iterrows():
        tu, co_so, bd = r.get("Từ kỳ"), r.get("Lãi suất cơ sở (%/năm)"), r.get("Biên độ (%/năm)")
        if tu is None or pd.isna(tu):
            continue
        if co_so is None or pd.isna(co_so):
            loi.append(f"Giai đoạn từ kỳ {int(tu)}: chưa nhập lãi suất cơ sở.")
            continue
        bd = 0.0 if bd is None or pd.isna(bd) else float(bd)
        ds.append((int(tu), (float(co_so) + bd) / 100))
    ds.sort()
    if ds and ds[0][0] != 1:
        loi.append("Cần có một giai đoạn lãi suất bắt đầu từ kỳ 1.")
    return ds, loi


def lap_lich_tra_no(P, n, ngay_gn, ngay_lai, ngay_thu, pt, chu_ky_goc, giai_doan, doi_ls,
                    co_so, dem_ky_dau, cach_tron, so_le):
    """Trả về danh sách các kỳ (số tiền tính theo cùng đơn vị với P)."""
    def ls_theo_ky(k):
        return [r for tu, r in giai_doan if tu <= k][-1]

    moc_ngay = [(cong_thang(ngay_gn, tu - 1, ngay_gn.day), r) for tu, r in giai_doan]

    def ls_theo_ngay(d):
        return [r for m, r in moc_ngay if m <= d][-1]

    tron = lambda x: lam_tron(x, cach_tron, so_le)  # noqa: E731
    chot_1 = ngay_hop_le(ngay_gn.year, ngay_gn.month, ngay_lai)
    if chot_1 <= ngay_gn:
        chot_1 = cong_thang(ngay_gn, 1, ngay_lai)

    du_no, chot_truoc, rows = P, None, []
    tra_deu, ls_tra_deu = None, None
    so_lan_goc = math.ceil(n / chu_ky_goc) if pt == PTL_GOC_DINH_KY else n

    for k in range(1, n + 1):
        chot = cong_thang(chot_1, k - 1, ngay_lai)
        if k == 1:
            tu_ngay = ngay_gn if dem_ky_dau == DK_CA_HAI_DAU else ngay_gn + timedelta(days=1)
        else:
            tu_ngay = chot_truoc + timedelta(days=1)
        so_ngay = (chot - tu_ngay).days + 1

        # Chia đoạn theo lãi suất
        if doi_ls == DLS_THEO_KY:
            doan = [[so_ngay, ls_theo_ky(k)]]
        else:
            doan = []
            for i in range(so_ngay):
                r = ls_theo_ngay(tu_ngay + timedelta(days=i))
                if doan and doan[-1][1] == r:
                    doan[-1][0] += 1
                else:
                    doan.append([1, r])
        lai = tron(sum(du_no * r * d / co_so for d, r in doan))
        ls_ky = doan[-1][1]

        if pt == PTL_GOC_DEU:
            goc = tron(P / n)
        elif pt == PTL_NIEN_KIM:
            if tra_deu is None or ls_ky != ls_tra_deu:
                i, con = ls_ky / 12, n - k + 1
                tra_deu = tron(du_no * i / (1 - (1 + i) ** (-con)) if i > 0 else du_no / con)
                ls_tra_deu = ls_ky
            goc = max(tra_deu - lai, 0)
        elif pt == PTL_GOC_CUOI:
            goc = 0.0
        else:
            goc = tron(P / so_lan_goc) if k % chu_ky_goc == 0 else 0.0
        if k == n or goc > du_no:
            goc = du_no

        ngay_tra = cong_thang(chot, 0 if ngay_thu > ngay_lai else 1, ngay_thu)
        cong_thuc = " + ".join(
            f"{so_vn(du_no, so_le)}*{so_vn(r * 100, 4)}%*{d}/{co_so}" for d, r in doan)
        rows.append({
            "Kỳ": k,
            "Ngày thu nợ": ngay_tra.strftime("%d/%m/%Y"),
            "Kỳ tính lãi": f"{tu_ngay:%d/%m/%Y} – {chot:%d/%m/%Y}",
            "Số ngày": so_ngay,
            "Lãi suất (%/năm)": " → ".join(so_vn(r * 100, 4) for _, r in doan),
            "Dư nợ": du_no,
            "Gốc phải trả": goc,
            "Lãi phải trả": lai,
            "Tổng gốc + lãi": goc + lai,
            "Công thức tiền lãi": f"{cong_thuc} = {so_vn(lai, so_le, False)}",
        })
        du_no = max(du_no - goc, 0.0)
        if abs(du_no) < 1e-9:
            du_no = 0.0
        chot_truoc = chot
    return rows


def ap_dung_mau():
    mau = MAU_DE_BAI.get(st.session_state["lt_mau"])
    if not mau:
        return
    st.session_state.update({
        "lt_stv": mau["stv"], "lt_han": mau["han"], "lt_dv": mau["dv"], "lt_gn": mau["gn"],
        "lt_ngay_lai": mau["ngay_lai"], "lt_ngay_thu": mau["ngay_thu"], "lt_pt": PTL_GOC_DEU,
        "lt_doi_ls": DLS_THEO_KY, "lt_dem": DK_CA_HAI_DAU, "lt_tron": LT_CAT, "lt_sole": 2,
        "lt_coso": 365, "lt_so_ky": 5, "lt_tat_ca": False,
    })
    df = pd.DataFrame(mau["ls"], columns=COT_LS)
    st.session_state["lt_ls_df"] = df.astype({"Từ kỳ": "int64", COT_LS[1]: "float64", COT_LS[2]: "float64"})
    st.session_state["lt_ls_ver"] = st.session_state.get("lt_ls_ver", 0) + 1


def trang_lich_tra_no():
    if "lt_stv" not in st.session_state:
        st.session_state["lt_mau"] = next(iter(MAU_DE_BAI))
        ap_dung_mau()
        st.session_state["lt_chu_ky"] = 3

    st.selectbox(
        "📚 Nạp dữ liệu đề bài mẫu", list(MAU_DE_BAI) + ["Tự nhập"], key="lt_mau", on_change=ap_dung_mau,
        help="Chọn đề bài mẫu để điền sẵn số liệu, sau đó có thể sửa bất kỳ ô nào.",
    )

    with st.form("lich_tra_no"):
        html('<div class="sec">💳 Khoản vay</div>')
        c1, c2, c3 = st.columns([1.3, 1, 0.8])
        c1.number_input("Số tiền vay (triệu đ)", 0.0, step=10.0, format="%.2f", key="lt_stv")
        c2.number_input("Thời hạn vay", 1, 600, step=1, key="lt_han")
        c3.selectbox("Đơn vị", ["năm", "tháng"], key="lt_dv")

        html('<div class="sec">📅 Ngày tháng</div>')
        d1, d2, d3 = st.columns(3)
        d1.date_input("Ngày giải ngân", format="DD/MM/YYYY", key="lt_gn",
                      min_value=date(2000, 1, 1), max_value=date(2100, 12, 31))
        d2.number_input("Ngày tính lãi hằng tháng", 1, 31, step=1, key="lt_ngay_lai",
                        help="Ngày chốt dư nợ để tính lãi (VD: ngày 10 tây hằng tháng).")
        d3.number_input("Ngày thu nợ hằng tháng", 1, 31, step=1, key="lt_ngay_thu",
                        help="Ngày khách hàng nộp tiền (VD: ngày 15 tây hằng tháng).")

        html('<div class="sec">💸 Phương thức trả nợ</div>')
        p1, p2 = st.columns([2, 1])
        p1.selectbox("Phương thức", [PTL_GOC_DEU, PTL_NIEN_KIM, PTL_GOC_CUOI, PTL_GOC_DINH_KY], key="lt_pt")
        p2.number_input("Gốc trả mỗi … tháng", 1, 60, step=1, key="lt_chu_ky",
                        help="Chỉ dùng cho phương thức gốc trả định kỳ (3 = theo quý, 6 = nửa năm).")

        html('<div class="sec">📈 Lãi suất theo giai đoạn <small>— thêm/xoá dòng tuỳ ý</small></div>')
        ls_df = st.data_editor(
            st.session_state["lt_ls_df"], key=f"lt_ls_{st.session_state['lt_ls_ver']}",
            num_rows="dynamic", hide_index=True, width="stretch",
            column_config={
                "Từ kỳ": st.column_config.NumberColumn(min_value=1, step=1, required=True,
                                                       help="Giai đoạn áp dụng từ kỳ (tháng) thứ mấy."),
                "Lãi suất cơ sở (%/năm)": st.column_config.NumberColumn(
                    min_value=0.0, format="%.2f", required=True,
                    help="Lãi suất cố định, hoặc lãi suất huy động nếu cho vay thả nổi."),
                "Biên độ (%/năm)": st.column_config.NumberColumn(
                    format="%.2f", default=0.0, help="Biên độ cộng thêm; để 0 nếu lãi suất cố định."),
                "Ghi chú": st.column_config.TextColumn(),
            },
        )
        st.caption("Lãi suất cho vay = **Lãi suất cơ sở + Biên độ**. Lãi suất cố định: nhập vào cột cơ sở, "
                   "biên độ = 0. Thả nổi: nhập lãi suất huy động và biên độ.")

        with st.expander("⚙️ Quy ước tính toán & hiển thị"):
            q1, q2 = st.columns(2)
            q1.selectbox("Đổi lãi suất", [DLS_THEO_KY, DLS_THEO_NGAY], key="lt_doi_ls",
                         help="Theo ngày: kỳ nào chứa ngày đổi lãi suất sẽ được tách thành 2 đoạn để tính lãi.")
            q2.selectbox("Số ngày kỳ đầu tiên", [DK_CA_HAI_DAU, DK_THUC_TE], key="lt_dem")
            q1.selectbox("Làm tròn tiền gốc và tiền lãi", [LT_CAT, LT_TRON, LT_GIU], key="lt_tron")
            q2.number_input("Số chữ số thập phân (theo triệu đ)", 0, 6, step=1, key="lt_sole",
                            help="2 chữ số thập phân theo triệu đồng = làm tròn đến 10.000 đ.")
            q1.selectbox("Số ngày trong năm", [365, 360], key="lt_coso")
            q2.number_input("Số kỳ hiển thị", 1, 600, step=1, key="lt_so_ky")
            st.checkbox("Hiển thị toàn bộ các kỳ", key="lt_tat_ca")

        bam = st.form_submit_button("📅  Lập bảng kế hoạch trả nợ", type="primary", width="stretch")

    if bam:
        st.session_state["lt_da_lap"] = True
    if not st.session_state.get("lt_da_lap"):
        html('<div class="hint">📝 Nhập thông tin khoản vay (hoặc chọn đề bài mẫu), '
             'sau đó bấm <b>Lập bảng kế hoạch trả nợ</b>.</div>')
        return

    ss = st.session_state
    giai_doan, loi = doc_giai_doan(ls_df)
    if not giai_doan:
        loi.append("Chưa nhập giai đoạn lãi suất nào.")
    n = int(ss["lt_han"]) * (12 if ss["lt_dv"] == "năm" else 1)
    if ss["lt_stv"] <= 0:
        loi.append("Số tiền vay phải lớn hơn 0.")
    if loi:
        for e in loi:
            st.error(e)
        return

    pt = ss["lt_pt"]
    chu_ky = int(ss["lt_chu_ky"]) if pt == PTL_GOC_DINH_KY else 1
    rows = lap_lich_tra_no(
        float(ss["lt_stv"]), n, ss["lt_gn"], int(ss["lt_ngay_lai"]), int(ss["lt_ngay_thu"]), pt, chu_ky,
        giai_doan, ss["lt_doi_ls"], int(ss["lt_coso"]), ss["lt_dem"], ss["lt_tron"], int(ss["lt_sole"]),
    )
    df_all = pd.DataFrame(rows)
    df = df_all if ss["lt_tat_ca"] else df_all.head(int(ss["lt_so_ky"]))
    sl = int(ss["lt_sole"])

    st.write("")
    html(f'<div class="sec">📋 Bảng kế hoạch trả nợ <small>— {len(df)}/{n} kỳ · đơn vị: triệu đồng</small></div>')
    html(
        '<div class="kpis">'
        f'<div class="kpi"><div class="kpi-l">Gốc phải trả ({len(df)} kỳ)</div>'
        f'<div class="kpi-v">{so_vn(df["Gốc phải trả"].sum(), sl, False)}</div>'
        f'<div class="kpi-s" style="color:#64748B">Cả khoản vay: {so_vn(df_all["Gốc phải trả"].sum(), sl, False)}</div></div>'
        f'<div class="kpi"><div class="kpi-l">Lãi phải trả ({len(df)} kỳ)</div>'
        f'<div class="kpi-v">{so_vn(df["Lãi phải trả"].sum(), sl, False)}</div>'
        f'<div class="kpi-s" style="color:#64748B">Cả khoản vay: {so_vn(df_all["Lãi phải trả"].sum(), sl, False)}</div></div>'
        f'<div class="kpi"><div class="kpi-l">Tổng gốc + lãi ({len(df)} kỳ)</div>'
        f'<div class="kpi-v">{so_vn(df["Tổng gốc + lãi"].sum(), sl, False)}</div>'
        f'<div class="kpi-s" style="color:#64748B">Kỳ trả cao nhất: {so_vn(df_all["Tổng gốc + lãi"].max(), sl, False)}</div></div>'
        '</div>'
    )
    fmt = f"%.{sl}f" if ss["lt_tron"] != LT_GIU else "%.4f"
    st.dataframe(
        df, hide_index=True, width="stretch",
        column_config={c: st.column_config.NumberColumn(format=fmt)
                       for c in ["Dư nợ", "Gốc phải trả", "Lãi phải trả", "Tổng gốc + lãi"]},
    )
    st.caption("Tiền lãi = Dư nợ × Lãi suất × Số ngày / Số ngày trong năm. "
               "Số ngày tính giữa hai ngày tính lãi; tiền lãi thu vào ngày thu nợ ngay sau đó.")
    if pt == PTL_NIEN_KIM:
        st.caption("Niên kim: số tiền trả mỗi kỳ = Dư nợ × i / (1 − (1 + i)^−số kỳ còn lại), i = lãi suất/12; "
                   "tính lại khi lãi suất thay đổi. Gốc = số tiền trả − tiền lãi theo ngày thực tế.")

    buf = io.BytesIO()
    try:
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_all.to_excel(w, index=False, sheet_name="Lich tra no")
        st.download_button("⬇️  Tải bảng trả nợ (Excel, toàn bộ kỳ)", buf.getvalue(), "bang_tra_no.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except ImportError:
        st.download_button("⬇️  Tải bảng trả nợ (CSV, toàn bộ kỳ)",
                           df_all.to_csv(index=False).encode("utf-8-sig"), "bang_tra_no.csv", "text/csv")


# =====================================================================
# HEADER
# =====================================================================
html(
    f'<div class="hero"><span class="hero-badge">THẨM ĐỊNH TÍN DỤNG · CHỈ SỐ DTI</span>'
    f'<div class="hero-title">🏦 {TIEU_DE}</div>'
    f'<div class="hero-sub">Đánh giá khả năng trả nợ của khách hàng và đề xuất giải pháp để đủ điều kiện vay</div></div>'
)

tab_dti, tab_lich = st.tabs(["🏦 Thẩm định DTI", "📅 Lập bảng kế hoạch trả nợ"])

# Tab lập bảng trả nợ chạy trước vì tab DTI có thể dừng script (st.stop) khi chưa bấm thẩm định
with tab_lich:
    trang_lich_tra_no()

with tab_dti:
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
