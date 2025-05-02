"""Enumeration classes for various statuses."""

from enum import Enum


class AnalysisStatus(str, Enum):
    processing = "processing"
    completed = "completed"
    failed = "failed"
