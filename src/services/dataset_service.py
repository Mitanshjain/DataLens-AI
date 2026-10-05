# ==========================================
# DATALENS AI - DATASET SERVICE V3
# ==========================================

import json

from pathlib import Path
from uuid import UUID, uuid4

import pandas as pd

from fastapi import UploadFile


# ==========================================
# UPLOAD DIRECTORY
# ==========================================

UPLOAD_DIRECTORY = Path(
    "data/uploads"
)

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# ALLOWED FILE TYPES
# ==========================================

ALLOWED_EXTENSIONS = {
    ".csv"
}


# ==========================================
# VALIDATE UPLOADED FILE
# ==========================================

def validate_uploaded_file(
    file: UploadFile
):
    """
    Validate basic uploaded-file information.

    DataLens currently supports CSV files only.
    """

    if not file.filename:

        raise ValueError(
            "Uploaded file does not have a filename."
        )


    extension = (
        Path(file.filename)
        .suffix
        .lower()
    )


    if extension not in ALLOWED_EXTENSIONS:

        raise ValueError(
            "Unsupported file type. "
            "DataLens currently supports CSV files only."
        )


    return extension


# ==========================================
# VALIDATE DATAFRAME STRUCTURE
# ==========================================

def validate_dataframe_structure(
    df: pd.DataFrame
):
    """
    Validate the basic structure of a parsed
    CSV dataset.

    This function does NOT modify the dataset.
    """

    # --------------------------------------
    # COLUMN CHECK
    # --------------------------------------

    if len(df.columns) == 0:

        raise ValueError(
            "Uploaded CSV does not contain any columns."
        )


    # --------------------------------------
    # ROW CHECK
    # --------------------------------------

    if df.empty:

        raise ValueError(
            "Uploaded CSV does not contain any data rows."
        )


    # --------------------------------------
    # DUPLICATE COLUMN NAMES
    # --------------------------------------

    duplicate_columns = (
        df.columns[
            df.columns.duplicated()
        ]
        .tolist()
    )


    if duplicate_columns:

        raise ValueError(
            "Uploaded CSV contains duplicate column "
            f"names: {duplicate_columns}"
        )


    # --------------------------------------
    # EMPTY COLUMN NAMES
    # --------------------------------------

    empty_column_names = [
        column
        for column in df.columns
        if not str(column).strip()
    ]


    if empty_column_names:

        raise ValueError(
            "Uploaded CSV contains one or more "
            "columns without a valid name."
        )


    return True


# ==========================================
# SAVE UPLOADED DATASET
# ==========================================

async def save_uploaded_dataset(
    file: UploadFile
):
    """
    Save uploaded CSV using a UUID.

    Dataset metadata is stored separately
    so the original filename can be
    recovered later.

    The original dataset is preserved.
    """

    extension = (
        validate_uploaded_file(
            file
        )
    )


    # --------------------------------------
    # GENERATE DATASET ID
    # --------------------------------------

    dataset_id = str(
        uuid4()
    )


    # --------------------------------------
    # STORAGE PATHS
    # --------------------------------------

    file_path = (
        UPLOAD_DIRECTORY
        / f"{dataset_id}{extension}"
    )


    metadata_path = (
        UPLOAD_DIRECTORY
        / f"{dataset_id}.json"
    )


    # --------------------------------------
    # READ UPLOADED FILE
    # --------------------------------------

    content = await file.read()


    if not content:

        raise ValueError(
            "Uploaded CSV file is empty."
        )


    # --------------------------------------
    # SAVE CSV
    # --------------------------------------

    try:

        with open(
            file_path,
            "wb"
        ) as destination:

            destination.write(
                content
            )

    except Exception as error:

        raise RuntimeError(
            f"Could not save uploaded dataset: {error}"
        ) from error


    # --------------------------------------
    # READ / VALIDATE CSV
    # --------------------------------------

    try:

        df = pd.read_csv(
            file_path
        )

    except Exception as error:

        if file_path.exists():
            file_path.unlink()

        raise ValueError(
            "Uploaded file is not a valid "
            f"readable CSV: {error}"
        ) from error


    # --------------------------------------
    # VALIDATE DATAFRAME STRUCTURE
    # --------------------------------------

    try:

        validate_dataframe_structure(
            df
        )

    except ValueError:

        if file_path.exists():
            file_path.unlink()

        raise


    # --------------------------------------
    # DATASET METADATA
    # --------------------------------------

    metadata = {

        "dataset_id":
            dataset_id,

        "filename":
            file.filename,

        "stored_filename":
            file_path.name,

        "rows":
            int(len(df)),

        "columns":
            int(len(df.columns))
    }


    # --------------------------------------
    # SAVE METADATA
    # --------------------------------------

    try:

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as metadata_file:

            json.dump(
                metadata,
                metadata_file,
                indent=4
            )

    except Exception as error:

        if file_path.exists():
            file_path.unlink()

        if metadata_path.exists():
            metadata_path.unlink()

        raise RuntimeError(
            f"Could not save dataset metadata: {error}"
        ) from error


    # ======================================
    # RESPONSE
    # ======================================

    return {

        "dataset_id":
            dataset_id,

        "filename":
            file.filename,

        "file_path":
            str(file_path),

        "rows":
            int(len(df)),

        "columns":
            int(len(df.columns)),

        "column_names":
            df.columns.tolist()
    }


# ==========================================
# VALIDATE DATASET ID
# ==========================================

def validate_dataset_id(
    dataset_id: str
):
    """
    Validate UUID-based dataset ID.
    """

    try:

        return str(
            UUID(dataset_id)
        )

    except (
        ValueError,
        TypeError,
        AttributeError
    ):

        raise ValueError(
            "Invalid dataset ID."
        )


# ==========================================
# GET DATASET FILE PATH
# ==========================================

def get_dataset_path(
    dataset_id: str
):
    """
    Resolve dataset ID to its stored
    CSV path.
    """

    validated_dataset_id = (
        validate_dataset_id(
            dataset_id
        )
    )


    file_path = (
        UPLOAD_DIRECTORY
        / f"{validated_dataset_id}.csv"
    )


    if not file_path.exists():

        raise FileNotFoundError(
            "Dataset was not found."
        )


    return file_path


# ==========================================
# GET DATASET METADATA
# ==========================================

def get_dataset_metadata(
    dataset_id: str
):
    """
    Load metadata associated with a
    stored dataset.
    """

    validated_dataset_id = (
        validate_dataset_id(
            dataset_id
        )
    )


    metadata_path = (
        UPLOAD_DIRECTORY
        / f"{validated_dataset_id}.json"
    )


    if not metadata_path.exists():

        raise FileNotFoundError(
            "Dataset metadata was not found."
        )


    try:

        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as metadata_file:

            metadata = json.load(
                metadata_file
            )

    except Exception as error:

        raise RuntimeError(
            f"Could not read dataset metadata: {error}"
        ) from error


    return metadata


# ==========================================
# GET DATASET INFORMATION
# ==========================================

def get_dataset_info(
    dataset_id: str
):
    """
    Return stored dataset information
    required by the frontend.
    """

    file_path = (
        get_dataset_path(
            dataset_id
        )
    )


    metadata = (
        get_dataset_metadata(
            dataset_id
        )
    )


    try:

        df = pd.read_csv(
            file_path
        )

    except Exception as error:

        raise RuntimeError(
            f"Could not read stored dataset: {error}"
        ) from error


    validate_dataframe_structure(
        df
    )


    return {

        "dataset_id":
            dataset_id,

        "filename":
            metadata["filename"],

        "file_path":
            str(file_path),

        "rows":
            int(len(df)),

        "columns":
            int(len(df.columns)),

        "column_names":
            df.columns.tolist()
    }