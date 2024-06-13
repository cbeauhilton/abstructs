import instructor
from abstructs.config import settings
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine

db_url = f"sqlite+{settings.TURSO_DATABASE_URL}/?authToken={settings.TURSO_AUTH_TOKEN}&secure=true"
# db_url = "sqlite:///cache.db"

engine = create_engine(db_url, connect_args={"check_same_thread": False}, echo=True)


class URLRequest(BaseModel):
    url: str


class StructuredResponse(SQLModel, instructor.OpenAISchema):
    """
    A response model for summarizing clinical trial data from an abstract.
    This model is intended for use by oncologists to provide clear, structured information extracted from the abstract text.

    System Prompt: Extract the following fields from the provided abstract text. If a concept is not present in the abstract, leave the field empty.
    """

    id: int | None = Field(default=None, primary_key=True)
    Diagnosis: str = Field(
        "",
        description="The type of cancer or condition being diagnosed or treated, including stage or descriptor if available (e.g., recurrent, unresectable, metastatic, localized, etc.). Example: 'Non-small cell lung cancer, metastatic'.",
    )
    Drugs: str = Field(
        "",
        description="The drugs studied in the trial, including their names and dosages. Example: 'Pembrolizumab 200 mg'.",
    )
    Line_of_therapy: str = Field(
        "",
        description="The stage of treatment in which the drug or regimen is being used (e.g., first-line, second-line, adjuvant, neoadjuvant). Example: 'First-line therapy'.",
    )
    Regimen: str = Field(
        "",
        description="The treatment plan including the schedule of administration of drugs. Example: 'Pembrolizumab every 3 weeks with carboplatin and pemetrexed'.",
    )
    Primary_End_Point: str = Field(
        "",
        description="The main outcome that is being measured in the trial to determine the effectiveness of the treatment. Example: 'Overall survival'.",
    )
    Secondary_End_Point: str = Field(
        "",
        description="Additional outcomes measured in the trial to evaluate other effects of the treatment. Example: 'Progression-free survival'.",
    )
    Competitor_arm: str = Field(
        "",
        description="Details about the control or comparison group in the trial. Example: 'Standard chemotherapy regimen'.",
    )
    Efficacy: str = Field(
        "",
        description="Results related to the effectiveness of the treatment. Example: 'The treatment resulted in a 30% increase in overall survival compared to the control group'.",
    )
    Response_Types: str = Field(
        "",
        description="Types of responses observed in patients (e.g., partial response, complete response). Example: '10% complete response, 20% partial response'.",
    )
    Time_to_Response: str = Field(
        "",
        description="The duration it takes for patients to exhibit a response to the treatment. Example: 'Median time to response was 8 weeks'.",
    )
    Surveillance: str = Field(
        "",
        description="Monitoring and follow-up strategies used in the trial, specifying the type of surveillance if known (e.g., PET-CT, specific tumor markers). Example: 'Patients were followed up every 3 months for 2 years with PET-CT scans'.",
    )
    Subsets: str = Field(
        "",
        description="Specific subgroups of patients analyzed in the trial. Example: 'Patients with PD-L1 expression ≥ 50%'.",
    )
    Adverse_Events: str = Field(
        "",
        description="Side effects or adverse reactions observed during the trial, including percentages and grades if available. Example: 'Common adverse events included fatigue (30%, Grade 2), nausea (20%, Grade 1), and rash (10%, Grade 3)'.",
    )
    Trial_Name: str = Field(
        "",
        description="The name or identifier of the clinical trial. Example: 'KEYNOTE-189'.",
    )
    Others: str = Field(
        "",
        description="Any additional relevant information not covered by other fields, including the NCT number if available. Example: 'The trial also assessed quality of life and patient-reported outcomes. NCT number: NCT03158883'.",
    )
    Conclusion: str = Field(
        "",
        description="The overall findings and conclusions drawn from the trial. Example: 'Pembrolizumab combined with chemotherapy significantly improves survival in NSCLC patients'.",
    )


# class StructuredResponse(SQLModel, instructor.OpenAISchema):
#     id: int | None = Field(default=None, primary_key=True)
#     Diagnosis: str
#     Drugs: str
#     Line_of_therapy: str
#     Regimen: str
#     Primary_End_Point: str
#     Secondary_End_Point: str
#     Competitor_arm: str
#     Efficacy: str
#     Response_Types: str
#     Time_to_Response: str
#     Surveillance: str
#     Subsets: str
#     Adverse_Events: str
#     Trial_Name: str
#     Others: str
#     Conclusion: str


class StructuredResponseWithURL(StructuredResponse, table=True):
    url: str
    doi: str


SQLModel.metadata.create_all(engine)
