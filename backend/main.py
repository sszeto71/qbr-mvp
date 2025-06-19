# backend/main.py
import csv
import json
import logging
import os
from typing import List

import google.generativeai as genai
import PyPDF2
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile, responses, Request
from fastapi.middleware.cors import CORSMiddleware

from prompt_generator import create_qbr_prompt
from pdf_generator import generate_qbr_pdf, create_pdf_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Replace with your actual Gemini API key
# Load .env file from the backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if GOOGLE_API_KEY is set
if GOOGLE_API_KEY:
    logger.info("GOOGLE_API_KEY is set")
else:
    logger.warning("GOOGLE_API_KEY is not set")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        logger.debug(f"Extracting text from PDF: {pdf_file.filename}")
        pdf_reader = PyPDF2.PdfReader(pdf_file.file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        logger.debug(f"Extracted text from PDF: {text}")
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
    logger.debug(f"Extracted text: {text}")
    return text


def extract_data_from_csv(csv_file):
    data = []
    try:
        logger.debug(f"Extracting data from CSV: {csv_file.filename}")
        csv_reader = csv.DictReader(csv_file.file.read().decode('utf-8').splitlines())
        for row in csv_reader:
            data.append(row)
        logger.debug(f"Extracted data from CSV: {data}")
        logger.debug(f"Type of extracted data: {type(data)}")
    except Exception as e:
        logger.error(f"Error extracting data from CSV: {e}")
    logger.debug(f"Extracted data: {data}")
    return data


def calculate_revenue_and_aov(data):
    total_revenue = 0
    total_purchases = 0
    for row in data:
        try:
            revenue = float(row.get('Revenue', 0))
            purchases = int(row.get('Purchases', 0))
            total_revenue += revenue
            total_purchases += purchases
        except ValueError as e:
            logger.error(f"ValueError: {e}. Skipping row: {row}")
            continue  # Skip this row and move to the next one
        except TypeError as e:
            logger.error(f"TypeError: {e}. Skipping row: {row}")
            continue
    
    average_order_value = total_revenue / total_purchases if total_purchases else 0
    return total_revenue, total_purchases, average_order_value

def format_numbers_in_qbr(qbr_content_json):
    logger.info("Starting format_numbers_in_qbr")
    logger.info(f"Input type: {type(qbr_content_json)}")
    logger.info(f"Input preview: {str(qbr_content_json)[:200]}...")
    
    try:
        qbr_content = json.loads(qbr_content_json)
        logger.info(f"Successfully parsed JSON, structure: {list(qbr_content.keys()) if isinstance(qbr_content, dict) else 'Not a dict'}")
        
        # Format numbers in slide 2 (Key Metrics)
        if "slide2" in qbr_content and "content" in qbr_content["slide2"]:
            logger.info(f"Processing slide2 content with {len(qbr_content['slide2']['content'])} items")
            formatted_content = []
            for i, item in enumerate(qbr_content["slide2"]["content"]):
                logger.info(f"Processing slide2 item {i}: '{item}'")
                # Use regex to find and format numbers, handling both integers and floats
                import re
                
                def format_number(match):
                    number_str = match.group(0)
                    logger.info(f"format_number processing: '{number_str}'")
                    
                    # Skip if already formatted (contains commas)
                    if ',' in number_str:
                        logger.info(f"Skipping already formatted number: '{number_str}'")
                        return number_str
                    
                    if '.' in number_str:
                        # It's a float, format it with commas and keep the decimal part
                        parts = number_str.split('.')
                        try:
                            integer_part = int(parts[0])
                            formatted = f"{integer_part:,}.{parts[1]}"
                            logger.info(f"Formatted float '{number_str}' to '{formatted}'")
                            return formatted
                        except ValueError as e:
                            logger.error(f"Failed to format float '{number_str}': {e}")
                            return number_str
                    else:
                        # It's an integer, format it with commas
                        try:
                            formatted = f"{int(number_str):,}"
                            logger.info(f"Formatted integer '{number_str}' to '{formatted}'")
                            return formatted
                        except ValueError as e:
                            logger.error(f"Failed to format integer '{number_str}': {e}")
                            return number_str

                # Regex to find numbers (including those with commas and decimals)
                # This regex will find sequences of digits, optionally with commas, and optionally a decimal part.
                item = re.sub(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+', format_number, item)
                formatted_content.append(item)
            qbr_content["slide2"]["content"] = formatted_content

        return json.dumps(qbr_content)
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Error formatting numbers in QBR content: {e}")
        return qbr_content_json # Return original content if formatting fails

def generate_qbr_content(client_name, client_website, industry, extracted_data, total_revenue, total_purchases, average_order_value):
    # Create a summary of the data analysis for the prompt
    data_summary = f"""
Total Revenue: ${total_revenue:,.2f}
Total Purchases: {total_purchases:,}
Average Order Value: ${average_order_value:,.2f}
Data Extract (first 1000 chars):
{str(extracted_data[:1000])}...
"""

    prompt = create_qbr_prompt(client_name, client_website, industry, data_summary)

    try:
        logger.info("Generating QBR content with enhanced prompt")
        logger.debug(f"Full prompt: {prompt}")
        response = model.generate_content(prompt)
        logger.info(f"Generated QBR content: {response.text}")

        # Clean up the response to extract JSON from markdown code blocks
        response_text = response.text.strip()
        
        # Find the JSON content between ```json and ```
        if "```json" in response_text:
            start_index = response_text.find("```json") + 7
            end_index = response_text.find("```", start_index)
            if end_index != -1:
                response_text = response_text[start_index:end_index].strip()
            else:
                # If no closing ```, take everything after ```json
                response_text = response_text[start_index:].strip()
        
        # Additional cleanup for any remaining markdown or extra text
        if response_text.startswith("```"):
            response_text = response_text[3:].strip()
        if response_text.endswith("```"):
            response_text = response_text[:-3].strip()
            
        # Find the actual JSON object (starts with { and ends with })
        start_brace = response_text.find('{')
        if start_brace != -1:
            # Find the matching closing brace
            brace_count = 0
            end_brace = -1
            for i in range(start_brace, len(response_text)):
                if response_text[i] == '{':
                    brace_count += 1
                elif response_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_brace = i
                        break
            
            if end_brace != -1:
                response_text = response_text[start_brace:end_brace + 1]
        
        return response_text
    except Exception as e:
        logger.error(f"Error generating content with Gemini Pro: {e}")
        return "{}"


@app.post("/api/generate")
async def generate_qbr(
    client_name: str = Form(...),
    client_website: str = Form(...),
    industry: str = Form(...),
    customer_data_files: List[UploadFile] = File(default=[]),
):
    logger.info("Received request at /api/generate")
    logger.info(f"Client Name: {client_name}")
    logger.info(f"Client Website: {client_website}")
    logger.info(f"Industry: {industry}")
    
    # Log the types of the input variables
    logger.info(f"Type of client_name: {type(client_name)}")
    logger.info(f"Type of client_website: {type(client_website)}")
    logger.info(f"Type of industry: {type(industry)}")
    logger.info(f"Type of customer_data_files: {type(customer_data_files)}")
    
    extracted_data = ""
    # Initialize variables to avoid NameError
    total_revenue = 0
    total_purchases = 0
    average_order_value = 0
    
    try:
        if not customer_data_files:
            logger.warning("No files uploaded, proceeding with empty data")
            extracted_data = "No customer data files provided"
        else:
            for file in customer_data_files:
                logger.info(f"Processing file: {file.filename}")
                logger.info(f"File content type: {file.content_type}")
                logger.info(f"File size: {len(await file.read())} bytes")
                await file.seek(0)  # Reset file pointer after reading
                try:
                    if file.filename.endswith(".pdf"):
                        extracted_data += extract_text_from_pdf(file)
                    elif file.filename.endswith(".csv"):
                        csv_data = extract_data_from_csv(file)
                        extracted_data += str(csv_data)
                        total_revenue, total_purchases, average_order_value = calculate_revenue_and_aov(csv_data)
                    else:
                        logger.warning(f"Unsupported file type: {file.filename}")
                except Exception as e:
                    logger.error(f"Error processing file {file.filename}: {e}")
        
        logger.info(f"Extracted data before QBR generation: {extracted_data}")
        logger.info(f"Type of extracted_data: {type(extracted_data)}")
        logger.debug(f"Extracted data content: {extracted_data}")
        logger.info("Calling generate_qbr_content")
        qbr_content = generate_qbr_content(client_name, client_website, industry, extracted_data, total_revenue, total_purchases, average_order_value)
        logger.info("generate_qbr_content returned")
        logger.debug(f"Raw QBR content from Gemini: {qbr_content}")

        # Format numbers in the QBR content before returning
        qbr_content = format_numbers_in_qbr(qbr_content)

        # Parse the JSON string to ensure it's valid JSON
        import json
        logger.debug("Parsing JSON")
        try:
            parsed_content = json.loads(qbr_content)
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}, content: {qbr_content}")
            return {"error": "JSONDecodeError"}
        logger.debug("JSON parsed")
        logger.info(f"QBR content: {qbr_content}")
        logger.debug(f"About to create response_data with qbr_content type: {type(parsed_content)}")
        response_data = {
            "qbr_content": json.dumps(parsed_content),
            "total_revenue": total_revenue,
            "total_purchases": total_purchases,
            "average_order_value": average_order_value
        }
        logger.debug(f"Response data keys: {list(response_data.keys())}")
        response = responses.JSONResponse(content=response_data)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response
    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: {e}, qbr_content: {qbr_content}")
        return {
            "error": "JSONDecodeError",
            "qbr_content": "{}",  # Provide empty QBR content
            "total_revenue": total_revenue,
            "total_purchases": total_purchases,
            "average_order_value": average_order_value
        }
    except Exception as e:
        logger.error(f"Error in generate_qbr_content: {e}")
        logger.exception(e)
        return {
            "error": "Internal Server Error",
            "qbr_content": "{}",  # Provide empty QBR content
            "total_revenue": total_revenue,
            "total_purchases": total_purchases,
            "average_order_value": average_order_value
        }
    finally:
        logger.info("Finished processing request at /api/generate")


@app.post("/api/export-pdf")
async def export_pdf(
    client_name: str = Form(...),
    client_website: str = Form(...),
    industry: str = Form(...),
    qbr_content: str = Form(...),
):
    """
    Export QBR content to PDF format with Blueshift branding
    
    Args:
        client_name: Name of the client
        client_website: Client's website URL
        industry: Client's industry
        qbr_content: JSON string containing the QBR slide data
    
    Returns:
        PDF file as downloadable attachment
    """
    logger.info("Received request at /api/export-pdf")
    logger.info(f"Client Name: {client_name}")
    logger.info(f"Industry: {industry}")
    
    try:
        # Generate PDF
        pdf_bytes = generate_qbr_pdf(
            qbr_data=qbr_content,
            client_name=client_name,
            client_website=client_website,
            industry=industry
        )
        
        # Create filename
        safe_client_name = "".join(c for c in client_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"QBR_{safe_client_name.replace(' ', '_')}.pdf"
        
        logger.info(f"Successfully generated PDF: {filename}")
        
        # Return PDF as downloadable file
        return create_pdf_response(pdf_bytes, filename)
        
    except Exception as e:
        logger.error(f"Error exporting PDF: {str(e)}")
        logger.exception(e)
        return {
            "error": "PDF Export Error",
            "message": f"Failed to generate PDF: {str(e)}"
        }
