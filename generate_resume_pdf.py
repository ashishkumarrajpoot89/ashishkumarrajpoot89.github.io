"""
Generate static/resume.pdf from Ashish Kumar's resume content.
Run once: python generate_resume_pdf.py
Replace static/resume.pdf anytime with your own PDF if you prefer.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, ListFlowable, ListItem,
)

ACCENT = colors.HexColor("#FF4103")
DARK = colors.HexColor("#001621")

OUT = os.path.join("static", "resume.pdf")


def build_styles():
    s = getSampleStyleSheet()
    styles = {
        "name": ParagraphStyle("name", parent=s["Title"], fontSize=21, textColor=DARK,
                               alignment=TA_CENTER, spaceAfter=2, leading=24),
        "subtitle": ParagraphStyle("subtitle", parent=s["Normal"], fontSize=10,
                                   textColor=ACCENT, alignment=TA_CENTER, spaceAfter=2),
        "contact": ParagraphStyle("contact", parent=s["Normal"], fontSize=8.8,
                                  textColor=colors.HexColor("#444444"), alignment=TA_CENTER, spaceAfter=9),
        "h2": ParagraphStyle("h2", parent=s["Heading2"], fontSize=10.5, textColor=DARK,
                             spaceBefore=5, spaceAfter=1, leading=12),
        "role": ParagraphStyle("role", parent=s["Normal"], fontSize=9.2, textColor=DARK,
                              spaceBefore=3, spaceAfter=1, leading=11.5),
        "meta": ParagraphStyle("meta", parent=s["Normal"], fontSize=8.3,
                              textColor=colors.HexColor("#666666"), spaceAfter=1),
        "body": ParagraphStyle("body", parent=s["Normal"], fontSize=8.8, leading=10.4,
                              alignment=TA_JUSTIFY, spaceAfter=2),
        "bullet": ParagraphStyle("bullet", parent=s["Normal"], fontSize=8.8, leading=10.4),
        "skills": ParagraphStyle("skills", parent=s["Normal"], fontSize=8, leading=9.7,
                               alignment=TA_JUSTIFY, spaceAfter=1.2),
    }
    return styles


def rule():
    return HRFlowable(width="100%", thickness=1, color=ACCENT, spaceBefore=1, spaceAfter=2.5)


def bullets(items, st):
    return ListFlowable(
        [ListItem(Paragraph(t, st["bullet"]), leftIndent=10, value="•") for t in items],
        bulletType="bullet", start="•", leftIndent=12, bulletColor=ACCENT, spaceBefore=0, spaceAfter=1.5,
    )


def main():
    st = build_styles()
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm,
                            topMargin=10 * mm, bottomMargin=9 * mm, title="Ashish Kumar - Resume")
    e = []

    e.append(Paragraph("ASHISH KUMAR", st["name"]))
    e.append(Paragraph("Data Engineer | Python | SQL | ETL | Apache Airflow | Agentic AI", st["subtitle"]))
    e.append(Paragraph("8707418744 &nbsp;|&nbsp; <link href=\"mailto:beashishrj@gmail.com\">beashishrj@gmail.com</link> &nbsp;|&nbsp; "
                       "<link href=\"https://www.linkedin.com/in/ashishkumarrajpoot/\">LinkedIn</link> &nbsp;|&nbsp; <link href=\"https://github.com/ashishkumarrajpoot89\">GitHub</link> &nbsp;|&nbsp; Delhi &amp; Noida, India", st["contact"]))

    e.append(Paragraph("PROFESSIONAL SUMMARY", st["h2"]))
    e.append(rule())
    e.append(Paragraph(
        "Data Engineer with hands-on experience building Python-based ETL/ELT pipelines, SQL workflows, "
        "data-quality validation, and API integrations for a government student-admission platform. Delivered "
        "a rank-and-preference-based seat allocation engine processing 1M+ student records using Python, SQL, "
        "Apache Airflow, MySQL, ClickHouse, FastAPI, and SQLAlchemy, cutting manual processing time by an "
        "estimated 50%+. Skilled in data modeling, workflow orchestration, and schema validation. Currently "
        "upskilling in Agentic AI and LLM application development (RAG, MCP, LangGraph) to transition into "
        "AI-focused data engineering roles.", st["body"]))

    e.append(Paragraph("PROFESSIONAL EXPERIENCE", st["h2"]))
    e.append(rule())
    e.append(Paragraph("<b>Software Developer</b> | Samarth eGov (Ministry of Education, GoI)", st["role"]))
    e.append(Paragraph("June 2026 - Present", st["meta"]))
    e.append(bullets([
        "As part of the Data Science Team, developed and maintained a rank-and-preference-based seat allocation "
        "engine processing 1M+ student records, including reprocessing logic for displaced candidates across "
        "multiple preference lists.",
        "Engineered merit-ranking logic implementing multi-level tie-breaking rules based on marks, date of "
        "birth, and name across 2M+ applicant records, ensuring fair and auditable admissions outcomes.",
        "Built and orchestrated Python-based ETL pipelines using Apache Airflow to automate data ingestion, "
        "transformation, and scheduling, cutting manual data-processing time by an estimated 50%+.",
        "Implemented schema validation and column-level data-quality checks to proactively identify missing "
        "fields and table mismatches, with automated email alerts on pipeline failures that saved an estimated "
        "2-5 hours of manual debugging per week.",
        "Integrated Strapi and Directus APIs into production data pipelines, built 3-5 internal FastAPI "
        "endpoints, and authored ClickHouse queries for internal reporting and analytics.",
    ], st))

    e.append(Paragraph("<b>Data Science Intern</b> | Samarth eGov (Ministry of Education, GoI)", st["role"]))
    e.append(Paragraph("March 2026 - June 2026", st["meta"]))
    e.append(bullets([
        "Built foundational data-engineering components for a state-level student admission and seat allocation "
        "system used by the Ministry of Education.",
        "Contributed to seat allocation and merit-ranking logic, MySQL data-extraction workflows, and Apache "
        "Airflow DAG development.",
        "Implemented schema-validation checks to support accurate and reliable processing of admission datasets.",
    ], st))

    e.append(Paragraph("PROJECTS", st["h2"]))
    e.append(rule())
    e.append(Paragraph("<b>Adventure Works Sales Analytics</b> | Python | SQL (SQLAlchemy) | Power BI | Pandas", st["role"]))
    e.append(bullets([
        "Built an end-to-end sales analytics pipeline in Python to analyze sales performance and employee "
        "productivity metrics.",
        "Cleaned and transformed raw data using Pandas, handled missing values, and loaded processed data into "
        "SQL via SQLAlchemy.",
        "Designed interactive Power BI dashboards covering sales trends, top performers, and profit margins "
        "for stakeholder reporting.",
    ], st))

    e.append(Paragraph("<b>SQL Bot</b> | Python | FastAPI | Streamlit | MySQL | sqlglot | "
                       "<link href=\"https://github.com/ashishkumarrajpoot89/SQL_BOT\" color=\"#FF4103\">GitHub</link>", st["role"]))
    e.append(bullets([
        "Built a natural-language-to-SQL bot with a FastAPI backend and Streamlit UI; the AI receives only schema "
        "structure and the question, never table rows or query results.",
        "Validated generated SQL with sqlglot (single SELECT only) and ran it read-only with row cap and timeout; "
        "added a data-leakage test and automatic SQL repair.",
    ], st))

    e.append(Paragraph("TECHNICAL SKILLS", st["h2"]))
    e.append(rule())
    for label, items in [
        ("Programming &amp; Data Engineering", "Python, SQL, ETL, ELT, Data Pipelines, Data Integration, Data Modeling, Data Warehousing, Data Lake, Data Lakehouse, Batch &amp; Stream Processing, Schema Validation, Schema Evolution, Data Quality, Multiprocessing"),
        ("Big Data &amp; Distributed Processing", "Apache Hadoop, HDFS, YARN, Apache Hive, Apache Spark, PySpark, Databricks"),
        ("Transformation &amp; Orchestration", "dbt, Apache Airflow"),
        ("Databases &amp; Warehousing", "MySQL, PostgreSQL, ClickHouse, SQLite, Amazon Redshift, Snowflake, BigQuery"),
        ("Streaming &amp; CDC", "Apache Kafka, Amazon Kinesis, AWS DMS, Debezium, Change Data Capture (CDC)"),
        ("Cloud (AWS)", "Amazon S3, AWS Glue, Redshift, Athena, EMR, Lambda, IAM, DMS, Kinesis | Familiar with GCP &amp; Azure"),
        ("Data Lakehouse &amp; Storage", "Delta Lake, Apache Iceberg, Parquet"),
        ("APIs &amp; Development", "FastAPI, REST APIs, Strapi, Directus, Streamlit"),
        ("Data &amp; Analytics", "Pandas, NumPy, SciPy, Scikit-learn, Data Cleaning, Data Preprocessing"),
        ("BI &amp; Visualization", "Power BI, Apache Superset, Matplotlib, Seaborn"),
        ("DevOps &amp; Tools", "Docker, Git, GitHub, DataGrip, VS Code, Jupyter Notebook, Excel, Google Sheets"),
    ]:
        e.append(Paragraph(f"<b>{label}:</b> {items}", st["skills"]))

    e.append(Paragraph("CURRENTLY LEARNING — AGENTIC AI &amp; GENAI", st["h2"]))
    e.append(rule())
    e.append(Paragraph(
        "Actively upskilling toward AI/agentic engineering roles: LangChain, LangGraph, OpenAI Agents SDK, MCP, "
        "A2A, RAG, Agentic RAG, Context Engineering, Prompt Engineering, Pydantic, Vector Databases, FAISS, "
        "Agent Evaluation, Guardrails, LangSmith, AgentOps, Opik, Langfuse, Docker, GitHub Actions, Nginx, "
        "OpenAI, Anthropic, Gemini, Groq, Ollama, AWS Bedrock, Azure OpenAI.", st["body"]))

    e.append(Paragraph("EDUCATION", st["h2"]))
    e.append(rule())
    e.append(Paragraph("<b>Bachelor of Technology (B.Tech), Computer Science and Engineering</b>", st["role"]))
    e.append(Paragraph("Bundelkhand University, Jhansi, Uttar Pradesh &nbsp;&nbsp;|&nbsp;&nbsp; August 2019 - June 2023", st["meta"]))

    doc.build(e)
    print("Wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
