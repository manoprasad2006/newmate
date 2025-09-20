# What Does This Repository Do?

## Quick Overview

This repository contains a **Certificate Verifier** - a complete system that uses artificial intelligence to verify academic certificates and credentials.

## How It Works

```
📤 Upload Certificate Image → 🤖 AI Analysis → ✅ Verification → 🔐 Digital Proof
```

### 1. Upload & Extract
- Users upload images of their certificates (diplomas, transcripts, etc.)
- AI automatically reads and extracts key information like:
  - Student name
  - Institution name  
  - Course/degree
  - Issue date
  - Certificate ID

### 2. Verify & Validate
- Checks extracted data against institution databases
- Calculates risk scores to detect potential fraud
- Flags suspicious certificates for human review

### 3. Generate Proof
- Creates cryptographic signatures for verified certificates
- Generates QR codes for instant verification
- Produces tamper-proof digital attestations

## What's Included

- **🖥️ Web Application**: React frontend for uploading and managing certificates
- **⚙️ API Backend**: FastAPI server handling AI processing and verification
- **🤖 AI Engine**: Integration with Donut model for document understanding
- **🔒 Security**: Cryptographic signing and attestation system
- **📊 Dashboard**: Analytics and monitoring tools
- **👥 Review System**: Manual review interface for edge cases

## Who Would Use This?

- **🏫 Universities**: Verify and issue digital credentials
- **💼 Employers**: Validate job candidate qualifications  
- **🎓 Students**: Get digitally-verified proof of their degrees
- **🏛️ Government**: Immigration, licensing, and credential services
- **🔍 Verification Services**: Third-party credential checking companies

## Technology Stack

- **Frontend**: React + Tailwind CSS
- **Backend**: Python + FastAPI
- **AI/ML**: PyTorch + Transformers (Donut model)
- **Database**: Supabase (PostgreSQL)
- **Security**: ECDSA signatures + QR codes
- **Deployment**: Docker + Docker Compose

---

**In Simple Terms**: Upload a certificate image → AI reads it → System verifies it's real → Get a digital proof with QR code that anyone can scan to confirm authenticity.