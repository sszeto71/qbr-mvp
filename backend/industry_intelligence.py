"""
Industry Intelligence Module

This module provides a knowledge base for industry-specific customer engagement strategies,
challenges, and relevant Blueshift platform capabilities.
"""

INDUSTRY_DATA = {
    "E-Commerce": {
        "challenges": [
            "High cart abandonment rates (average 69%)",
            "Optimizing customer acquisition cost (CAC)",
            "Enhancing customer lifetime value (CLV)",
            "Personalizing the shopping experience at scale"
        ],
        "strategies": [
            "Implement multi-stage abandoned cart recovery campaigns.",
            "Utilize behavioral triggers for personalized product recommendations.",
            "Develop loyalty programs to increase customer retention.",
            "Optimize marketing spend by focusing on high-CLV customer segments."
        ],
        "blueshift_capabilities": [
            "Advanced segmentation based on purchase history and browsing behavior.",
            "AI-powered predictive recommendations for cross-sell and upsell.",
            "Journey builder for creating automated, multi-channel lifecycle campaigns.",
            "Revenue attribution to track the impact of marketing efforts."
        ],
        "kpis": [
            "Conversion Rate",
            "Average Order Value (AOV)",
            "Customer Lifetime Value (CLV)",
            "Cart Abandonment Rate",
            "Revenue per Customer"
        ]
    },
    "Finance": {
        "challenges": [
            "Building and maintaining customer trust.",
            "Navigating strict regulatory and compliance requirements (e.g., GDPR, CCPA).",
            "High competition and low differentiation in product offerings.",
            "Educating customers on complex financial products."
        ],
        "strategies": [
            "Create automated educational journeys for new customers.",
            "Use segmentation to deliver targeted, relevant financial advice.",
            "Implement secure and compliant communication channels.",
            "Develop loyalty programs that reward long-term customer relationships."
        ],
        "blueshift_capabilities": [
            "Secure data handling and compliance with industry standards.",
            "Segmentation based on financial product ownership and engagement.",
            "Multi-channel journeys for onboarding and customer education.",
            "Personalization of content to reflect customer's financial goals."
        ],
        "kpis": [
            "Customer Retention Rate",
            "Cross-Sell Ratio",
            "Customer Satisfaction (CSAT)",
            "Product Adoption Rate",
            "Compliance Adherence"
        ]
    },
    "Media": {
        "challenges": [
            "High subscription churn rates.",
            "Monetizing content effectively without alienating the audience.",
            "Keeping audiences engaged in a crowded content landscape.",
            "Understanding content consumption patterns to inform strategy."
        ],
        "strategies": [
            "Develop personalized content recommendations based on viewing history.",
            "Implement re-engagement campaigns for users at risk of churning.",
            "Use A/B testing to optimize headlines and content formats.",
            "Create exclusive content for loyal subscribers."
        ],
        "blueshift_capabilities": [
            "Tracking of content consumption across multiple platforms.",
            "AI-powered content recommendations to increase engagement.",
            "Segmentation based on content preferences and engagement levels.",
            "Automated journeys to manage the subscriber lifecycle."
        ],
        "kpis": [
            "Subscriber Growth Rate",
            "Engagement Rate (e.g., time spent, articles read)",
            "Churn Rate",
            "Customer Lifetime Value (CLV)",
            "Ad Revenue per User"
        ]
    }
}

def get_industry_context(industry: str) -> dict:
    """
    Retrieves the context for a given industry.

    Args:
        industry: The name of the industry.

    Returns:
        A dictionary containing the industry's challenges, strategies,
        Blueshift capabilities, and KPIs. Returns an empty dictionary
        if the industry is not found.
    """
    return INDUSTRY_DATA.get(industry, {})