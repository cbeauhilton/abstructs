from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from abstructs.templating import get_templates
from abstructs.database import StructuredResponseWithURL, engine
from abstructs.config import settings
from sqlmodel import Session, select
import random

router = APIRouter()
# templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


def get_random_summary():
    with Session(engine) as session:
        result = session.exec(select(StructuredResponseWithURL)).all()
        if result:
            return random.choice(result)
        return None


@router.get("/", response_class=HTMLResponse)
async def get_home(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
):
    summary = get_random_summary()
    with Session(engine) as session:
        abstructs = session.exec(select(StructuredResponseWithURL)).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "summary": summary,
            "summary_json": summary.model_dump_json() if summary else None,
            "abstructs": abstructs,
        },
    )
