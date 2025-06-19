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
Generate a comprehensive 2nd Quarter Business Review (QBR) presentation for {client_name} ({client_website}),
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
Each key should correspond to a slide and have a "title" and "content" (a JSON array of strings).
The content should be detailed, insightful, and directly reference the provided data and industry context.

**SLIDE STRUCTURE:**
1.  **Executive Summary**: High-level overview of the quarter, referencing key achievements and challenges in the context of the {industry} industry.
2.  **Performance Review**: Detailed analysis of key metrics from the data, comparing them to {industry} industry benchmarks and KPIs.
3.  **Key Achievements**: Highlight successful campaigns, explaining why they worked well for the {industry} market.
4.  **Challenges & Opportunities**: Identify challenges from the data and frame them as opportunities, considering the {industry} landscape.
5.  **Strategic Recommendations**: Propose actionable strategies for the next quarter, leveraging the identified Blueshift capabilities for the {industry} sector.
6.  **Q3 2025 Outlook**: Set specific, measurable, achievable, relevant, and time-bound (SMART) goals for the upcoming quarter that align with the client's objectives in the {industry} market.

Ensure the entire output is a single, valid JSON object.
"""
    return prompt