def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (int(salary_from) + int(salary_to)) / 2
    elif salary_from:
        return int(salary_from) * 1.2
    elif salary_to:
        return int(salary_to) * 0.8