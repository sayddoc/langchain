"""Data tools for analysis and metrics generation."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from langchain_core.tools import tool


@tool
def clean_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize a list of records by removing null-only columns and duplicates."""
    if not records:
        return []

    frame = pd.DataFrame(records)
    frame = frame.drop_duplicates().dropna(axis=1, how="all")
    frame.columns = [str(column).strip().lower().replace(" ", "_") for column in frame.columns]
    return frame.fillna("").to_dict(orient="records")


@tool
def descriptive_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute basic descriptive metrics from records."""
    if not records:
        return {"row_count": 0, "column_count": 0, "numeric_summary": {}}

    frame = pd.DataFrame(records)
    numeric_frame = frame.select_dtypes(include=[np.number])

    summary = {}
    if not numeric_frame.empty:
        stats = numeric_frame.describe().to_dict()
        for column, values in stats.items():
            summary[column] = {key: float(value) for key, value in values.items()}

    return {
        "row_count": int(frame.shape[0]),
        "column_count": int(frame.shape[1]),
        "numeric_summary": summary,
    }
