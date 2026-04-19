from typing import Awaitable, Optional
from .utils.to_async import to_async
from ..grades import GradesService
from ...net.sdk_config import SdkConfig
from ...models import Grade


class GradesServiceAsync(GradesService):
    """
    Async Wrapper for GradesServiceAsync
    """

    def create_grades(
        self, request_body: Grade, *, request_config: Optional[SdkConfig] = None
    ) -> Awaitable[None]:
        return to_async(super().create_grades)(
            request_body, request_config=request_config
        )
