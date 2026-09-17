from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time

from models import ResumePayload
from ai_polisher import STARBulletPolisher
from pdf_renderer import HTMLPDFResumeRenderer

app = FastAPI(
    title="ResumeForge-API",
    description="Enterprise-Grade Async Resume & Portfolio Generation Microservice",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

polisher = STARBulletPolisher()
renderer = HTMLPDFResumeRenderer()

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "ResumeForge-API", "timestamp": time.time()}

@app.post("/api/v1/resume/validate", tags=["Validation"])
async def validate_resume_payload(payload: ResumePayload):
    """
    Validates incoming JSON resume payload against strict Pydantic v2 schema rules.
    """
    return {
        "status": "VALIDATED",
        "message": "Payload conforms strictly to Pydantic v2 schemas.",
        "payload_summary": {
            "candidate_name": payload.personal_info.full_name,
            "experience_count": len(payload.experience),
            "skills_categories": len(payload.skills)
        }
    }

@app.post("/api/v1/resume/polish-bullet", tags=["AI Microservice"])
async def polish_bullet_point(raw_bullet: str, target_job_description: str = ""):
    """
    GenAI Bullet Polisher: Uses STAR methodology to rewrite raw achievement bullets.
    """
    result = polisher.polish_bullet(raw_bullet, target_job_description)
    return result

@app.post("/api/v1/resume/generate", tags=["PDF & HTML Render"])
async def generate_resume_document(payload: ResumePayload, format_type: str = "html"):
    """
    Async document compilation endpoint. Injects validated Pydantic model into Jinja2 HTML template.
    """
    try:
        html_content = renderer.render_html(payload.model_dump())
        if format_type == "json":
            return JSONResponse(content={"html": html_content, "payload": payload.model_dump()})
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate resume: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
