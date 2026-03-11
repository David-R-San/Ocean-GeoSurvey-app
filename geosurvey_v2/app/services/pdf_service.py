from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import os


def generate_pdf(report_text: str):

    file_path = "ocean_report.pdf"

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph("Ocean GeoSurvey – Thermal Anomaly Report", styles['Title'])
    elements.append(title)

    elements.append(Spacer(1, 20))

    paragraphs = report_text.split("\n")

    for p in paragraphs:
        if p.strip() != "":
            elements.append(Paragraph(p, styles['BodyText']))
            elements.append(Spacer(1, 12))

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    doc.build(elements)

    return file_path