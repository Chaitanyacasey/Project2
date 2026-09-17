from jinja2 import Template

HTML_RESUME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ payload.personal_info.full_name }} - Resume</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #1E293B;
            margin: 0;
            padding: 36px;
            background-color: #FFFFFF;
            line-height: 1.5;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #6366F1;
            padding-bottom: 14px;
            margin-bottom: 20px;
        }
        .header h1 {
            margin: 0 0 4px 0;
            font-size: 26px;
            color: #0F172A;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .contact-info {
            font-size: 13px;
            color: #475569;
        }
        .contact-info span {
            margin: 0 6px;
        }
        .section-title {
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #6366F1;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 4px;
            margin-top: 20px;
            margin-bottom: 12px;
        }
        .summary-text {
            font-size: 13.5px;
            color: #334155;
            margin-bottom: 16px;
        }
        .job-block {
            margin-bottom: 14px;
        }
        .job-header {
            display: flex;
            justify-content: space-between;
            font-size: 14px;
            font-weight: 700;
            color: #0F172A;
        }
        .job-sub {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            font-style: italic;
            color: #64748B;
            margin-bottom: 6px;
        }
        ul {
            margin: 4px 0 0 0;
            padding-left: 18px;
            font-size: 13px;
            color: #334155;
        }
        li {
            margin-bottom: 4px;
        }
        .skill-group {
            font-size: 13px;
            margin-bottom: 6px;
        }
        .skill-group strong {
            color: #0F172A;
        }
        .project-block {
            margin-bottom: 10px;
        }
        .project-title {
            font-size: 13.5px;
            font-weight: 700;
            color: #0F172A;
        }
        .tech-tag {
            font-size: 11px;
            background-color: #EEF2FF;
            color: #4F46E5;
            padding: 2px 6px;
            border-radius: 4px;
            margin-right: 4px;
        }
    </style>
</head>
<body>

    <div class="header">
        <h1>{{ payload.personal_info.full_name }}</h1>
        <div class="contact-info">
            {{ payload.personal_info.location }} | {{ payload.personal_info.phone }} | {{ payload.personal_info.email }}
            {% if payload.personal_info.linkedin %} | {{ payload.personal_info.linkedin }}{% endif %}
            {% if payload.personal_info.github %} | {{ payload.personal_info.github }}{% endif %}
        </div>
    </div>

    {% if payload.summary %}
    <div class="section-title">Professional Summary</div>
    <div class="summary-text">{{ payload.summary }}</div>
    {% endif %}

    <div class="section-title">Work Experience</div>
    {% for job in payload.experience %}
    <div class="job-block">
        <div class="job-header">
            <span>{{ job.position }}</span>
            <span>{{ job.location }}</span>
        </div>
        <div class="job-sub">
            <span>{{ job.company }}</span>
            <span>{{ job.start_date }} – {{ job.end_date }}</span>
        </div>
        <ul>
            {% for bullet in job.bullets %}
            <li>{{ bullet }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endfor %}

    {% if payload.projects %}
    <div class="section-title">Key Engineering Projects</div>
    {% for proj in payload.projects %}
    <div class="project-block">
        <div class="project-title">
            {{ proj.title }}
            {% for tag in proj.tech_stack %}
            <span class="tech-tag">{{ tag }}</span>
            {% endfor %}
        </div>
        <div style="font-size: 13px; color: #334155; margin-top: 2px;">{{ proj.description }}</div>
    </div>
    {% endfor %}
    {% endif %}

    <div class="section-title">Technical Skills</div>
    {% for cat in payload.skills %}
    <div class="skill-group">
        <strong>{{ cat.category_name }}:</strong> {{ cat.skills | join(', ') }}
    </div>
    {% endfor %}

    <div class="section-title">Education</div>
    {% for edu in payload.education %}
    <div class="job-block">
        <div class="job-header">
            <span>{{ edu.institution }}</span>
            <span>{{ edu.graduation_year }}</span>
        </div>
        <div class="job-sub">
            <span>{{ edu.degree }} in {{ edu.field_of_study }}</span>
            {% if edu.gpa %}<span>GPA: {{ edu.gpa }}</span>{% endif %}
        </div>
    </div>
    {% endfor %}

</body>
</html>
"""

class HTMLPDFResumeRenderer:
    """Renders Pydantic payload models into Jinja2 HTML/CSS ATS resumes."""
    def __init__(self):
        self.template = Template(HTML_RESUME_TEMPLATE)

    def render_html(self, payload_dict: dict) -> str:
        """Renders payload into Jinja2 ATS HTML."""
        return self.template.render(payload=payload_dict)
