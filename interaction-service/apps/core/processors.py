from abc import abstractmethod
import json
from typing import Any


class AbstractBaseStreamEventProcessor:

    def __init__(self, raw_message: list[list[tuple[str, dict]]]) -> None:
        self._raw_message = raw_message
        self._extracted_messages = self._extract_messages()
        self._messages = self.get_decoded_messages()

    def _extract_messages(self) -> list[dict | None]:
        extracted_messages = []
        try:
            for item in self._raw_message[0][1]:
                _, extracted_message = item
                extracted_messages.append(extracted_message)

        except IndexError:
            pass
        return extracted_messages

    def get_decoded_messages(self) -> list[dict | None]:
        return [json.loads(message.get("message")) for message in self._extracted_messages]

    @abstractmethod
    async def process(self) -> Any:
        raise NotImplementedError
