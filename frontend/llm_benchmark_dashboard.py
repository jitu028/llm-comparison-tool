import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

# Set page configuration
st.set_page_config(page_title="LLM Benchmarking Dashboard", layout="wide")

# Backend API URLs (Update these for Cloud Run)
BACKEND_URL = "https://rag-benchmark-lklkjunb6q-uc.a.run.app"
BENCHMARK_URL = f"{BACKEND_URL}/benchmark"
UPDATE_FEEDBACK_URL = f"{BACKEND_URL}/update-feedback"
PAST_RESULTS_URL = f"{BACKEND_URL}/past-results"

# Hardcoded available models
openai_models = ["gpt-4o", "gpt-4o-mini", "gpt-4.5-preview", "gpt-4-turbo", "gpt-3.5-turbo"]
gemini_models = ["gemini-2.0-flash-001", "gemini-2.0-flash-lite-preview-02-05", "gemini-2.0-pro-exp-02-05",
                 "gemini-2.0-flash-exp", "gemini-2.0-flash-thinking-exp-01-21", "gemini-1.5-flash-002",
                 "gemini-1.5-pro-002", "gemini-1.5-flash-001", "gemini-1.5-pro-001", "gemini-1.0-pro-002",
                 "gemini-1.0-pro-001", "gemini-1.0-pro-vision-001"]
cohere_models = ["command-r", "command-light", "command-xlarge", "command-medium"]
anthropic_models = ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku", "claude-2.1", "claude-2"]

all_models = openai_models + gemini_models + cohere_models + anthropic_models

# Streamlit UI
st.title("📊 LLM Benchmarking Dashboard")
st.subheader("Compare Performance Across OpenAI, Google Gemini, Cohere, and Anthropic Models")

# Load past results from Cloud Run backend
@st.cache_data(ttl=60)  # Cache for 1 minute to avoid excessive API calls
def load_past_results():
    response = requests.get(PAST_RESULTS_URL)
    if response.status_code == 200:
        return response.json()
    return []

past_results = load_past_results()

# Display existing results
if past_results:
    df_past = pd.DataFrame(past_results)
    st.subheader("📌 Past Benchmarking Results")
    st.dataframe(df_past)

    # Metrics visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Latency Distribution")
        fig_latency = px.box(df_past, x="model_name", y="latency_ms", title="Latency (ms) per Model")
        st.plotly_chart(fig_latency, use_container_width=True)
    
    with col2:
        st.subheader("📊 Cost per 1K Tokens")
        fig_cost = px.bar(df_past, x="model_name", y="cost_per_1k_tokens", title="Cost per 1K Tokens")
        st.plotly_chart(fig_cost, use_container_width=True)

# Show available models
with st.expander("🔍 View Available Models"):
    st.write("### **OpenAI Models**")
    st.write(openai_models)
    st.write("### **Google Gemini Models**")
    st.write(gemini_models)
    st.write("### **Cohere Models**")
    st.write(cohere_models)
    st.write("### **Anthropic Claude Models**")
    st.write(anthropic_models)

# User input for benchmarking
prompt_input = st.text_area("Enter Prompt:", "What is Generative AI?")
selected_models = st.multiselect("Select Models to Benchmark", all_models, default=["gpt-4o", "gemini-2.0-flash-001"])

# **Session state to store user feedback**
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# Run Benchmark Button
if st.button("🚀 Run Benchmark") and prompt_input and selected_models:
    benchmark_results = []

    with st.spinner("Running benchmark..."):
        for model in selected_models:
            start_time = time.time()
            try:
                response = requests.post(
                    BENCHMARK_URL,
                    json={"model_name": model, "prompt": prompt_input},
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )

                end_time = time.time()
                latency = round((end_time - start_time) * 1000, 2)

                if response.status_code == 200:
                    data = response.json()
                    benchmark_results.append({
                        "Model": data["model"],
                        "Prompt": prompt_input,
                        "Response": data["response"],
                        "Latency (ms)": latency,
                        "Accuracy Score": round(time.time() % 1, 2),  # Placeholder for accuracy
                        "Cost per 1K Tokens": round(latency * 0.0001, 4),  # Placeholder for cost
                        "User Feedback": 3  # Default rating
                    })
                    st.session_state.feedback[data["model"]] = 3  # Initialize slider
                else:
                    benchmark_results.append({
                        "Model": model,
                        "Prompt": prompt_input,
                        "Response": f"Error: {response.text}",
                        "Latency (ms)": latency,
                        "Accuracy Score": 0,
                        "Cost per 1K Tokens": 0,
                        "User Feedback": 0
                    })
                    st.session_state.feedback[model] = 0

            except Exception as e:
                benchmark_results.append({
                    "Model": model,
                    "Prompt": prompt_input,
                    "Response": f"Exception: {str(e)}",
                    "Latency (ms)": "N/A",
                    "Accuracy Score": 0,
                    "Cost per 1K Tokens": 0,
                    "User Feedback": 0
                })
                st.session_state.feedback[model] = 0

    df = pd.DataFrame(benchmark_results)
    st.subheader("📌 Benchmarking Results")
    st.dataframe(df)

    # **Store results in session state for user feedback**
    st.session_state.benchmark_results = df

# Collect user feedback (Without refreshing the page)
if "benchmark_results" in st.session_state:
    df = st.session_state.benchmark_results

    st.subheader("🔄 Update User Feedback")
    feedback_updates = []

    for index, row in df.iterrows():
        feedback = st.slider(f"Rate {row['Model']}", 1, 5, int(st.session_state.feedback[row["Model"]]), key=row["Model"])
        st.session_state.feedback[row["Model"]] = feedback
        feedback_updates.append({"model_name": row["Model"], "prompt": row["Prompt"], "user_feedback": feedback})

    if st.button("✅ Submit Feedback for All Models"):
        response = requests.post(UPDATE_FEEDBACK_URL, json=feedback_updates, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            st.success("✅ Feedback updated for all selected models!")
        else:
            st.error("❌ Failed to update feedback!")

