from fastapi.templating import Jinja2Templates
from abstructs.config import settings


def get_templates() -> Jinja2Templates:
    return Jinja2Templates(directory=settings.TEMPLATES_DIR)


print(settings.TEMPLATES_DIR)
