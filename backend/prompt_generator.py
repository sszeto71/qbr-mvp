"""
Enhanced Prompt Generator Module

This module constructs dynamic, industry-aware prompts for the QBR
content generation.
"""

from industry_intelligence import get_industry_context

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

5.  **Strategic Achievements & Challenges**:
    - Key accomplishments and learnings narrative
    - Challenges converted to opportunities table
    - Strategic initiative progress tracking

6.  **Q3 2025 Roadmap & Goals**:
    - Strategic priorities narrative
    - SMART goals table with success metrics
    - Quarterly targets and milestones overview

**DATA FORMATTING GUIDELINES:**
- For metrics arrays: {{"name": "Metric Name", "current": "Current Value", "previous": "Previous Value", "change": "+X%" or "-X%"}}
- For summary arrays: {{"label": "Summary Point", "value": "Key Data/Outcome"}}
- For tables arrays: {{"title": "Table Title", "headers": ["Col1", "Col2", ...], "data": [["Row1Data1", "Row1Data2"], ...]}}

Make the presentation executive-ready with clear business impact focus. Ensure the entire output is a single, valid JSON object.
"""
    return prompt