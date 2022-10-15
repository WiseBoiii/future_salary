import requests
from pprint import pprint
from dotenv import load_dotenv
import os


def get_hh_vacancies(language):
    hh_url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': f'Программист {language}',
        'area': '1'
    }
    response = requests.get(hh_url, params=payload)
    response.raise_for_status()
    hh_vacancies = response.json()
    return hh_vacancies['found'], hh_vacancies['items']


def get_sj_vacancies(language, sj_token):
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    payload = {
        'keyword': f'Программист {language}',
        'town': 'Москва'
    }
    headers = {
        'X-Api-App-Id': sj_token
    }
    response = requests.get(sj_url, params=payload, headers=headers)
    response.raise_for_status()
    sj_vacancies = response.json()
    return sj_vacancies['total'], sj_vacancies['objects']


def predict_rub_salary(salary_from, salary_to, salary_currency):
    if not salary_currency == 'RUR' and not salary_currency == 'rub':
        return
    if salary_from and salary_to:
        return (int(salary_from) + int(salary_to)) / 2
    elif salary_from:
        return int(salary_from) * 1.2
    elif salary_to:
        return int(salary_to) * 0.8


if __name__ == '__main__':
    load_dotenv()
    languages = ['TypeScript', 'Swift', 'Scala', 'Objective-C', 'Shell', 'Go', 'C', 'C#', 'C++', 'PHP', 'Ruby',
                 'Python', 'Java', 'JavaScript']
    sj_token = os.environ['SJ_TOKEN']
    salaries = []
    languaged_vacancies = {}
    for language in languages:
        try:
            hh_vacancies_found, hh_vacancies = get_hh_vacancies(language)
            sj_vacancies_found, sj_vacancies = get_sj_vacancies(language, sj_token)
        except requests.exceptions.HTTPError:
            continue
        predicted_sj_salary = predict_rub_salary(sj_vacancies['payment_from'], sj_vacancies['payment_to'],
                                                 sj_vacancies['currency'])
        #Написать цикл для формирования зп и словаря
        for vacancy in hh_vacancies:
            if not vacancy.get('salary'):
                continue
            predicted_hh_salary = predict_rub_salary(vacancy['salary']['from'], vacancy['salary']['to'],
                                                     vacancy['salary']['currency'])
            if predicted_hh_salary:
                salaries.append(predicted_hh_salary)
        average_salary = 0
        if salaries:
            average_salary = int(sum(salaries) / len(salaries))
        languaged_vacancies[language] = {'vacancies_found': hh_vacancies_found, 'vacancies_processed': len(salaries),
                                         'average_salary': average_salary}
    pprint(languaged_vacancies)
