# AWS Bedrock DeepSeek-R1 RAG Chatbot

A cloud-native, Retrieval-Augmented Generation (RAG) chatbot built with Python, Streamlit, and **Amazon Bedrock**, featuring **DeepSeek-R1** as the core reasoning model and automated document indexing via **Amazon S3** and **Bedrock Knowledge Bases**.

---

## 🏗️ Architecture Overview

```
[ User Browser (Streamlit UI) ]
│ (HTTP / Port 8501)
▼
[ AWS EC2 Instance (Ubuntu / Python venv) ]
├──> 1. Amazon Bedrock Knowledge Base (Managed Vector Store via S3)
│         └── Retrieves context from: s3://deepseek-bedrocks/Rashmitha-Resume-SRE-1.pdf
│
└──> 2. Amazon Bedrock Runtime API (client.converse)
├── Model: DeepSeek-R1 (us.deepseek.r1-v1:0)
└── Guardrails: Safety filtering & content moderation
```

---

## 🚀 What I Built & Key Features

1. **Serverless GenAI Migration:** Architected a pipeline to transition third-party AI workloads onto fully managed cloud infrastructure using Amazon Bedrock.
2. **Retrieval-Augmented Generation (RAG):** Connected **Amazon S3** (`deepseek-bedrocks`) as the authoritative document repository containing source resumes/technical profiles. Configured **Amazon Bedrock Knowledge Bases** to automatically chunk, embed, and index documents for semantic retrieval.
3. **DeepSeek-R1 Integration:** Utilized **DeepSeek-R1 (`us.deepseek.r1-v1:0`)** hosted natively on Amazon Bedrock via the Bedrock Runtime API (`client.converse`) to handle deep reasoning tasks and eliminate hallucinations using verified retrieved context.
4. **Security & IAM Least Privilege:** Configured dedicated IAM roles (`Bedrockaccess`) attached with `AmazonBedrockFullAccess` policies, ensuring secure, credential-free SDK authentication from the EC2 hosting environment.
5. **Observability & SRE Monitoring:** Integrated **Amazon CloudWatch** dashboards (`Bedrock-Monitoring`) to track invocation metrics, input/output token usage, invocation latency, and client error rates in real-time.
6. **Interactive Web Interface:** Developed a stateful, low-latency UI using **Streamlit** (`app.py`) to manage session states and conversation histories seamlessly.

---

## 📂 Tech Stack
* **Cloud Platform:** AWS (EC2, S3, IAM, CloudWatch)
* **AI & ML Services:** Amazon Bedrock, Bedrock Knowledge Bases, DeepSeek-R1 (`us.deepseek.r1-v1:0`)
* **Languages & Frameworks:** Python, Streamlit, Boto3

---

## ⚙️ Local Setup & Deployment

1. **Clone the repository:**
 
 ```
   git clone [https://github.com/Rashmitha0705/aws-bedrock-deepseek-rag.git](https://github.com/Rashmitha0705/aws-bedrock-deepseek-rag.git)
   cd aws-bedrock-deepseek-rag
 ```

2. Set up a Python virtual environment:
 
```
 python3 -m venv venv
 source venv/bin/activate
 ```
 3. Install dependencies:

 ```
pip install streamlit boto3

```
4. Run the Streamlit application:

```
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
