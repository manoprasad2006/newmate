# Branch1 - Hardcoded Configuration

This branch contains hardcoded environment variables for easy deployment without requiring .env file setup.

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv310
.\venv310\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🔧 Hardcoded Configuration

All environment variables are hardcoded in `backend/hardcoded_env.py`:

- **Supabase URL**: `https://kjoqiorgzdiinamsauzb.supabase.co`
- **Gemini API Key**: `AIzaSyApje8wDzq4SwS0yjDxhy4ss2wVeH3rjts`
- **Database**: Supabase PostgreSQL
- **Ports**: Backend (8000), Frontend (3000)

## ✨ Features

- ✅ **Multi-format Support**: PNG, JPG, PDF uploads
- ✅ **Gemini AI Extraction**: Extracts all certificate fields including institution name
- ✅ **Database Storage**: Stores extracted data in Supabase
- ✅ **Institution Extraction**: Now extracts institution/university names
- ✅ **No .env Required**: All configuration is hardcoded

## 📊 Extracted Fields

- Student Name
- Roll Number
- Certificate Number
- Course Name
- **Institution Name** (NEW!)
- Year
- Grade

## 🎯 API Endpoints

- `POST /api/upload` - Upload certificate (PNG/JPG/PDF)
- `GET /api/certificates` - Get all certificates
- `GET /api/certificates/{certificate_id}` - Get certificate by ID
- `GET /api/certificates/student/{student_name}` - Get certificates by student

## 🔄 How It Works

1. Upload certificate file (PNG/JPG/PDF)
2. Gemini AI extracts all fields including institution
3. Data is stored in Supabase database
4. Response includes all extracted information

## 🚨 Security Note

This branch contains hardcoded API keys for demonstration purposes. In production, use proper environment variable management.
