# 📄 ResumeForge-API | Resume-Maker

> Automated Resume & Portfolio Generator with Pydantic v2 Schema Validation, Jinja2 PDF Rendering Pipeline, and GenAI STAR Bullet Optimization.

---

## 📌 Project Overview

**ResumeForge-API** programmatically parses structured career data (JSON/YAML), validates schemas via Pydantic v2, applies dynamic Jinja2 ATS templating, and leverages an LLM microservice to optimize achievement bullet points based on target job descriptions using the **STAR (Situation, Task, Action, Result)** methodology.

---

## 🛠️ Tech Stack & Architecture

- **Language & Runtime:** Python 3.10+ AsyncIO
- **API Framework:** FastAPI (Async REST serving with Swagger UI)
- **Data Validation:** Pydantic v2 (Strict type enforcement)
- **Templating & PDF Engine:** Jinja2 + ATS HTML/CSS Compilation
- **AI Microservice:** Open-Source STAR Bullet Polisher & Keyword Alignment Engine
- **Containerization:** Docker & Docker Compose

---

## 🚀 Quick Start & Local Execution

### 1. Run UI Web Dashboard (Streamlit)
```bash
cd /Users/sai/Desktop/Chaitanya/projects/Resume-Maker
streamlit run app.py
```
App will open at: `http://localhost:8501`

### 2. Run FastAPI Microservice
```bash
uvicorn api_server:app --reload --port 8000
```
Swagger API Docs available at: `http://localhost:8000/docs`

---

## 💡 Interview Talking Points

### When asked about backend architecture:
> *"I structured ResumeForge-API using a clean separation of concerns: input data is strictly validated via Pydantic models, processed asynchronously through FastAPI, and rendered via a headless Jinja2-to-PDF pipeline. This ensures zero blocking on I/O-bound operations and guarantees schema integrity."*

### When asked about scalability:
> *"Because the core engine is containerized with Docker and exposes an async FastAPI interface, it can easily scale horizontally behind an AWS ALB or be deployed as a serverless AWS Lambda function triggered by event queues."*
