from abstructs.auth.auth import authenticate
from abstructs.database import StructuredResponseWithURL, engine
from abstructs.fetcher import extract_doi, fetch_abstract
from abstructs.llm_client import get_llm_response
from abstructs.logging_config import setup_logging
from abstructs.config import settings
from abstructs.templating import get_templates
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session, select

from fastapi.templating import Jinja2Templates

# templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

logger = setup_logging()
router = APIRouter()


async def get_structured_response(url: str):
    logger.info(f"Received URL: {url}")

    doi = extract_doi(url)
    with Session(engine) as session:
        statement = select(StructuredResponseWithURL).where(
            StructuredResponseWithURL.doi == doi
        )
        cached_response = session.exec(statement).first()
    if cached_response:
        llm_response = cached_response
        logger.info(f"Loaded from cache: {llm_response}")
    else:
        abstract = await fetch_abstract(url)
        llm_response = await get_llm_response(abstract)
        structured_response = StructuredResponseWithURL(
            url=url, doi=doi, **llm_response.model_dump()
        )
        with Session(engine) as session:
            session.add(structured_response)
            session.commit()
        logger.info(f"Processed Summary: {llm_response}")

    return llm_response


@router.get("/abstructs/{abstruct_id}", response_class=HTMLResponse)
async def get_abstruct(
    request: Request,
    abstruct_id: int,
    templates: Jinja2Templates = Depends(get_templates),
):
    with Session(engine) as session:
        abstruct = session.get(StructuredResponseWithURL, abstruct_id)
    if not abstruct:
        raise HTTPException(status_code=404, detail="Abstruct not found")
    return templates.TemplateResponse(
        "summary.html",
        {
            "request": request,
            "summary": abstruct,
            "summary_json": abstruct.model_dump_json(),
        },
    )


@router.post("/abstructs", response_class=HTMLResponse)
async def create_abstruct(
    request: Request,
    url: str = Form(...),
    templates: Jinja2Templates = Depends(get_templates),
):
    try:
        llm_response = await get_structured_response(url)
        return templates.TemplateResponse(
            "summary.html",
            {
                "request": request,
                "summary": llm_response,
                "summary_json": llm_response.model_dump_json(),
            },
        )
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/abstructs/json")
async def create_abstruct_json(url: str):
    try:
        llm_response = await get_structured_response(url)
        return JSONResponse(content=llm_response.model_dump())
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/abstructs")
async def manually_create_or_update_abstruct(
    doi: str, abstract: str, username: str = Depends(authenticate)
):
    try:
        llm_response = await get_llm_response(abstract)

        with Session(engine) as session:
            statement = select(StructuredResponseWithURL).where(
                StructuredResponseWithURL.doi == doi
            )
            db_response = session.exec(statement).first()

            if db_response:
                session.delete(db_response)
                session.commit()

            new_response = StructuredResponseWithURL(
                url="", doi=doi, **llm_response.model_dump()
            )
            session.add(new_response)
            session.commit()
            session.refresh(new_response)

            return {"message": "Abstruct updated successfully"}

    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
