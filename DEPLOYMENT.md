# Vercel Deployment Guide

## Overview
Your Personal Finance Monte Carlo Simulator is now configured to deploy both the React frontend and Python FastAPI backend to Vercel as a full-stack application.

## Project Structure
```
foundation/
├── api/                    # Python backend (FastAPI)
│   ├── main.py            # API entry point
│   ├── monte_carlo.py     # Monte Carlo simulation logic
│   └── requirements.txt   # Python dependencies
├── src/                   # React frontend
├── vercel.json           # Vercel configuration
└── package.json          # Node.js dependencies
```

## Deployment Steps

### 1. Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

### 2. Deploy to Vercel
From the project root directory:
```bash
vercel
```

Follow the prompts:
- **Set up and deploy?** → Yes
- **Which scope?** → Your personal account or team
- **Link to existing project?** → No (first time) or Yes (subsequent deployments)
- **Project name** → foundation (or your preferred name)
- **Directory** → ./ (current directory)

### 3. Automatic Configuration
Vercel will automatically detect:
- ✅ React/Vite frontend
- ✅ Python FastAPI backend
- ✅ Build and routing configuration

## How It Works

### Frontend (React + Vite)
- Built as static files in `/dist`
- Served from the root path (`/`)
- Automatically detects production vs development for API calls

### Backend (Python FastAPI)
- Deployed as serverless functions
- Available at `/api/*` endpoints
- Automatically handles CORS for cross-origin requests

### API Routes
- `GET /api/` → API status message
- `POST /api/simulate` → Run Monte Carlo simulation
- `GET /api/health` → Health check

## Environment Detection
The frontend automatically switches between:
- **Development**: `http://localhost:8000/simulate`
- **Production**: `/api/simulate` (relative to your Vercel domain)

## Post-Deployment
After deployment, Vercel will provide:
1. **Production URL** → Your live application
2. **Preview URLs** → For each commit/branch
3. **Deployment dashboard** → Monitor and manage deployments

## Security Notes
- CORS is currently set to allow all origins (`*`) for initial deployment
- In production, update `api/main.py` to restrict CORS to your specific domain:
  ```python
  allow_origins=["https://your-domain.vercel.app"]
  ```

## Troubleshooting

### Build Issues
If the build fails, check:
- All dependencies are in `requirements.txt`
- No missing imports in Python files
- TypeScript compilation passes locally

### API Issues
If API calls fail:
- Check Vercel function logs in the dashboard
- Verify the API endpoint paths match the routing
- Ensure CORS settings allow your frontend domain

## Local Development
Continue developing locally with:
```bash
# Frontend
npm run dev

# Backend (in separate terminal)
cd api && uv run python start.py
```

The production deployment won't affect your local development workflow.