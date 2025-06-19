import json
import os
from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
import logging

logger = logging.getLogger(__name__)

# Blueshift Brand Colors
BLUESHIFT_BLUE = colors.Color(0, 0.4, 0.8)  # #0066CC
BLUESHIFT_LIGHT_BLUE = colors.Color(0.9, 0.95, 1)  # #E6F3FF
BLUESHIFT_ACCENT = colors.Color(0.1, 0.6, 0.9)  # #1A99E6
SUCCESS_GREEN = colors.Color(0.2, 0.7, 0.3)  # #33B34D
WARNING_ORANGE = colors.Color(1, 0.6, 0.2)  # #FF9933
DARK_GRAY = colors.Color(0.2, 0.2, 0.2)  # #333333
MEDIUM_GRAY = colors.Color(0.4, 0.4, 0.4)  # #666666
LIGHT_GRAY = colors.Color(0.6, 0.6, 0.6)  # #999999
VERY_LIGHT_GRAY = colors.Color(0.95, 0.95, 0.95)  # #F2F2F2

class BlueshiftPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom styles for Blueshift branding"""
        # Title style for slide headers
        self.styles.add(ParagraphStyle(
            name='BlueshiftTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            spaceAfter=25,
            textColor=BLUESHIFT_BLUE,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        # Slide title style
        self.styles.add(ParagraphStyle(
            name='SlideTitle',
            parent=self.styles['Heading2'],
            fontSize=20,
            spaceAfter=20,
            spaceBefore=15,
            textColor=BLUESHIFT_BLUE,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        # Section subtitle style
        self.styles.add(ParagraphStyle(
            name='SectionSubtitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=12,
            textColor=BLUESHIFT_ACCENT,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        # Bullet point style
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=3,
            leftIndent=20,
            bulletIndent=10,
            fontName='Helvetica',
            textColor=DARK_GRAY,
            alignment=TA_LEFT
        ))
        
        # Key metric style
        self.styles.add(ParagraphStyle(
            name='KeyMetric',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            fontName='Helvetica',
            textColor=DARK_GRAY,
            alignment=TA_LEFT
        ))
        
        # Positive metric style
        self.styles.add(ParagraphStyle(
            name='PositiveMetric',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            fontName='Helvetica-Bold',
            textColor=SUCCESS_GREEN,
            alignment=TA_LEFT
        ))
        
        # Warning metric style
        self.styles.add(ParagraphStyle(
            name='WarningMetric',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=4,
            fontName='Helvetica-Bold',
            textColor=WARNING_ORANGE,
            alignment=TA_LEFT
        ))
        
        # Table header style
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))
        
        # Table cell style
        self.styles.add(ParagraphStyle(
            name='TableCell',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=DARK_GRAY,
            fontName='Helvetica',
            alignment=TA_CENTER
        ))
        
        # Header style
        self.styles.add(ParagraphStyle(
            name='Header',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=BLUESHIFT_BLUE,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=LIGHT_GRAY,
            fontName='Helvetica',
            alignment=TA_CENTER
        ))
    
    def create_metrics_table(self, metrics_data):
        """Create a formatted metrics table"""
        if not metrics_data:
            return None
            
        # Prepare table data
        table_data = [
            [Paragraph('Metric', self.styles['TableHeader']), 
             Paragraph('Current Period', self.styles['TableHeader']), 
             Paragraph('Previous Period', self.styles['TableHeader']),
             Paragraph('Change', self.styles['TableHeader'])]
        ]
        
        for metric in metrics_data:
            current = metric.get('current', 'N/A')
            previous = metric.get('previous', 'N/A')
            change = metric.get('change', 'N/A')
            
            # Format change with color coding
            if isinstance(change, str) and '%' in change:
                try:
                    change_val = float(change.replace('%', '').replace('+', '').replace('Target: ', ''))
                    if change_val > 0:
                        change_style = 'PositiveMetric'
                        change_text = f"+{change}" if not change.startswith('+') and not change.startswith('Target:') else change
                    elif change_val < 0:
                        change_style = 'WarningMetric'
                        change_text = change
                    else:
                        change_style = 'TableCell'
                        change_text = change
                except:
                    change_style = 'TableCell'
                    change_text = change
            else:
                change_style = 'TableCell'
                change_text = str(change)
            
            table_data.append([
                Paragraph(metric.get('name', ''), self.styles['TableCell']),
                Paragraph(str(current), self.styles['TableCell']),
                Paragraph(str(previous), self.styles['TableCell']),
                Paragraph(change_text, self.styles[change_style])
            ])
        
        # Create table
        table = Table(table_data, colWidths=[2.2*inch, 1.5*inch, 1.5*inch, 1.2*inch])
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), BLUESHIFT_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            
            # Data rows styling  
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), DARK_GRAY),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, LIGHT_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, VERY_LIGHT_GRAY]),
        ]))
        
        return table
    
    def create_summary_table(self, summary_data):
        """Create a two-column summary table"""
        if not summary_data:
            return None
            
        table_data = []
        for item in summary_data:
            table_data.append([
                Paragraph(f"<b>{item.get('label', '')}</b>", self.styles['TableCell']),
                Paragraph(str(item.get('value', '')), self.styles['TableCell'])
            ])
        
        table = Table(table_data, colWidths=[3*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, LIGHT_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (0, -1), VERY_LIGHT_GRAY),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return table
    
    def create_custom_table(self, table_data):
        """Create a custom formatted table from structured data"""
        if not table_data or 'data' not in table_data:
            return None
            
        rows = table_data['data']
        if not rows:
            return None
            
        # Build table data with proper formatting
        formatted_data = []
        
        # Add header if present
        if 'headers' in table_data and table_data['headers']:
            header_row = []
            for header in table_data['headers']:
                header_row.append(Paragraph(str(header), self.styles['TableHeader']))
            formatted_data.append(header_row)
        
        # Add data rows
        for row in rows:
            formatted_row = []
            for cell in row:
                formatted_row.append(Paragraph(str(cell), self.styles['TableCell']))
            formatted_data.append(formatted_row)
        
        # Calculate column widths
        num_cols = len(formatted_data[0]) if formatted_data else 1
        col_width = 6.5*inch / num_cols
        col_widths = [col_width] * num_cols
        
        # Create table
        table = Table(formatted_data, colWidths=col_widths)
        
        # Apply styling
        table_style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, LIGHT_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]
        
        # Header styling if present
        if 'headers' in table_data and table_data['headers']:
            table_style.extend([
                ('BACKGROUND', (0, 0), (-1, 0), BLUESHIFT_BLUE),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
            ])
            
            # Alternating row colors for data
            table_style.append(('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, VERY_LIGHT_GRAY]))
        else:
            # Alternating row colors for all rows
            table_style.append(('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, VERY_LIGHT_GRAY]))
        
        table.setStyle(TableStyle(table_style))
        return table

class BlueshiftPageTemplate(PageTemplate):
    def __init__(self, doc, client_name="", **kwargs):
        self.client_name = client_name
        self.doc = doc
        frame = Frame(0.75*inch, 0.75*inch, 
                     doc.width, doc.height - 1.5*inch,
                     id='main', leftPadding=0, rightPadding=0,
                     topPadding=0, bottomPadding=0)
        super().__init__('main', [frame], **kwargs)
        
    def beforeDrawPage(self, canvas, doc):
        """Draw header and footer on each page"""
        canvas.saveState()
        
        # Header
        canvas.setFillColor(BLUESHIFT_BLUE)
        canvas.rect(0, doc.height + 0.75*inch, doc.width + 1.5*inch, 0.75*inch, fill=1)
        
        # Header text
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica-Bold', 16)
        canvas.drawString(0.75*inch, doc.height + inch, "Quarterly Business Review")
        
        # Client name in header
        if self.client_name:
            canvas.setFont('Helvetica', 12)
            canvas.drawRightString(doc.width + 0.75*inch, doc.height + inch, 
                                 f"Client: {self.client_name}")
        
        # Date in header
        canvas.setFont('Helvetica', 10)
        canvas.drawRightString(doc.width + 0.75*inch, doc.height + 0.85*inch, 
                             datetime.now().strftime("%B %d, %Y"))
        
        # Footer
        canvas.setFillColor(LIGHT_GRAY)
        canvas.setFont('Helvetica', 9)
        canvas.drawCentredString(doc.width/2 + 0.75*inch, 0.5*inch,
                               f"Generated by Blueshift | Page {doc.page}")
        
        # Footer line
        canvas.setStrokeColor(BLUESHIFT_BLUE)
        canvas.setLineWidth(2)
        canvas.line(0.75*inch, 0.7*inch, doc.width + 0.75*inch, 0.7*inch)
        
        canvas.restoreState()

class BlueshiftDocTemplate(BaseDocTemplate):
    def __init__(self, filename, client_name="", **kwargs):
        super().__init__(filename, **kwargs)
        template = BlueshiftPageTemplate(self, client_name)
        self.addPageTemplates([template])

def generate_qbr_pdf(qbr_data, client_name="", client_website="", industry=""):
    """
    Generate a branded PDF from QBR data
    
    Args:
        qbr_data: Dictionary containing slide data
        client_name: Name of the client
        client_website: Client's website
        industry: Client's industry
    
    Returns:
        BytesIO object containing the PDF
    """
    try:
        logger.info(f"Generating PDF for client: {client_name}")
        
        # Parse QBR data if it's a string
        if isinstance(qbr_data, str):
            qbr_content = json.loads(qbr_data)
        else:
            qbr_content = qbr_data
            
        # Create PDF in memory
        buffer = BytesIO()
        
        # Create document with custom template
        doc = BlueshiftDocTemplate(buffer, client_name=client_name, pagesize=letter)
        
        # Create PDF generator instance for styles
        pdf_gen = BlueshiftPDFGenerator()
        
        # Build content
        story = []
        
        # Title page content
        story.append(Paragraph(f"Quarterly Business Review", pdf_gen.styles['BlueshiftTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Client information
        if client_name:
            story.append(Paragraph(f"<b>Client:</b> {client_name}", pdf_gen.styles['Normal']))
        if client_website:
            story.append(Paragraph(f"<b>Website:</b> {client_website}", pdf_gen.styles['Normal']))
        if industry:
            story.append(Paragraph(f"<b>Industry:</b> {industry}", pdf_gen.styles['Normal']))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Process each slide with enhanced formatting
        slide_count = 0
        for slide_key in sorted(qbr_content.keys()):
            if slide_key.startswith('slide'):
                slide_count += 1
                slide_data = qbr_content[slide_key]
                
                # Add page break for slides after the first
                if slide_count > 1:
                    story.append(PageBreak())
                
                # Slide title
                title = slide_data.get('title', f'Slide {slide_count}')
                story.append(Paragraph(title, pdf_gen.styles['SlideTitle']))
                story.append(Spacer(1, 0.2*inch))
                
                # Process slide content with enhanced formatting
                content = slide_data.get('content', [])
                tables = slide_data.get('tables', [])
                metrics = slide_data.get('metrics', [])
                summary = slide_data.get('summary', [])
                
                # Add metrics table if present
                if metrics:
                    story.append(Paragraph("Key Performance Indicators", pdf_gen.styles['SectionSubtitle']))
                    story.append(Spacer(1, 0.1*inch))
                    metrics_table = pdf_gen.create_metrics_table(metrics)
                    if metrics_table:
                        story.append(KeepTogether(metrics_table))
                        story.append(Spacer(1, 0.2*inch))
                
                # Add summary table if present
                if summary:
                    story.append(Paragraph("Summary", pdf_gen.styles['SectionSubtitle']))
                    story.append(Spacer(1, 0.1*inch))
                    summary_table = pdf_gen.create_summary_table(summary)
                    if summary_table:
                        story.append(KeepTogether(summary_table))
                        story.append(Spacer(1, 0.2*inch))
                
                # Add custom tables if present
                if tables:
                    for table_data in tables:
                        table_title = table_data.get('title', '')
                        if table_title:
                            story.append(Paragraph(table_title, pdf_gen.styles['SectionSubtitle']))
                            story.append(Spacer(1, 0.1*inch))
                        
                        custom_table = pdf_gen.create_custom_table(table_data)
                        if custom_table:
                            story.append(KeepTogether(custom_table))
                            story.append(Spacer(1, 0.2*inch))
                
                # Process regular content
                if isinstance(content, list):
                    for item in content:
                        if item.strip():  # Only add non-empty items
                            # Check if item contains structured data
                            if '|' in item:  # Potential table row
                                continue  # Skip, will be handled by table processing
                            else:
                                # Create enhanced bullet point with better formatting
                                bullet_text = f"• {item}"
                                story.append(Paragraph(bullet_text, pdf_gen.styles['BulletPoint']))
                elif isinstance(content, str):
                    story.append(Paragraph(content, pdf_gen.styles['Normal']))
                
                story.append(Spacer(1, 0.3*inch))
        
        # Add summary footer if no slides were found
        if slide_count == 0:
            story.append(Paragraph("No slide content available", pdf_gen.styles['Normal']))
        
        # Build the PDF
        doc.build(story)
        
        # Get the PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        logger.info(f"Successfully generated PDF with {slide_count} slides")
        return pdf_bytes
        
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise Exception(f"PDF generation failed: {str(e)}")

def create_pdf_response(pdf_bytes, filename="QBR_Presentation.pdf"):
    """
    Create a FastAPI response for PDF download
    
    Args:
        pdf_bytes: PDF content as bytes
        filename: Name for the downloaded file
    
    Returns:
        FastAPI Response object
    """
    from fastapi import Response
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/pdf"
        }
    )