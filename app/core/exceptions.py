"""Custom exceptions for application-level error handling."""

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base class for custom app exceptions."""

    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(status_code=status_code, detail=detail)


class UploadAudioException(AppException):
    """Raised when there is a failure uploading the audio to storage."""

    def __init__(self, detail: str = "Error uploading audio file"):
        super().__init__(
            detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class AnalyzeAudioException(AppException):
    """Raised when the audio analysis service fails."""

    def __init__(self, detail: str = "Error analyzing the audio"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_502_BAD_GATEWAY,
        )


class InvalidAudioFormatException(AppException):
    """Raised when the uploaded audio file is in an unsupported format."""

    def __init__(
        self,
        detail: str = "Invalid file type. Accepted formats: .mp3, .wav",
    ):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UnexpectedAppException(AppException):
    """Raised when an unexpected, uncaught error occurs."""

    def __init__(self, detail: str = "Unexpected internal error"):
        super().__init__(
            detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
