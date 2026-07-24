# PedagogyX - Autonomous Repository

![CI Status](https://img.shields.io/github/actions/workflow/status/owner/repo/test.yml?branch=main&label=CI)
![Auto-Docs](https://img.shields.io/badge/Docs-Auto--Generated-blue)

## Project Overview
This repository is continuously analyzed, documented, and visualized automatically.

## Technology Stack
- FastAPI
- React
- Next.js

## AI Generated Architecture Summary (Fallback)

This repository is built using **FastAPI, React, Next.js**.

### Core Services

- **worker-metrics**: Microservice part of the architecture.
- **web**: Microservice part of the architecture.
- **worker-asr**: Microservice part of the architecture.
- **api**: Microservice part of the architecture.
- **worker-cv**: Microservice part of the architecture.


## Repository Structure
- **[worker-metrics](services/worker-metrics)**
- **[web](services/web)**
- **[worker-asr](services/worker-asr)**
- **[api](services/api)**
- **[worker-cv](services/worker-cv)**

## Architecture Diagrams

### Services & Frameworks

```mermaid
graph TD
    subgraph Services
        worker_metrics["worker-metrics"]
        click worker_metrics href "services/worker-metrics" "Go to worker-metrics source"
        web["web"]
        click web href "services/web" "Go to web source"
        worker_asr["worker-asr"]
        click worker_asr href "services/worker-asr" "Go to worker-asr source"
        api["api"]
        click api href "services/api" "Go to api source"
        worker_cv["worker-cv"]
        click worker_cv href "services/worker-cv" "Go to worker-cv source"
    end

    subgraph Frameworks
        FastAPI(FastAPI)
        React(React)
        Next_js(Next.js)
    end

```


## Setup Instructions
1. Install dependencies via `pip install -r services/api/requirements.txt` or Node/NPM.
2. Run locally via Docker: `docker compose -f infra/compose.dev.yaml up --build`

## Environment Variables
The following environment variables are detected in the codebase:

## Contribution Guide
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

