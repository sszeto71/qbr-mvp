"""
Enhanced Prompt Generator Module

This module constructs dynamic, industry-aware prompts for the QBR
content generation.
"""

from industry_intelligence import get_industry_context
from blueshift_content_templates import (
    CHALLENGES_OPPORTUNITIES_CONTENT,
    STRATEGIC_RECOMMENDATIONS_CONTENT,
    BLUESHIFT_VALUE_PROPOSITIONS,
    ROI_PROOF_POINTS,
    get_blueshift_recommendations,
    get_roi_projections
)

def create_qbr_prompt(client_name: str, client_website: str, industry: str, data_analysis: str) -> str:
    """
    Creates an enhanced, industry-aware prompt for QBR content generation.

    Args:
        client_name: The name of the client.
        client_website: The website of the client.
        industry: The client's industry.
        data_analysis: A summary of the client's campaign performance data.

    Returns:
        A detailed, industry-specific prompt for the AI model.
    """
    industry_context = get_industry_context(industry)

    if not industry_context:
        # Fallback to a generic prompt if industry context is not found
        return f"""
Generate a 2nd Quarter Business Review (QBR) presentation content for {client_name} ({client_website}),
an {industry} company.

The QBR should be structured into 6 slides with a 'title' and 'content' (as a JSON array of strings).
The slides are:
1.  **Executive Summary**: High-level overview of the quarter.
2.  **Performance Review**: Analysis of key metrics and campaign performance.
3.  **Key Achievements**: Highlight successful campaigns and milestones.
4.  **Challenges & Opportunities**: Identify areas for improvement and growth.
5.  **Strategic Recommendations**: Propose actionable strategies for the next quarter.
6.  **Q3 2025 Outlook**: Set goals and expectations for the upcoming quarter.

Analyze the following data and incorporate it into the presentation:
{data_analysis}
"""

    prompt = f"""
Generate a comprehensive, visually-enhanced 2nd Quarter Business Review (QBR) presentation for {client_name} ({client_website}),
a leading company in the {industry} sector, leveraging Blueshift's customer engagement platform.

**INDUSTRY CONTEXT: {industry.upper()}**
- **Key Challenges for this Industry**: {', '.join(industry_context.get('challenges', []))}
- **Proven Strategies for Success**: {', '.join(industry_context.get('strategies', []))}
- **Relevant Blueshift Capabilities**: {', '.join(industry_context.get('blueshift_capabilities', []))}
- **Core KPIs to Focus On**: {', '.join(industry_context.get('kpis', []))}

**PERFORMANCE DATA ANALYSIS:**
Analyze the following campaign performance data summary. Identify trends, top-performing campaigns,
and areas with potential for improvement, keeping the industry context in mind.
{data_analysis}

**BLUESHIFT PLATFORM FOCUS:**
This QBR must demonstrate the exceptional value and ROI of Blueshift's intelligent customer engagement platform.
Highlight these key differentiators:
- **AI-Powered Journey Optimization**: Showcase how Blueshift's machine learning automatically optimizes customer journeys
- **Real-Time Personalization**: Emphasize dynamic content adaptation and behavioral triggers
- **Unified Customer Data Platform**: Highlight the single source of truth for customer interactions
- **Cross-Channel Orchestration**: Demonstrate seamless email, SMS, push, and web coordination
- **Predictive Analytics**: Show churn prediction, lifetime value optimization, and customer scoring capabilities

**ROI DEMONSTRATION REQUIREMENTS:**
- Include specific percentage improvements and financial impact metrics
- Show before/after comparisons with Blueshift implementation
- Highlight industry-leading performance benchmarks
- Demonstrate cost savings through automation and efficiency gains
- Project future growth potential with continued platform optimization

**PRESENTATION REQUIREMENTS:**
Generate the QBR content structured as a JSON object with 6 keys: "slide1", "slide2", ..., "slide6".
Each slide should have:
- "title": Clear, engaging slide title
- "content": Array of key narrative points (2-4 bullet points maximum)
- "metrics": Array of key performance indicators with current/previous period comparisons (when applicable)
- "summary": Array of key summary points for executive overview (when applicable)
- "tables": Array of structured data tables for detailed metrics (when applicable)

**ENHANCED VISUAL FORMAT REQUIREMENTS:**
- Use tables for numerical data comparisons (current vs previous period, benchmarks, etc.)
- Include percentage changes with clear indicators of positive/negative trends
- Present data in customer-friendly language, avoiding technical jargon
- Focus on business impact and outcomes rather than just raw metrics
- Highlight success stories and improvement opportunities

**SLIDE STRUCTURE:**
1.  **Executive Summary**:
    - Overview narrative with key highlights
    - Summary table of top 3-4 achievements with quantified impact
    - Quarter-over-quarter comparison metrics table

2.  **Financial Performance**:
    - Revenue and profitability narrative
    - Financial metrics comparison table (current vs previous period)
    - Key financial KPIs with industry benchmark comparisons

3.  **Customer Engagement & Growth**:
    - Customer acquisition and retention narrative
    - Customer metrics table showing growth trends
    - Engagement performance indicators with percentage changes

4.  **Campaign Performance Analysis**:
    - Top performing campaigns overview
    - Campaign performance comparison table
    - Channel effectiveness metrics with ROI data

5.  **Challenges & Opportunities**:
    - Current market challenges analysis with Blueshift's competitive advantages
    - Untapped growth opportunities with quantified revenue potential ($X.XM annually)
    - Platform capability gaps assessment and Blueshift solutions mapping
    - ROI optimization opportunities with specific improvement percentages
    - Customer engagement evolution possibilities through AI-driven personalization

6.  **Strategic Recommendations**:
    - Priority initiatives leveraging Blueshift's AI and machine learning capabilities
    - Personalization acceleration strategies with projected conversion improvements
    - Cross-channel integration roadmap for unified customer experiences
    - Investment priorities with specific ROI multiples (3x, 4x, 5x returns)
    - Implementation timeline with quick wins and long-term strategic gains
    - Success metrics and KPIs for measuring Blueshift platform optimization

**DATA FORMATTING GUIDELINES:**
- For metrics arrays: {{"name": "Metric Name", "current": "Current Value", "previous": "Previous Value", "change": "+X%" or "-X%"}}
- For summary arrays: {{"label": "Summary Point", "value": "Key Data/Outcome"}}
- For tables arrays: {{"title": "Table Title", "headers": ["Col1", "Col2", ...], "data": [["Row1Data1", "Row1Data2"], ...]}}

**SPECIFIC CONTENT EXAMPLES FOR KEY SLIDES:**

**Slide 5 - Challenges & Opportunities Template:**
Content should include:
- "Market Challenges: Rising customer acquisition costs (+X% YoY) and increasing competition present opportunities for AI-driven personalization"
- "Engagement Opportunity: X% of customers show higher lifetime value with personalized cross-channel journeys - Blueshift's AI unlocks this potential"
- "Data Utilization Gap: Only X% of available customer data currently leveraged - significant growth through Blueshift's unified customer profiles"
- "Automation Expansion: Manual processes consuming X% of marketing resources - Blueshift's intelligent automation reclaims capacity"

Metrics should include improvements like:
- Customer Acquisition Cost trends with Blueshift optimization
- Email engagement rate improvements (target: +25-40%)
- Customer Lifetime Value increases (target: +20-45%)
- Marketing automation coverage growth (target: +50-70%)

**Slide 6 - Strategic Recommendations Template:**
Content should include:
- "Immediate Priority: Deploy Blueshift's AI-powered journey orchestration to increase engagement by X% and reduce manual work by X%"
- "Personalization Acceleration: Leverage Blueshift's real-time CDP for dynamic campaigns delivering 3x higher conversion rates"
- "Cross-Channel Integration: Implement unified experiences using Blueshift's omnichannel capabilities"
- "Predictive Analytics Investment: Utilize ML models for churn prediction and LTV optimization to increase retention by X%"

ROI Projections should show:
- AI Journey Orchestration: 340% ROI with 45% engagement increase
- Real-Time Personalization: 280% ROI with 35% click rate improvement
- Predictive Segmentation: 420% ROI with 50% relevance increase
- Cross-Channel Optimization: 250% ROI with 25% channel synergy improvement

Make the presentation executive-ready with clear business impact focus and specific Blueshift value propositions. Ensure the entire output is a single, valid JSON object.
"""
    return prompt