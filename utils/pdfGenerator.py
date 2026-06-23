import os
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)


def generate_pdf(topic, report, feedback, sources):
    """
    Generate a professional research report PDF.

    Args:
        topic (str)
        report (str)
        feedback (str)
        sources (list | str)

    Returns:
        str -> PDF file path
    """

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{topic.replace(' ','_')}_Research_Report.pdf"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = HexColor("#0B5394")

    heading = styles["Heading2"]
    heading.textColor = HexColor("#1F4E79")

    normal = styles["BodyText"]

    story = []

    # ==========================
    # Cover Title
    # ==========================

    story.append(Paragraph("AI Multi-Agent Research Report", title_style))
    story.append(Spacer(1, 0.35 * inch))

    story.append(
        Paragraph(f"<b>Research Topic:</b> {topic}", normal)
    )

    story.append(
        Paragraph(
            f"<b>Generated On:</b> {datetime.now().strftime('%d %B %Y %I:%M %p')}",
            normal,
        )
    )

    story.append(Spacer(1, 0.4 * inch))

    # ==========================
    # Executive Summary
    # ==========================

    story.append(Paragraph("Executive Summary", heading))
    story.append(Spacer(1, 0.15 * inch))

    summary = report[:700]

    story.append(Paragraph(summary.replace("\n", "<br/>"), normal))

    story.append(Spacer(1, 0.35 * inch))

    # ==========================
    # Detailed Report
    # ==========================

    story.append(Paragraph("Detailed Research Report", heading))
    story.append(Spacer(1, 0.15 * inch))

    story.append(
        Paragraph(report.replace("\n", "<br/>"), normal)
    )

    story.append(Spacer(1, 0.35 * inch))

    # ==========================
    # Critic Analysis
    # ==========================

    story.append(Paragraph("Critic Review", heading))
    story.append(Spacer(1, 0.15 * inch))

    story.append(
        Paragraph(feedback.replace("\n", "<br/>"), normal)
    )

    story.append(Spacer(1, 0.35 * inch))

    # ==========================
    # Sources
    # ==========================

    story.append(Paragraph("Sources Used", heading))
    story.append(Spacer(1, 0.15 * inch))

    if isinstance(sources, list):

        for i, source in enumerate(sources, start=1):
            story.append(
                Paragraph(f"{i}. {source}", normal)
            )

    else:
        story.append(
            Paragraph(str(sources).replace("\n", "<br/>"), normal)
        )

    story.append(Spacer(1, 0.35 * inch))

    # ==========================
    # Footer
    # ==========================

    story.append(Paragraph("Generated using:", heading))

    story.append(
        Paragraph(
            """
            • LangChain<br/>
            • Mistral AI<br/>
            • Tavily Search API<br/>
            • BeautifulSoup<br/>
            • Streamlit<br/>
            """,
            normal,
        )
    )

    doc.build(story)

    return filename

    