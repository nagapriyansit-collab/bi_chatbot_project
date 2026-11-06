
import os
import json
from io import BytesIO

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from langchain_groq import ChatGroq


# ============================================================
# 1. APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Business Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered Business Intelligence Platform")
st.caption(
    "Business Data Analytics | Interactive BI | Revenue Prediction | AI Chatbot"
)


# ============================================================
# 2. API CONFIGURATION
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Fetch Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        GROQ_API_KEY = None

llm = None

if GROQ_API_KEY:
    try:
        llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0
    )
    except Exception as e:
        st.warning(f"Groq initialization failed: {e}")
else:
    st.warning(
        "Groq API key is missing. Dashboard analytics will work, "
        "but the AI chatbot will be unavailable."
    )


# ============================================================
# 3. BUSINESS DATA INGESTION
# ============================================================

st.sidebar.header("📁 Business Data Management")

uploaded_file = st.sidebar.file_uploader(
    "Upload Business Dataset",
    type=["csv", "xlsx"]
)


def load_business_data(file):

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)

    else:
        df = pd.read_excel(file)

    # Normalize column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )

    # Recognize common business column names
    aliases = {
        "product": "product_name",
        "item": "product_name",
        "product": "product_name",
        "sales": "revenue",
        "total_sales": "revenue",
        "amount": "revenue",
        "total_revenue": "revenue",
        "quantity": "units_sold",
        "units": "units_sold",
        "date": "sale_date",
        "order_date": "sale_date",
        "transaction_date": "sale_date",
        "department": "category"
    }

    rename_columns = {}

    for column in df.columns:
        if column in aliases:
            rename_columns[column] = aliases[column]

    df = df.rename(columns=rename_columns)

    if "revenue" not in df.columns:
        raise ValueError(
            "The dataset must contain a revenue or sales column."
        )

    # Add optional fields if missing
    if "product_name" not in df.columns:
        df["product_name"] = "Unknown"

    if "category" not in df.columns:
        df["category"] = "Uncategorized"

    if "units_sold" not in df.columns:
        df["units_sold"] = 0

    if "sale_date" not in df.columns:
        df["sale_date"] = pd.NaT

    # Data type conversion
    df["revenue"] = pd.to_numeric(
        df["revenue"], errors="coerce"
    )

    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )

    df["sale_date"] = pd.to_datetime(
        df["sale_date"], errors="coerce"
    )

    # Remove invalid revenue records
    df = df.dropna(subset=["revenue"]).copy()

    df["units_sold"] = df["units_sold"].fillna(0)

    return df


# Load uploaded or sample dataset
if uploaded_file is not None:

    try:
        df = load_business_data(uploaded_file)

        st.session_state["business_data"] = df

        st.success("Business dataset uploaded successfully!")

    except Exception as e:
        st.error(f"Dataset processing error: {e}")
        st.stop()

elif "business_data" in st.session_state:

    df = st.session_state["business_data"]

else:

    st.info("Upload a business CSV or Excel dataset to begin.")

    st.stop()


# ============================================================
# 4. DATA PROCESSING AND PREVIEW
# ============================================================

st.header("📂 Business Data Overview")

with st.expander("View Uploaded Business Dataset", expanded=True):

    st.dataframe(
        df,
        use_container_width=True,
        height=250
    )

    st.write("Dataset Shape:", df.shape)

    st.write("Missing Values:")

    st.dataframe(
        df.isnull().sum().rename("Missing Count"),
        use_container_width=True
    )


# ============================================================
# 5. BUSINESS KPI CALCULATIONS
# ============================================================

total_revenue = df["revenue"].sum()

total_units = df["units_sold"].sum()

average_revenue = df["revenue"].mean()

total_transactions = len(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}"
)

col2.metric(
    "Units Sold",
    f"{total_units:,.0f}"
)

col3.metric(
    "Average Revenue",
    f"{average_revenue:,.2f}"
)

col4.metric(
    "Transactions",
    f"{total_transactions:,}"
)


# ============================================================
# 6. INTERACTIVE BUSINESS VISUALIZATION
# ============================================================

st.header("📈 Business Intelligence Dashboard")

tab1, tab2, tab3 = st.tabs([
    "Revenue Analysis",
    "Product Analysis",
    "Time-Series Analysis"
])


# Revenue Analysis
with tab1:

    col1, col2 = st.columns(2)

    with col1:

        category_revenue = (
            df.groupby("category", dropna=False)["revenue"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_revenue,
            x="category",
            y="revenue",
            color="category",
            title="Revenue by Business Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.pie(
            category_revenue,
            names="category",
            values="revenue",
            title="Revenue Contribution by Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Product Analysis
with tab2:

    col1, col2 = st.columns(2)

    with col1:

        product_revenue = (
            df.groupby("product_name")["revenue"]
            .sum()
            .reset_index()
            .sort_values("revenue", ascending=False)
        )

        fig = px.bar(
            product_revenue,
            x="product_name",
            y="revenue",
            title="Product-wise Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        product_units = (
            df.groupby("product_name")["units_sold"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            product_units,
            x="product_name",
            y="units_sold",
            title="Product-wise Units Sold"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# Time-Series Analysis
with tab3:

    time_data = df.dropna(subset=["sale_date"]).copy()

    if not time_data.empty:

        daily_revenue = (
            time_data.groupby("sale_date")["revenue"]
            .sum()
            .reset_index()
            .sort_values("sale_date")
        )

        fig = px.line(
            daily_revenue,
            x="sale_date",
            y="revenue",
            markers=True,
            title="Business Revenue Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "A valid date column is required for time-series visualization."
        )


# ============================================================
# 7. REVENUE PREDICTION ENGINE
# ============================================================

st.header("🔮 Business Revenue Prediction")

forecast_days = st.slider(
    "Select future prediction period (days)",
    min_value=1,
    max_value=30,
    value=7
)


def predict_revenue(data, days):

    valid_data = data.dropna(
        subset=["sale_date", "revenue"]
    ).copy()

    daily = (
        valid_data.groupby("sale_date")["revenue"]
        .sum()
        .reset_index()
        .sort_values("sale_date")
    )

    if len(daily) < 2:
        raise ValueError(
            "At least two distinct dates are required for forecasting."
        )

    # Convert dates into sequential numeric values
    x = np.arange(len(daily))
    y = daily["revenue"].values

    # Linear regression using NumPy
    slope, intercept = np.polyfit(x, y, 1)

    future_x = np.arange(
        len(daily),
        len(daily) + days
    )

    predicted = slope * future_x + intercept

    # Revenue cannot be negative
    predicted = np.maximum(predicted, 0)

    future_dates = pd.date_range(
        start=daily["sale_date"].max() + pd.Timedelta(days=1),
        periods=days,
        freq="D"
    )

    forecast_df = pd.DataFrame({
        "sale_date": future_dates,
        "predicted_revenue": predicted
    })

    return forecast_df


if st.button("Generate Revenue Prediction"):

    try:

        forecast_df = predict_revenue(
            df,
            forecast_days
        )

        st.session_state["forecast_data"] = forecast_df

        st.success("Revenue prediction generated!")

    except Exception as e:

        st.error(str(e))


if "forecast_data" in st.session_state:

    forecast_df = st.session_state["forecast_data"]

    fig = px.line(
        forecast_df,
        x="sale_date",
        y="predicted_revenue",
        markers=True,
        title="Predicted Future Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        forecast_df,
        use_container_width=True
    )

    st.metric(
        "Expected Revenue",
        f"{forecast_df['predicted_revenue'].sum():,.2f}"
    )


# ============================================================
# 8. SAFE AI ANALYTICAL EXECUTION ENGINE
# ============================================================

def execute_analysis(data, plan):

    action = plan.get("action", "aggregate")

    metric = plan.get("metric", "revenue")

    operation = plan.get("operation", "sum")

    group_by = plan.get("group_by")

    filters = plan.get("filters", {})

    # Only predefined columns are allowed
    allowed_metrics = [
        "revenue",
        "units_sold"
    ]

    allowed_groups = [
        "product_name",
        "category"
    ]

    allowed_operations = [
        "sum",
        "mean",
        "min",
        "max",
        "count"
    ]

    if action == "summary":

        return {
            "Total Revenue": float(data["revenue"].sum()),
            "Total Units Sold": float(data["units_sold"].sum()),
            "Average Revenue": float(data["revenue"].mean()),
            "Transactions": int(len(data))
        }

    if action == "forecast":

        days = int(plan.get("horizon", 7))

        if not 1 <= days <= 90:
            raise ValueError("Forecast horizon must be between 1 and 90 days.")

        return predict_revenue(data, days)

    if action != "aggregate":
        raise ValueError("Unsupported analytical action.")

    if metric not in allowed_metrics:
        raise ValueError("Unsupported metric requested.")

    if operation not in allowed_operations:
        raise ValueError("Unsupported aggregation operation.")

    result_data = data.copy()

    # Validate and apply filters
    if not isinstance(filters, dict):
        raise ValueError("Invalid filter format.")

    allowed_filters = [
        "category",
        "product_name"
    ]

    for column, value in filters.items():

        if column not in allowed_filters:
            raise ValueError("Unsupported filter column.")

        if not isinstance(value, str):
            raise ValueError("Invalid filter value.")

        result_data = result_data[
            result_data[column].astype(str).str.lower()
            == value.lower()
        ]

    if result_data.empty:
        return "No matching business records found."

    if group_by:

        if group_by not in allowed_groups:
            raise ValueError("Unsupported grouping column.")

        if operation == "count":

            result = (
                result_data.groupby(group_by)
                .size()
                .reset_index(name="count")
            )

        else:

            result = (
                result_data.groupby(group_by)[metric]
                .agg(operation)
                .reset_index()
            )

        return result

    if operation == "count":

        return int(len(result_data))

    return float(
        getattr(result_data[metric], operation)()
    )


# ============================================================
# 9. GROQ AI CHATBOT
# ============================================================

st.header("🤖 AI Business Intelligence Assistant")

st.write(
    "Ask questions about your business revenue, products, "
    "categories, calculations and future predictions."
)

if "chat_history" not in st.session_state:

    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hello! I can analyze your uploaded business dataset. "
                "Ask me about revenue, product performance, KPIs "
                "or future revenue predictions."
            )
        }
    ]


# Display chat history
for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


user_question = st.chat_input(
    "Ask your business analytics question..."
)


if user_question:

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):

        if llm is None:

            answer = "Groq is unavailable. Configure your GROQ_API_KEY to enable the chatbot."

        else:

            with st.spinner("Analyzing business data..."):

                try:

                    system_prompt = f"""
You are an AI Business Intelligence analyst.

Your task is to convert a user's business analytics question
into a JSON analytical plan.

Available dataframe columns:
{list(df.columns)}

Allowed actions:
1. aggregate
2. summary
3. forecast

Allowed metrics:
- revenue
- units_sold

Allowed operations:
- sum
- mean
- min
- max
- count

Allowed group_by:
- product_name
- category
- null

Allowed filters:
- category
- product_name

JSON format:

{{
  "action": "aggregate",
  "metric": "revenue",
  "operation": "sum",
  "group_by": "category",
  "filters": {{}},
  "horizon": 7,
  "explanation": "Explain the intended calculation"
}}

Rules:

- Return ONLY valid JSON.
- Never generate Python code.
- Never generate SQL.
- Never invent business values.
- Use summary for overall KPI questions.
- Use forecast for future revenue prediction questions.
- Use aggregate for calculations and grouping.
- Use only the allowed columns, metrics and operations.
- For forecast, specify the requested number of days.
- If the user does not specify a period, use 7 days.
- Do not claim that a forecast is an actual result.
"""

                    response = llm.invoke([
                        ("system", system_prompt),
                        ("human", user_question)
                    ])

                    response_text = response.content

                    if isinstance(response_text, list):
                        response_text = "".join(
                            str(part.get("text", ""))
                            if isinstance(part, dict)
                            else str(part)
                            for part in response_text
                        )

                    # Parse structured JSON
                    response_text = response_text.strip()

                    if response_text.startswith("```"):
                        response_text = (
                            response_text
                            .removeprefix("```json")
                            .removeprefix("```")
                            .removesuffix("```")
                            .strip()
                        )

                    plan = json.loads(response_text)

                    # Execute only validated predefined operations
                    result = execute_analysis(
                        df,
                        plan
                    )

                    explanation = plan.get(
                        "explanation",
                        "Analysis completed using the uploaded business data."
                    )

                    answer = f"**Business Insight:** {explanation}\n\n"

                    if isinstance(result, pd.DataFrame):

                        answer += "**Calculated Business Result:**\n\n"

                        answer += result.to_markdown(index=False)

                    elif isinstance(result, dict):

                        answer += "**Business KPI Summary:**\n\n"

                        for key, value in result.items():

                            answer += (
                                f"- **{key}:** "
                                f"{value:,.2f}"
                                if isinstance(value, float)
                                else f"- **{key}:** {value:,}"
                            )

                            answer += "\n"

                    elif isinstance(result, (int, float)):

                        answer += (
                            f"**Calculated Value:** "
                            f"{result:,.2f}\n"
                        )

                    else:

                        answer += str(result)

                    answer += (
                        "\n\n*The result is calculated from "
                        "your currently uploaded dataset.*"
                    )

                except Exception as e:

                    answer = (
                        "I could not complete that analysis. "
                        f"Please check your question or dataset. "
                        f"Details: {str(e)}"
                    )

        st.markdown(answer)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })


# ============================================================
# 10. POWER BI DATA EXPORT
# ============================================================

st.header("📥 Power BI Data Export")

st.write(
    "Download the cleaned business dataset and import it into "
    "Microsoft Power BI Desktop to create a native Power BI report."
)

col1, col2 = st.columns(2)

with col1:

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Cleaned CSV",
        data=csv_data,
        file_name="business_analytics_data.csv",
        mime="text/csv"
    )

with col2:

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Business_Data",
            index=False
        )

        if "forecast_data" in st.session_state:

            st.session_state["forecast_data"].to_excel(
                writer,
                sheet_name="Revenue_Forecast",
                index=False
            )

    st.download_button(
        label="Download Excel Workbook",
        data=excel_buffer.getvalue(),
        file_name="business_analytics_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


st.divider()

st.caption(
    "AI Business Intelligence Platform | "
    "Streamlit + Pandas + Plotly + Groq + NumPy"
)
