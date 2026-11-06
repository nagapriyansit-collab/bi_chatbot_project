# AI-Powered Business Intelligence Dashboard with Predictive Analytics

## Project Overview

An interactive Business Intelligence (BI) application built using Python and Streamlit that helps businesses analyze sales data, monitor performance, and make data-driven decisions. It integrates a Groq-powered AI chatbot that allows users to ask business-related questions in natural language and receive analytical insights.

The application also provides interactive visualizations, key performance indicators (KPIs), and basic revenue forecasting.

## Key Features

- **Data Upload:** Upload business datasets in CSV and Excel formats.
- **Data Processing:** Clean, transform, and analyze business data using Pandas.
- **Interactive Dashboard:** Visualize sales trends, product performance, and category-wise revenue.
- **KPI Analysis:** Calculate total revenue, units sold, and other business metrics.
- **AI Chatbot:** Ask natural-language questions about business data using the Groq API.
- **Predictive Analytics:** Forecast future revenue using historical sales data.
- **Data Export:** Export processed datasets and forecasting results into CSV and Excel files.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data processing and analysis |
| NumPy | Numerical computations |
| Plotly | Interactive data visualization |
| Groq API | AI-powered chatbot |
| LangChain | LLM integration and prompt management |
| Excel / CSV | Business data storage and export |

## Project Structure

```text
Business_AI_Project/
│
├── app.py
├── requirements.txt
├── README.md
├── business_analytics_sample.xlsx
│
└── .streamlit/
    └── secrets.toml
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Business_AI_Project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Groq API Key

Create a `.streamlit` folder in the project directory and add a file named `secrets.toml`.

Add your Groq API key:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

Get an API key from: https://console.groq.com/keys

**Security:** Never upload your API key or `secrets.toml` file to GitHub.

Add the following to `.gitignore`:

```text
.streamlit/secrets.toml
.env
__pycache__/
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your web browser.

## Sample Business Dataset

The project includes a sample business dataset containing synthetic sales transactions with fields such as:

- Transaction ID
- Sale Date
- Product Name
- Category
- Units Sold
- Unit Price
- Discount Percentage
- Revenue
- Cost
- Profit
- Region
- Customer Segment
- Sales Channel

Users can also upload their own compatible CSV or Excel datasets.

## Example AI Chatbot Questions

- What is the total revenue generated?
- Which product has the highest revenue?
- Which region generates the highest profit?
- Compare sales performance across categories.
- What is the overall profit margin?
- Predict revenue for the next 30 days.
- Identify products with low profitability.
- Suggest business strategies based on sales performance.

## Future Enhancements

- Advanced machine learning-based forecasting.
- Automated anomaly detection.
- Customer segmentation and purchase behavior analysis.
- Power BI Service integration and report embedding.
- More advanced business recommendations.
- Real-time business data integration.

## Project Objective

To develop an AI-powered Business Intelligence solution that combines data analytics, interactive visualization, and natural-language interaction to simplify business reporting and support informed decision-making.

## Author

**Your Name**

