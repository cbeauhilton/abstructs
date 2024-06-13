# Abstructs

---

Disclaimer: ChatGPT wrote most of this readme. 
I added very little manually.
It's a placeholder based on passing in some of the files as of 2024-06-13.

---

Abstructs is a Python-based application using FastAPI and LLMs
to generate structured summaries of clinical trial data from abstracts. 
The application interacts with various language model clients, manages configurations, and handles database operations.

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

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
