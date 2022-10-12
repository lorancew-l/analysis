import requests
from time import sleep
import argparse

from store import Vacancies
from common import progress_bar

BASE_URL = 'https://api.hh.ru/'
PER_PAGE = 100
IT_SPECIALIZATION_ID = 1
AREA_ID = 113
RPS_LIMIT = 5


class VacanciesCollector:
    def __init__(self):
        args = self.get_collection_args()

        self.count = args.count
        self.vacancies = []
        self.area = args.area or AREA_ID

    def get_collection_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-c', '--count', help='Vacancies count', type=int, required=True)
        parser.add_argument(
            '-a', '--area', help='Search area id', type=int, required=True)

        args = parser.parse_args()

        return args

    def collect(self):
        page_count = min([max(self.count // PER_PAGE, 1), 20])
        vacancies = []
        vacancies_detailed_info = []

        def collect_part(page):
            response = requests.get(f'{BASE_URL}vacancies', params={
                                    'specialization': IT_SPECIALIZATION_ID, 'area': self.area, 'only_with_salary': True, 'per_page': PER_PAGE, 'page': page})
            response_data = response.json()
            return response_data['items']

        for page in range(page_count):
            vacancies.extend(collect_part(page))
            sleep(1 / RPS_LIMIT)

        processed_vacancies_count = 0

        for vacancy in vacancies:
            response = requests.get(f'{BASE_URL}vacancies/{vacancy["id"]}')

            response_data = response.json()
            vacancies_detailed_info.append(self.transform(response_data))

            sleep(1 / RPS_LIMIT)

            processed_vacancies_count += 1
            progress_bar(processed_vacancies_count, len(vacancies))

        self.vacancies = vacancies_detailed_info

    def write(self, db):
        db.open()
        db.insert_many(self.vacancies)
        db.close()

    @staticmethod
    def transform(vacancy):
        vacancy['_id'] = vacancy.pop('id')
        vacancy['area'] = vacancy['area']['name']

        salary = vacancy['salary']
        salary_low = salary['from']
        salary_high = salary['to']

        if (salary_low and salary_high):
            vacancy['salary'] = (salary_low + salary_high) / 2

        vacancy['salary'] = salary_low if salary_low else salary_high

        return vacancy


if __name__ == '__main__':
    collector = VacanciesCollector()
    collector.collect()

    vacancies_db = Vacancies()
    collector.write(vacancies_db)
