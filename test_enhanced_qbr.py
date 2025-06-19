#!/usr/bin/env python3
"""
Test script for enhanced QBR generation with visual tables and formatting
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.pdf_generator_enhanced import generate_qbr_pdf
import json

def create_enhanced_qbr_data():
    """Create sample QBR data with enhanced visual formatting and tables"""
    return {
        "slide1": {
            "title": "Executive Summary",
            "content": [
                "Outstanding Q2 performance with record-breaking growth across all key metrics",
                "Successfully expanded customer base by 28% while maintaining high retention rates",
                "Digital transformation initiatives delivered measurable ROI improvements"
            ],
            "summary": [
                {"label": "Revenue Growth", "value": "+24% ($3.2M vs $2.6M)"},
                {"label": "New Customers Acquired", "value": "1,847 customers (+28%)"},
                {"label": "Customer Satisfaction", "value": "94% (Industry avg: 87%)"},
                {"label": "Marketing ROI", "value": "385% (+45% improvement)"}
            ],
            "metrics": [
                {"name": "Total Revenue", "current": "$3.2M", "previous": "$2.6M", "change": "+24%"},
                {"name": "Active Customers", "current": "8,634", "previous": "6,787", "change": "+28%"},
                {"name": "Avg Order Value", "current": "$184", "previous": "$156", "change": "+18%"},
                {"name": "Customer Retention", "current": "91%", "previous": "87%", "change": "+4%"}
            ]
        },
        "slide2": {
            "title": "Financial Performance",
            "content": [
                "Revenue exceeded targets by 12% driven by strong customer acquisition",
                "Improved operational efficiency resulted in 6% margin improvement",
                "Strategic investments in technology showing positive returns"
            ],
            "metrics": [
                {"name": "Total Revenue", "current": "$3.2M", "previous": "$2.6M", "change": "+24%"},
                {"name": "Gross Margin", "current": "72%", "previous": "68%", "change": "+4%"},
                {"name": "Customer Acquisition Cost", "current": "$45", "previous": "$52", "change": "-13%"},
                {"name": "Lifetime Value", "current": "$890", "previous": "$750", "change": "+19%"}
            ],
            "tables": [
                {
                    "title": "Revenue Breakdown by Channel",
                    "headers": ["Channel", "Q2 2025", "Q1 2025", "Growth %"],
                    "data": [
                        ["Email Marketing", "$1.2M", "$950K", "+26%"],
                        ["Social Media", "$800K", "$650K", "+23%"],
                        ["Direct Traffic", "$720K", "$580K", "+24%"],
                        ["Paid Advertising", "$480K", "$420K", "+14%"]
                    ]
                }
            ]
        },
        "slide3": {
            "title": "Customer Engagement & Growth",
            "content": [
                "Achieved highest engagement rates in company history across all channels",
                "Customer onboarding improvements reduced time-to-value by 35%",
                "Personalization engine drove 40% increase in cross-sell opportunities"
            ],
            "metrics": [
                {"name": "Email Open Rate", "current": "34.2%", "previous": "28.5%", "change": "+20%"},
                {"name": "Click-Through Rate", "current": "5.8%", "previous": "4.1%", "change": "+41%"},
                {"name": "Social Engagement", "current": "12.3K", "previous": "8.7K", "change": "+41%"},
                {"name": "App Session Duration", "current": "8.2 min", "previous": "6.4 min", "change": "+28%"}
            ],
            "tables": [
                {
                    "title": "Customer Segmentation Performance",
                    "headers": ["Segment", "Size", "Engagement Score", "Revenue Contribution"],
                    "data": [
                        ["Premium Users", "1,250", "9.2/10", "45%"],
                        ["Regular Users", "4,890", "7.8/10", "38%"],
                        ["New Users", "2,494", "6.5/10", "17%"]
                    ]
                }
            ]
        },
        "slide4": {
            "title": "Campaign Performance Analysis",
            "content": [
                "Summer campaign series delivered exceptional results with 385% ROI",
                "A/B testing program improved conversion rates by 32% across all channels",
                "Cross-channel orchestration increased customer journey completion by 28%"
            ],
            "tables": [
                {
                    "title": "Top Performing Campaigns",
                    "headers": ["Campaign Name", "Reach", "Conversion Rate", "ROI"],
                    "data": [
                        ["Summer Sale 2025", "45,000", "12.3%", "420%"],
                        ["Product Launch Series", "32,000", "9.8%", "385%"],
                        ["Loyalty Program Promo", "28,500", "15.2%", "340%"],
                        ["Back-to-School", "38,000", "8.9%", "295%"]
                    ]
                }
            ],
            "metrics": [
                {"name": "Average Campaign ROI", "current": "385%", "previous": "265%", "change": "+45%"},
                {"name": "Conversion Rate", "current": "11.2%", "previous": "8.6%", "change": "+30%"},
                {"name": "Cost Per Acquisition", "current": "$35", "previous": "$48", "change": "-27%"},
                {"name": "Campaign Reach", "current": "156K", "previous": "124K", "change": "+26%"}
            ]
        },
        "slide5": {
            "title": "Strategic Achievements & Opportunities",
            "content": [
                "Successfully launched AI-powered personalization resulting in 40% lift in engagement",
                "Implemented real-time customer journey optimization with immediate impact",
                "Identified key growth opportunities in mobile commerce and international expansion"
            ],
            "summary": [
                {"label": "AI Personalization Launch", "value": "40% engagement lift, 25% revenue increase"},
                {"label": "Mobile Commerce Growth", "value": "65% of traffic, 58% of conversions"},
                {"label": "International Opportunity", "value": "$2.1M potential revenue (3 markets)"},
                {"label": "Customer Service Automation", "value": "35% cost reduction, 92% satisfaction"}
            ],
            "tables": [
                {
                    "title": "Strategic Initiative Progress",
                    "headers": ["Initiative", "Status", "Impact", "Next Steps"],
                    "data": [
                        ["AI Personalization", "Completed", "+40% engagement", "Expand to mobile"],
                        ["Mobile Optimization", "In Progress", "+25% mobile conv.", "Launch Q3"],
                        ["International Expansion", "Planning", "Market research", "Pilot in Q4"],
                        ["Customer Service AI", "Testing", "35% cost reduction", "Full rollout Q3"]
                    ]
                }
            ]
        },
        "slide6": {
            "title": "Q3 2025 Roadmap & Strategic Goals",
            "content": [
                "Aggressive growth targets supported by proven strategies and enhanced capabilities",
                "Focus on international expansion and mobile-first customer experience",
                "Investment in advanced analytics and predictive modeling for competitive advantage"
            ],
            "tables": [
                {
                    "title": "Q3 2025 SMART Goals",
                    "headers": ["Goal", "Target", "Success Metric", "Timeline"],
                    "data": [
                        ["Revenue Growth", "+30%", "$4.16M total revenue", "Sep 30, 2025"],
                        ["Customer Acquisition", "+35%", "2,500 new customers", "Sep 30, 2025"],
                        ["International Launch", "3 markets", "Launch in UK, CA, AU", "Aug 15, 2025"],
                        ["Mobile Conversion", "+40%", "75% mobile conversion rate", "Aug 31, 2025"]
                    ]
                }
            ],
            "metrics": [
                {"name": "Revenue Target", "current": "$3.2M", "previous": "$2.6M", "change": "Target: +30%"},
                {"name": "Customer Target", "current": "8,634", "previous": "6,787", "change": "Target: +35%"},
                {"name": "Market Expansion", "current": "1 market", "previous": "1 market", "change": "Target: +3 markets"},
                {"name": "Mobile Optimization", "current": "58%", "previous": "45%", "change": "Target: 75%"}
            ]
        }
    }

def main():
    """Test enhanced QBR generation"""
    print("=" * 60)
    print("🎨 Testing Enhanced Visual QBR Generation")
    print("=" * 60)
    
    # Create enhanced QBR data
    qbr_data = create_enhanced_qbr_data()
    
    # Generate PDF with enhanced formatting
    try:
        pdf_bytes = generate_qbr_pdf(
            qbr_data=qbr_data,
            client_name="Acme Corporation",
            client_website="https://acmecorp.com",
            industry="E-Commerce"
        )
        
        # Save the PDF
        output_file = "enhanced_QBR_Acme_Corporation.pdf"
        with open(output_file, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ Enhanced PDF generated successfully!")
        print(f"📄 File saved as: {output_file}")
        print(f"📊 PDF size: {len(pdf_bytes)} bytes")
        print("\n📋 Features included:")
        print("   • Professional visual design with Blueshift branding")
        print("   • Executive summary tables with key metrics")
        print("   • Performance comparison tables (current vs previous)")
        print("   • Campaign performance analysis tables")
        print("   • Strategic initiative tracking tables")
        print("   • SMART goals and targets tables")
        print("   • Color-coded positive/negative metrics")
        print("   • Customer-friendly language and formatting")
        
        print("=" * 60)
        print("✅ Enhanced QBR generation test completed successfully!")
        print("🎉 The presentation is now more visual and customer-friendly!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error generating enhanced PDF: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()