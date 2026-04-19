from typing import Any, Optional
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.sdk_config import SdkConfig
from ..net.environment.environment import Environment
from ..models.utils.cast_models import cast_models
from ..models import Grade


class GradesService(BaseService):
    """
    Service class for GradesService operations.
    Provides methods to interact with GradesService-related API endpoints.
    Inherits common functionality from BaseService including authentication and request handling.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the service and method-level configurations."""
        super().__init__(*args, **kwargs)
        self._create_grades_config: SdkConfig = {}

    def set_create_grades_config(self, config: SdkConfig):
        """
        Sets method-level configuration for create_grades.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._create_grades_config = config
        return self

    @cast_models
    def create_grades(
        self, request_body: Grade, *, request_config: Optional[SdkConfig] = None
    ) -> None:
        """create_grades

        :param request_body: The request body.
        :type request_body: Grade
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(Grade).validate(request_body)

        resolved_config = self._get_resolved_config(
            self._create_grades_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/grades",
                [self.get_api_key(resolved_config)],
                resolved_config,
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        self.send_request(serialized_request)
