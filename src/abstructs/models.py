from pydantic import BaseModel
from sqlmodel import SQLModel, Field
import instructor


class URLRequest(BaseModel):
    url: str


class StructuredResponse(SQLModel, instructor.OpenAISchema, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str = Field(unique=True)
    Diagnosis: str
    Drugs: str
    Line_of_therapy: str
    Regimen: str
    Primary_End_Point: str
    Secondary_End_Point: str
    Competitor_arm: str
    Efficacy: str
    Response_Types: str
    Time_to_Response: str
    Surveillance: str
    Subsets: str
    Adverse_Events: str
    Trial_Name: str
    Others: str
    Conclusion: str


class CachedResponse(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str = Field(unique=True)
    summary: str
