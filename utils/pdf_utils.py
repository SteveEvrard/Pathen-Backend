from fpdf import FPDF
import json
from datetime import datetime

def generate_pdf(sections, filename="recommendation.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(0, 51, 102)  # Navy blue (RGB: 0, 51, 102)
    pdf.cell(0, 10, "Product Recommendation Report", ln=True, align='C')
    pdf.ln(2)
    pdf.set_draw_color(0, 51, 102)
    pdf.set_line_width(0.7)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # Prepared info
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Prepared by: Pathen Enhanced Intelligence", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%B %d, %Y')}", ln=True)
    pdf.cell(0, 10, f"Solution Type: Product Recommendation", ln=True)
    pdf.ln(10)

    # Sections
    for title, content in sections.items():
        pdf.set_font("Arial", "B", 14)
        formatted_title = title.replace("_", " ").title()
        pdf.multi_cell(0, 10, formatted_title)
        pdf.ln(2)

        pdf.set_font("Arial", "", 12)

        if isinstance(content, dict) or isinstance(content, list):
            content_str = json.dumps(content, indent=2)
        else:
            content_str = content

        pdf.multi_cell(0, 8, content_str)
        pdf.ln(5)

    pdf_path = f"/tmp/{filename}"
    pdf.output(pdf_path, "F")
    return pdf_path
