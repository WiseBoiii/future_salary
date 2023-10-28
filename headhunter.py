import requests
from predict_rub_salary import predict_rub_salary


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
    return response.json(), response.json()['found']


def get_hh_salary(vacancies):
    salaries = []
    for vacancy in vacancies:
        salaries.append(vacancy['salary'])
    return salaries


def get_hh_statistics():
    languages = ['TypeScript', 'Swift', 'Scala', 'Shell', 'Go', 'C', 'C#', 'C++', 'PHP', 'Ruby',
                 'Python', 'Java', 'JavaScript']
    hh_statistics = {}
    for language in languages:
        average_salaries = []
        for page in range(20):
            languaged_vacancies, vacancies_found = get_hh_vacancies(language, page)
            if page >= languaged_vacancies["pages"] - 1:
                break
            salaries = get_hh_salary(languaged_vacancies['items'])
            for salary in salaries:
                if not salary:
                    average_salaries.append(None)
                elif salary['currency'] != 'RUR':
                    average_salaries.append(None)
                else:
                    average_salaries.append(predict_rub_salary(salary['from'], salary['to']))
        processed_vacancies = 0
        average_salary = 0
        for salary in average_salaries:
            if salary is not None:
                processed_vacancies += 1
                average_salary += salary
        hh_statistics[language] = {
            'vacancies_found': len(average_salaries),
            'vacancies_processed': processed_vacancies,
            'average_salary': average_salary / processed_vacancies
        }
    return hh_statistics
