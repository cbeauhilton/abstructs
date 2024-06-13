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

## Database

Database operations are handled in `database.py`. This file contains the setup and interaction logic for the database. To initialize the database, the `init_db` function is called on startup.

### Example Models

```python
from sqlmodel import Field, SQLModel

class StructuredResponse(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    Diagnosis: str
    # ... other fields ...
```

## Running the Application

To run the FastAPI application, execute the following command:

```bash
uvicorn main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

## Endpoints

### `/structured-response/json`

Create a structured response from a URL.

**POST** `/structured-response/json`

#### Request Body

```json
{
    "url": "string"
}
```

#### Response

```json
{
    "id": 1,
    "Diagnosis": "string",
    // ... other fields ...
}
```


## Contributing

Fork and PR, you know the drill.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
