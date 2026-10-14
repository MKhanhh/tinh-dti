import math

import pandas as pd
import streamlit as st

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(page_title="Thẩm định tín dụng - DTI", page_icon="💰", layout="centered")

NGUONG_DTI = 0.7        # Ngưỡng 70%
THOI_HAN_TOI_DA = 20    # Thời hạn vay tối đa ngân hàng cho phép (năm)


def vnd(x: float) -> str:
    """Định dạng số tiền kiểu Việt Nam: 1.000.000 đ"""
    return f"{x:,.0f} đ".replace(",", ".")


def tinh_dti(stv, thv, LS, nc, tn, cpsh, sn):
    """Trả về DTI (số thập phân) hoặc None nếu thu nhập còn lại <= 0."""
    con_lai = tn - cpsh * sn
    if con_lai <= 0:
        return None
    tra_hang_thang = stv / (thv * 12) + stv * LS / 12
    return (tra_hang_thang + nc) / con_lai


def pct(x) -> str:
    return "—" if x is None else f"{x * 100:.2f}%"


# ================== GIAO DIỆN ==================
st.title("💰 Phần mềm thẩm định tín dụng_Nguyễn Viết Minh Khánh")
st.caption(
    "DTI = (Tiền gốc + lãi phải trả hàng tháng + Nợ cũ) / "
    "(Thu nhập − Chi phí sinh hoạt × Số người)"
)

with st.form("dti_form"):
    col1, col2 = st.columns(2)

    with col1:
        stv = st.number_input(
            "Số tiền vay (VNĐ)",
            min_value=0, value=800_000_000, step=10_000_000, format="%d",
        )
        thv = st.number_input(
            "Thời hạn vay (năm)",
            min_value=1, max_value=THOI_HAN_TOI_DA, value=5, step=1,
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
            min_value=10.0, max_value=NGUONG_DTI * 100, value=NGUONG_DTI * 100, step=1.0,
            format="%.1f",
            help="Các giải pháp sẽ đưa DTI xuống dưới mức này (tối đa 70%).",
        )

    submitted = st.form_submit_button("📊 Tính DTI")

# ================== TÍNH TOÁN ==================
if submitted:
    LS = ls / 100  # đổi % sang số thập phân

    tra_goc = stv / (thv * 12)          # gốc phải trả mỗi tháng
    tra_lai = stv * (LS / 12)           # lãi phải trả mỗi tháng
    tra_khoan_moi = tra_goc + tra_lai   # khoản vay mới mỗi tháng
    tong_no = tra_khoan_moi + nc        # tổng nợ phải trả mỗi tháng
    chi_phi_sh = cpsh * sn
    thu_nhap_con_lai = tn - chi_phi_sh  # thu nhập sau chi phí sinh hoạt

    st.divider()
    st.subheader("Kết quả")

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
        c2.metric("Ngưỡng cho phép", f"< {NGUONG_DTI * 100:.0f}%")

        if DTI < NGUONG_DTI:
            st.success(f"✅ **ĐƯỢC VAY** — DTI = {DTI * 100:.2f}% nhỏ hơn {NGUONG_DTI * 100:.0f}%")
        else:
            st.error(f"❌ **KHÔNG ĐƯỢC VAY** — DTI = {DTI * 100:.2f}% từ {NGUONG_DTI * 100:.0f}% trở lên")

        st.progress(min(DTI, 1.0))

    with st.expander("Xem chi tiết tính toán"):
        st.write(f"- Gốc trả hàng tháng: **{vnd(tra_goc)}**")
        st.write(f"- Lãi trả hàng tháng: **{vnd(tra_lai)}**")
        st.write(f"- Khoản vay mới / tháng: **{vnd(tra_khoan_moi)}**")
        st.write(f"- Nợ cũ / tháng: **{vnd(nc)}**")
        st.write(f"- **Tổng nợ phải trả / tháng: {vnd(tong_no)}**")
        st.write(f"- Tổng chi phí sinh hoạt: **{vnd(chi_phi_sh)}**")
        st.write(f"- **Thu nhập còn lại: {vnd(thu_nhap_con_lai)}**")

    # ================== TƯ VẤN GIẢM DTI ==================
    # Mục tiêu: DTI < mục tiêu (và luôn < ngưỡng 70%)
    T = min(muc_tieu / 100, NGUONG_DTI) - 0.0005  # chừa biên 0,05% để kết quả hiển thị luôn dưới mục tiêu

    if DTI is None or DTI >= T:
        st.divider()
        st.subheader("💡 Tư vấn giải pháp giảm DTI")
        st.caption(
            f"Mục tiêu: đưa DTI xuống dưới **{muc_tieu:.1f}%**. Mỗi giải pháp dưới đây "
            "chỉ điều chỉnh MỘT yếu tố, các yếu tố khác giữ nguyên."
        )

        he_so_tra = 1 / (thv * 12) + LS / 12  # số tiền trả / tháng cho mỗi 1 đồng vay
        bang = []

        # ---------- 1. Giảm số tiền vay ----------
        st.markdown("#### 1️⃣ Giảm số tiền vay")
        if thu_nhap_con_lai <= 0:
            st.write("Không áp dụng được — thu nhập còn lại ≤ 0, cần tăng thu nhập trước.")
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
                stv_max = math.floor(du_dia / he_so_tra / 1_000_000) * 1_000_000
                dti_moi = tinh_dti(stv_max, thv, LS, nc, tn, cpsh, sn)
                st.write(
                    f"Vay tối đa **{vnd(stv_max)}** (giảm {vnd(stv - stv_max)} so với đề nghị), "
                    f"thời hạn giữ nguyên {thv} năm → DTI ≈ **{pct(dti_moi)}**."
                )
                st.write(
                    "👉 Tư vấn: khách hàng bổ sung phần còn thiếu bằng vốn tự có "
                    "hoặc chọn tài sản/phương án có giá trị thấp hơn."
                )
                bang.append(["Giảm số tiền vay", f"Vay tối đa {vnd(stv_max)}", pct(dti_moi), "✅"])

                # Gợi ý kết hợp: kéo dài tối đa + giảm số tiền vay
                if thv < THOI_HAN_TOI_DA:
                    he_so_max = 1 / (THOI_HAN_TOI_DA * 12) + LS / 12
                    stv_max20 = math.floor(du_dia / he_so_max / 1_000_000) * 1_000_000
                    st.caption(
                        f"Nếu đồng thời kéo dài lên {THOI_HAN_TOI_DA} năm thì có thể vay tối đa "
                        f"{vnd(stv_max20)}."
                    )

        # ---------- 2. Kéo dài thời hạn vay ----------
        st.markdown("#### 2️⃣ Kéo dài thời hạn vay")
        if thu_nhap_con_lai <= 0:
            st.write("Không áp dụng được — thu nhập còn lại ≤ 0, cần tăng thu nhập trước.")
            bang.append(["Kéo dài thời hạn", "Không áp dụng", "—", "❌"])
        elif stv == 0:
            st.write("Không áp dụng — số tiền vay bằng 0.")
            bang.append(["Kéo dài thời hạn", "Không áp dụng", "—", "❌"])
        else:
            du_dia_goc = T * thu_nhap_con_lai - nc - stv * LS / 12  # phần còn lại để trả gốc
            if du_dia_goc <= 0:
                st.write(
                    "Không khả thi — riêng tiền lãi và nợ cũ đã vượt mức cho phép, "
                    "kéo dài bao lâu cũng không đạt."
                )
                bang.append(["Kéo dài thời hạn", "Không khả thi", "—", "❌"])
            else:
                n_min = math.ceil(stv / (12 * du_dia_goc))
                n_min = max(n_min, thv)
                if n_min > THOI_HAN_TOI_DA:
                    dti_20 = tinh_dti(stv, THOI_HAN_TOI_DA, LS, nc, tn, cpsh, sn)
                    st.write(
                        f"Cần vay ít nhất **{n_min} năm**, vượt thời hạn tối đa {THOI_HAN_TOI_DA} năm "
                        f"của ngân hàng. Kéo dài lên {THOI_HAN_TOI_DA} năm thì DTI còn "
                        f"**{pct(dti_20)}** — chưa đạt, cần kết hợp thêm giải pháp khác."
                    )
                    bang.append([
                        "Kéo dài thời hạn",
                        f"Cần {n_min} năm (> {THOI_HAN_TOI_DA} năm)",
                        pct(dti_20) + f" (ở {THOI_HAN_TOI_DA} năm)",
                        "⚠️",
                    ])
                else:
                    dti_moi = tinh_dti(stv, n_min, LS, nc, tn, cpsh, sn)
                    tra_moi = stv / (n_min * 12) + stv * LS / 12
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
            st.write("Không áp dụng được — thu nhập còn lại ≤ 0, cần tăng thu nhập trước.")
            bang.append(["Trả bớt nợ cũ", "Không áp dụng", "—", "❌"])
        elif nc == 0:
            st.write("Không áp dụng — khách hàng không có nợ cũ.")
            bang.append(["Trả bớt nợ cũ", "Không có nợ cũ", "—", "❌"])
        else:
            nc_max = T * thu_nhap_con_lai - tra_khoan_moi
            if nc_max < 0:
                dti_0 = tinh_dti(stv, thv, LS, 0, tn, cpsh, sn)
                st.write(
                    f"Không khả thi — dù tất toán toàn bộ nợ cũ, DTI vẫn còn **{pct(dti_0)}**. "
                    "Cần kết hợp thêm giải pháp khác."
                )
                bang.append(["Trả bớt nợ cũ", "Tất toán hết vẫn chưa đạt", pct(dti_0), "⚠️"])
            else:
                nc_max = math.floor(nc_max / 1_000) * 1_000
                dti_moi = tinh_dti(stv, thv, LS, nc_max, tn, cpsh, sn)
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
        dti_moi = tinh_dti(stv, thv, LS, nc, tn_min, cpsh, sn)
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
