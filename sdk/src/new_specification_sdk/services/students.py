from typing import Any, Optional, List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.sdk_config import SdkConfig
from ..net.environment.environment import Environment
from ..models.utils.cast_models import cast_models
from ..models import Student


class StudentsService(BaseService):
    """
    Service class for StudentsService operations.
    Provides methods to interact with StudentsService-related API endpoints.
    Inherits common functionality from BaseService including authentication and request handling.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the service and method-level configurations."""
        super().__init__(*args, **kwargs)
        self._get_students_config: SdkConfig = {}
        self._create_students_config: SdkConfig = {}

    def set_get_students_config(self, config: SdkConfig):
        """
        Sets method-level configuration for get_students.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._get_students_config = config
        return self

    def set_create_students_config(self, config: SdkConfig):
        """
        Sets method-level configuration for create_students.

        :param SdkConfig config: Configuration dictionary to override service-level defaults.
        :return: The service instance for method chaining.
        """
        self._create_students_config = config
        return self

    @cast_models
    def get_students(
        self, *, request_config: Optional[SdkConfig] = None
    ) -> List[Student]:
        """get_students

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: List[Student]
        """

        resolved_config = self._get_resolved_config(
            self._get_students_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/students",
                [self.get_api_key(resolved_config)],
                resolved_config,
            )
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return [Student.model_validate(item) for item in response]

    @cast_models
    def create_students(
        self, request_body: Student, *, request_config: Optional[SdkConfig] = None
    ) -> None:
        """create_students

        :param request_body: The request body.
        :type request_body: Student
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(Student).validate(request_body)

        resolved_config = self._get_resolved_config(
            self._create_students_config, request_config
        )

        serialized_request = (
            Serializer(
                f"{resolved_config.get('base_url') or self.base_url or Environment.DEFAULT.url}/students",
                [self.get_api_key(resolved_config)],
                resolved_config,
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        self.send_request(serialized_request)
