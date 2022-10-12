import pandas as pd

import re

from store import Vacancies


def get_salary_by_area(area_list, role=None):
    vacancies = Vacancies()

    vacancies.open()

    if role:
        data = list(vacancies.get_vacancy_by_role(role))
    else:
        data = list(vacancies.get_vacancies())

    vacancies.close()
    df = pd.DataFrame.from_records(data, index='_id')

    df = df.groupby('area').median(
        'salary').sort_values(by='salary', ascending=False)

    df = df.loc[df.index.intersection(area_list)]

    return (df.index, df['salary'])


def get_specialization_proportions():
    vacancies = Vacancies()

    vacancies.open()

    def get_proportion(current, total):
        return int(current / total * 100)

    total_dev_count = vacancies.count_vacancy(
        '', 'dev')

    frotend_count = vacancies.count_vacancy(
        re.compile('front|фронтенд|верстальщик', re.IGNORECASE), 'dev')
    backend_count = vacancies.count_vacancy(
        re.compile('back|бэкенд', re.IGNORECASE), 'dev')
    mobile_count = vacancies.count_vacancy(
        re.compile('мобильн|mobile|ios|android', re.IGNORECASE), 'dev')
    mobile_count = vacancies.count_vacancy(
        re.compile('мобильн|mobile|ios|android', re.IGNORECASE), 'dev')
    analytics_count = vacancies.count_vacancy(
        '', 'analytics')
    qa_count = vacancies.count_vacancy(
        '', 'qa')
    sys_admin_count = vacancies.count_vacancy(
        '', 'sys_admin')

    total_count = total_dev_count + analytics_count + qa_count

    frontend = get_proportion(frotend_count, total_count)
    backend = get_proportion(backend_count, total_count)
    mobile = get_proportion(mobile_count, total_count)
    analytics = get_proportion(analytics_count, total_count)
    qa = get_proportion(qa_count, total_count)
    sys_admin = get_proportion(sys_admin_count, total_count)

    other = 100 - frontend - backend - mobile - analytics - qa - sys_admin

    return {
        'frontend': frontend,
        'backend': backend,
        'mobile': mobile,
        'qa': qa,
        'analytics': analytics,
        'sys_admin': sys_admin,
        'other': other
    }
