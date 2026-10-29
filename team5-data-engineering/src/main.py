
import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.data_validator import validate_csv

load_dotenv()

app = FastAPI(
    title="Team 5 Data Engineering API",
    description="API for dataset validation and profiling",
    version="1.0.0",
)


class DatasetReference(BaseModel):
    dataset_id: str = Field(min_length=1)


class ProfileRequest(BaseModel):
    dataset_reference: DatasetReference
    expected_types: dict[str, str] = Field(default_factory=dict)


def get_dataset_metadata(dataset_id: str):
    try:
        with psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT dataset_id, dataset_name, file_path, file_format
                    FROM dataset_metadata
                    WHERE dataset_id = %s
                    """,
                    (dataset_id,),
                )
                return cursor.fetchone()

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve dataset metadata from the database.",
        )


@app.get("/health")
def health_check():
    return {
        "status": "success",
        "message": "Team 5 Data Engineering API is running",
    }


@app.post("/api/v1/datasets/profile")
def profile_dataset(request: ProfileRequest):
    dataset_id = request.dataset_reference.dataset_id

    metadata = get_dataset_metadata(dataset_id)

    if metadata is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )

    dataset_id, dataset_name, file_path, file_format = metadata

    if file_format.lower() != "csv":
        raise HTTPException(
            status_code=400,
            detail="Only CSV datasets are supported.",
        )

    validation_result = validate_csv(
        file_path,
        expected_types=request.expected_types
    )

    return {
        "status": validation_result["api_status"],
        "dataset_id": dataset_id,
        "dataset_name": dataset_name,
        "validation": validation_result,
    }
