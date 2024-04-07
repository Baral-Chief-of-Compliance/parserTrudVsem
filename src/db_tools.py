import sqlite3


def addVacancy(data: tuple) -> None:
    connection = sqlite3.connect("vacancies.db")

    cursor = connection.cursor()

    cursor.execute('''
                   insert into Vacancy 
                   (
                   vacancy_name, 
                   vacancy_company,
                   vacancy_salary,
                   vacancy_updateTime,
                   vacancy_info,
                   vacancy_place
                   ) 
                   values (?, ?, ?, ?, ?, ?)
                   ''', data)
    
    connection.commit()

    connection.close()


def crateDb() -> None:
    connection = sqlite3.connect("vacancies.db")

    cursor = connection.cursor()

    cursor.execute('''create table Vacancy 
                   (
                   vacancy_id integer primary key AUTOINCREMENT, 
                   vacancy_name text, 
                   vacancy_company text,
                   vacancy_salary text,
                   vacancy_updateTime text,
                   vacancy_info text,
                   vacancy_place text
                   )
                   ''')

    connection.commit()

    connection.close()