import instructor
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine

engine = create_engine("sqlite:///cache.db")


class URLRequest(BaseModel):
    url: str


class StructuredResponse(SQLModel, instructor.OpenAISchema):
    id: int | None = Field(default=None, primary_key=True)
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


class StructuredResponseWithURL(StructuredResponse, table=True):
    url: str  # = Field(unique=True)


SQLModel.metadata.create_all(engine)
