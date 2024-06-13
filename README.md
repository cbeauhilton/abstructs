# abstructs

`abstructs` is a Python-based application using FastAPI and LLMs
to generate structured summaries of clinical trial data from abstracts. 

It was inspired by the indomitable Jim Chen's Pythonista script.
## Installation

To install the required dependencies, use the following command:

```bash
poetry install
```

Ensure you have Poetry installed. If not, you can install it from [here](https://python-poetry.org/docs/#installation).

## Deployment

You'll need an API key for
[OpenAI](https://openai.com/)
or
[Groq](https://www.groq.com/)
(choose your model in the [llm_client.py](./src/abstructs/llm_client.py) file).
[Turso](https://www.turso.tech/) provides databases (free tier is plenty).
[Fly.io](https://fly.io/) provides VMs (free tier is also plenty).


## Configuration

The project configuration is managed using `config.py`. The default configuration settings include:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    TURSO_DATABASE_URL: str
    TURSO_AUTH_TOKEN: str
    PYALEX_EMAIL: str # Whatever email address you want,
    # doesn't even have to be real.
    # It's not required to use their API, but makes you a good citizen
    # and might get you slightly faster responses.
    # abstructs will error if it's not provided.

    class Config:
        env_file = ".env"

settings = Settings()
```

Make sure to update the `.env` file with your actual keys and database URL.

## Endpoints

### `/structured-response`

Create a structured response from a URL and show it on the web page.

### `/structured-response/json`

Same deal, but returns raw JSON.

## Contributing

Fork and PR, you know the drill.

## TODO

- add a dev mode flag that selects local db and uses a free LLM
- add a popout pane on the main page that lists out urls that have already been made into abstructs
- prepopulate the main page on load with a random cached abstruct
- scrape HemOnc.org for a bajillion trials and cache these (when I'm confident the LLM is doing a good enough job)
