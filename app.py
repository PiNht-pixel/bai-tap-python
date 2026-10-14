import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cấu hình ứng dụng
st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="📚",
    layout="wide"
)

st.title("📚 ỨNG DỤNG QUẢN LÝ ĐIỂM SINH VIÊN")
st.write(
    "Tính điểm tổng kết, thống kê kết quả học tập "
    "và trực quan hóa điểm số của lớp."
)

# 2. Khởi tạo dữ liệu ban đầu
data = {
    "Họ và tên": [
        "Nguyễn Văn Ân",
        "Trần Thị Bình",
        "Lê Hoàng Cường",
        "Phạm Minh Dương",
        "Lưu Hoàng Anh",
        "Vũ Thị Phương",
        "Đặng Quốc Huy",
        "Bùi Thị Nguyên",
        "Đỗ Văn Minh",
        "Cao Thị Oanh",
    ],
    "Điểm chuyên cần": [
        9.0, 8.5, 10.0, 7.5, 8.0,
        9.5, 6.5, 9.0, 8.0, 10.0
    ],
    "Điểm giữa kỳ": [
        7.5, 8.0, 6.5, 9.0, 7.0,
        8.5, 6.0, 9.5, 7.5, 8.5
    ],
    "Điểm cuối kỳ": [
        8.0, 8.5, 7.0, 8.5, 6.5,
        9.0, 7.0, 9.0, 8.0, 9.0
    ],
}

df = pd.DataFrame(data)

# 3. Tính điểm tổng kết
df["Tổng kết"] = (
    0.2 * df["Điểm chuyên cần"]
    + 0.3 * df["Điểm giữa kỳ"]
    + 0.5 * df["Điểm cuối kỳ"]
).round(2)

# 4. Cho phép người dùng tải dữ liệu mới
st.sidebar.header("📂 Dữ liệu")

uploaded_file = st.sidebar.file_uploader(
    "Tải bảng điểm CSV (tùy chọn)",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df_input = pd.read_csv(uploaded_file)

        required_columns = [
            "Họ và tên",
            "Điểm chuyên cần",
            "Điểm giữa kỳ",
            "Điểm cuối kỳ"
        ]

        if not all(
            col in df_input.columns
            for col in required_columns
        ):
            st.error(
                "File CSV phải có các cột: Họ và tên, "
                "Điểm chuyên cần, Điểm giữa kỳ, "
                "Điểm cuối kỳ."
            )
            st.stop()

        df = df_input[required_columns].copy()

        score_columns = [
            "Điểm chuyên cần",
            "Điểm giữa kỳ",
            "Điểm cuối kỳ"
        ]

        for col in score_columns:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

        df = df.dropna(
            subset=["Họ và tên"] + score_columns
        )

        if df.empty:
            st.error("File không có dữ liệu hợp lệ.")
            st.stop()

        if (
            (df[score_columns] < 0).any().any()
            or (df[score_columns] > 10).any().any()
        ):
            st.error("Điểm số phải nằm trong khoảng 0 đến 10.")
            st.stop()

        df["Tổng kết"] = (
            0.2 * df["Điểm chuyên cần"]
            + 0.3 * df["Điểm giữa kỳ"]
            + 0.5 * df["Điểm cuối kỳ"]
        ).round(2)

    except Exception as e:
        st.error(f"Không thể đọc file: {e}")
        st.stop()

# 5. Hiển thị bảng điểm
st.subheader("1. Bảng điểm sinh viên")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# 6. Thống kê kết quả
dtb_lop = df["Tổng kết"].mean()
sv_cao_nhat = df[df["Tổng kết"] == df["Tổng kết"].max()]
sv_thap_nhat = df[df["Tổng kết"] == df["Tổng kết"].min()]
so_sv_dat = (df["Tổng kết"] >= 5.0).sum()

st.subheader("2. Thống kê kết quả học tập")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Điểm trung bình lớp",
    f"{dtb_lop:.2f}"
)

col2.metric(
    "Số sinh viên đạt",
    f"{so_sv_dat}/{len(df)}"
)

col3.metric(
    "Số sinh viên",
    len(df)
)

st.write("**Sinh viên có điểm tổng kết cao nhất:**")
st.dataframe(
    sv_cao_nhat[["Họ và tên", "Tổng kết"]],
    use_container_width=True,
    hide_index=True
)

st.write("**Sinh viên có điểm tổng kết thấp nhất:**")
st.dataframe(
    sv_thap_nhat[["Họ và tên", "Tổng kết"]],
    use_container_width=True,
    hide_index=True
)

# 7. Vẽ biểu đồ cột
st.subheader("3. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 6))

ax.bar(
    df["Họ và tên"],
    df["Tổng kết"]
)

ax.set_title("Điểm tổng kết của sinh viên")
ax.set_xlabel("Họ và tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# 8. Tải bảng điểm về máy
st.subheader("4. Xuất dữ liệu")

csv_data = df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="⬇️ Tải bảng điểm CSV",
    data=csv_data,
    file_name="bang_diem_sinh_vien.csv",
    mime="text/csv"
)

st.success("Đã hoàn tất thống kê bảng điểm!")
