#!/usr/bin/env python3
"""
Test script to verify PDF export functionality
"""
import sys
import os
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.pdf_generator import generate_qbr_pdf

def test_pdf_generation():
    """Test the PDF generation with sample QBR data"""
    
    # Sample QBR data structure
    test_qbr_data = {
        "slide1": {
            "title": "Executive Summary",
            "content": [
                "Strong quarterly performance with 15% revenue growth",
                "Successful launch of new product line",
                "Expanded market presence in 3 new regions",
                "Customer satisfaction scores increased to 94%"
            ]
        },
        "slide2": {
            "title": "Financial Performance",
            "content": [
                "Total revenue: $2.4M (15% increase YoY)",
                "Gross margin: 68% (improved from 62%)",
                "Customer acquisition cost reduced by 12%",
                "Average order value increased to $156"
            ]
        },
        "slide3": {
            "title": "Key Metrics & KPIs",
            "content": [
                "Monthly active users: 45,000 (+22%)",
                "Conversion rate: 3.2% (+0.8%)",
                "Customer retention: 87% (+5%)",
                "Net promoter score: 42 (industry benchmark: 31)"
            ]
        },
        "slide4": {
            "title": "Market Analysis",
            "content": [
                "E-commerce market grew 18% in Q4",
                "Mobile commerce represents 65% of total sales",
                "Competitive landscape analysis shows strong positioning",
                "Emerging trends in social commerce identified"
            ]
        },
        "slide5": {
            "title": "Strategic Initiatives",
            "content": [
                "Launch of AI-powered personalization engine",
                "Investment in customer service automation",
                "Expansion into international markets",
                "Partnership with major logistics providers"
            ]
        },
        "slide6": {
            "title": "Next Quarter Outlook",
            "content": [
                "Projected revenue growth of 12-18%",
                "Launch of premium product tier",
                "Implementation of advanced analytics platform",
                "Focus on sustainability initiatives"
            ]
        }
    }
    
    # Test client information
    client_name = "Acme Corporation"
    client_website = "https://acmecorp.com"
    industry = "E-Commerce"
    
    try:
        print("Testing PDF generation...")
        print(f"Client: {client_name}")
        print(f"Website: {client_website}")
        print(f"Industry: {industry}")
        print(f"Slides: {len(test_qbr_data)}")
        
        # Generate PDF
        pdf_bytes = generate_qbr_pdf(
            qbr_data=test_qbr_data,
            client_name=client_name,
            client_website=client_website,
            industry=industry
        )
        
        # Save PDF to file
        output_file = f"test_QBR_{client_name.replace(' ', '_')}.pdf"
        with open(output_file, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF generated successfully!")
        print(f"📄 File saved as: {output_file}")
        print(f"📊 PDF size: {len(pdf_bytes)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Testing PDF Export Functionality")
    print("=" * 60)
    
    success = test_pdf_generation()
    
    print("=" * 60)
    if success:
        print("✅ All tests passed! PDF export feature is working correctly.")
        print("🎉 The PDF export functionality is ready for use.")
    else:
        print("❌ Tests failed. Please check the error messages above.")
    print("=" * 60)