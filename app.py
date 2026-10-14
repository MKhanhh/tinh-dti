import streamlit as st

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(page_title="Phần mềm thẩm định tín dụng_Nguyễn Viết Minh Khánh", page_icon="💰", layout="centered")

NGUONG_DTI = 0.7  # Ngưỡng 70%


def vnd(x: float) -> str:
    """Định dạng số tiền kiểu Việt Nam: 1.000.000 đ"""
    return f"{x:,.0f} đ".replace(",", ".")


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
            min_value=1, value=5, step=1,
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

    submitted = st.form_submit_button("📊 Tính DTI")

# ================== TÍNH TOÁN ==================
if submitted:
    LS = ls / 100  # đổi % sang số thập phân

    tra_goc = stv / (thv * 12)          # gốc phải trả mỗi tháng
    tra_lai = stv * (LS / 12)           # lãi phải trả mỗi tháng
    tra_khoan_moi = tra_goc + tra_lai   # khoản vay mới mỗi tháng
    tong_no = tra_khoan_moi + nc        # tổng nợ phải trả mỗi tháng
    thu_nhap_con_lai = tn - cpsh * sn   # thu nhập sau chi phí sinh hoạt

    st.divider()
    st.subheader("Kết quả")

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
        st.write(f"- Tổng chi phí sinh hoạt: **{vnd(cpsh * sn)}**")
        st.write(f"- **Thu nhập còn lại: {vnd(thu_nhap_con_lai)}**")
