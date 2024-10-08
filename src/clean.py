import sqlite3
from lxml import etree
from bs4 import BeautifulSoup
import os

DIRECTORY_NAME = 'volume'

FROM_DB : str = f"{DIRECTORY_NAME}/vacancies.db"
NEW_DB : str = f"{DIRECTORY_NAME}/vacancies_new.db"
UP_LETTER_DB : str = f"{DIRECTORY_NAME}/vacanciesUPLetter.db"

#для скрещивания 
MURMAN_DB : str = f"{DIRECTORY_NAME}/vacanciesFromMurmanskUPletter.db"
VACANCY_DB : str = f"{DIRECTORY_NAME}/vacanciesUPLetter.db"

#для сортировки
SORT_DB : str = f"{DIRECTORY_NAME}/vacancies_sort.db"


#функция для создания бд
def crateINDb(name_db: str) -> None:
    connection = sqlite3.connect(name_db)

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
    

def handel():
    connection_out = sqlite3.connect(FROM_DB)
    


    cursor = connection_out.cursor()

    cursor.execute('select * from Vacancy')

    vacancies = cursor.fetchall()

    connection_out.close()

    for v in vacancies:
        soup = BeautifulSoup(v[5])


        for tag in soup.find_all("div", {"data-content" : "vacancy-map"}):
            print("уничтожил тек в котором хранится яндкс карта")
            tag.decompose()


        for tag in soup.find_all("div", {"class" : "row row_bottom mt-5 mb-2"}):
            print("уничтожил тек в котором хранится название для поля в котором храниалася яндкес карта")
            tag.decompose()


        for a in soup.find_all("a"):
            a['href'] = "#"

        connection_in = sqlite3.connect(NEW_DB)
        cursor = connection_in.cursor()
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
                    ''', (v[1], v[2], v[3], v[4], soup.prettify(), v[6]))
        
        connection_in.commit()

        connection_in.close()

#функция для изменения верхнего регистра названия вакансии
def upFirstLetter() -> None:
    connection = sqlite3.connect(NEW_DB)


    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Vacancy")

    vacancies = cursor.fetchall()

    for v in vacancies:
        connectionUPDB = sqlite3.connect(UP_LETTER_DB)
        cursor = connectionUPDB.cursor()

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
                    ''', (v[1].title(), v[2], v[3], v[4], v[5], v[6]))
        
        connectionUPDB.commit()

        connectionUPDB.close()
        


#функция для сортировки по алфивиту
def sortAlphabet() -> None:
    connection = sqlite3.connect(VACANCY_DB)

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Vacancy ORDER BY vacancy_name")

    vacancies = cursor.fetchall()

    for v in vacancies:
        
        connectionSortDb = sqlite3.connect(SORT_DB)

        cursorSort = connectionSortDb.cursor()

        cursorSort.execute('''
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
                    ''', (v[1], v[2], v[3], v[4], v[5], v[6]))
        
        connectionSortDb.commit()
        connectionSortDb.close()

    connection.close()

#функция чтобы удалить из базы данных вакансий вакансии из мурманска
def delMurmanVacansy() -> None:
    connection = sqlite3.connect(UP_LETTER_DB)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Vacancy WHERE vacancy_place = 'Мурманск'")
    
    connection.commit()

    connection.close()


#функция для скрещивания баз данных вакансий
def CrossingDB() -> None:

    connectionMurman = sqlite3.connect(MURMAN_DB)

    cursor = connectionMurman.cursor()

    vacncies = cursor.execute("SELECT * FROM Vacancy")

    for v in vacncies:
        connectionVacancyDB = sqlite3.connect(VACANCY_DB)

        cursorVacancyDB = connectionVacancyDB.cursor()

        cursorVacancyDB.execute('''
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
            ''', (v[1], v[2], v[3], v[4], v[5], v[6]))
        
        connectionVacancyDB.commit()

        connectionVacancyDB.close()

    connectionMurman.close()


#функция для удаления таблицы
def del_db(db_name: str) -> None:
    if os.path.isfile(db_name):
        os.remove(db_name)

#функция для создания отсортированной и чистой бд
def clean_db() -> None:
    #создаем базы для работы
    crateINDb(NEW_DB)
    crateINDb(UP_LETTER_DB)
    crateINDb(SORT_DB)

    handel()

    upFirstLetter()
    sortAlphabet()

    #удаляем базы для работы
    del_db(UP_LETTER_DB)
    del_db(SORT_DB)