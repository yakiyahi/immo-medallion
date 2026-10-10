"""Configuration MinIO partagée par tous les scripts du projet."""
import os
import sys
from pathlib import Path

import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

BUCKETS = ["bronze", "silver", "gold"]
REGION = "us-east-1"


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        sys.exit(f"Variable {name} manquante : copie .env.example en .env et renseigne-la.")
    return value


ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
ACCESS_KEY = _require("MINIO_ROOT_USER")
SECRET_KEY = _require("MINIO_ROOT_PASSWORD")


def s3_client():
    """Client boto3 pointant sur MinIO."""
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION,
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )


def delta_storage_options() -> dict:
    """Options pour écrire/lire des tables Delta sur MinIO."""
    return {
        "AWS_ACCESS_KEY_ID": ACCESS_KEY,
        "AWS_SECRET_ACCESS_KEY": SECRET_KEY,
        "AWS_ENDPOINT_URL": ENDPOINT,
        "AWS_REGION": REGION,
        "AWS_ALLOW_HTTP": "true",             # MinIO local en HTTP
        "AWS_S3_ALLOW_UNSAFE_RENAME": "true", # écrivain unique en local
    }