import requests
import os
from predict_rub_salary import predict_rub_salary


def get_sj_vacancies(language, page, sj_token):
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    payload = {
        'town': 'Moscow',
        'count': 25,
        'keyword': f'Программист {language}',
        'page': page
    }
    headers = {
        'X-Api-App-Id': sj_token
    }
    response = requests.get(sj_url, params=payload, headers=headers)
    response.raise_for_status()
    sj_vacancies = response.json()
    return sj_vacancies, sj_vacancies['total']


def get_sj_salaries(vacancies):
    salaries = []
    for vacancy in vacancies:
        if vacancy['currency'] != 'rub':
            continue
        else:
            salaries.append(predict_rub_salary(vacancy['payment_from'], vacancy['payment_to']))
    return salaries


def get_sj_statistics(sj_token):
    languages = ['TypeScript', 'Swift', 'Scala', 'Shell', 'Go', 'C', 'C#', 'C++', 'PHP', 'Ruby',
                 'Python', 'Java', 'JavaScript']
    sj_statistics = {}
    for language in languages:
        all_salaries = []
        vacancies = get_sj_vacancies(language, page=0, sj_token=sj_token)[0]
        for page in range(vacancies['total']):
            languaged_vacancies, vacancies_found = get_sj_vacancies(language, page, sj_token)
            salaries = get_sj_salaries(languaged_vacancies['objects'])
            all_salaries.extend(salaries)
        processed_vacancies = 0
        average_salary = 0
        for salary in all_salaries:
            if salary:
                processed_vacancies += 1
                average_salary += salary
        try:
            average_salary = average_salary / processed_vacancies
        except ZeroDivisionError:
            average_salary = 'Salary couldn`t be calculated'
        sj_statistics[language] = {
            'vacancies_found': len(all_salaries),
            'vacancies_processed': processed_vacancies,
            'average_salary': average_salary
        }

    return sj_statistics
