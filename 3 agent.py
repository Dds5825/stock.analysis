import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create agents
web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True
)

agent_team = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True
)

# Streamlit app
st.markdown("<h1 style='text-align: center; color: blue;'>Stock Analysis Tool</h1>", unsafe_allow_html=True)

# Form for user input
with st.form("stock_form"):
    ticker_symbol = st.text_input("Enter Ticker Symbol (e.g., NVDA):")
    submit_button = st.form_submit_button(label="Analyze", help="Get stock analysis")

# Process input and display response
if submit_button:
    with st.spinner("Fetching stock data and news..."):
        try:
            response = agent_team.print_response(
                f"Summarize analyst recommendations and share the latest news for {ticker_symbol}",
                stream=False  # Set stream to False to avoid LiveError
            )
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")