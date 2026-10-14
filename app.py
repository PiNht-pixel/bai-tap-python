import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cấu hình trang web
st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="📚",
    layout="wide"
)

# 2. Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN-")

st.write("Ứng dụng thống kê và tra cứu điểm sinh viên.")

# 3. Dữ liệu 10 sinh viên
data = {
    "Họ tên": [
        "Nguyễn Văn Ân",
        "Trần Thị Bình",
        "Lê Hoàng Cường",
        "Phạm Minh Dương",
        "Lưu Hoàng Anh",
        "Vũ Thị Phương",
        "Đặng Quốc Huy",
        "Bùi Thị Nguyên",
        "Đỗ Văn Minh",
        "Cao Thị Oanh"
    ],
    "Chuyên cần": [
        9.0, 8.5, 10.0, 7.5, 8.0,
        9.5, 6.5, 9.0, 8.0, 10.0
    ],
    "Giữa kỳ": [
        7.5, 8.0, 6.5, 9.0, 7.0,
        8.5, 6.0, 9.5, 7.5, 8.5
    ],
    "Cuối kỳ": [
        8.0, 8.5, 7.0, 8.5, 6.5,
        9.0, 7.0, 9.0, 8.0, 9.0
    ]
}

df = pd.DataFrame(data)

# 4. Tính điểm tổng kết
df["Tổng kết"] = (
    df["Chuyên cần"] * 0.2
    + df["Giữa kỳ"] * 0.3
    + df["Cuối kỳ"] * 0.5
).round(2)

# 5. Xếp loại sinh viên
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# 6. Hiển thị bảng điểm
st.subheader("1. Bảng điểm 10 sinh viên")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# 7. Thống kê điểm của lớp
diem_tb = df["Tổng kết"].mean()
diem_cao_nhat = df["Tổng kết"].max()
diem_thap_nhat = df["Tổng kết"].min()

sv_cao_nhat = df[df["Tổng kết"] == diem_cao_nhat]
sv_thap_nhat = df[df["Tổng kết"] == diem_thap_nhat]

so_sv_dat = (df["Tổng kết"] >= 5).sum()

st.subheader("2. Thống kê kết quả học tập")

cot1, cot2, cot3 = st.columns(3)

cot1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
cot2.metric("Số sinh viên đạt", f"{so_sv_dat}/10")
cot3.metric("Số sinh viên", len(df))

st.write("**Sinh viên có điểm tổng kết cao nhất:**")
st.dataframe(
    sv_cao_nhat[["Họ tên", "Tổng kết"]],
    hide_index=True,
    use_container_width=True
)

st.write("**Sinh viên có điểm tổng kết thấp nhất:**")
st.dataframe(
    sv_thap_nhat[["Họ tên", "Tổng kết"]],
    hide_index=True,
    use_container_width=True
)

# 8. Selectbox chọn sinh viên
st.subheader("3. Tra cứu điểm từng sinh viên")

ten_sv = st.selectbox(
    "Chọn họ tên sinh viên:",
    df["Họ tên"]
)

sv = df[df["Họ tên"] == ten_sv].iloc[0]

st.write(f"**Họ tên:** {sv['Họ tên']}")

a, b, c, d, e = st.columns(5)

a.metric("Chuyên cần", f"{sv['Chuyên cần']:.2f}")
b.metric("Giữa kỳ", f"{sv['Giữa kỳ']:.2f}")
c.metric("Cuối kỳ", f"{sv['Cuối kỳ']:.2f}")
d.metric("Tổng kết", f"{sv['Tổng kết']:.2f}")
e.metric("Xếp loại", sv["Xếp loại"])

# 9. Biểu đồ cột điểm tổng kết
st.subheader("4. Biểu đồ cột điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(df["Họ tên"], df["Tổng kết"])

ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# 10. Thông tin người tạo ứng dụng ở cuối trang
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; font-size:12px; color:gray;">
        <p>Danh sách sinh viên thực hiện ứng dụng</p>
        <p>Nguyễn Văn Ân - MSSV: 23110001</p>
        <p>Trần Thị Bình - MSSV: 23110002</p>
        <p>Lê Hoàng Cường - MSSV: 23110003</p>
        <p>Phạm Minh Dương - MSSV: 23110004</p>
        <p>Lưu Hoàng Anh - MSSV: 23110005</p>
        <p>Vũ Thị Phương - MSSV: 23110006</p>
        <p>Đặng Quốc Huy - MSSV: 23110007</p>
        <p>Bùi Thị Nguyên - MSSV: 23110008</p>
        <p>Đỗ Văn Minh - MSSV: 23110009</p>
        <p>Cao Thị Oanh - MSSV: 23110010</p>
    </div>
    """,
    unsafe_allow_html=True
)
