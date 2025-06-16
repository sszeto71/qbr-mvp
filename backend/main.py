import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info(f"Backend port is set to: 8000")
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# backend/main.py
import fastapi
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import google.generativeai as genai
import PyPDF2
import csv
import logging
import json

# logger.debug("google.generativeai imported successfully")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("google.generativeai imported successfully")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Replace with your actual Gemini API key
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
import logging
logging.basicConfig(level=logging.DEBUG)

# Check if GOOGLE_API_KEY is set
if "GOOGLE_API_KEY" in os.environ:
    logging.info("GOOGLE_API_KEY is set")
    logging.info(f"GOOGLE_API_KEY value: {os.environ['GOOGLE_API_KEY']}")
else:
    logging.info("GOOGLE_API_KEY is not set")

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


def generate_qbr_content(client_name, client_website, industry, extracted_data):
    prompt = f"""
    Generate a Quarterly Business Review (QBR) presentation content for {client_name} ({client_website}), an {industry} company.
    Use the following data to create content for 6 slides:

    Data:
    {extracted_data}

    Slide Themes:
    1. Account Overview: Key performance highlights
    2. Campaign Performance: Highlight key trends/analysis on campaigns
    3. Campaign Performance By Type: Share insight and results base on campaign type. Identify the campaign type that has the best results
    4. Campaign Categorization: Identify campaign categorization and top performing campaign category
    5. Driving Marketing Success: Identify benefits and results from platform's key features and capabilities
    6. Blueshift Recommendations: Suggest actionable next steps for the next 1-2 quarters.

    Format the output as a JSON object with the following structure:
    {{
        "slide1": {{"title": "Account Overview", "content": ["Bullet point 1", "Bullet point 2", ...]}},
        "slide2": {{"title": "Campaign Performance", "content": ["Bullet point 1", "Bullet point 2", ...]}},
        ...
    }}
    """

    try:
        logger.info(f"Generating QBR content with prompt: {prompt}")
        logger.debug(f"Full prompt: {prompt}")
        logger.debug(f"Extracted data: {extracted_data}")
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
    customer_data_files: List[UploadFile] = File(...),
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
    try:
        for file in customer_data_files:
            logger.info(f"Processing file: {file.filename}")
            logger.info(f"File content type: {file.content_type}")
            logger.info(f"File size: {len(await file.read())} bytes")
            await file.seek(0)  # Reset file pointer after reading
            try:
                if file.filename.endswith(".pdf"):
                    extracted_data += extract_text_from_pdf(file)
                elif file.filename.endswith(".csv"):
                    extracted_data += str(extract_data_from_csv(file))
                else:
                    logger.warning(f"Unsupported file type: {file.filename}")
            except Exception as e:
                logger.error(f"Error processing file {file.filename}: {e}")
        
        logger.info(f"Extracted data before QBR generation: {extracted_data}")
        logger.info(f"Type of extracted_data: {type(extracted_data)}")
        logger.info("Calling generate_qbr_content")
        qbr_content = generate_qbr_content(client_name, client_website, industry, extracted_data)
        logger.info("generate_qbr_content returned")
        # Parse the JSON string to ensure it's valid JSON
        import json
        logger.debug("Parsing JSON")
        parsed_content = json.loads(qbr_content)
        logger.debug("JSON parsed")
        logger.info(f"QBR content: {qbr_content}")
        logger.info("Returning parsed content")
        response = fastapi.responses.JSONResponse(content=parsed_content)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response
    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: {e}")
        return {"error": "JSONDecodeError"}  # Return an error message
    except Exception as e:
        logger.error(f"Error in generate_qbr_content: {e}")
        logger.exception(e)
        return {"error": "Internal Server Error"}  # Return an error message
    finally:
        logger.info("Finished processing request at /api/generate")

if __name__ == "__main__":
    port = 8000
    logger.info(f"Backend port is set to: {port}")
    logger.info("Starting uvicorn")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
    logger.info(f"Starting Uvicorn server on port {port}")
    logger.info(f"Uvicorn server started on port {port}")