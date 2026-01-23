# AI‑Powered Cloud Observability & FinOps on AWS EKS

This project demonstrates a **production‑style cloud observability platform** built on **AWS EKS**, enhanced with **AI‑driven log summarization and incident explanation**. It combines **Terraform‑based infrastructure**, **microservices**, **Grafana/Prometheus monitoring**, and **local + cloud LLMs** (LLaMA 3, OpenAI, Bedrock‑ready).

The goal is to bridge the gap between Cloud Resources usage and FinOps with granular monitoring and reduce **alert fatigue** and **mean time to understanding (MTTU)** by letting AI explain *what went wrong* in Kubernetes workloads

---

## High‑Level Architecture

* **AWS EKS** (managed Kubernetes)
* **Terraform** for infra provisioning
* **Microservices**: auth, order, payment
* **Docker + ECR** per service
* **Prometheus + Grafana** behind **ALB Ingress**
* **Fluent Bit + CloudWatch Logs**
* **AI Observability Service** (FastAPI)
* **LLM Providers**:

  * LLaMA 3 (local via Ollama)
  * OpenAI GPT (pluggable)
  * AWS Bedrock (future‑ready)

---

## Repository Structure

```
cloud-observability-finops/
│
├── ai-observability/          # AI log analysis service
│   ├── app/
│   │   ├── main.py            # FastAPI entrypoint
│   │   ├── services/
│   │   │   └── summarizer.py  # LLM selector + orchestration
│   │   ├── llm/
│   │   │   ├── base.py        # Abstract LLM interface
│   │   │   ├── llama.py       # LLaMA 3 client (Ollama)
│   │   │   └── openai.py      # OpenAI client
│   │   └── models/
│   ├── scripts/
│   │   └── log-feeder.py      # Fetch K8s logs → AI
│   ├── requirements.txt
│   └── Dockerfile
│
├── services/                  # Microservices
│   ├── auth-service/
│   ├── order-service/
│   └── payment-service/
│
├── observability/             # Prometheus, Grafana manifests
├── Kubernetes-files/          # App deployments & services
├── terraform/                 # EKS, nodegroups, IAM, ALB
└── README.md
```

---

## AI Observability – How It Works

1. **Logs are collected** from Kubernetes pods using `kubectl logs` (local) or Fluent Bit (cloud)
2. Logs are sent to a **FastAPI AI service**
3. The service selects an LLM via abstraction (`BaseLLM`)
4. The LLM:

   * Summarizes the incident
   * Explains root cause
   * Suggests next steps (SRE‑style)

Example output:

> "Order service pod is restarting due to failed liveness probes. This likely indicates application startup delays or memory pressure. Check container resource limits and health check thresholds."

---

## LLM Abstraction Design

```text
BaseLLM (abstract)
 ├── summarize(logs)
 └── explain_error(logs)

LlamaClient (Ollama)
OpenAIClient (API)
BedrockClient (planned)
```

This design allows **switching LLMs without changing application logic**.

---

## Local Setup (AI Service)

### 1. Start LLaMA 3 locally

```bash
brew install ollama
ollama serve
ollama run llama3
```

### 2. Setup Python environment

```bash
cd ai-observability
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run AI API

```bash
export LLM_PROVIDER=llama
uvicorn app.main:app --reload
```

### 4. Test API

```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"logs":"Order service pod is restarting due to liveness probe failure"}'
```

---

## Feeding Kubernetes Logs to AI

Use the **log-feeder script**:

```bash
python3 scripts/log-feeder.py
```

What it does:

* Finds pods for application services
* Fetches recent logs
* Sends logs to AI service
* Prints summarized incident

This can be:

* Scheduled (cronjob)
* Triggered by alerts
* Converted into a Kubernetes Job

---

## Observability Stack

* **Prometheus** – metrics collection
* **Grafana** – dashboards & alerts
* **ALB Ingress** – secure access (no port‑forwarding)
* **Separate ALB** for monitoring (best practice)

Grafana + Prometheus run independently from application ALB.

---

## FinOps & Cost Awareness

* Right‑sized node groups
* Avoided over‑provisioning
* Local LLM for zero inference cost
* Optional switch to Bedrock/OpenAI

---

## Security Considerations

* IAM least privilege
* Separate ALBs
* No public access to metrics endpoints
* Future: IRSA for AI + logging components

---

## What Makes This Project Different

✔ Real‑world Automated EKS setup
✔ AI used for **incident understanding**
✔ LLM‑agnostic design
✔ SRE‑focused outcomes

---

## Next Phases

* Convert it into GitOps model, CI/CD using GtiHb Actions and Argo CD
* Streaming logs → AI (near‑real‑time)
* Alert → AI explanation in Grafana
* Bedrock/Open AI integration
* Security hardening & threat modeling

---

## Author

**Piyush Panchal**
DevOps | SRE | Platform Engineering
AWS • Kubernetes • Observability • AI

---

⭐ If you find this useful, feel free to star the repo or reach out on LinkedIn.


