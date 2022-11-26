import requests
from dotenv import load_dotenv
import os
from terminaltables import AsciiTable


def get_hh_vacancies(language):
    hh_url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': f'Программист {language}',
        'area': f'{MOSCOW_AREA_NUMBER}'
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


def make_table(languaged_vacancies, company):
    table_payload = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for lang, lang_params in languaged_vacancies.items():
        table_payload.append(
            [
                lang,
                lang_params['vacancies_found'],
                lang_params['vacancies_processed'],
                lang_params['average_salary']
            ])
    if company == 'sj':
        actual_table = AsciiTable(table_payload, title='SuperJob Moscow')
    if company == 'hh':
        actual_table = AsciiTable(table_payload, title='HeadHunter Moscow')
    return actual_table


if __name__ == '__main__':
    load_dotenv()
    MOSCOW_AREA_NUMBER = 1
    languages = ['TypeScript', 'Swift', 'Scala', 'Objective-C', 'Shell', 'Go', 'C', 'C#', 'C++', 'PHP', 'Ruby',
                 'Python', 'Java', 'JavaScript']
    sj_token = os.environ['SJ_TOKEN']
    hh_salaries, sj_salaries = [], []
    hh_languaged_vacancies, sj_languaged_vacancies = {}, {}
    for language in languages:
        try:
            hh_vacancies_found, hh_vacancies = get_hh_vacancies(language)
            sj_vacancies_found, sj_vacancies = get_sj_vacancies(language, sj_token)
        except requests.exceptions.HTTPError:
            continue
        for vacancy in sj_vacancies:
            if not vacancy.get('payment_from') and not vacancy.get('payment_to'):
                continue
            predicted_sj_salary = predict_rub_salary(
                vacancy['payment_from'],
                vacancy['payment_to'],
                vacancy['currency']
            )
            if predicted_sj_salary:
                sj_salaries.append(predicted_sj_salary)

        average_salary = 0
        if sj_salaries:
            sj_average_salary = int(sum(sj_salaries) / len(sj_salaries))
            sj_languaged_vacancies[language] = {
                'vacancies_found': sj_vacancies_found,
                'vacancies_processed': len(sj_salaries),
                'average_salary': sj_average_salary
            }
        for vacancy in hh_vacancies:
            if not vacancy.get('salary'):
                continue
            predicted_hh_salary = predict_rub_salary(
                vacancy['salary']['from'],
                vacancy['salary']['to'],
                vacancy['salary']['currency']
                )
            if predicted_hh_salary:
                hh_salaries.append(predicted_hh_salary)
        average_salary = 0
        if hh_salaries:
            hh_average_salary = int(sum(hh_salaries) / len(hh_salaries))
            hh_languaged_vacancies[language] = {
                'vacancies_found': hh_vacancies_found,
                'vacancies_processed': len(hh_salaries),
                'average_salary': hh_average_salary
            }
    sj_table = make_table(sj_languaged_vacancies, 'sj')
    hh_table = make_table(hh_languaged_vacancies, 'hh')
    print(sj_table.table)
    print(hh_table.table)