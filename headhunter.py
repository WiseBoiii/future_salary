import requests
from predict_rub_salary import predict_rub_salary
from itertools import count


def get_hh_vacancies(language, page):
    area = 1
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': f'Программист {language}',
        'area': area,
        'page': page,
        'per_page': 100
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    hh_vacancies = response.json()
    return hh_vacancies


def get_hh_statistics():
    languages = ['TypeScript', 'Swift', 'Scala', 'Shell', 'Go', 'C', 'C#', 'C++', 'PHP', 'Ruby',
                 'Python', 'Java', 'JavaScript']
    hh_statistics = {}
    for language in languages:
        average_salaries = []
        salaries = []
        for page in count(0, 1):
            languaged_vacancies = get_hh_vacancies(language, page)
            if page >= languaged_vacancies['pages'] - 1:
                break
            for vacancy in languaged_vacancies['items']:
                salaries.append(vacancy['salary'])
        for salary in salaries:
            if not salary:
                continue
            elif salary['currency'] != 'RUR':
                continue
            else:
                average_salaries.append(predict_rub_salary(salary['from'], salary['to']))
        processed_vacancies = 0
        salary_sum = 0
        for salary in average_salaries:
            if salary:
                processed_vacancies += 1
                salary_sum += salary
        try:
            average_salary = salary_sum / processed_vacancies
        except ZeroDivisionError:
            average_salary = 'Salary couldn`t be calculated'
        hh_statistics[language] = {
            'vacancies_found': languaged_vacancies['found'],
            'vacancies_processed': processed_vacancies,
            'average_salary': average_salary
        }
    return hh_statistics
