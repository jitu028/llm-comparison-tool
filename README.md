
---

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

## **🛠️ Project Structure**  
```bash
llm-comparison-tool/
│── backend/                # Backend API
│   ├── .gcloudignore
│   ├── Dockerfile
│   ├── llm_benchmark_api.py   # Backend API script
│   ├── requirements.txt
│
│── frontend/               # Streamlit Dashboard UI
│   ├── Dockerfile
│   ├── llm_benchmark_dashboard.py  # UI script
│   ├── requirements.txt
│
│── scripts/                # Deployment Scripts
│   ├── deploy_llm_comparison_api.sh
│   ├── deploy_llm_comparison_dashboard.sh
│
│── README.md
```

---

## **📦 Installation & Setup**  

### **🔹 1. Clone the Repository**
```bash
git clone https://github.com/jitu028/llm-comparison-tool.git
cd llm-comparison-tool
```

### **🔹 2. Install Dependencies**
#### Backend API:
```bash
cd backend
pip install -r requirements.txt
```
#### Frontend Dashboard:
```bash
cd frontend
pip install -r requirements.txt
```

### **🔹 3. Run Locally**
#### Run Backend API:
```bash
cd backend
python llm_benchmark_api.py
```
#### Run Frontend Dashboard:
```bash
cd frontend
streamlit run llm_benchmark_dashboard.py
```

---

## **🚀 Deployment to Google Cloud Run**
You can deploy both **frontend (Streamlit UI)** and **backend (Flask API)** to **Cloud Run**.

### **🔹 1. Deploy Backend API**
Run the following deployment script:
```bash
./scripts/deploy_llm_comparison_api.sh
```
This will:
- Build & push the backend API Docker image
- Deploy it to **Google Cloud Run**

### **🔹 2. Deploy Frontend Dashboard**
Run the following deployment script:
```bash
./scripts/deploy_llm_comparison_dashboard.sh
```
This will:
- Build & push the frontend Streamlit UI Docker image
- Deploy it to **Google Cloud Run**

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

---
