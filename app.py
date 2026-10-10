"""
Ashish Kumar - Portfolio Website
Flask application serving a multi-page data-professional portfolio.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "ashish-portfolio-secret-key"

# When exported as a static site (GitHub Pages), the Flask contact route won't
# exist, so the form posts to Formspree instead. Set FORMSPREE_ENDPOINT to your
# own Formspree form URL (https://formspree.io -> create form -> copy the URL).
# When FREEZE=1 (used by freeze.py), the form uses this endpoint.
FORMSPREE_ENDPOINT = os.environ.get("FORMSPREE_ENDPOINT", "https://formspree.io/f/your-form-id")
IS_STATIC_BUILD = os.environ.get("FREEZE") == "1"
# Public site URL (used for canonical + Open Graph tags).
SITE_URL = os.environ.get("SITE_URL", "https://ashishkumarrajpoot89.github.io")

# ---------------------------------------------------------------------------
# Site-wide data (single source of truth, sourced from resume + GitHub)
# ---------------------------------------------------------------------------
PROFILE = {
    "name": "Ashish Kumar Rajpoot",
    "roles": ["Data Engineer", "Data Analyst", "Python Developer"],
    "tagline": "Turning data into meaningful insights and building scalable solutions for a better tomorrow.",
    "location": "Delhi & Noida, India",
    "email": "beashishrj@gmail.com",
    "phone": "+91 8707418744",
    "github": "https://github.com/ashishkumarrajpoot89",
    "linkedin": "https://www.linkedin.com/in/ashishkumarrajpoot/",
    "photo": "img/profile.jpg",
    "resume_file": "resume.pdf",
    "summary": (
        "Data Engineer with hands-on experience building Python-based ETL/ELT pipelines, SQL workflows, "
        "data-quality validation, and API integrations for a government student-admission platform. "
        "Delivered a rank-and-preference-based seat allocation engine processing 1M+ student records using "
        "Python, SQL, Apache Airflow, MySQL, ClickHouse, FastAPI, and SQLAlchemy, cutting manual processing "
        "time by an estimated 50%+. Skilled in data modeling, workflow orchestration, and schema validation. "
        "Currently upskilling in Agentic AI and LLM application development (RAG, MCP, LangGraph) to transition "
        "into AI-focused data engineering roles."
    ),
}

STATS = [
    {"value": "1M+", "label": "Records Processed"},
    {"value": "50%+", "label": "Manual Time Saved"},
    {"value": "15+", "label": "Projects on GitHub"},
    {"value": "100%", "label": "Passion for Data"},
]

TRAITS = [
    {"icon": "🧩", "title": "Problem Solver"},
    {"icon": "📚", "title": "Continuous Learner"},
    {"icon": "🤝", "title": "Team Player"},
    {"icon": "🚀", "title": "Passionate about Data"},
]

# Each skill is a (name, logo-url) pair. `logo` is a full icon URL or None.
# Logos come from simple-icons (si) or devicon (dv) — devicon covers brand icons
# that simple-icons dropped (Power BI, VS Code, Excel, AWS, dbt, etc.).
# In the template every skill renders as ONE pill: icon + name if a logo exists,
# just the name otherwise. All pills in a category flow in a single wrapping row.
def _si(slug, color="FF4103"):
    return f"https://cdn.simpleicons.org/{slug}/{color}"


def _dv(path):
    return f"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{path}"


def _skill(name, logo=None):
    return {"name": name, "logo": logo}


SKILLS = {
    "Programming & Data Engineering": [
        _skill("Python", _si("python", "3776AB")),
        _skill("SQL", _si("postgresql", "4169E1")),
        _skill("ETL / ELT"),
        _skill("Data Pipelines"),
        _skill("Data Integration"),
        _skill("Data Modeling"),
        _skill("Data Warehousing"),
        _skill("Data Lake"),
        _skill("Data Lakehouse"),
        _skill("Batch Processing"),
        _skill("Stream Processing"),
        _skill("Schema Validation"),
        _skill("Schema Evolution"),
        _skill("Data Quality"),
        _skill("Multiprocessing"),
    ],
    "Big Data & Distributed Processing": [
        _skill("Apache Hadoop", _dv("apachehadoop/apachehadoop-original.svg")),
        _skill("HDFS"),
        _skill("YARN"),
        _skill("Apache Hive", _si("apachehive", "FDEE21")),
        _skill("Apache Spark", _si("apachespark", "E25A1C")),
        _skill("PySpark", _si("apachespark", "E25A1C")),
        _skill("Databricks", _si("databricks", "FF3621")),
    ],
    "Data Transformation & Orchestration": [
        _skill("Apache Airflow", _si("apacheairflow", "017CEE")),
        _skill("dbt", _dv("dbt/dbt-original.svg")),
    ],
    "Databases & Data Warehousing": [
        _skill("MySQL", _si("mysql", "4479A1")),
        _skill("PostgreSQL", _si("postgresql", "4169E1")),
        _skill("ClickHouse", _si("clickhouse", "FFCC01")),
        _skill("SQLite", _si("sqlite", "003B57")),
        _skill("Amazon Redshift", _dv("amazonwebservices/amazonwebservices-original.svg")),
        _skill("Snowflake", _si("snowflake", "29B5E8")),
        _skill("BigQuery", _si("googlebigquery", "669DF6")),
    ],
    "Streaming & CDC": [
        _skill("Apache Kafka", _si("apachekafka", "FF4103")),
        _skill("Amazon Kinesis"),
        _skill("AWS DMS"),
        _skill("Debezium"),
        _skill("Change Data Capture"),
    ],
    "Cloud (AWS)": [
        _skill("Amazon S3"),
        _skill("AWS Glue"),
        _skill("Amazon Redshift"),
        _skill("Amazon Athena"),
        _skill("Amazon EMR"),
        _skill("AWS Lambda"),
        _skill("AWS IAM"),
        _skill("AWS DMS"),
        _skill("Amazon Kinesis"),
    ],
    "Cloud Platforms": [
        _skill("AWS", _dv("amazonwebservices/amazonwebservices-original.svg")),
        _skill("GCP (familiar)", _si("googlecloud", "4285F4")),
        _skill("Azure (familiar)", _dv("azure/azure-original.svg")),
    ],
    "Data Lakehouse & Storage": [
        _skill("Parquet", _si("apacheparquet", "50ABF1")),
        _skill("Delta Lake"),
        _skill("Apache Iceberg"),
    ],
    "APIs & Development": [
        _skill("FastAPI", _si("fastapi", "009688")),
        _skill("REST APIs"),
        _skill("Strapi", _si("strapi", "4945FF")),
        _skill("Directus", _si("directus", "6644FF")),
        _skill("Streamlit", _si("streamlit", "FF4B4B")),
    ],
    "Data & Analytics": [
        _skill("Pandas", _si("pandas", "150458")),
        _skill("NumPy", _si("numpy", "4D77CF")),
        _skill("SciPy", _si("scipy", "8CAAE6")),
        _skill("scikit-learn", _si("scikitlearn", "F7931E")),
        _skill("Data Cleaning"),
        _skill("Data Preprocessing"),
    ],
    "BI & Visualization": [
        _skill("Power BI", _dv("powerbi/powerbi-original.svg")),
        _skill("Apache Superset", _si("apachesuperset", "20A6C9")),
        _skill("Matplotlib", _dv("matplotlib/matplotlib-original.svg")),
        _skill("Seaborn"),
    ],
    "DevOps & Tools": [
        _skill("Docker", _si("docker", "2496ED")),
        _skill("Git", _si("git", "F05032")),
        _skill("GitHub", _si("github", "FFFFFF")),
        _skill("DataGrip", _si("datagrip", "22D88F")),
        _skill("Jupyter", _si("jupyter", "F37626")),
        _skill("Google Sheets", _si("googlesheets", "34A853")),
        _skill("VS Code", _dv("vscode/vscode-original.svg")),
        _skill("Excel", _dv("excel/excel-original.svg")),
    ],
}

# The 6 PINNED repos shown on the GitHub profile Overview, with their real descriptions.
# `scene` picks a CSS/SVG illustration: dashboard | pipeline | house.
GITHUB = PROFILE["github"]
PROJECTS = [
    {
        "slug": "adventure-works",
        "title": "Adventure Works Sales Analytics",
        "tags": ["Data Analytics", "Power BI"],
        "accent": "#FF4103",
        "scene": "dashboard",
        "short": "End-to-end sales analytics pipeline using Python, MySQL and Power BI.",
        "description": (
            "Developed a complete data analytics pipeline using Python and SQL for Adventure Works, enhancing "
            "data accuracy and management. Tech Stack: Python, MySQL, Power BI."
        ),
        "stack": ["Python", "MySQL", "Power BI"],
        "github": GITHUB + "/Adventure_works_",
        "sections": {
            "Overview": "End-to-end sales analytics pipeline enhancing data accuracy and management.",
            "Tech Stack": "Python, MySQL and Power BI.",
            "Highlights": "Data cleaning and transformation, SQL loading, and interactive dashboards.",
        },
        "features": [
            "Complete Python + SQL analytics pipeline",
            "Improved data accuracy and management",
            "Interactive Power BI dashboards for reporting",
        ],
    },
    {
        "slug": "sales-demand-forecast",
        "title": "Sales Demand Forecast",
        "tags": ["Machine Learning", "Pipeline"],
        "accent": "#ff6a3d",
        "scene": "house",
        "short": "Full ML pipeline to forecast product sales demand end to end.",
        "description": (
            "A full-fledged machine learning pipeline to forecast product sales demand. It includes data "
            "ingestion, validation, transformation, model training, evaluation, logging, and deployment."
        ),
        "stack": ["Python", "scikit-learn", "Pandas"],
        "github": GITHUB + "/Sales-Demand-Forecast",
        "sections": {
            "Overview": "End-to-end ML pipeline for product sales demand forecasting.",
            "Tech Stack": "Python and scikit-learn.",
            "Highlights": "Ingestion, validation, transformation, training, evaluation, logging and deployment.",
        },
        "features": [
            "Data ingestion, validation and transformation",
            "Model training, evaluation and logging",
            "Deployment-ready pipeline",
        ],
    },
    {
        "slug": "insurance-fraud-detection",
        "title": "Insurance Fraud Detection",
        "tags": ["Machine Learning", "Pipeline"],
        "accent": "#d6350a",
        "scene": "pipeline",
        "short": "End-to-end ML pipeline to detect fraudulent insurance claims.",
        "description": (
            "A complete end-to-end machine learning pipeline to detect fraudulent insurance claims using "
            "historical data. This project automates the entire process from data ingestion and validation to "
            "model training and evaluation."
        ),
        "stack": ["Python", "scikit-learn", "Pandas"],
        "github": GITHUB + "/Insurance-Fraud-detection",
        "sections": {
            "Overview": "Detects fraudulent insurance claims from historical data.",
            "Tech Stack": "Python and scikit-learn.",
            "Highlights": "Automated ingestion, validation, training and evaluation.",
        },
        "features": [
            "Automated data ingestion and validation",
            "Fraud classification model",
            "End-to-end automated pipeline",
        ],
    },
    {
        "slug": "olympics-analysis",
        "title": "Olympics Analysis",
        "tags": ["Data Analytics", "Streamlit"],
        "accent": "#ff8a5c",
        "scene": "dashboard",
        "short": "Interactive Streamlit app analyzing 120 years of Olympic history.",
        "description": (
            "Developed an interactive web application using Streamlit to analyze 120 years of Olympic history "
            "with dynamic visualizations. Created country-specific and athlete-wise performance statistics to "
            "explore trends over time."
        ),
        "stack": ["Python", "Streamlit", "Pandas"],
        "github": GITHUB + "/Olympics-Analysis-",
        "sections": {
            "Overview": "Interactive analysis of 120 years of Olympic history.",
            "Tech Stack": "Python and Streamlit.",
            "Highlights": "Country-specific and athlete-wise performance statistics with dynamic visualizations.",
        },
        "features": [
            "120 years of Olympic data analyzed",
            "Country and athlete-wise statistics",
            "Dynamic visualizations in Streamlit",
        ],
    },
    {
        "slug": "movie-ratings-analysis",
        "title": "Movie Ratings & Genre Analysis",
        "tags": ["Data Analytics", "Streamlit"],
        "accent": "#FF4103",
        "scene": "dashboard",
        "short": "Streamlit dashboard exploring trends in movie ratings and genres.",
        "description": (
            "A Python-based data analysis project that explores trends in movie ratings and genres. Using a "
            "Streamlit dashboard, it provides insights into popular genres, audience preferences, and rating "
            "patterns."
        ),
        "stack": ["Python", "Streamlit", "Pandas"],
        "github": GITHUB + "/Movie_Ratings_and_Genre_Analysis",
        "sections": {
            "Overview": "Explores trends in movie ratings and genres.",
            "Tech Stack": "Python and Streamlit.",
            "Highlights": "Popular genres, audience preferences and rating patterns.",
        },
        "features": [
            "Genre popularity analysis",
            "Audience preference insights",
            "Interactive Streamlit dashboard",
        ],
    },
    {
        "slug": "fake-news-detector",
        "title": "Fake News Detector (GPT-2)",
        "tags": ["NLP", "Machine Learning"],
        "accent": "#ff6a3d",
        "scene": "pipeline",
        "short": "Identifies human-written vs GPT-2 generated text.",
        "description": (
            "This project focuses on identifying whether a given piece of text is human-written or generated "
            "by GPT-2 models of various sizes. Using the official GPT-2 Output Dataset released by OpenAI, it "
            "analyzes and classifies the text."
        ),
        "stack": ["Python", "NLP", "scikit-learn"],
        "github": GITHUB + "/Fake-News-Detector-Using-ChatCPT-2",
        "sections": {
            "Overview": "Classifies whether text is human-written or GPT-2 generated.",
            "Tech Stack": "Python and NLP.",
            "Highlights": "Uses the official OpenAI GPT-2 Output Dataset across model sizes.",
        },
        "features": [
            "Human vs GPT-2 text classification",
            "Built on OpenAI's GPT-2 Output Dataset",
            "NLP feature analysis",
        ],
    },
]

EXPERIENCE = [
    {
        "period": "June 2026 - Present",
        "role": "Junior Software Developer",
        "org": "Samarth eGov (Ministry of Education, GoI)",
        "points": [
            "Developed and maintained a rank-and-preference-based seat allocation engine processing 1M+ student records.",
            "Engineered merit-ranking logic with multi-level tie-breaking across 2M+ applicant records.",
            "Built and orchestrated Python ETL pipelines with Apache Airflow, cutting manual processing time by ~50%+.",
            "Integrated Strapi and Directus APIs and built internal FastAPI endpoints for reporting.",
        ],
    },
    {
        "period": "March 2026 - June 2026",
        "role": "Data Science Intern",
        "org": "Samarth eGov (Ministry of Education, GoI)",
        "points": [
            "Built foundational data-engineering components for a state-level student admission system.",
            "Contributed to seat allocation, merit-ranking logic and MySQL data-extraction workflows.",
            "Developed Apache Airflow DAGs and schema-validation checks.",
        ],
    },
]

EDUCATION = [
    {
        "degree": "B.Tech, Computer Science and Engineering",
        "school": "Bundelkhand University, Jhansi, Uttar Pradesh",
        "period": "August 2019 - June 2023",
    },
]

# The resume lists no certifications, but has a "Currently Learning" section — real content.
LEARNING = [
    "LangChain & LangGraph",
    "OpenAI Agents SDK, MCP & A2A",
    "RAG & Agentic RAG",
    "Context & Prompt Engineering",
    "Vector Databases & FAISS",
    "Guardrails, LangSmith & Langfuse",
    "Docker, GitHub Actions & Nginx",
    "OpenAI, Anthropic, Gemini, Groq, Ollama",
]

# No real blog content exists, so the blog section is omitted to avoid fabricating posts.


@app.context_processor
def inject_globals():
    # On the single-page home, anchor links are bare "#section".
    # On other pages (e.g. project detail) they become "/#section" to go home first.
    nav_base = "" if request.path == "/" else url_for("home")
    # Static build posts the contact form to Formspree; Flask build uses its route.
    contact_action = FORMSPREE_ENDPOINT if IS_STATIC_BUILD else url_for("contact_submit")
    # Static build links Download straight to the PDF; Flask build uses its route.
    if IS_STATIC_BUILD:
        resume_download_url = url_for("static", filename=PROFILE["resume_file"])
    else:
        resume_download_url = url_for("resume_download")
    meta_description = (
        "Ashish Kumar Rajpoot — Data Engineer building Python ETL/ELT pipelines, SQL workflows and "
        "data-quality systems. Experienced with Apache Airflow, Spark, AWS, FastAPI; upskilling in Agentic AI."
    )
    return {
        "profile": PROFILE,
        "current_year": 2026,
        "nav_base": nav_base,
        "contact_action": contact_action,
        "resume_download_url": resume_download_url,
        "site_url": SITE_URL,
        "meta_description": meta_description,
    }


@app.route("/")
def home():
    """Single-page portfolio: all sections stacked on one scrollable page."""
    return render_template(
        "index.html",
        stats=STATS,
        traits=TRAITS,
        skills=SKILLS,
        projects=PROJECTS,
        experience=EXPERIENCE,
        education=EDUCATION,
        learning=LEARNING,
    )


# --- Backward-compatible routes: redirect old page URLs to the matching anchor ---
@app.route("/about")
def about():
    return redirect(url_for("home") + "#about")


@app.route("/skills")
def skills():
    return redirect(url_for("home") + "#skills")


@app.route("/projects")
def projects():
    return redirect(url_for("home") + "#projects")


@app.route("/experience")
def experience():
    return redirect(url_for("home") + "#experience")


@app.route("/education")
def education():
    return redirect(url_for("home") + "#education")


@app.route("/resume")
def resume():
    return redirect(url_for("home") + "#resume")


@app.route("/contact")
def contact():
    return redirect(url_for("home") + "#contact")


# --- Project detail keeps its own page for the deep view ---
@app.route("/projects/<slug>")
def project_detail(slug):
    project = next((p for p in PROJECTS if p["slug"] == slug), None)
    if project is None:
        return render_template("404.html"), 404
    return render_template("project_detail.html", project=project, active="projects")


@app.route("/resume/download")
def resume_download():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        PROFILE["resume_file"],
        as_attachment=True,
    )


@app.route("/contact/submit", methods=["POST"])
def contact_submit():
    name = request.form.get("name", "").strip()
    # In a real deployment this would send an email or store the message.
    flash(f"Thanks {name or 'there'}! Your message has been received.", "success")
    return redirect(url_for("home") + "#contact")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Local dev runs on port 5000 with debug on. Hosting platforms set $PORT and
    # run the app via gunicorn (see Procfile), so this block is dev-only.
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
