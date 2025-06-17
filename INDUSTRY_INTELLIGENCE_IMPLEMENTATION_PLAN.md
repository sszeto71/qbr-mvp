# Industry Intelligence System - Implementation Plan

## Overview
Enhance the QBR generator to provide industry-specific content by implementing an Industry Intelligence System that incorporates customer engagement strategies, challenges, and Blueshift platform capabilities for E-Commerce, Finance, and Media industries.

## Current Issue
The [`generate_qbr_content()`](backend/main.py:96) function uses a generic prompt that only mentions industry name without industry-specific context.

## Implementation Steps

### 1. Create Industry Intelligence Module
**File:** `backend/industry_intelligence.py`
- Define industry-specific contexts and challenges
- Map Blueshift capabilities to industry needs
- Create success metric frameworks for each industry

### 2. Build Enhanced Prompt Generator
**File:** `backend/prompt_generator.py`
- Implement dynamic prompt construction
- Add industry-specific insight generation
- Integrate Blueshift feature highlighting

### 3. Update Main Application
**File:** `backend/main.py`
- Modify [`generate_qbr_content()`](backend/main.py:96) function
- Integrate industry intelligence system
- Replace generic prompt with industry-aware prompts

## Industry-Specific Focus Areas

### E-Commerce
- Cart abandonment recovery strategies
- Customer lifecycle optimization
- Conversion rate enhancement
- Revenue per customer analysis

### Finance
- Customer retention and trust building
- Compliance-aware marketing strategies
- Lifecycle value maximization
- Cross-selling opportunities

### Media
- Content engagement optimization
- Subscription lifecycle management
- Audience segmentation strategies
- Content consumption patterns

## Expected Outcome
Transform generic QBR content into industry-tailored presentations that demonstrate deep understanding of sector-specific challenges and leverage relevant Blueshift platform capabilities.

## Technical Changes Required
1. Create `backend/industry_intelligence.py` - Industry knowledge base
2. Create `backend/prompt_generator.py` - Dynamic prompt builder
3. Update `backend/main.py` - Enhanced [`generate_qbr_content()`](backend/main.py:96) function
4. Test with sample data for all three industries

## Next Steps
Switch to Code mode to implement the Industry Intelligence System components.