from typing import Awaitable, Optional, List
from .utils.to_async import to_async
from ..students import StudentsService
from ...net.sdk_config import SdkConfig
from ...models import Student


class StudentsServiceAsync(StudentsService):
    """
    Async Wrapper for StudentsServiceAsync
    """

    def get_students(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[List[Student]]:
        return to_async(super().get_students)(request_config=request_config)

    def create_students(
        self, request_body: Student, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[None]:
        return to_async(super().create_students)(
            request_body, request_config=request_config
        )
