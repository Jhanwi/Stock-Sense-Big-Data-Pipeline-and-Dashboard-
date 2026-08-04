# 🚀 Stock Sense: Big Data Pipeline & Dashboard

> A high-performance, full-stack big data platform that ingests, processes, and visualizes massive historical financial datasets in near real-time. 

### 🚧 Project Status: Active Development
*This project is currently under active development. New features, pipeline optimizations, and dashboard updates are being pushed regularly.*

---

## 📌 Table of Contents
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#-tech-stack)
- [🏗️ System Architecture](#%EF%B8%8F-system-architecture)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
- [🗺️ Product Roadmap](#%EF%B8%8F-product-roadmap)
- [🔄 CI/CD & Deployment](#-cicd--deployment)
- [📬 Contact](#-contact)

---

## ✨ Key Features
- **High-Efficiency Ingestion**: Custom pipeline cutting data ingestion time from 4 hours to 45 minutes, delivering a **70% efficiency gain**.
- **Distributed Processing**: PySpark ETL workflows to clean, structure, and parse massive historical financial datasets.
- **Robust Storage**: Highly scalable data lake architecture leveraging AWS S3 for raw and processed financial feeds.
- **Modern Dashboard**: Responsive React frontend powered by a high-throughput FastAPI backend for real-time stock insights.
- **Automated Delivery**: Dockerized environments and GitHub Actions CI/CD workflows ensuring zero payload errors during deployment.

---

## 🛠️ Tech Stack

### Big Data & Cloud
- **Language**: Python
- **Processing Engine**: PySpark (Apache Spark)
- **Cloud Storage**: AWS S3

### Full-Stack Web App
- **Backend API**: FastAPI
- **Frontend UI**: React.js

### DevOps & Automation
- **Containerisation**: Docker
- **CI/CD Pipeline**: GitHub Actions

---

## 🏗️ System Architecture
1. **Data Ingestion**: Raw historical financial data is loaded into an AWS S3 data lake.
2. **ETL Pipeline**: Distributed PySpark jobs clean, transform, and aggregate the raw data.
3. **API Layer**: FastAPI queries the processed data and serves it via secure, optimized endpoints.
4. **UI Layer**: The React dashboard fetches the API data to render real-time financial charts and analytics.

---

## 🚀 Getting Started

*(Note: As this project is actively developing, setup steps are subject to change.)*

### Prerequisites
Ensure you have the following installed locally:
- Python 3.10+
- Node.js (v18+)
- Docker & Docker Compose
- Apache Spark (for local PySpark testing)
- AWS CLI (configured with access to your S3 buckets)

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd stock-sense
   ```

2. **Set up the Backend & Pipeline:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set up the Frontend:**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
   ```env
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   S3_BUCKET_NAME=your_bucket_name
   FASTAPI_PORT=8000
   ```

5. **Run the Application via Docker:**
   ```bash
   docker-compose up --build
   ```

---

## 🗺️ Product Roadmap

This project is actively evolving. Below is the development timeline mapping out completed achievements and current engineering priorities.

### 👥 Phase 1: Foundation & Ingestion (Completed)
- [x] Architected AWS S3 data lake topology for raw financial datasets.
- [x] Built the initial FastAPI core skeleton and React dashboard boilerplate.
- [x] Configured multi-stage Dockerfiles and initialized GitHub Actions workflows.

### ⚙️ Phase 2: Pipeline Optimization (Current Focus)
- [x] Engineered distributed PySpark ETL pipelines to optimize heavy historical data parses.
- [x] Slashed data ingestion processing bottlenecks from 4 hours down to 45 minutes.
- [/] **In Progress**: Implementing incremental data loading to append daily market close data without re-processing entire historical datasets.
- [/] **In Progress**: Writing comprehensive PySpark unit tests using `chispa` to validate transformations inside the CI/CD runner.

### 📊 Phase 3: Advanced Analytics & Dashboard UI (Up Next)
- [ ] Implement WebSockets in FastAPI to push streaming live ticker updates to the UI.
- [ ] Build interactive financial charting capabilities (Candlestick, Moving Averages) in React using Recharts or Chart.js.
- [ ] Integrate a lightweight caching layer (Redis) to accelerate recurrent API responses for common stock queries.
- [ ] Add customizable multi-stock watchlist functionality with user authentication.

---

## 🔄 CI/CD & Deployment
This project uses **GitHub Actions** to automate testing and deployment. Every push to the `main` branch triggers:
- Linter and code quality checks.
- Docker image compilation.
- Automated pipeline validation to guarantee **zero payload errors** before staging.

---

## 📬 Contact
- **Project Lead**: Jhanwi Kumari jhanwi352002@gmail.com
- **GitHub Repository**: [https://github.com/Jhanwi ](https://github.com)
