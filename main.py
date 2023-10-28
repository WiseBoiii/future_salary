from terminaltables import AsciiTable
from headhunter import get_hh_statistics
from superjob import get_sj_statistics


def make_table(languaged_vacancies, company_name):
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

        actual_table = AsciiTable(table_payload, company_name)

    return actual_table


def main():
    hh_vacancies = make_table(get_hh_statistics(), 'HeadHunter Moscow')
    sj_vacancies = make_table(get_sj_statistics(), 'SuperJob Moscow')
    print(hh_vacancies.table, '\n', sj_vacancies.table)


if __name__ == '__main__':
    main()
