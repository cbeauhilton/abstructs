from sqlmodel import Session, select
from abstructs.database import (
    StructuredResponseWithURL,
    engine,
)
from abstructs.llm_client import get_llm_response
from abstructs.fetcher import fetch_abstract, extract_doi
from abstructs.logging_config import setup_logging
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

logger = setup_logging()
templates = Jinja2Templates(directory="src/templates")
app = FastAPI()


async def get_structured_response(url: str):
    logger.info(f"Received URL: {url}")
    # Check if a response for the given URL already exists in the database
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


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/structured-response", response_class=HTMLResponse)
async def create_structured_response(request: Request, url: str = Form(...)):
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


@app.post("/structured-response/json")
async def create_structured_response_json(url: str):
    try:
        llm_response = await get_structured_response(url)
        return JSONResponse(content=llm_response.model_dump())
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
