import os
import argparse
import regex

from donki.notifications import NotificationParser
from donki.repository import NotificationsRepository

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)
API_KEY = os.getenv("API_KEY", "12345")


def parse_date_arguments():
    correct_date_form = "([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
    parser = argparse.ArgumentParser(description="Start and End Date Parser")
    parser.add_argument(
        "start_date", type=str,
        help="Start date for data ingestion")
    parser.add_argument(
        "end_date", type=str,
        help="End date for data ingestion")
    args = parser.parse_args()
    start_date, end_date = args.start_date, args.end_date
    if regex.match(correct_date_form, start_date) is None:
        parser.error("'start_date' has incorrect date form, the correct version"
                     " is %Y-%m-%d")
    if regex.match(correct_date_form, end_date) is None:
        parser.error("'end_date' has incorrect date form, the correct version"
                     " is %Y-%m-%d")
    return start_date, end_date


if __name__ == "__main__":

    start_date, end_date = parse_date_arguments()

    donki_parser = NotificationParser(
        start_date=start_date,
        end_date=end_date,
        api_key=API_KEY
    )

    notifications = donki_parser.create_message_dictionary()
    notifications_as_dict = list(map(lambda n: n.dict(), notifications))

    notifications_repository = NotificationsRepository(
        host=MONGO_HOST,
        port=MONGO_PORT
    )

    notifications_repository.insert_many(notifications_as_dict)
