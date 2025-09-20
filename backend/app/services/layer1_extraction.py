"""
Layer 1 - Field Extraction Service
Simple Gemini API-based extraction using Google's Gemini 2.5 Flash model
"""
import os
import google.generativeai as genai
import json
import logging
from typing import Dict, Any, Optional
from PIL import Image
import io

from ..models import ExtractedFields, ExtractionMethod

logger = logging.getLogger(__name__)

class Layer1ExtractionService:
    """
    Layer 1: Simple Gemini API-based field extraction
    Uses Google's Gemini 2.5 Flash model for certificate data extraction
    """
    
    def __init__(self):
        # Configure Gemini API
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        
        logger.info("Layer1 extraction service initialized with Gemini API")
    
    async def extract_fields(self, image: Image.Image, use_fallback: bool = True) -> ExtractedFields:
        """
        Extract certificate fields using Gemini API
        """
        try:
            # Convert PIL image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            image_data = img_byte_arr.getvalue()
            
            # Create a PIL Image object from the image data
            pil_image = Image.open(io.BytesIO(image_data))
            
            # Define the extraction prompt
            prompt_text = """
            From this certificate image, extract the following information and return it as a JSON object:

            {
                "name": "full_name_of_student",
                "roll_no": "student_roll_number",
                "certificate_no": "certificate_identification_number",
                "course": "course_name",
                "institution": "institution_or_university_name",
                "month": "month_of_completion",
                "year": "year_of_completion",
                "grade": "final_grade_or_score"
            }

            Make sure the response is a single, valid JSON object and nothing else. Also in some cases certificate number is not present so in that case just return that as null.
            """
            
            # The prompt parts now correctly contain a string and the image object.
            prompt_parts = [prompt_text, pil_image]
            
            # Generate content using the Gemini model
            logger.info("Calling Gemini API for certificate extraction...")
            response = self.model.generate_content(prompt_parts)
            
            # Attempt to parse the JSON response
            json_start = response.text.find('{')
            json_end = response.text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_string = response.text[json_start:json_end]
                extracted_data = json.loads(json_string)
                
                # Convert to ExtractedFields
                result = ExtractedFields(
                    name=extracted_data.get('name', ''),
                    roll_no=extracted_data.get('roll_no', ''),
                    certificate_id=extracted_data.get('certificate_no'),
                    course_name=extracted_data.get('course', ''),
                    institution=extracted_data.get('institution', ''),
                    year=extracted_data.get('year', ''),
                    grade=extracted_data.get('grade', ''),
                    issue_date='',  # Not extracted by current prompt
                )
                
                # Set high confidence for Gemini results
                result.field_confidences = {
                    'name': 0.9,
                    'roll_no': 0.9,
                    'certificate_id': 0.9,
                    'course_name': 0.9,
                    'institution': 0.9,
                    'year': 0.8,
                    'grade': 0.8
                }
                
                result.extraction_method = ExtractionMethod.DONUT_PRIMARY  # Using existing enum
                
                logger.info("Certificate data extracted successfully using Gemini")
                return result
            else:
                logger.warning("No valid JSON found in Gemini response")
                return ExtractedFields()
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Gemini response: {str(e)}")
            logger.error(f"Raw response: {response.text}")
            return ExtractedFields()
        except Exception as e:
            logger.error(f"Gemini extraction failed: {str(e)}")
            return ExtractedFields()
    
    async def extract_fields_from_pdf(self, pdf_contents: bytes) -> ExtractedFields:
        """
        Extract certificate fields from PDF using Gemini API
        """
        try:
            # Define the extraction prompt for PDF
            prompt_text = """
            From this PDF certificate document, extract the following information and return it as a JSON object:

            {
                "name": "full_name_of_student",
                "roll_no": "student_roll_number",
                "certificate_no": "certificate_identification_number",
                "course": "course_name",
                "institution": "institution_or_university_name",
                "month": "month_of_completion",
                "year": "year_of_completion",
                "grade": "final_grade_or_score"
            }

            Make sure the response is a single, valid JSON object and nothing else. Also in some cases certificate number is not present so in that case just return that as null.
            """
            
            # Generate content using the Gemini model with PDF content
            logger.info("Calling Gemini API for PDF certificate extraction...")
            response = self.model.generate_content([prompt_text, pdf_contents])
            
            # Attempt to parse the JSON response
            json_start = response.text.find('{')
            json_end = response.text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_string = response.text[json_start:json_end]
                extracted_data = json.loads(json_string)
                
                # Convert to ExtractedFields
                result = ExtractedFields(
                    name=extracted_data.get('name', ''),
                    roll_no=extracted_data.get('roll_no', ''),
                    certificate_id=extracted_data.get('certificate_no'),
                    course_name=extracted_data.get('course', ''),
                    institution=extracted_data.get('institution', ''),
                    year=extracted_data.get('year', ''),
                    grade=extracted_data.get('grade', ''),
                    issue_date='',  # Not extracted by current prompt
                )
                
                # Set high confidence for Gemini results
                result.field_confidences = {
                    'name': 0.9,
                    'roll_no': 0.9,
                    'certificate_id': 0.9,
                    'course_name': 0.9,
                    'institution': 0.9,
                    'year': 0.8,
                    'grade': 0.8
                }
                
                result.extraction_method = ExtractionMethod.DONUT_PRIMARY  # Using existing enum
                
                logger.info("PDF certificate data extracted successfully using Gemini")
                return result
            else:
                logger.warning("No valid JSON found in Gemini response for PDF")
                return ExtractedFields()
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Gemini PDF response: {str(e)}")
            logger.error(f"Raw response: {response.text}")
            return ExtractedFields()
        except Exception as e:
            logger.error(f"Gemini PDF extraction failed: {str(e)}")
            return ExtractedFields()