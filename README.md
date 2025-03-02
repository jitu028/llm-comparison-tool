
# **LLM Comparison Tool 🚀**  
*A Streamlit-based benchmarking dashboard for comparing LLMs like OpenAI GPT, Google Gemini, Cohere, and Anthropic Claude.*

![LLM Benchmarking](https://raw.githubusercontent.com/jitu028/llm-comparison-tool/main/assets/banner.png) 

---

## **📌 Overview**  
The **LLM Comparison Tool** allows users to **benchmark, analyze, and compare** various Large Language Models (LLMs) across **latency, accuracy, and cost per 1K tokens**.  

### **🎯 Key Features**  
✅ Compare multiple LLMs from **OpenAI, Google Gemini, Cohere, and Anthropic**  
✅ **Interactive UI** using **Streamlit** for seamless benchmarking  
✅ **Performance Metrics:** Latency, cost, and accuracy visualization  
✅ **User Feedback Collection** & Cloud Storage Logging  
✅ **Fully Deployable on Cloud Run**  

---

## **🛠️ Tech Stack**  
- **Frontend:** [Streamlit](https://streamlit.io/)  
- **Backend:** Python (Flask API on Google Cloud Run)  
- **Cloud Services:** Google Cloud Storage (GCS), Cloud Run  
- **ML Models:** OpenAI GPT, Google Gemini, Cohere, Anthropic Claude  

---

## **📦 Installation & Setup**  

### **🔹 1. Clone the Repository**
```bash
git clone https://github.com/jitu028/llm-comparison-tool.git
cd llm-comparison-tool
```

### **🔹 2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **🔹 3. Run Locally**
```bash
streamlit run rag_benchmark_dashboard.py
```

---

## **🚀 Deployment to Google Cloud Run**
You can deploy both **frontend (Streamlit UI)** and **backend (Flask API)** to **Cloud Run**.

### **🔹 1. Build and Push Docker Images**
#### **Backend**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/rag-benchmark-backend
gcloud run deploy rag-benchmark-backend \
    --image gcr.io/YOUR_PROJECT_ID/rag-benchmark-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

#### **Frontend**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/rag-benchmark-dashboard
gcloud run deploy rag-benchmark-dashboard \
    --image gcr.io/YOUR_PROJECT_ID/rag-benchmark-dashboard \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

Replace **`YOUR_PROJECT_ID`** with your GCP project.

---

## **🌐 API Endpoints**
| Endpoint              | Method | Description |
|----------------------|--------|-------------|
| `/benchmark`         | POST   | Run a benchmark for a model |
| `/update-feedback`   | POST   | Update user feedback |
| `/past-results`      | GET    | Retrieve past benchmark results |

Example **cURL request**:
```bash
curl -X POST "https://YOUR_BACKEND_URL/benchmark" \
     -H "Content-Type: application/json" \
     -d '{"model_name": "gemini-1.5-pro-001", "prompt": "What is Generative AI?"}'
```

---

## **📊 Dashboard Features**
### **🔹 LLM Benchmarking**
- Compare multiple models side-by-side  
- Measure **latency, accuracy, and cost per 1K tokens**  
- Interactive **bar & box plots**  

### **🔹 User Feedback**
- **Rate model responses (1-5)**  
- Store & update feedback in **Google Cloud Storage**  

### **🔹 Past Benchmark Results**
- View **previous benchmarking data**  
- Sort & filter by **model type, latency, and cost**  

---

## **📜 Roadmap**
- [ ] **Add More LLM Providers** (Meta Llama, Mistral)  
- [ ] **Live Model Cost Tracking**  
- [ ] **Auto-generated Model Insights**  
- [ ] **Multi-user login for personalized tracking**  

---

## **📩 Contributions**
Contributions are **welcome**! Feel free to **fork, submit PRs, or open issues**.

---

## **👤 Author**
**Jitendra Gupta** ([@jitu028](https://github.com/jitu028))  

---

## **📄 License**
This project is licensed under the **MIT License**.
