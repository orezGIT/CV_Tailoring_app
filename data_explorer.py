import streamlit as st
import pandas as pd
import itertools
from datetime import datetime

# ====== CUSTOM STYLING ======
st.markdown("""
<style>
    /* ====== 🌿 Global Page ====== */
    .main {
        background-color: #f6fdf7;
        font-family: 'Segoe UI', sans-serif;
        color: #2f3e46;
    }

    /* ====== 🌿 Headings ====== */
    h1, h2, h3 {
        color: #1b7a3a;
        font-weight: 700;
    }

    h1 {
        font-size: 2.2rem;
        margin-bottom: 0.4rem;
        border-left: 6px solid #28a745;
        padding-left: 10px;
    }

    h2 {
        margin-top: 1.2rem;
        font-size: 1.5rem;
    }

    /* ====== 💚 Buttons ====== */
    .stButton>button {
        background: linear-gradient(135deg, #28a745, #23913b);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6em 1.4em;
        transition: all 0.25s ease;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.12);
        cursor: pointer;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #218838, #1e7a33);
        color: #fff;
        transform: translateY(-2px);
        box-shadow: 0px 5px 10px rgba(0,0,0,0.18);
    }

    /* ====== 📦 Inputs ====== */
    .stTextInput>div>div>input,
    .stFileUploader>div>div>div>input {
        border: 1px solid #28a745;
        border-radius: 6px;
        padding: 0.5em;
        transition: 0.2s ease-in-out;
    }

    .stTextInput>div>div>input:focus,
    .stFileUploader>div>div>div>input:hover {
        border-color: #1e7a33;
        box-shadow: 0 0 0 3px rgba(40,167,69,0.2);
    }

    /* ====== 💬 Alerts ====== */
    .stAlert {
        border-radius: 10px !important;
        border-left: 5px solid #28a745 !important;
    }

    /* ====== 💻 Code Blocks ====== */
    pre {
        background-color: #e9f5ee !important;
        border-left: 5px solid #28a745 !important;
        border-radius: 6px;
        padding: 1em;
        font-size: 0.9rem;
    }

    /* ====== 📊 Sidebar ====== */
    section[data-testid="stSidebar"] {
        background-color: #e8f8ed;
        color: #2f3e46;
    }

    section[data-testid="stSidebar"] .css-1d391kg {
        color: #1b7a3a;
    }
</style>
""", unsafe_allow_html=True)

# ====== APP HEADER ======
st.set_page_config(page_title="Full-Stack Data Assistant", layout="wide")
st.title("🤖 Full-Stack Data Assistant")
st.caption("Upload datasets, auto-generate SQL queries, DAX measures, and chart recommendations.")

# ====== 1. UPLOAD CSV DATASETS ======
st.subheader("📂 Upload one or more CSV files")
uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

datasets = {}
if uploaded_files:
    for file in uploaded_files:
        df = pd.read_csv(file)
        datasets[file.name] = df
        st.write(f"### Dataset: {file.name}")
        st.dataframe(df.head())
        st.write("**Summary:**")
        st.write(df.describe(include='all').transpose())

# ====== 2. DETECT RELATIONSHIPS & JOIN KEYS ======
def detect_relationships(datasets):
    keys = {}
    if len(datasets) > 1:
        for (name1, df1), (name2, df2) in itertools.combinations(datasets.items(), 2):
            common_cols = set(df1.columns).intersection(df2.columns)
            if common_cols:
                keys[(name1, name2)] = list(common_cols)
    return keys

join_keys = detect_relationships(datasets)
if join_keys:
    st.subheader("🔗 Suggested JOIN Relationships")
    for (d1, d2), cols in join_keys.items():
        st.write(f"**{d1}** ⟷ **{d2}** → Possible JOIN keys: `{', '.join(cols)}`")

# ====== 3. NATURAL LANGUAGE QUESTION BOX ======
st.subheader("💬 Ask a Question in Plain English")
user_query = st.text_input("Type your question, e.g., 'Show average sales by product for Q1 2024'")

# ====== 4. SQL QUERY GENERATOR ======
def generate_sql(user_query, datasets, join_keys):
    if not user_query or not datasets:
        return "Type a question above and upload data."

    sql_parts = []
    if len(datasets) == 1:
        table = list(datasets.keys())[0].replace(".csv", "")
        sql_parts.append(f"-- Single table query for {table}")
        sql_parts.append(f"SELECT column1, column2, AVG(column3) AS avg_value")
        sql_parts.append(f"FROM {table}")
        sql_parts.append("WHERE date BETWEEN [start] AND [end]")
        sql_parts.append("GROUP BY column1, column2;")
    else:
        (t1, t2), cols = list(join_keys.items())[0]
        join_col = cols[0]
        sql_parts.append(f"-- Auto-generated JOIN query")
        sql_parts.append(f"SELECT t1.columnA, t2.columnB, SUM(t1.metric) AS total_metric")
        sql_parts.append(f"FROM {t1.replace('.csv','')} t1")
        sql_parts.append(f"JOIN {t2.replace('.csv','')} t2 ON t1.{join_col} = t2.{join_col}")
        sql_parts.append("WHERE t1.date BETWEEN [start] AND [end]")
        sql_parts.append("GROUP BY t1.columnA, t2.columnB;")
    return "\n".join(sql_parts)

if user_query:
    st.subheader("🧩 Suggested SQL Query")
    sql_output = generate_sql(user_query, datasets, join_keys)
    st.code(sql_output, language="sql")

# ====== 5. POWER BI DAX SUGGESTIONS ======
def suggest_dax(user_query):
    if "average" in user_query.lower():
        return "DAX Suggestion: `Average Sales = AVERAGE(Sales[Amount])`"
    elif "total" in user_query.lower() or "sum" in user_query.lower():
        return "DAX Suggestion: `Total Sales = SUM(Sales[Amount])`"
    elif "count" in user_query.lower():
        return "DAX Suggestion: `Customer Count = DISTINCTCOUNT(Customer[ID])`"
    else:
        return "DAX Suggestion: Try `Measure = SUM(Table[Metric]) / COUNT(Table[ID])`"

if user_query:
    st.subheader("📊 Suggested DAX Measure")
    st.info(suggest_dax(user_query))

# ====== 6. CHART RECOMMENDER ======
def recommend_chart(df, user_query):
    if any(word in user_query.lower() for word in ["trend", "over time", "date"]):
        return "📈 Recommended Chart: Line Chart (showing trends over time)"
    elif "compare" in user_query.lower() or "by" in user_query.lower():
        return "📊 Recommended Chart: Bar Chart (compare categories)"
    elif "distribution" in user_query.lower():
        return "📦 Recommended Chart: Histogram"
    elif "correlation" in user_query.lower():
        return "🔗 Recommended Chart: Scatter Plot"
    else:
        return "🧭 Recommended Chart: Summary Table or Pie Chart"

if uploaded_files and user_query:
    st.subheader("🪄 Chart Recommendation")
    first_df = list(datasets.values())[0]
    st.success(recommend_chart(first_df, user_query))