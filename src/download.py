from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit

def create_pdf(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    
    y_position = height - 50
    left_margin = 50
    right_margin = 50
    usable_width = width - left_margin - right_margin
    line_height = 15  # Adjust if needed
    
    for line in text.split("\n"):
        wrapped_lines = simpleSplit(line, c._fontname, c._fontsize, usable_width)
        for wline in wrapped_lines:
            if y_position < 50:  # Start a new page
                c.showPage()
                c.setFont("Helvetica", 12)
                y_position = height - 50
            c.drawString(left_margin, y_position, wline)
            y_position -= line_height
    
    c.save()
    buffer.seek(0)
    return buffer

def pdf(data):
    return create_pdf(data)
