from bson.json_util import dumps
import json
from bson.objectid import ObjectId
from database import ConDatabase
from config import CONFIG


'''motor Mongo Db connection '''

db = ConDatabase.connect()


# noinspection PyMethodMayBeStatic
class RasaConversations:

    async def get_conversations(self, sender_id):
        print("Pulling tracker data for a conversation")

        result = await db.conversations.find_one({"sender_id": sender_id})
        return json.loads(dumps(result))


# noinspection PyMethodMayBeStatic
class RefreshDb:

    async def refresh_db(self):
        print('received request to refresh database')

        # Setting source data paths

        seed_data_path = CONFIG.get('api_gateway', 'SEED_DATA_PATH')

        # Cleaning up collections
        await db.entities.delete_many({})

        await db.projects.delete_many({})
        await db.domains.delete_many({})
        await db.intents.delete_many({})
        await db.responses.delete_many({})
        await db.stories.delete_many({})
        await db.conversations.delete_many({})
        await db.actions.delete_many({})

        # Inserting Data in collection

        with open(seed_data_path+'projects.json') as json_file:
            data = json.load(json_file)
            await db.projects.insert_many(data)

        # Get project ID

        project = await db.projects.find_one({})
        project_id = project.get('_id')
        print("project ID {}".format(project_id))

        with open(seed_data_path+'domains.json') as json_file:
            data = json.load(json_file)
            await db.domains.insert_many(data)

        await db.domains.update_many({}, {'$set': {'project_id': str(project_id)}})
        domain_id = await db.domains.find_one({})

        with open(seed_data_path+'intents.json') as json_file:
            data = json.load(json_file)
            await db.intents.insert_many(data)

        await db.intents.update_many({}, {'$set': {'project_id': str(project_id), 'domain_id': str(domain_id.get('_id'))}})

        with open(seed_data_path+'entities.json') as json_file:
            data = json.load(json_file)
            await db.entities.insert_many(data)

        await db.entities.update_many({}, {'$set': {'project_id': str(project_id)}})

        with open(seed_data_path+'responses.json') as json_file:
            data = json.load(json_file)
            await db.responses.insert_many(data)

        await db.responses.update_many({}, {'$set': {'project_id': str(project_id), 'domain_id': str(domain_id.get('_id'))}})

        with open(seed_data_path+'stories.json') as json_file:
            data = json.load(json_file)
            await db.stories.insert_many(data)

        await db.stories.update_many({}, {'$set': {'project_id': str(project_id), 'domain_id': str(domain_id.get('_id'))}})

        with open(seed_data_path+'actions.json') as json_file:
            data = json.load(json_file)
            await db.actions.insert_many(data)

        return "Success"


# noinspection PyMethodMayBeStatic
class ProjectsModel:

    def __init__(self):
        pass

    async def get_projects(self):
        cursor = db.projects.find()
        result = await cursor.to_list(length=1000)
        print("Projects sent {}".format(json.loads(dumps(result))))
        return json.loads(dumps(result))

    async def create_projects(self, record):

        json_record = json.loads(json.dumps(record))

        # Validation to check if project already exists

        val_res = await db.projects.find_one({"project_name": json_record['project_name']})

        if val_res is not None:
            print('Project already exists')
            return {"status": "Error", "message": "Project already exists"}
        else:
            result = await db.projects.insert_one(json_record)
            print("project created {}".format(result.inserted_id))
            return {"status": "Success", "message": "Project Created with ID {}".format(result.inserted_id)}

    async def delete_project(self, object_id):
        query = {"_id": ObjectId("{}".format(object_id))}

        # Delete Domains Intents , Entities , Stories , Responses

        result = await db.domains.delete_many({"project_id": object_id})
        print("Domains Deleted - count {}".format(result))

        result = await db.intents.delete_many({"project_id": object_id})
        print("Intents Deleted - count {}".format(result))

        result = await db.entities.delete_many({"project_id": object_id})
        print("Entities Deleted - count {}".format(result))

        result = await db.stories.delete_many({"project_id": object_id})
        print("Stories Deleted - count {}".format(result))

        result = await db.responses.delete_many({"project_id": object_id})
        print("Responses Deleted - count {}".format(result))

        # Delete Project
        result = await db.projects.delete_one(query)
        print("Project Deleted count {}".format(result))
        return {"status": "Success", "message": "Project Deleted Successfully"}

    async def update_project(self, record):

        json_record = json.loads(json.dumps(record))

        #val_res = await db.projects.find_one({"project_name": json_record['project_name']})
        '''
        if val_res is not None:
            print('Project already exists')
            return {"status": "Error", "message": "Project name already exists"}
        else:
            query = {"_id": ObjectId("{}".format(json_record['object_id']))}
            update_field = {"$set": {"project_description": json_record['project_description']
                                     }}
            result = await db.projects.update_one(query, update_field)
            print("Project Updated , rows modified {}".format(result))
            return {"status": "Success", "message": "Project details updated successfully "}
        '''
        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        update_field = {"$set": {"project_description": json_record['project_description']
                                 }}
        result = await db.projects.update_one(query, update_field)
        print("Project Updated , rows modified {}".format(result))
        return {"status": "Success", "message": "Project details updated successfully "}

    async def update_project_model(self, record):
        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        update_field = {"$set": {"model_name": json_record['model_name'],
                                 "state": json_record['state']
                                 }}

        res_archived = await db.projects.update_many({"state": "Published"}, {"$set": {"state": "Archived"}})
        result = await db.projects.update_one(query, update_field)

        print("Projects set to Archived state {}".format(res_archived))
        print("Project Updated , rows modified {}".format(result))
        return {"status": "Success", "message": "Model Published "}

    async def copy_project(self, record):
        json_record = json.loads(json.dumps(record))

        # check if the project name exists

        val_res = await db.projects.find_one({"project_name": json_record['project_name']})

        if val_res is not None:
            print('Project already exists')
            return {"status": "Error", "message": "Project already exists"}
        else:

            # get source project ID

            source_project = await db.projects.find_one({"project_name": json_record['source']})
            source_project_id = source_project.get('_id')
            print("Source project ID {}".format(source_project_id))

            # Create Project

            new_project = await db.projects.insert_one(json_record)
            print("project created {}".format(new_project.inserted_id))

            # Copy Entities

            entities_cursor = db.entities.find({"project_id": str(source_project_id)})
            for entity in await entities_cursor.to_list(length=100):
                del entity['_id']
                entity['project_id'] = "{}".format(new_project.inserted_id)
                new_entity = await db.entities.insert_one(entity)
                print("new entity inserted with id {}".format(new_entity.inserted_id))

            # Copy domains

            domains_cursor = db.domains.find({"project_id": str(source_project_id)})
            for domain in await domains_cursor.to_list(length=100):
                source_domain_id = domain.get('_id')
                del domain['_id']
                domain['project_id'] = "{}".format(new_project.inserted_id)
                new_domain = await db.domains.insert_one(domain)
                print("new domain inserted with id {}".format(new_domain.inserted_id))

                # Copy Intents

                intents_cursor = db.intents.find({"project_id": str(source_project_id), "domain_id": str(source_domain_id)})
                for intents in await intents_cursor.to_list(length=100):
                    del intents['_id']
                    intents['project_id'] = "{}".format(new_project.inserted_id)
                    intents['domain_id'] = "{}".format(new_domain.inserted_id)
                    new_intents = await db.intents.insert_one(intents)
                    print("new intents inserted with id {}".format(new_intents.inserted_id))

                # Copy Responses

                responses_cursor = db.responses.find({"project_id": str(source_project_id), "domain_id": str(source_domain_id)})
                for response in await responses_cursor.to_list(length=100):
                    del response['_id']
                    response['project_id'] = "{}".format(new_project.inserted_id)
                    response['domain_id'] = "{}".format(new_domain.inserted_id)
                    new_responses = await db.responses.insert_one(response)
                    print("new response inserted with id {}".format(new_responses.inserted_id))

                # Copy Stories

                stories_cursor = db.stories.find({"project_id": str(source_project_id), "domain_id": str(source_domain_id)})
                for story in await stories_cursor.to_list(length=100):
                    del story['_id']
                    story['project_id'] = "{}".format(new_project.inserted_id)
                    story['domain_id'] = "{}".format(new_domain.inserted_id)
                    new_story = await db.stories.insert_one(story)
                    print("new story inserted with id {}".format(new_story.inserted_id))

            return {"status": "Success", "message": "Project Copied ID {}".format(new_project.inserted_id)}


# noinspection PyMethodMayBeStatic
class DomainsModel:

    def __init__(self):
        pass

    async def get_domains(self, project_id):
        query = {"project_id": project_id}
        cursor = db.domains.find(query)
        result = await cursor.to_list(length=1000)
        print("Domains sent {}".format(json.loads(dumps(result))))
        return json.loads(dumps(result))

    async def create_domain(self, record):

        json_record = json.loads(json.dumps(record))

        insert_record = {"project_id": json_record['project_id'], "domain_name": json_record['domain_name'],
                         "domain_description": json_record['domain_description']}

        # Check if domain exists already

        val_res = await db.domains.find_one({"project_id": json_record['project_id'],
                                             "domain_name": json_record['domain_name']})

        if val_res is not None:
            print('Domain already exists')
            return {"status": "Error", "message": "Domain already exists"}, None
        else:
            insert_result = await db.domains.insert_one(json.loads(json.dumps(insert_record)))
            print("Domain created with ID {}".format(insert_result.inserted_id))

            domains_list = await self.get_domains(json_record['project_id'])
            return {"status": "Success", "message": "Domain created successfully"}, domains_list

    async def delete_domain(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}

        result = await db.intents.delete_many({"domain_id": json_record['object_id']})
        print("Intents Deleted - count {}".format(result))

        result = await db.stories.delete_many({"domain_id": json_record['object_id']})
        print("Stories Deleted - count {}".format(result))

        result = await db.responses.delete_many({"domain_id": json_record['object_id']})
        print("Responses Deleted - count {}".format(result))

        delete_record = await db.domains.delete_one(query)
        print("Domain Deleted count {}".format(delete_record))

        domains_list = await self.get_domains(json_record['project_id'])

        return {"status": "Success", "message": "Domain Deleted Successfully"}, domains_list

    async def update_domain(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        update_field = {"$set": {"domain_name": json_record['domain_name'],
                                 "domain_description": json_record['domain_description']}}

        # Check if Domain already exists
        val_res = await db.domains.find_one({"project_id": json_record['project_id'],
                                             "domain_name": json_record['domain_name']})

        if val_res is None:
            update_record = await db.domains.update_one(query, update_field)
            print("Domain Updated , rows modified {}".format(update_record))

            domains_list = await self.get_domains(json_record['project_id'])
            return {"status": "Success", "message": "Domain updated successfully "}, domains_list

        elif val_res['domain_name'] == json_record['domain_name']:
            print("updating domain description")

            update_record = await db.domains.update_one(query, update_field)
            print("Domain Updated , rows modified {}".format(update_record))

            domains_list = await self.get_domains(json_record['project_id'])
            return {"status": "Success", "message": "Domain updated successfully "}, domains_list

        else:
            print('Domain already exists')
            return {"status": "Error", "message": "Domain already exists"}, None


# noinspection PyMethodMayBeStatic
class IntentsModel:

    def __init__(self):
        pass

    async def get_intents(self, record):

        json_record = json.loads(json.dumps(record))

        cursor = db.intents.find(json_record, {"project_id": 1, "domain_id": 1, "intent_name": 1, "intent_description": 1})
        result = await cursor.to_list(length=1000)
        json_result = json.loads(dumps(result))
        print("Intents sent {}".format(json_result))
        return json_result

    async def create_intent(self, record):

        json_record = json.loads(json.dumps(record))

        insert_record = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id'],
                         "intent_name": json_record['intent_name'],
                         "intent_description": json_record['intent_description'], "text_entities": []}

        val_res = await db.intents.find_one({"project_id": json_record['project_id'],
                                             #"domain_id": json_record['domain_id'],
                                             "intent_name": json_record['intent_name']})

        if val_res is not None:
            print('Intent already exists')
            return {"status": "Error", "message": "Intent already exists"}, None
        else:
            result = await db.intents.insert_one(json.loads(json.dumps(insert_record)))
            message = {"status": "Success", "message": "Intent created with ID {}".format(result.inserted_id)}

            get_intents = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id']}
            intents_list = await self.get_intents(get_intents)

            return message, intents_list

    async def delete_intent(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}

        # Query to check intent   - {"story": {$elemMatch: {"key": "greet" }}}

        # check if intent exists in any story

        intent_detail = await db.intents.find_one(query)

        exists = await db.stories.find_one({"story": {"$elemMatch": {"key": intent_detail['intent_name']}}})

        if exists is None:

            result = await db.intents.delete_one(query)
            print("Intent deleted successfully {}".format(result))
            message = {"status": "Success", "message": "Intent deleted successfully "}

            get_intents = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id']}
            intents_list = await self.get_intents(get_intents)

            return message, intents_list
        else:

            message = {"status": "Error", "message": "Intent is used in a story cannot delete this intent"}
            return message, None

    async def update_intent(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        update_field = {"$set": {"intent_name": json_record['intent_name'],
                                 "intent_description": json_record['intent_description']}}

        # Check if intent already exists
        val_res = await db.intents.find_one({"project_id": json_record['project_id'],
                                             #"domain_id": json_record['domain_id'],
                                             "intent_name": json_record['intent_name']})

        if val_res is None or val_res['intent_name'] == json_record['intent_name']:

            update_record = await db.intents.update_one(query, update_field)

            print("Intent Updated , rows modified {}".format(update_record))

            get_intents = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id']}
            intents_list = await self.get_intents(get_intents)

            return {"status": "Success", "message": "Intent Updated Successfully"}, intents_list
        else:
            return {"status": "Error", "message": "Intent Name already exists"}, None

    async def get_intent_details(self, data):

        json_record = json.loads(json.dumps(data))
        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        result = await db.intents.find_one(query)
        print("Intent Details sent {}".format(json.loads(dumps(result))))
        return json.loads(dumps(result))

    async def insert_intent_detail(self, data):

        # Data format - No check for Intent already exists
        # {"object_id":"", "text":"I am in india ","entities":[{"start":8,"end":13,"value":"india","entity":"timezone"}]}

        json_record = json.loads(json.dumps(data))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}

        object_id = json_record['object_id']
        del json_record['object_id']

        result = await db.intents.update_one(query, {"$addToSet": {"text_entities": json_record}})
        print("Inserted new row in Intent {}".format(result))

        intent_detail = await self.get_intent_details({"object_id": object_id})
        print("Result of Intent Addition {}".format(result.modified_count))
        if result.modified_count == 1:
            return {"status": "Success", "message": "Intent text added "}, intent_detail
        else:
            return {"status": "Error", "message": "Intent already exists "}, intent_detail

    async def update_intent_detail(self, data):

        json_record = json.loads(json.dumps(data))

        object_id = json_record['object_id']
        index = json_record['doc_index']
        del json_record['object_id']
        del json_record['doc_index']
        query = {"_id": ObjectId("{}".format(object_id))}
        result = await db.intents.update_one(query, {"$set": {"text_entities."+index: json_record}})
        print("Record updated {}".format(result))

        intent_detail = await self.get_intent_details({"object_id": object_id})
        return {"status": "Success", "message": "Intent Updated successfully"}, intent_detail

    async def delete_intent_detail(self, data):

        # {"object_id": "", "text":"I am in india ","entities":[{"start":8,"end":13,"value":"india","entity":"timezone"}] }

        json_record = json.loads(json.dumps(data))
        object_id = json_record['object_id']
        del json_record['object_id']

        intent_detail = await self.get_intent_details({"object_id": object_id})
        print("Intent Details count {}".format(intent_detail['text_entities'][0]))

        try:
            res = intent_detail['text_entities'][1]
        except IndexError:
            return {"status": "Error", "message": "Atleast one record should be present for an Intent"}, intent_detail

        query = {"_id": ObjectId("{}".format(object_id))}

        result = await db.intents.update_one(query, {"$pull": {"text_entities": json_record}})
        print("Removed row from Intent {}".format(result))

        intent_detail = await self.get_intent_details({"object_id": object_id})
        return {"status": "Success", "message": "Intent text Removed "}, intent_detail


# noinspection PyMethodMayBeStatic
class ResponseModel:

    def __init__(self):
        pass

    async def get_responses(self, record):

        json_record = json.loads(json.dumps(record))

        cursor = db.responses.find(json_record, {"project_id": 1, "domain_id": 1, "response_name": 1, "response_description": 1})
        result = await cursor.to_list(length=1000)

        print("Responses sent {}".format(json.loads(dumps(result))))
        return json.loads(dumps(result))

    async def create_response(self, record):

        json_record = json.loads(json.dumps(record))

        insert_record = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id'],
                         "response_name": json_record['response_name'],
                         "response_description": json_record['response_description'], "text_entities": []}

        val_res = await db.responses.find_one({"project_id": json_record['project_id'],
                                               #"domain_id": json_record['domain_id'],
                                               "response_name": json_record['response_name']})

        if val_res is not None:
            print('Response already exists')
            return {"status": "Error", "message": "Response already exists"}, None
        else:

            result = await db.responses.insert_one(json.loads(json.dumps(insert_record)))
            print("Response created with ID {}".format(result.inserted_id))

            get_responses = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id']}
            responses_list = await self.get_responses(get_responses)

            return {"status": "Success", "message": "Response created successfully"}, responses_list

    async def delete_response(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}

        # check if response exists in any story

        response_detail = await db.responses.find_one(query)

        exists = await db.stories.find_one({"story": {"$elemMatch": {"key": response_detail['response_name']}}})

        if exists is None:

            result = await db.responses.delete_one(query)
            print("Response Deleted count {}".format(result))

            get_responses = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id']}
            responses_list = await self.get_responses(get_responses)

            return {"status": "Success", "message": "Response Deleted successfully"}, responses_list
        else:
            return {"status": "Error", "message": "Response exists in story cannot delete response"}, None

    async def update_response(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        update_field = {"$set": {"response_name": json_record['response_name'],
                                 "response_description": json_record['response_description']}}

        # Check if Response already exists
        val_res = await db.responses.find_one({"project_id": json_record['project_id'],
                                               #"domain_id": json_record['domain_id'],
                                               "response_name": json_record['response_name']})

        if val_res is None or val_res['response_name'] == json_record['response_name']:
            update_record = await db.responses.update_one(query, update_field)

            print("Response Updated , rows modified {}".format(update_record))

            get_responses = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id']}
            responses_list = await self.get_responses(get_responses)

            return {"status": "Success", "message": "Response Updated successfully"}, responses_list
        else:
            return {"status": "Error", "message": "Response Name already exists"}, None

    async def get_response_details(self, data):

        json_record = json.loads(json.dumps(data))
        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        result = await db.responses.find_one(query)
        print("Response Details sent {}".format(json.loads(dumps(result))))
        return json.loads(dumps(result))

    async def insert_response_detail(self, data):

        json_record = json.loads(json.dumps(data))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}

        object_id = json_record['object_id']
        del json_record['object_id']

        # to Prevent Duplicates

        result = await db.responses.update_one(query, {"$addToSet": {"text_entities": json_record['text_entities']}})

        print("Inserted new row in Intent {}".format(result.modified_count))

        intent_detail = await self.get_response_details({"object_id": object_id})

        if result.modified_count == 1:
            return {"status": "Success", "message": "Response added "}, intent_detail
        else:
            return {"status": "Error", "message": "Response Already exists "}, intent_detail

    async def delete_response_detail(self, data):

        # {"object_id": "", "text":"I am in india ","entities":[{"start":8,"end":13,"value":"india","entity":"timezone"}] }

        json_record = json.loads(json.dumps(data))
        object_id = json_record['object_id']
        del json_record['object_id']

        response_detail = await self.get_response_details({"object_id": object_id})
        try:
            res = response_detail['text_entities'][1]
        except IndexError:
            return {"status": "Error", "message": "Atleast one record should be present for an Response"}, response_detail

        query = {"_id": ObjectId("{}".format(object_id))}

        result = await db.responses.update_one(query, {"$pull": {"text_entities": json_record['text_entities']}})
        print("Removed row from Intent {}".format(result))

        response_detail = await self.get_response_details({"object_id": object_id})
        return {"status": "Success", "message": "Response text Removed "}, response_detail


# noinspection PyMethodMayBeStatic
class StoryModel:

    def __init__(self):
        pass

    async def get_stories(self, record):

        json_record = json.loads(json.dumps(record))

        cursor = db.stories.find(json_record, {"project_id": 1, "domain_id": 1, "story_name": 1, "story_description": 1})
        result = await cursor.to_list(length=1000)

        print("Stories sent {}".format(json.loads(dumps(result))))
        return json.loads(dumps(result))

    async def create_story(self, record):

        json_record = json.loads(json.dumps(record))

        insert_record = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id'],
                         "story_name": json_record['story_name'],
                         "story_description": json_record['story_description'], "story": []}

        val_res = await db.stories.find_one({"project_id": json_record['project_id'],
                                             "domain_id": json_record['domain_id'],
                                             "story_name": json_record['story_name']})

        if val_res is not None:
            print('Story already exists')
            return {"status": "Error", "message": "Story already exists"}, None

        else:

            result = await db.stories.insert_one(json.loads(json.dumps(insert_record)))
            print("Story created with ID {}".format(result.inserted_id))

            get_stories = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id']}
            stories_list = await self.get_stories(get_stories)

            return {"status": "Success", "message": "Story created successfully "}, stories_list

    async def delete_story(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}

        result = await db.stories.delete_one(query)
        print("Story Deleted count {}".format(result))

        get_stories = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id']}
        stories_list = await self.get_stories(get_stories)

        return {"status": "Success", "message": "Story Deleted successfully"}, stories_list

    async def update_story(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        update_field = {"$set": {"story_name": json_record['story_name'],
                                 "story_description": json_record['story_description']}}

        # Check if Response already exists
        val_res = await db.stories.find_one({"project_id": json_record['project_id'],
                                             "domain_id": json_record['domain_id'],
                                             "story_name": json_record['story_name']})

        if val_res is None or val_res['story_name'] == json_record['story_name']:

            update_record = await db.stories.update_one(query, update_field)
            print("Story Updated , rows modified {}".format(update_record))

            get_stories = {"project_id": json_record['project_id'], "domain_id": json_record['domain_id']}
            stories_list = await self.get_stories(get_stories)
            return {"status": "Success", "message": "Story Updated successfully "}, stories_list

        else:
            return {"status": "Error", "message": "Story Name already exists"}, None

    async def get_only_story_details(self, data):

        json_record = json.loads(json.dumps(data))
        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        result = await db.stories.find_one(query)
        print("Story Details sent {}".format(json.loads(dumps(result))))
        return result

    async def get_story_details(self, data):

        json_record = json.loads(json.dumps(data))
        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        result = await db.stories.find_one(query)
        print("Story Details sent {}".format(json.loads(dumps(result))))

        # TODO  - Verify if this works If intents or responses are created , when user is in Story details page , all intents / responses should be
        #  broadcast to this room as well

        # Get intents
        # cursor = db.intents.find({"project_id": json_record['project_id'], "domain_id": json_record['domain_id']})

        cursor = db.intents.find({"project_id": json_record['project_id']})
        result_intents = await cursor.to_list(length=1000)
        intents_list = json.loads(dumps(result_intents))

        # Get Responses
        # cursor = db.responses.find({"project_id": json_record['project_id'], "domain_id": json_record['domain_id']})

        cursor = db.responses.find({"project_id": json_record['project_id']})
        result_response = await cursor.to_list(length=1000)
        response_list = json.loads(dumps(result_response))

        # get actions
        cursor = db.actions.find({})
        result_action = await cursor.to_list(length=1000)
        action_list = json.loads(dumps(result_action))

        return json.loads(dumps(result)), intents_list, response_list, action_list

    async def insert_story_details(self, data):

        # {'object_id':"", "position":"", "story": ["key":"abc", "value":"", "type": "intent",
        #                           "entities": [{"entity_name": "test entity", "entity_value": "Test"}]]}

        json_record = json.loads(json.dumps(data))
        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        position = json_record['position']

        result = await db.stories.update_one(query, {"$push": {"story": {"$each": json_record['story'],
                                                                         "$position": position}
                                                               }})

        print("Story Details Updated {}".format(result))

        story_details, intents_list, response_list, actions_list = await self.get_story_details({"object_id": json_record['object_id'],
                                                                                   "project_id": json_record['project_id'],
                                                                                   "domain_id": json_record['domain_id']})

        return {"status": "Success", "message": "Story created"}, story_details, intents_list, response_list, actions_list

    async def delete_story_detail(self, data):

        json_record = json.loads(json.dumps(data))
        object_id = json_record['object_id']
        index = json_record['doc_index']

        query = {"_id": ObjectId("{}".format(object_id))}

        # Unset the record at  position provided and then pull it to properly remove the element
        result1 = await db.stories.update_one(query, {"$unset": {"story."+str(index): 1}})

        result = await db.stories.update_one(query, {"$pull": {"story": None}})

        print("Removed row from Story {}".format(result))

        story_detail,  intents_list, response_list,actions_list = await self.get_story_details({"object_id": json_record['object_id'],
                                                                                   "project_id": json_record['project_id'],
                                                                                   "domain_id": json_record['domain_id']})
        return {"status": "Success", "message": "Story element Removed "}, story_detail, intents_list, response_list, actions_list

    async def update_story_detail(self, data):

        json_record = json.loads(json.dumps(data))

        object_id = json_record['object_id']
        index = json_record['doc_index']
        query = {"_id": ObjectId("{}".format(object_id))}
        result = await db.stories.update_one(query, {"$set": {"story."+str(index): json_record['story']}})
        print("Record updated {}".format(result))

        story_detail,  intents_list, response_list, actions_list = await self.get_story_details({"object_id": json_record['object_id'],
                                                                                   "project_id": json_record['project_id'],
                                                                                   "domain_id": json_record['domain_id']})
        return {"status": "Success", "message": "Story Updated successfully"}, story_detail, intents_list, response_list, actions_list


# noinspection PyMethodMayBeStatic
class EntityModel:

    def __init__(self):
        pass

    async def get_entities(self, record):

        json_record = json.loads(json.dumps(record))
        cursor = db.entities.find(json_record)
        result = await cursor.to_list(length=1000)
        print("Entities sent {}".format(json.loads(dumps(result))))
        return json.loads(dumps(result))

    async def create_entity(self, record):

        json_record = json.loads(json.dumps(record))

        # Check if Entity already exists
        val_res = await db.entities.find_one({"project_id": json_record['project_id'],
                                              "entity_name": json_record['entity_name']})

        if val_res is not None:
            print("Entity Already exists ")
            return {"status": "Error", "message": "Entity Already exists "}, None
        else:
            result = await db.entities.insert_one(json_record)
            print("Entity created with ID {}".format(result.inserted_id))

            get_entities = {"project_id": json_record['project_id']}
            entities_list = await self.get_entities(get_entities)

            return {"status": "Success", "message": "Entity created successfully"}, entities_list

    async def delete_entity(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}

        # check if entity is used in any Intent
        # {"text_entities": {"$elemMatch":  {"entities.entity": "location_value"} }}

        entity_detail = await db.entities.find_one(query)

        res = await db.intents.find_one({"text_entities": {"$elemMatch":  {"entities.entity": entity_detail['entity_name']}}})

        res2 = await db.responses.find_one({"text_entities": "/"+entity_detail['entity_name']+"/"})

        if res is None and res2 is None:

            result = await db.entities.delete_one(query)
            print("Entity Deleted count {}".format(result))

            get_entities = {"project_id": json_record['project_id']}
            entities_list = await self.get_entities(get_entities)

            return {"status": "Success", "message": "Entity deleted successfully"}, entities_list
        elif res is None:
            return {"status": "Error", "message": "Unable to delete entity , its used in an Response"}, None
        else:
            return {"status": "Error", "message": "Unable to delete entity , its used in an Intent"}, None

    async def update_entity(self, record):

        json_record = json.loads(json.dumps(record))

        # Check if Entity already exists
        val_res = await db.entities.find_one({"project_id": json_record['project_id'],
                                              "entity_name": json_record['entity_name']})

        object_id = val_res.get('_id')
        query = {"_id": ObjectId("{}".format(object_id))}

        if val_res is None or val_res['entity_name'] == json_record['entity_name']:
            del json_record['_id']
            print("Got value ", json_record)
            update_record = await db.entities.update_one(query, {"$set": json_record})
            print("Entity Updated , rows modified {}".format(update_record.modified_count))

            get_entities = {"project_id": json_record['project_id']}
            entities_list = await self.get_entities(get_entities)
            return {"status": "Success", "message": "Entity updated successfully"}, entities_list

        else:
            return {"status": "Error", "message": "Entity Name already exists"}, None


class ValidateData:
    def __int__(self):
        pass

    async def validate_data(self, project_id):
        ret_val = ''
        query = {"project_id": project_id}

        # TODO
        #  Intent 'intent1' has only 1 training examples! Minimum is 2, training may fail
        #  Story must have valid data in it

        # Check for count of Intents in project

        cursor = db.intents.find(query)
        result = await cursor.to_list(length=10)
        print("Count of intents in Project {}".format(len(result)))

        if len(result) < 1:
            ret_val = ret_val + "Atleast one Intent should be defined in the Project \n"

        # Check for count of Responses in project

        cursor = db.responses.find(query)
        result = await cursor.to_list(length=10)
        print("Count of Responses in Project {}".format(len(result)))

        if len(result) < 1:
            ret_val = ret_val + "Atleast one Response should be defined in the Project \n"

        # Check for count of Story in project

        cursor = db.stories.find(query)
        result = await cursor.to_list(length=10)
        print("Count of Stories in Project {}".format(len(result)))

        if len(result) < 1:
            ret_val = ret_val + "Atleast one Story should be defined in the Project \n"
        else:
            # get the first story
            try:
                print("First story from the result {}".format(result[0]['story'][0]))
            except IndexError:
                ret_val = ret_val + "Story {} should have atleast one Intent and Response ".format(result[0]['story_name'])

        # Check for count of Entity in project

        cursor = db.entities.find(query)
        result = await cursor.to_list(length=10)
        print("Count of entities in Project {}".format(len(result)))

        if len(result) < 1:
            ret_val = ret_val + "Atleast one Entity should be defined in the Project \n"

        # checks for two stage fallback policy
        # Check for Negative Intent if its present.

        cursor = db.intents.find({"project_id": project_id, "intent_name": "negative"})
        result = await cursor.to_list(length=10)
        print("Count of negative intents in Project {}".format(len(result)))

        if len(result) < 1:
            ret_val = ret_val + "Intent 'negative' should be defined in the Project \n"

        # check for utter_default
        cursor = db.responses.find({"project_id": project_id, "response_name": "utter_default"})
        result = await cursor.to_list(length=10)
        print("Count of Responses in Project {}".format(len(result)))

        if len(result) < 1:
            ret_val = ret_val + "Response default should be defined in the Project \n"

        # check for utter_ask_rephrase
        cursor = db.responses.find({"project_id": project_id, "response_name": "utter_ask_rephrase"})
        result = await cursor.to_list(length=10)
        print("Count of Responses in Project {}".format(len(result)))

        if len(result) < 1:
            ret_val = ret_val + "Response ask_rephrase should be defined in the Project \n"

        return ret_val


class CustomActionsModel:
    def __init__(self):
        pass

    async def get_custom_actions(self):
        cursor = db.actions.find({})
        result = await cursor.to_list(length=1000)
        print("Custom Actions  {}".format(json.loads(dumps(result))))
        return json.loads(dumps(result))
    
    async def create_action(self, record):

        json_record = json.loads(json.dumps(record))

        # Validation to check if action already exists

        val_res = await db.actions.find_one({"action_name": json_record['action_name']})

        if val_res is not None:
            print('Action already exists')
            return {"status": "Error", "message": "Action already exists"}
        else:
            result = await db.actions.insert_one(json_record)
            print("Action created {}".format(result.inserted_id))
            return {"status": "Success", "message": "Action Has Been Created"}
    
    async def update_action(self, record):

        json_record = json.loads(json.dumps(record))

        query = {"_id": ObjectId("{}".format(json_record['object_id']))}
        update_field = {"$set": {"action_description": json_record['action_description']
                                 }}
        result = await db.actions.update_one(query, update_field)
        print("Action Updated , rows modified {}".format(result))
        return {"status": "Success", "message": "Action details updated successfully "}
    
    async def delete_action(self, object_id):
        query = {"_id": ObjectId("{}".format(object_id))}

        # Delete Action
        result = await db.actions.delete_one(query)
        print("Action Deleted count {}".format(result))
        return {"status": "Success", "message": "Action Deleted Successfully"}


class GrievanceModel:
    def __init__(self):
        pass

    async def get_grievance(self):
        cursor = db.grievance.find({})
        result = await cursor.to_list(length=1000)
        print("Grievance  {}".format(json.loads(dumps(result))))
        return json.loads(dumps(result))