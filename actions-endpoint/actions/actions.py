# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/core/customactions/#custom-actions-written-in-python


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# import cx_Oracle

# Connect to oracle database
# connection = cx_Oracle.connect("apps", "apps", "vision.ncbs.com/VIS")


class ActionOnhandQuantity(Action):

    def name(self) -> Text:
        return "action_onhand_quantity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cursor = connection.cursor()
        cursor.execute("select transaction_id from mtl_material_transactions where rownum = 1")

        for transaction_id in cursor:
            dispatcher.utter_message("Transaction ID is {}".format(transaction_id))

        #dispatcher.utter_message("My first action ")

        return []


import requests
import json

from pymongo import MongoClient
client = MongoClient('mongodb', 27017)
db = client['eva_platform']



import logging
logger = logging.getLogger(__name__)


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("My first action")

        return []

class ActionGrievanceDepartment(Action):

    def name(self) -> Text:
        return "action_grievance_department"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        complainant_name = tracker.get_slot('complainant_name')
        complainant_city = tracker.get_slot('complainant_city')
        complainant_mobile = tracker.get_slot('complainant_mobile')
        complainant_email = tracker.get_slot('complainant_email')
        latest_intent_name = tracker.latest_message['intent'].get('name')
        grievance_issue = tracker.get_slot(latest_intent_name)
        insert_record = {
            "sender_id": tracker.sender_id,
            "complainant_name": complainant_name,
            "complainant_city": complainant_city,
            "complainant_mobile": complainant_mobile,
            "complainant_email": complainant_email,
            "ministry_department": latest_intent_name.replace('_', ' '),
            "grievance_issue": grievance_issue
            }

        insert_result = db.grievance.insert_one(json.loads(json.dumps(insert_record)))
        dispatcher.utter_message("Your grievance for "+ latest_intent_name.replace('_', ' ') +" department has been logged.")
        return []
