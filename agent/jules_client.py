import os
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel
from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception,
)


class JulesAPIError(Exception):
    """Exception raised for errors in the Jules API."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class CreateCodingTaskResponse(BaseModel):
    session_id: str
    status: str


class SessionStatusResponse(BaseModel):
    session_id: str
    status: str
    details: Optional[Dict[str, Any]] = None


class ManageSessionResponse(BaseModel):
    session_id: str
    status: str
    action_taken: str


def _is_transient_error(e: BaseException) -> bool:
    if isinstance(e, httpx.HTTPStatusError):
        return e.response.status_code in (429, 500, 502, 503, 504)
    if isinstance(e, httpx.RequestError):
        return True
    return False


class JulesClient:
    BASE_URL = "https://jules.googleapis.com/v1alpha/"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("JULES_API_KEY")
        if not self.api_key:
            raise ValueError("JULES_API_KEY environment variable is not set")

        self.headers = {
            "X-Goog-Api-Key": self.api_key,
            "Content-Type": "application/json",
        }
        self.client = httpx.AsyncClient(headers=self.headers, base_url=self.BASE_URL)

    async def close(self):
        await self.client.aclose()

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=60),
        stop=stop_after_attempt(5),
        retry=retry_if_exception(_is_transient_error),
        reraise=True,
    )
    async def _execute_request(
        self, method: str, endpoint: str, **kwargs
    ) -> httpx.Response:
        response = await self.client.request(method, endpoint, **kwargs)
        response.raise_for_status()
        return response

    async def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Dict[str, Any]:
        try:
            response = await self._execute_request(method, endpoint, **kwargs)
            if response.status_code == 204:
                return {}
            return response.json()
        except httpx.HTTPStatusError as e:
            raise JulesAPIError(
                f"Jules API error: {e.response.status_code} {e.response.reason_phrase}",
                status_code=e.response.status_code,
                response_text=e.response.text,
            ) from e
        except httpx.RequestError as e:
            raise JulesAPIError(f"Jules API network error: {str(e)}") from e

    async def create_coding_task(
        self, task_description: str, repository_url: Optional[str] = None
    ) -> CreateCodingTaskResponse:
        data = {"task_description": task_description}
        if repository_url:
            data["repository_url"] = repository_url

        response_data = await self._make_request("POST", "sessions", json=data)
        return CreateCodingTaskResponse(**response_data)

    async def get_session_status(self, session_id: str) -> SessionStatusResponse:
        response_data = await self._make_request("GET", f"sessions/{session_id}")
        return SessionStatusResponse(**response_data)

    async def manage_session(
        self, session_id: str, action: str, message: Optional[str] = None
    ) -> ManageSessionResponse:
        valid_actions = {"send_message", "approve_plan", "reject_plan"}
        if action not in valid_actions:
            raise ValueError(
                f"Invalid action '{action}'. Must be one of: {valid_actions}"
            )

        data = {"action": action}
        if message:
            data["message"] = message

        response_data = await self._make_request(
            "POST", f"sessions/{session_id}:manage", json=data
        )
        return ManageSessionResponse(**response_data)

    async def delete_session(self, session_id: str) -> None:
        await self._make_request("DELETE", f"sessions/{session_id}")
