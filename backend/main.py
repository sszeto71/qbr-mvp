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
from fastapi import FastAPI, File, Form, UploadFile, responses
from fastapi.middleware.cors import CORSMiddleware

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
load_dotenv()

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


def generate_qbr_content(client_name, client_website, industry, extracted_data, total_revenue, average_order_value):
    prompt = f"""
    Generate a 2nd Quarter Business Review (QBR) presentation content for {client_name} ({client_website}), an {industry} company.
    Total Revenue: ${total_revenue:,.2f}. Average Order Value: ${average_order_value:,.2f}.
    Use the following data to create content for 6 slides.

    Data:
    {extracted_data}

    The following columns should be included as part of this analysis.

    Column Name
    Campaign
    Campaign Segment
    Campaign Type
    Unique Impressions (user only)
    Revenue per Purchase
    Revenue
    Purchases
    Unique Open Rate
    Unique Clicks (user only)
    Unique Click %
    CTOR
    Add to Cart
    Impressions (user only)
    Revenue per Delivered
    Revenue per Impression
    Revenue per Order
    Revenue per Unique Click

    Identify trends and insights
    Identify the best performing segments
    Identify the best segment categories that were used for the best performing campaigns
    Identify the benefits and capabilities that are driving the best results and performance for the {client_name} ({client_website}), which is using the Blueshift platform (https://blueshift.com/) for executing their marketing strategy and running their digital marketing campaigns to achieve their marketing and company goals and objectives.

    Slide Themes:
    1. Account Overview: Key performance highlights
    2. Campaign Performance: Highlight key trends/analysis on campaigns
    3. Campaign Performance By Type: Share insight and results base on campaign type. Identify the campaign type that has the best results
    4. Campaign Categorization: Identify campaign categorization and top performing campaign segment category
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
        logger.info("Generating QBR content with prompt")
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
        qbr_content = generate_qbr_content(client_name, client_website, industry, extracted_data, total_revenue, average_order_value)
        logger.info("generate_qbr_content returned")
        logger.debug(f"Raw QBR content from Gemini: {qbr_content}")

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
