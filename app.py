import streamlit as st
import pandas as pd

st.set_page_config(page_title="Education Analytics Dashboard", page_icon="🎓", layout="wide")
st.title("🎓 Education Analytics Dashboard")
st.write("Analyze student marks, attendance, and academic performance.")
st.caption("Demonstration dashboard using sample classroom data.")

data = {
    "Student": ["Amit", "Priya", "Rahul", "Sneha", "Rohan", "Pooja", "Vikas", "Neha", "Arjun", "Anjali"],
    "Maths": [85, 92, 67, 88, 76, 95, 58, 81, 73, 90],
    "Science": [80, 95, 70, 85, 78, 92, 60, 84, 75, 89],
    "English": [78, 90, 72, 86, 80, 94, 65, 82, 77, 91],
    "Attendance": [90, 98, 75, 92, 80, 99, 65, 88, 78, 95],
}
df = pd.DataFrame(data)
df["Total"] = df[["Maths", "Science", "English"]].sum(axis=1)
df["Average"] = df[["Maths", "Science", "English"]].mean(axis=1).round(2)
df["Result"] = df["Average"].apply(lambda x: "Pass" if x >= 35 else "Fail")

st.sidebar.header("Dashboard Filters")
min_attendance = st.sidebar.slider("Minimum attendance (%)", 0, 100, 0, 5)
results = st.sidebar.multiselect("Result", ["Pass", "Fail"], default=["Pass", "Fail"])
filtered = df[(df["Attendance"] >= min_attendance) & (df["Result"].isin(results))]

n = len(filtered)
avg_marks = filtered["Average"].mean() if n else 0
avg_att = filtered["Attendance"].mean() if n else 0
passed = int((filtered["Result"] == "Pass").sum())

a, b, c, d = st.columns(4)
a.metric("Total Students", n)
b.metric("Average Marks", f"{avg_marks:.2f}/100" if n else "—")
c.metric("Average Attendance", f"{avg_att:.1f}%" if n else "—")
d.metric("Students Passed", passed)

left, right = st.columns(2)
with left:
    st.subheader("Subject-wise Average Marks")
    if n:
        st.bar_chart(filtered[["Maths", "Science", "English"]].mean())
    else:
        st.info("No students match the selected filters.")
with right:
    st.subheader("Student Attendance")
    if n:
        st.bar_chart(filtered.set_index("Student")[["Attendance"]])
    else:
        st.info("No students match the selected filters.")

st.subheader("Student Performance Table")
if n:
    table = filtered.copy()
    table["Attendance"] = table["Attendance"].astype(str) + "%"
    st.dataframe(table, use_container_width=True, hide_index=True)
else:
    st.info("No students match the selected filters.")

st.subheader("Top 3 Students")
if n:
    top3 = filtered.nlargest(3, "Average")[["Student", "Average", "Attendance", "Result"]].copy()
    top3["Attendance"] = top3["Attendance"].astype(str) + "%"
    st.dataframe(top3, use_container_width=True, hide_index=True)

with st.expander("About this project"):
    st.write("This dashboard calculates total and average marks, summarizes attendance, compares subject averages, and lists top students. All names and scores are sample data.")
