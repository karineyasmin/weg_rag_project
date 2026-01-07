from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    Data model for user questions.
    """

    question: str = Field(..., example="What is the power of consumption of the motor?")


class QuestionResponse(BaseModel):
    """
    Data model for the LLM's response including references.
    """

    answer: str = Field(..., example="The motor's power consumption is 2.3 kw.")
    references: list[str] = Field(
        ..., example=["the motor xxx requires 2.3kw to operate"]
    )


class DocumentResponse(BaseModel):
    """
    Data model for the response after processing documents.
    """

    message: str = Field(..., example="Documents processed successfully")
    documents_indexed: int
    total_chunks: int
