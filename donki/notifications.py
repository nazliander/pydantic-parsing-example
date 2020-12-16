from datetime import datetime
import requests
from typing import List

from donki.models import NotificationMessageBody, NotificationMessage


class NotificationParser:

    def __init__(self, start_date, end_date, api_key):

        self.start_date = start_date
        self.end_date = end_date
        self.api_key = api_key
        self.now = datetime.utcnow()

    def _seperate_message_parts(self, notification: dict) -> list:
        return [
            f"message_type_abbreviation : {notification['messageType']}",
            f"message_url : {notification['messageURL']}",
            f"message_body : {notification['messageBody']}"
        ]

    def _exclude_small_messages(self, message_part: str) -> bool:
        return len(message_part) > 2

    def _trim_message_text(self, message_text: str) -> str:
        return message_text.strip()

    def _key_parse(self, dict_key: str) -> str:
        return dict_key.lower().strip().replace(" ", "_")

    def _exclude_certain_chars(self, message_text: str) -> str:
        return ' '.join(filter(None, message_text.strip().split()))

    def _parse_messages(self, notifications: list) -> List[List[str]]:

        return [list(map(self._trim_message_text, filter(self._exclude_small_messages, message)))
                for message in list(map(self._seperate_message_parts, notifications))]

    def _get_base_url(self):
        return ("https://api.nasa.gov/DONKI/notifications?"
                f"startDate={self.start_date}&endDate={self.end_date}"
                f"&type=all&api_key={self.api_key}")

    def _request_donki_notifications(self) -> str:
        base_url = self._get_base_url()
        try:
            return eval(requests.get(base_url).text)
        except Exception as e:
            return None

    def _message_body_parser(self,
                             message_body_list: List[str]) -> dict:
        message_dict = {}
        for message_text in message_body_list:
            message_pair = message_text.split(":", 1)
            if len(message_pair) >= 2:
                parsed_key = self._key_parse(message_pair[0])
                if parsed_key == "message_issue_date":
                    message_dict[parsed_key] = self._exclude_certain_chars(
                        ":".join(message_pair[1:])
                        .replace("T", " ")
                        .replace("Z", ""))
                    continue
                message_dict[parsed_key] = self._exclude_certain_chars(
                    " ".join(message_pair[1:]).strip())
        return NotificationMessageBody(**message_dict)

    def create_message_dictionary(self) -> List[dict]:

        notifications = self._request_donki_notifications()

        if notifications is None:
            return []

        messages = self._parse_messages(notifications)

        message_list_of_dict = []

        for message in messages:
            message_dict = {"insertion_date": self.now}
            for message_text in message:
                message_pair = message_text.split(":", 1)
                if len(message_pair) >= 2:
                    parsed_key = self._key_parse(message_pair[0])
                    if parsed_key == "message_body":
                        message_dict[parsed_key] = self._message_body_parser(
                            " ".join(message_pair[1:]).strip().split('\n##'))
                        continue
                    message_dict[parsed_key] = self._exclude_certain_chars(
                        " ".join(message_pair[1:]).strip())

            message_list_of_dict.append(
                NotificationMessage(**message_dict))

        return message_list_of_dict
