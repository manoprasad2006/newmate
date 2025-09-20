"""
FastAPI entrypoint with API routes for certificate verification
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from .config import settings
from .models import CertificateResponse, VerificationRequest
# from .services.supabase_client import SupabaseClient
# from .services.fusion_engine import EnhancedFusionEngine
# from .services.certificate_issuance import CertificateIssuanceService
# from .services.public_verification import PublicVerificationService
from .utils.helpers import setup_logging, process_image
from .services.layer1_extraction import Layer1ExtractionService
from .services.database_service import DatabaseService
from dotenv import load_dotenv
import os
import hashlib

# Load environment variables - try .env first, then fallback to hardcoded
try:
    load_dotenv('.env')
    print("✅ Loaded environment variables from .env file")
except:
    print("⚠️ .env file not found, using hardcoded environment variables")
    import hardcoded_env

# Setup logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="Certificate Verifier API",
    description="AI-powered certificate verification system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
# supabase_client = SupabaseClient()
# fusion_engine = EnhancedFusionEngine(supabase_client)
# issuance_service = CertificateIssuanceService(supabase_client)
# public_verification_service = PublicVerificationService(supabase_client)

# Initialize services
gemini_extractor = Layer1ExtractionService()
database_service = DatabaseService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Certificate Verifier API is running"}

@app.post("/api/upload")
async def upload_certificate_gemini(file: UploadFile = File(...)):
    """Upload PNG/JPEG/PDF certificate and extract details using Gemini AI"""
    try:
        # Check file type - accept images and PDFs
        allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'application/pdf']
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type not supported. Please upload PNG, JPG, or PDF files. Received: {file.content_type}"
            )
        
        # Read the uploaded file
        contents = await file.read()
        
        # Generate file hash for tracking
        file_hash = hashlib.sha256(contents).hexdigest()
        
        # Handle different file types
        from PIL import Image
        import io
        
        if file.content_type == 'application/pdf':
            # For PDF files, we'll need to convert to image first
            # For now, we'll pass the PDF directly to Gemini (it can handle PDFs)
            # You might want to add PDF to image conversion here if needed
            image = None  # Gemini can handle PDF directly
        else:
            # For image files, convert to PIL Image
            image = Image.open(io.BytesIO(contents))
        
        # Extract details using Gemini
        if file.content_type == 'application/pdf':
            # For PDF files, pass the file contents directly to Gemini
            extracted_data = await gemini_extractor.extract_fields_from_pdf(contents)
        else:
            # For image files, use the PIL image
            extracted_data = await gemini_extractor.extract_fields(image)
        
        # Save to database
        record_id = await database_service.save_certificate_data(extracted_data, file_hash)
        
        # Prepare response data
        response_data = {
            "student_name": extracted_data.name,
            "roll_number": extracted_data.roll_no,
            "certificate_number": extracted_data.certificate_id,
            "course_name": extracted_data.course_name,
            "year": extracted_data.year,
            "grade": extracted_data.grade,
            "institution": extracted_data.institution,
            "issue_date": extracted_data.issue_date,
            "extraction_method": extracted_data.extraction_method.value,
            "field_confidences": extracted_data.field_confidences,
            "database_id": record_id,
            "file_hash": file_hash,
            "file_type": file.content_type
        }
        
        # Return the extracted data
        return {
            "success": True,
            "message": "Certificate details extracted and saved successfully",
            "data": response_data
        }
        
    except Exception as e:
        logger.error(f"Error processing certificate with Gemini: {str(e)}")
        return {
            "success": False,
            "message": f"Error processing certificate: {str(e)}",
            "data": None
        }

@app.get("/api/certificates")
async def get_all_certificates(limit: int = 100):
    """Get all stored certificates"""
    try:
        certificates = await database_service.get_all_certificates(limit)
        return {
            "success": True,
            "data": certificates,
            "count": len(certificates)
        }
    except Exception as e:
        logger.error(f"Error retrieving certificates: {str(e)}")
        return {
            "success": False,
            "message": f"Error retrieving certificates: {str(e)}",
            "data": []
        }

@app.get("/api/certificates/{certificate_id}")
async def get_certificate_by_id(certificate_id: str):
    """Get certificate by certificate ID"""
    try:
        certificate = await database_service.get_certificate_by_id(certificate_id)
        if certificate:
            return {
                "success": True,
                "data": certificate
            }
        else:
            return {
                "success": False,
                "message": "Certificate not found",
                "data": None
            }
    except Exception as e:
        logger.error(f"Error retrieving certificate: {str(e)}")
        return {
            "success": False,
            "message": f"Error retrieving certificate: {str(e)}",
            "data": None
        }

@app.get("/api/certificates/student/{student_name}")
async def get_certificates_by_student(student_name: str):
    """Get all certificates for a specific student"""
    try:
        certificates = await database_service.get_certificates_by_student(student_name)
        return {
            "success": True,
            "data": certificates,
            "count": len(certificates)
        }
    except Exception as e:
        logger.error(f"Error retrieving student certificates: {str(e)}")
        return {
            "success": False,
            "message": f"Error retrieving student certificates: {str(e)}",
            "data": []
        }

@app.post("/upload", response_model=CertificateResponse)
async def upload_certificate(file: UploadFile = File(...)):
    """Upload and process certificate image"""
    try:
        # Process the uploaded image
        image_data = await process_image(file)
        
        # Run through fusion engine for verification
        result = await fusion_engine.verify_certificate(image_data)
        
        return result
    except Exception as e:
        logger.error(f"Error processing certificate: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify", response_model=CertificateResponse)
async def verify_certificate(request: VerificationRequest):
    """Verify certificate using manual input or image URL"""
    try:
        result = await fusion_engine.verify_certificate_by_data(request)
        return result
    except Exception as e:
        logger.error(f"Error verifying certificate: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/certificates/{certificate_id}")
async def get_certificate(certificate_id: str):
    """Get certificate details by ID"""
    try:
        result = await supabase_client.get_certificate(certificate_id)
        if not result:
            raise HTTPException(status_code=404, detail="Certificate not found")
        return result
    except Exception as e:
        logger.error(f"Error retrieving certificate: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================
# UNIVERSITY CERTIFICATE ISSUANCE ENDPOINTS
# =============================================

@app.post("/issue/certificate")
async def issue_certificate(certificate_data: dict, institution_id: str = "default"):
    """Issue a new certificate with QR code (University workflow)"""
    try:
        result = await issuance_service.issue_certificate(certificate_data, institution_id)
        return result
    except Exception as e:
        logger.error(f"Certificate issuance failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/issue/bulk")
async def bulk_issue_certificates(certificates_data: dict, institution_id: str = "default"):
    """Bulk issue certificates from CSV/ERP data"""
    try:
        certificates_list = certificates_data.get("certificates", [])
        if not certificates_list:
            raise HTTPException(status_code=400, detail="No certificates data provided")
        
        result = await issuance_service.bulk_issue_certificates(certificates_list, institution_id)
        return result
    except Exception as e:
        logger.error(f"Bulk certificate issuance failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================
# PUBLIC VERIFICATION ENDPOINTS (QR SCANNING)
# =============================================

@app.get("/verify/{attestation_id}")
async def verify_certificate_public(attestation_id: str):
    """Public certificate verification endpoint (Employer workflow)"""
    try:
        result = await public_verification_service.verify_by_attestation_id(attestation_id)
        return result
    except Exception as e:
        logger.error(f"Public verification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify/qr")
async def verify_by_qr_data(qr_data: dict):
    """Verify certificate by QR code data"""
    try:
        qr_content = qr_data.get("qr_content")
        if not qr_content:
            raise HTTPException(status_code=400, detail="QR content is required")
        
        result = await public_verification_service.verify_by_qr_data(qr_content)
        return result
    except Exception as e:
        logger.error(f"QR verification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/verify/{attestation_id}/image")
async def get_verified_certificate_image(attestation_id: str):
    """Get verified certificate image for display"""
    try:
        result = await public_verification_service.get_certificate_image(attestation_id)
        if not result:
            raise HTTPException(status_code=404, detail="Certificate image not found")
        return result
    except Exception as e:
        logger.error(f"Failed to get certificate image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================
# INSTITUTION MANAGEMENT ENDPOINTS
# =============================================

@app.post("/institutions/register")
async def register_institution(institution_data: dict):
    """Register a new institution"""
    try:
        institution_id = await supabase_client.store_institution(institution_data)
        return {"institution_id": institution_id, "status": "registered"}
    except Exception as e:
        logger.error(f"Institution registration failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/institutions/{institution_id}/certificates/import")
async def import_certificates(institution_id: str, certificates_data: dict):
    """Import certificates for an institution"""
    try:
        certificates_list = certificates_data.get("certificates", [])
        if not certificates_list:
            raise HTTPException(status_code=400, detail="No certificates data provided")
        
        imported_count = await supabase_client.import_certificates_batch(certificates_list)
        return {"imported_count": imported_count, "status": "success"}
    except Exception as e:
        logger.error(f"Certificate import failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================
# ANALYTICS AND REPORTING ENDPOINTS
# =============================================

@app.get("/analytics/verification-stats")
async def get_verification_statistics(institution_id: Optional[str] = None):
    """Get verification statistics"""
    try:
        stats = await public_verification_service.get_verification_statistics(institution_id)
        return stats
    except Exception as e:
        logger.error(f"Failed to get verification statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
