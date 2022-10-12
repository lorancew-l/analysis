import pymongo
import re

from common import ROLES


DEFAULT_URI = 'mongodb://localhost:27017/'
DEFAULT_DB = 'hh'


class Vacancies:
    collection = 'vacancies'

    def __init__(self, mongodb_uri=DEFAULT_URI, mongodb_db=DEFAULT_DB):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db

    def open(self):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]

    def close(self):
        self.client.close()

    def insert_many(self, items):
        self.db[self.collection].insert_many(items, ordered=False)

    def get_vacancies(self):
        return self.db[self.collection].find()

    def get_vacancy_by_role(self, role):
        result = self.db[self.collection].find(
            {'professional_roles.id': {'$in': ROLES[role]}})

        return result

    def count_vacancy(self, name, role):
        return self.db[self.collection].count_documents({'$and': [{'name': {'$regex': name}}, {'professional_roles.id': {'$in': ROLES[role]}}]})

    def get_vacancy_by_skills(self, skills):
        case_insensitive_skills = list(
            map(lambda skill: re.compile(f'^{skill}$', re.IGNORECASE), skills))

        result = self.db[self.collection].find(
            {'key_skills.name': {'$in': case_insensitive_skills}})

        return result

    def get_collection_size(self):
        return self.db[self.collection].count_documents({})
