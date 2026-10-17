```markdown
# SOVA — AI Video Compliance Analyzer

AI-powered video analysis system for detecting potential compliance violations.

## How to Run

### Requirements
- Git
- Docker Desktop

### 1. Clone the repository

```bash
git clone https://github.com/nurlyybekovva/SOVA.git
cd SOVA
```

### 2. Set up environment

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 3. Run the project

Make sure Docker Desktop is running.

```bash
docker compose up -d --build
```

### 4. Open the application

- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### 5. Stop the project

```bash
docker compose down
```

### Useful commands

```bash
docker compose up -d          # Start
docker compose down           # Stop
docker compose logs -f        # View logs
docker compose ps             # Check status
docker compose up -d --build  # Rebuild
```

## Project Structure

```text
SOVA/
├── frontend/               # React + TypeScript UI
│   └── src/
│       ├── components/     # UI components
│       ├── services/       # API requests
│       └── types/          # TypeScript interfaces
│
├── backend/                # Python FastAPI server
│   └── app/
│       ├── api/            # API endpoints
│       ├── services/       # Video processing and compliance logic
│       ├── ml/             # Qwen and DINOv2 models
│       ├── main.py         # Backend entry point
│       ├── schemas.py      # Request/response schemas
│       └── jobs.py         # Background job management
│
├── data/
│   ├── raw/                # Original videos and datasets
│   └── processed/          # Processed datasets
│
├── rules/                  # Kazakhstan compliance rules (JSON)
├── models/                 # Downloaded ML model weights
├── scripts/                # Training and evaluation scripts
├── tests/                  # Automated tests
├── outputs/                # Analysis results and evidence
│
├── .env.example            # Environment configuration template
├── .gitignore              # Ignored files
├── docker-compose.yml      # Docker services
└── README.md
```

## Development

Create a separate branch for your work:

```bash
git checkout -b feature/your-feature
```

Commit and push:

```bash
git add .
git commit -m "Add feature"
git push -u origin feature/your-feature
```

Create a Pull Request to merge changes into `main`.

**Note:** Data files, model weights, and `.env` are excluded from Git. Obtain required datasets separately.
```