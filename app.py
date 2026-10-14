import math

import pandas as pd
import streamlit as st

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(page_title="Thẩm định tín dụng - DTI", page_icon="💰", layout="centered")

PT_GOC_DEU = "Gốc đều + lãi trên số tiền vay (công thức gốc)"
PT_TRA_DEU = "Trả góp đều hàng tháng (niên kim)"


def vnd(x: float) -> str:
    """Định dạng số tiền kiểu Việt Nam: 1.000.000 đ"""
    return f"{x:,.0f} đ".replace(",", ".")


def pct(x) -> str:
    return "—" if x is None else f"{x * 100:.2f}%"


def tra_hang_thang(stv, nam, LS, pt):
    """Số tiền phải trả mỗi tháng cho khoản vay mới."""
    if stv <= 0:
        return 0.0
    so_thang = nam * 12
    r = LS / 12
    if pt == PT_TRA_DEU and r > 0:
        return stv * r / (1 - (1 + r) ** (-so_thang))
    if pt == PT_TRA_DEU:
        return stv / so_thang
    return stv / so_thang + stv * r


def tinh_dti(stv, nam, LS, nc, tn, cpsh, sn, pt):
    """Trả về DTI (số thập phân) hoặc None nếu thu nhập còn lại <= 0."""
    con_lai = tn - cpsh * sn
    if con_lai <= 0:
        return None
    return (tra_hang_thang(stv, nam, LS, pt) + nc) / con_lai


# ================== GIAO DIỆN ==================
st.title("💰 Phần mềm thẩm định tín dụng_Nguyễn Viết Minh Khánh")

with st.expander("⚙️ Tham số ngân hàng (bấm để thay đổi)"):
    b1, b2 = st.columns(2)
    nguong_pct = b1.number_input(
        "Ngưỡng DTI tối đa (%)", min_value=10.0, max_value=100.0, value=70.0, step=1.0, format="%.1f",
        help="Khách hàng được vay khi DTI nhỏ hơn ngưỡng này.",
    )
    THOI_HAN_TOI_DA = b2.number_input(
        "Thời hạn vay tối đa (năm)", min_value=1, max_value=50, value=20, step=1,
    )
    PT = st.radio(
        "Phương thức tính tiền trả nợ hàng tháng",
        [PT_GOC_DEU, PT_TRA_DEU],
        help=(
            "Gốc đều: gốc = số tiền vay / số tháng; lãi = số tiền vay × lãi suất / 12.\n\n"
            "Trả góp đều: mỗi tháng trả một số tiền cố định (gồm cả gốc và lãi)."
        ),
    )
NGUONG_DTI = nguong_pct / 100

if PT == PT_GOC_DEU:
    st.caption(
        "DTI = (Tiền gốc + lãi phải trả hàng tháng + Nợ cũ) / "
        "(Thu nhập − Chi phí sinh hoạt × Số người)"
    )
else:
    st.caption(
        "DTI = (Khoản trả góp đều hàng tháng + Nợ cũ) / "
        "(Thu nhập − Chi phí sinh hoạt × Số người)"
    )

with st.form("dti_form"):
    ten_kh = st.text_input("Tên khách hàng", placeholder="VD: Nguyễn Văn A")
    col1, col2 = st.columns(2)

    with col1:
        stv = st.number_input(
            "Số tiền vay (VNĐ)",
            min_value=0, value=800_000_000, step=10_000_000, format="%d",
        )
        thv = st.number_input(
            "Thời hạn vay (năm)",
            min_value=1, max_value=50, value=5, step=1,
        )
        ls = st.number_input(
            "Lãi suất vay (%/năm)",
            min_value=0.0, value=12.0, step=0.1, format="%.2f",
        )
        sn = st.number_input(
            "Số người trong gia đình",
            min_value=1, value=3, step=1,
        )

    with col2:
        tn = st.number_input(
            "Thu nhập hàng tháng (VNĐ)",
            min_value=0, value=45_000_000, step=1_000_000, format="%d",
        )
        nc = st.number_input(
            "Nợ cũ phải trả hàng tháng (VNĐ)",
            min_value=0, value=10_000_000, step=1_000_000, format="%d",
        )
        cpsh = st.number_input(
            "Chi phí sinh hoạt / người / tháng (VNĐ)",
            min_value=0, value=4_000_000, step=500_000, format="%d",
        )
        muc_tieu = st.number_input(
            "DTI mục tiêu khi tư vấn (%)",
            min_value=1.0, max_value=nguong_pct, value=nguong_pct, step=1.0,
            format="%.1f",
            help="Các giải pháp sẽ đưa DTI xuống dưới mức này (không vượt ngưỡng ngân hàng).",
        )

    submitted = st.form_submit_button("📊 Tính DTI")

if submitted:
    st.session_state["da_tinh"] = True
    st.session_state["lan_tinh"] = st.session_state.get("lan_tinh", 0) + 1

# ================== TÍNH TOÁN ==================
if st.session_state.get("da_tinh"):
    LS = ls / 100  # đổi % sang số thập phân
    ten_hien_thi = ten_kh.strip() or "(chưa nhập tên)"

    tra_khoan_moi = tra_hang_thang(stv, thv, LS, PT)  # khoản vay mới mỗi tháng
    tra_lai = stv * LS / 12                            # lãi tháng đầu
    tra_goc = tra_khoan_moi - tra_lai                  # gốc tháng đầu
    tong_no = tra_khoan_moi + nc                       # tổng nợ phải trả mỗi tháng
    chi_phi_sh = cpsh * sn
    thu_nhap_con_lai = tn - chi_phi_sh                 # thu nhập sau chi phí sinh hoạt

    st.divider()
    st.subheader(f"Kết quả thẩm định — Khách hàng: {ten_hien_thi}")

    if thv > THOI_HAN_TOI_DA:
        st.warning(f"⚠️ Thời hạn vay {thv} năm vượt mức tối đa {THOI_HAN_TOI_DA} năm của ngân hàng.")

    DTI = None
    if thu_nhap_con_lai <= 0:
        st.error(
            "❌ **KHÔNG ĐƯỢC VAY** — Thu nhập không đủ trang trải chi phí sinh hoạt "
            f"(còn lại {vnd(thu_nhap_con_lai)}), không thể tính DTI."
        )
    else:
        DTI = tong_no / thu_nhap_con_lai

        c1, c2 = st.columns(2)
        c1.metric("Chỉ số DTI", f"{DTI * 100:.2f}%")
        c2.metric("Ngưỡng cho phép", f"< {nguong_pct:g}%")

        if DTI < NGUONG_DTI:
            st.success(f"✅ **ĐƯỢC VAY** — DTI = {DTI * 100:.2f}% nhỏ hơn {nguong_pct:g}%")
        else:
            st.error(f"❌ **KHÔNG ĐƯỢC VAY** — DTI = {DTI * 100:.2f}% từ {nguong_pct:g}% trở lên")

        st.progress(min(DTI, 1.0))

    with st.expander("Xem chi tiết tính toán"):
        nhan = "hàng tháng" if PT == PT_GOC_DEU else "tháng đầu"
        st.write(f"- Phương thức: **{PT}**")
        st.write(f"- Gốc trả {nhan}: **{vnd(tra_goc)}**")
        st.write(f"- Lãi trả {nhan}: **{vnd(tra_lai)}**")
        st.write(f"- Khoản vay mới / tháng: **{vnd(tra_khoan_moi)}**")
        st.write(f"- Nợ cũ / tháng: **{vnd(nc)}**")
        st.write(f"- **Tổng nợ phải trả / tháng: {vnd(tong_no)}**")
        st.write(f"- Tổng chi phí sinh hoạt: **{vnd(chi_phi_sh)}**")
        st.write(f"- **Thu nhập còn lại: {vnd(thu_nhap_con_lai)}**")

    # ================== TƯ VẤN GIẢM DTI ==================
    # chừa biên 0,05% để kết quả hiển thị luôn dưới mục tiêu
    T = min(muc_tieu / 100, NGUONG_DTI) - 0.0005

    if DTI is None or DTI >= T:
        st.divider()
        st.subheader("💡 Tư vấn giải pháp giảm DTI")
        st.caption(
            f"Mục tiêu: đưa DTI xuống dưới **{muc_tieu:.1f}%**. Mỗi giải pháp dưới đây "
            "chỉ điều chỉnh MỘT yếu tố, các yếu tố khác giữ nguyên. "
            "Muốn kết hợp nhiều yếu tố, dùng phần **Mô phỏng kết hợp** ở cuối trang."
        )

        bang = []
        khong_ap_dung = "Không áp dụng được — thu nhập còn lại ≤ 0, cần tăng thu nhập trước."

        # ---------- 1. Giảm số tiền vay ----------
        st.markdown("#### 1️⃣ Giảm số tiền vay")
        if thu_nhap_con_lai <= 0:
            st.write(khong_ap_dung)
            bang.append(["Giảm số tiền vay", "Không áp dụng", "—", "❌"])
        else:
            du_dia = T * thu_nhap_con_lai - nc  # số tiền còn trả được cho khoản vay mới / tháng
            if du_dia <= 0:
                st.write(
                    f"Không khả thi — riêng nợ cũ ({vnd(nc)}/tháng) đã vượt mức cho phép, "
                    "dù vay 0 đồng cũng không đạt."
                )
                bang.append(["Giảm số tiền vay", "Không khả thi", "—", "❌"])
            else:
                he_so = tra_hang_thang(1, thv, LS, PT)  # tiền trả / tháng cho mỗi 1 đồng vay
                stv_max = min(stv, math.floor(du_dia / he_so / 1_000_000) * 1_000_000)
                dti_moi = tinh_dti(stv_max, thv, LS, nc, tn, cpsh, sn, PT)
                st.write(
                    f"Vay tối đa **{vnd(stv_max)}** (giảm {vnd(stv - stv_max)} so với đề nghị), "
                    f"thời hạn giữ nguyên {thv} năm → DTI ≈ **{pct(dti_moi)}**."
                )
                st.write(
                    "👉 Tư vấn: khách hàng bổ sung phần còn thiếu bằng vốn tự có "
                    "hoặc chọn tài sản/phương án có giá trị thấp hơn."
                )
                bang.append(["Giảm số tiền vay", f"Vay tối đa {vnd(stv_max)}", pct(dti_moi), "✅"])

                if thv < THOI_HAN_TOI_DA:
                    he_so_max = tra_hang_thang(1, THOI_HAN_TOI_DA, LS, PT)
                    stv_max2 = math.floor(du_dia / he_so_max / 1_000_000) * 1_000_000
                    st.caption(
                        f"Nếu đồng thời kéo dài lên {THOI_HAN_TOI_DA} năm thì có thể vay tối đa "
                        f"{vnd(stv_max2)}."
                    )

        # ---------- 2. Kéo dài thời hạn vay ----------
        st.markdown("#### 2️⃣ Kéo dài thời hạn vay")
        if thu_nhap_con_lai <= 0:
            st.write(khong_ap_dung)
            bang.append(["Kéo dài thời hạn", "Không áp dụng", "—", "❌"])
        elif stv == 0:
            st.write("Không áp dụng — số tiền vay bằng 0.")
            bang.append(["Kéo dài thời hạn", "Không áp dụng", "—", "❌"])
        else:
            n_min = None
            for n in range(thv, 101):
                d = tinh_dti(stv, n, LS, nc, tn, cpsh, sn, PT)
                if d is not None and d < T:
                    n_min = n
                    break
            if n_min is None:
                st.write(
                    "Không khả thi — dù kéo dài rất lâu, tiền lãi và nợ cũ vẫn vượt mức cho phép."
                )
                bang.append(["Kéo dài thời hạn", "Không khả thi", "—", "❌"])
            elif n_min > THOI_HAN_TOI_DA:
                dti_max = tinh_dti(stv, THOI_HAN_TOI_DA, LS, nc, tn, cpsh, sn, PT)
                st.write(
                    f"Cần vay ít nhất **{n_min} năm**, vượt thời hạn tối đa {THOI_HAN_TOI_DA} năm "
                    f"của ngân hàng. Kéo dài lên {THOI_HAN_TOI_DA} năm thì DTI còn "
                    f"**{pct(dti_max)}** — chưa đạt, cần kết hợp thêm giải pháp khác."
                )
                bang.append([
                    "Kéo dài thời hạn",
                    f"Cần {n_min} năm (> {THOI_HAN_TOI_DA} năm)",
                    f"{pct(dti_max)} (ở {THOI_HAN_TOI_DA} năm)",
                    "⚠️",
                ])
            else:
                dti_moi = tinh_dti(stv, n_min, LS, nc, tn, cpsh, sn, PT)
                tra_moi = tra_hang_thang(stv, n_min, LS, PT)
                st.write(
                    f"Kéo dài thời hạn từ {thv} lên **{n_min} năm** → khoản trả mới "
                    f"{vnd(tra_moi)}/tháng, DTI ≈ **{pct(dti_moi)}**."
                )
                st.write(
                    "👉 Tư vấn: số tiền trả hàng tháng giảm nhưng tổng tiền lãi phải trả "
                    "cả kỳ sẽ tăng; khách hàng có thể trả nợ trước hạn khi có điều kiện."
                )
                bang.append(["Kéo dài thời hạn", f"Vay {n_min} năm", pct(dti_moi), "✅"])

        # ---------- 3. Trả bớt nợ cũ ----------
        st.markdown("#### 3️⃣ Trả bớt nợ cũ")
        if thu_nhap_con_lai <= 0:
            st.write(khong_ap_dung)
            bang.append(["Trả bớt nợ cũ", "Không áp dụng", "—", "❌"])
        elif nc == 0:
            st.write("Không áp dụng — khách hàng không có nợ cũ.")
            bang.append(["Trả bớt nợ cũ", "Không có nợ cũ", "—", "❌"])
        else:
            nc_max = T * thu_nhap_con_lai - tra_khoan_moi
            if nc_max < 0:
                dti_0 = tinh_dti(stv, thv, LS, 0, tn, cpsh, sn, PT)
                st.write(
                    f"Không khả thi — dù tất toán toàn bộ nợ cũ, DTI vẫn còn **{pct(dti_0)}**. "
                    "Cần kết hợp thêm giải pháp khác."
                )
                bang.append(["Trả bớt nợ cũ", "Tất toán hết vẫn chưa đạt", pct(dti_0), "⚠️"])
            else:
                nc_max = math.floor(nc_max / 1_000) * 1_000
                dti_moi = tinh_dti(stv, thv, LS, nc_max, tn, cpsh, sn, PT)
                st.write(
                    f"Giảm nợ cũ phải trả từ {vnd(nc)} xuống tối đa **{vnd(nc_max)}/tháng** "
                    f"(giảm {vnd(nc - nc_max)}/tháng) → DTI ≈ **{pct(dti_moi)}**."
                )
                st.write(
                    "👉 Tư vấn: tất toán trước các khoản vay nhỏ / thẻ tín dụng, "
                    "hoặc cơ cấu lại nợ cũ để giảm số tiền trả hàng tháng."
                )
                bang.append(["Trả bớt nợ cũ", f"Nợ cũ ≤ {vnd(nc_max)}/tháng", pct(dti_moi), "✅"])

        # ---------- 4. Tăng thu nhập / thêm người đồng vay ----------
        st.markdown("#### 4️⃣ Tăng thu nhập / thêm người đồng vay")
        tn_min = tong_no / T + chi_phi_sh
        tn_min = math.ceil(tn_min / 100_000) * 100_000
        dti_moi = tinh_dti(stv, thv, LS, nc, tn_min, cpsh, sn, PT)
        st.write(
            f"Thu nhập hàng tháng cần đạt tối thiểu **{vnd(tn_min)}** "
            f"(tăng thêm {vnd(tn_min - tn)}/tháng) → DTI ≈ **{pct(dti_moi)}**."
        )
        st.write(
            "👉 Tư vấn: bổ sung người đồng vay (vợ/chồng, người thân) có thu nhập ổn định, "
            "hoặc chứng minh thêm nguồn thu nhập khác (cho thuê, kinh doanh...)."
        )
        bang.append(["Tăng thu nhập", f"Thu nhập ≥ {vnd(tn_min)}", pct(dti_moi), "✅"])

        # ---------- Bảng tóm tắt ----------
        st.markdown("#### 📋 Tóm tắt các phương án")
        df = pd.DataFrame(bang, columns=["Giải pháp", "Điều chỉnh", "DTI sau điều chỉnh", "Đạt"])
        st.dataframe(df, hide_index=True, width="stretch")
        st.caption("✅ Đạt mục tiêu · ⚠️ Cải thiện nhưng chưa đủ, cần kết hợp · ❌ Không áp dụng/không khả thi")

    # ================== MÔ PHỎNG KẾT HỢP ==================
    st.divider()
    st.subheader("🎛️ Mô phỏng kết hợp nhiều giải pháp")
    st.caption(
        "Kéo các thanh trượt để điều chỉnh đồng thời nhiều yếu tố cho khách hàng này; "
        "DTI mới được tính ngay. Bấm lại **Tính DTI** để đặt lại về số liệu ban đầu."
    )

    v = st.session_state.get("lan_tinh", 0)  # đổi key mỗi lần Tính DTI để reset thanh trượt

    m1, m2 = st.columns(2)
    with m1:
        if stv > 0:
            buoc_vay = 10_000_000 if stv >= 100_000_000 else 1_000_000
            stv_s = st.slider(
                "Số tiền vay (VNĐ)", 0, int(stv), int(stv), step=buoc_vay, key=f"s_stv_{v}",
            )
            st.caption(f"→ {vnd(stv_s)}")
        else:
            stv_s = 0
        thv_s = st.slider(
            "Thời hạn vay (năm)", 1, int(max(THOI_HAN_TOI_DA, thv)), int(thv), key=f"s_thv_{v}",
        )
        ls_s = st.number_input(
            "Lãi suất (%/năm)", min_value=0.0, value=float(ls), step=0.1, format="%.2f",
            key=f"s_ls_{v}",
            help="Có thể thử lãi suất ưu đãi / gói vay khác.",
        )
    with m2:
        if nc > 0:
            nc_s = st.slider(
                "Nợ cũ / tháng (VNĐ)", 0, int(nc), int(nc), step=100_000, key=f"s_nc_{v}",
            )
            st.caption(f"→ {vnd(nc_s)}")
        else:
            nc_s = 0
        tn_tran = int(max(tn * 3, tn + 50_000_000))
        tn_s = st.slider(
            "Thu nhập / tháng (VNĐ)", int(tn), tn_tran, int(tn), step=500_000, key=f"s_tn_{v}",
        )
        st.caption(f"→ {vnd(tn_s)}")
        sn_s = st.number_input(
            "Số người phụ thuộc chi phí", min_value=1, value=int(sn), step=1, key=f"s_sn_{v}",
        )

    dti_s = tinh_dti(stv_s, thv_s, ls_s / 100, nc_s, tn_s, cpsh, sn_s, PT)
    tra_s = tra_hang_thang(stv_s, thv_s, ls_s / 100, PT)

    r1, r2, r3 = st.columns(3)
    if dti_s is None:
        r1.metric("DTI sau điều chỉnh", "—")
    else:
        delta = None if DTI is None else f"{(dti_s - DTI) * 100:+.2f}%"
        r1.metric("DTI sau điều chỉnh", f"{dti_s * 100:.2f}%", delta=delta, delta_color="inverse")
    r2.metric("Trả khoản vay mới / tháng", vnd(tra_s))
    r3.metric("Tổng trả nợ / tháng", vnd(tra_s + nc_s))

    if dti_s is None:
        st.error("❌ Thu nhập vẫn không đủ trang trải chi phí sinh hoạt.")
    elif thv_s > THOI_HAN_TOI_DA:
        st.warning(f"⚠️ Thời hạn {thv_s} năm vượt mức tối đa {THOI_HAN_TOI_DA} năm.")
    elif dti_s < NGUONG_DTI:
        st.success(f"✅ **ĐƯỢC VAY** với phương án này — DTI = {dti_s * 100:.2f}% < {nguong_pct:g}%")
    else:
        st.error(f"❌ Chưa đạt — DTI = {dti_s * 100:.2f}% vẫn từ {nguong_pct:g}% trở lên")

    # Tóm tắt phương án để tư vấn khách hàng
    thay_doi = []
    if stv_s != stv:
        thay_doi.append(f"giảm số tiền vay xuống {vnd(stv_s)}")
    if thv_s != thv:
        thay_doi.append(f"{'kéo dài' if thv_s > thv else 'rút ngắn'} thời hạn vay thành {thv_s} năm")
    if abs(ls_s - ls) > 1e-9:
        thay_doi.append(f"lãi suất {ls_s:.2f}%/năm")
    if nc_s != nc:
        thay_doi.append(f"giảm nợ cũ còn {vnd(nc_s)}/tháng")
    if tn_s != tn:
        thay_doi.append(f"nâng thu nhập lên {vnd(tn_s)}/tháng (tăng {vnd(tn_s - tn)})")
    if sn_s != sn:
        thay_doi.append(f"số người phụ thuộc chi phí: {sn_s}")

    if thay_doi:
        st.info(
            f"📝 **Phương án tư vấn cho khách hàng {ten_hien_thi}:** "
            + "; ".join(thay_doi)
            + (f" → DTI = {dti_s * 100:.2f}%." if dti_s is not None else ".")
        )
