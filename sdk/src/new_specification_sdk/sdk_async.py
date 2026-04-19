from typing import Union
from .net.environment import Environment
from .sdk import NewSpecificationSdk
from .services.async_.students import StudentsServiceAsync
from .services.async_.grades import GradesServiceAsync


class NewSpecificationSdkAsync(NewSpecificationSdk):
    """
    NewSpecificationSdkAsync is the asynchronous version of the NewSpecificationSdk SDK Client.
    """

    def __init__(
        self,
        api_key: str = None,
        api_key_header: str = "X-API-KEY",
        base_url: Union[Environment, str, None] = None,
        timeout: int = 60000,
    ):
        super().__init__(
            api_key=api_key,
            api_key_header=api_key_header,
            base_url=base_url,
            timeout=timeout,
        )

        self.students = StudentsServiceAsync(base_url=self._base_url)
        self.grades = GradesServiceAsync(base_url=self._base_url)
