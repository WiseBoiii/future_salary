from terminaltables import AsciiTable
from headhunter import get_hh_statistics
from superjob import get_sj_statistics


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


def main():
    hh_vacancies = make_table(get_hh_statistics(), 'hh')
    sj_vacancies = make_table(get_sj_statistics(), 'sj')
    print(hh_vacancies.table, '\n', sj_vacancies.table)


if __name__ == '__main__':
    main()
