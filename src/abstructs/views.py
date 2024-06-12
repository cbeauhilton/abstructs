from fastapi import APIRouter

from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.events import GoToEvent, PageEvent
from abstruct.models import SummaryResponse, URLRequest

router = APIRouter()


@router.get("/summary", response_model=FastUI, response_model_exclude_none=True)
def summary_view() -> list[c.AnyComponent]:
    return [
        c.PageTitle(text="Article Summary"),
        c.Navbar(
            title="Article Summary",
            start_links=[
                c.Link(
                    components=[c.Text(text="Home")],
                    on_click=GoToEvent(url="/"),
                    active="startswith:/",
                ),
            ],
        ),
        c.Page(
            components=[
                c.Heading(text="Enter Article URL"),
                c.ModelForm(
                    model=URLRequest,
                    submit_url="/process_url",
                    method="POST",
                    display_mode="inline",
                ),
                # c.ServerLoad(
                #     path="/summary_result",
                #     load_trigger=PageEvent(name="submit-form"),
                # ),
            ],
        ),
    ]


@router.get("/summary_result", response_model=FastUI, response_model_exclude_none=True)
def summary_result(summary: SummaryResponse) -> list[c.AnyComponent]:
    return [
        c.Page(
            components=[
                c.Heading(text="Article Summary"),
                c.Details(data=summary),
            ],
        ),
    ]


@router.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI Demo"))
