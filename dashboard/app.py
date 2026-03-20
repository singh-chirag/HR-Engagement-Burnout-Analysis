import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import pickle

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/Palo Alto Networks.csv")

# Load model safely
try:
    model = pickle.load(open("models/attrition_model.pkl", "rb"))
except:
    model = None

st.set_page_config(page_title="HR Dashboard", layout="wide")

st.title("📊 HR Engagement, Burnout & Attrition Dashboard")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

department = st.sidebar.selectbox(
    "Select Department",
    df["Department"].unique()
)

overtime_filter = st.sidebar.selectbox(
    "Overtime",
    ["All", "Yes", "No"]
)

filtered = df[df["Department"] == department]

if overtime_filter != "All":
    filtered = filtered[filtered["OverTime"] == overtime_filter]

# ---------------- KPIs ----------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Employees", len(filtered))

col2.metric(
    "Avg Job Satisfaction",
    round(filtered["JobSatisfaction"].mean(), 2)
)

col3.metric(
    "Avg Work-Life Balance",
    round(filtered["WorkLifeBalance"].mean(), 2)
)

col4.metric(
    "Attrition Rate",
    str(round(filtered["Attrition"].mean() * 100, 2)) + "%"
)

# ---------------- ENGAGEMENT ----------------
st.subheader("📊 Engagement Analysis")

fig = px.histogram(filtered, x="JobSatisfaction")
st.plotly_chart(fig)

fig1 = px.histogram(filtered, x="JobSatisfaction", nbins=10)
st.plotly_chart(fig1)
# fig1, ax1 = plt.subplots()
# sns.histplot(filtered["JobSatisfaction"], bins=10, ax=ax1)
ax1.set_title("Job Satisfaction Distribution")
st.pyplot(fig1)

# ---------------- BURNOUT ----------------
st.subheader("🔥 Burnout Indicators")
fig2 = px.box(filtered, x="Attrition", y="MonthlyIncome")
st.plotly_chart(fig2)
# fig2, ax2 = plt.subplots()
# sns.countplot(x="OverTime", data=filtered, ax=ax2)
ax2.set_title("Overtime Distribution")
st.pyplot(fig2)

fig3, ax3 = plt.subplots()
sns.boxplot(
    x="OverTime",
    y="WorkLifeBalance",
    data=filtered,
    ax=ax3
)
ax3.set_title("Work-Life Balance vs Overtime")
st.pyplot(fig3)

# ---------------- ATTRITION ----------------
st.subheader("⚠️ Attrition Insights")

fig4, ax4 = plt.subplots()
sns.boxplot(
    x="Attrition",
    y="MonthlyIncome",
    data=filtered,
    ax=ax4
)
ax4.set_title("Salary vs Attrition")
st.pyplot(fig4)


fig = px.box(filtered, x="Attrition", y="MonthlyIncome")
st.plotly_chart(fig)
# ---------------- ALERT SECTION ----------------
st.subheader("🚨 HR Alerts")

high_risk = filtered[
    (filtered["OverTime"] == "Yes") &
    (filtered["WorkLifeBalance"] <= 2)
]

st.write("High Burnout Risk Employees:", len(high_risk))

if len(high_risk) > 0:
    st.warning("⚠️ High burnout risk detected!")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Built for HR Decision Support 🚀")