from pymongo import MongoClient


class NotificationsRepository:

    def __init__(self, host, port):
        mongo_client = MongoClient(host=host, port=port)
        donki_db = mongo_client.donki
        self.notifications_collection = donki_db.notifications

    def insert(self, notification):
        return self.notifications_collection.insert_one(notification)

    def insert_many(self, notifications):
        return self.notifications_collection.insert_many(notifications)

    def read_many(self, conditions):
        return self.notifications_collection.find(conditions)
