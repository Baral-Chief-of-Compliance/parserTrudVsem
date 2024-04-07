from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import db_tools


class VacanciesHandler():

    vacancies = []

    partOfMurmansk = [
        # {
        #     "name": "Терский район",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100600000000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name" : "Кировск",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000500000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Мончегорск",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000600000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Кандалакшский район",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100100000000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Североморск",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100001100000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Кольский район",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100300000000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Печенгский район",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100500000000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Ковдорский район",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100200000000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Гаджиево",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100001200000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Полярный",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100001000000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Снежногорск",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100001300000&page=0&salary=0&salary=999999"
        # },
        {
            "name": "Мурманск",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000100000&page=0&salary=0&salary=999999"
        },
        # {
        #     "name": "Апатиты",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000200000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Оленегорск",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&page=0&districts=5100000700000&districts=5100001500000&districts=5100001600000&salary=0&salary=999999"
        # },
        # {
        #     "name": "Ловозерский район",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100400000000&page=0&salary=0&salary=999999"
        # },
        # {
        #     "name": "Полярные Зори",
        #     "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000900000&page=0&salary=0&salary=999999"
        # }
    ]

    #path = "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&page=0&salary=0&salary=999999"

    #тестовый url для Терского райна
    pathTest = "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100600000000&page=0&salary=0&salary=999999"

    driver = webdriver.Chrome()

    #счетчик всех вакансий на сайте по региону и его XPath
    counterVacancies = 0
    counterVacanciesXPath = './/span[@class="ib-filter__result-counter"]'

    #XPath для элементов карточки вакансии
    mainBlocXPath = './/div[@class="main__search-sidebar"]'

    buttonMoreXPath = './/div[@data-content="more-btn"]' #получать от этого элемента класс button
    buttonMoreActivClass = 'align align_center mt-2'
    buttonMoreDeactiveClass = 'align align_center mt-2 d-none'

    cardVacanciXPath = './/div[@class="search-results-simple-card mb-1"]'
    cardVacanciActiveXPath = './/div[@class="search-results-simple-card mb-1 search-results-simple-card_active"]'

    #XPath элементов в полной карточке, в которой хранятся все информаци о вакансии
    fullInfoCardVacanciXPath = './/div[@class="search-results-full-card"]'
    nameVacanciXPath = './/h3[@class="content__section-title search-results-full-card__title"]'
    nameOraginiztionXPath = './/div[@class="search-results-full-card__extra-info content_clip"]'
    salaryXPath = './/span[@class="content__section-subtitle search-results-full-card__salary"]'
    timeUpdateCardXPath = './/span[@class="content_small content_pale"]'
    blocWithInfoXPath = './/div[@id="vacancy-details"]'
    titleForBlocsXPath = './/h3[@class="content__section-title content__section-title_small search-results-full-card__title-section"]'
    titleForBlocsClass = 'content__section-title content__section-title_small search-results-full-card__title-section'
    listItemClass = 'list__item'
    dlItemClass = 'definitions definitions_reverse'

    #кнопка о компании
    buttonAboutCompanyXPath = './/button[@data-target="#about-company"]'
    addressXPath = './/div[@class="mb-3"]'
    infInCardXPath = './/div[@class="search-results-full-card__content"]'
    
    #метод  для получения числа вакнский с сайта
    def getCounterVacancies(self) -> int:
        counterVacancies = int(self.driver.find_element(By.XPATH, self.counterVacanciesXPath).text.replace(" вакансий", "").replace(" ", ""))
        return counterVacancies

    #метод для нажати на кнопку Загрузить ещё, чтобы получать больше вакансий
    def pressButtonDowmloadMore(self)->None:
        mainBlock = self.driver.find_element(By.XPATH, self.buttonMoreXPath)
        button = self.driver.find_element(By.XPATH, self.buttonMoreXPath).find_element(By.TAG_NAME, "button")
        ActionChains(self.driver).scroll_to_element(button).perform()
        time.sleep(1)
        try:
            button.click()
        except:
            print("не получилось нажать")
        time.sleep(2)

    
    #метод для нажатия кнопки, пока она не пропадёт   
    def pressingProcess(self) -> None:
        workCondition = True
        while (workCondition):
            button = self.driver.find_element(By.XPATH, self.buttonMoreXPath)
            vacancies = self.driver.find_elements(By.XPATH, self.cardVacanciXPath)
            print(len(vacancies))
            if button.get_attribute("class") == self.buttonMoreActivClass:
                self.pressButtonDowmloadMore()
                nowVacancies = self.driver.find_elements(By.XPATH, self.cardVacanciXPath)
                if vacancies == nowVacancies:
                    workCondition = False
            elif button.get_attribute("class") == self.buttonMoreDeactiveClass:
                workCondition = False


    #метод для сбора информации с активной вакансии
    def getInfoFromActiveVacanci(self, place : str):
        mainBlock = self.driver.find_element(By.XPATH, self.mainBlocXPath)
        activeCard = mainBlock.find_element(By.XPATH, self.cardVacanciActiveXPath)
        ActionChains(self.driver).scroll_to_element(activeCard).perform()
        #buttonAbout = self.driver.find_element(By.XPATH, self.buttonAboutCompanyXPath)
        #ActionChains(self.driver).click(buttonAbout)
        
        data = {
            "job-name": self.driver.find_element(By.XPATH, self.nameVacanciXPath).text,
            "company": self.driver.find_element(By.XPATH, self.nameOraginiztionXPath).text,
            "salary": self.driver.find_element(By.XPATH, self.salaryXPath).text,
            "updateTime": self.driver.find_element(By.XPATH, self.timeUpdateCardXPath).text,
            "info": self.driver.find_element(By.XPATH, self.infInCardXPath).get_attribute('innerHTML'),
            "place": place
        }
        self.vacancies.append(data)

        dataTuple = (
            data["job-name"],
            data["company"],
            data["salary"],
            data["updateTime"],
            data["info"],
            data["place"]
        )

        db_tools.addVacancy(data=dataTuple)

        time.sleep(2)



    
    #метод для получения ифнормациия с карточек вакансий
    def getInfoFromVacanciCards(self, place : str) -> list:
        mainBlock = self.driver.find_element(By.XPATH, self.mainBlocXPath)

        cardsVacanci = mainBlock.find_elements(By.XPATH, self.cardVacanciXPath)

        #Сейчас будем собирать данные с активной карточки
        self.getInfoFromActiveVacanci(place=place)

        cardsUid = []

        for card in cardsVacanci:
            cardsUid.append(card.get_attribute('data-uid'))

        for uid in cardsUid:
            card = self.driver.find_element(By.XPATH, f".//div[@data-uid='{uid}']")
            print(card.text)
            print("\n\n")
            try:
                ActionChains(self.driver).scroll_to_element(card).perform()
            except:
                print("не удалось навеститсь")

            time.sleep(2)
            try:
                card.click()
            except:
                print("не удалось нажать")
            time.sleep(2)

            try:
                self.getInfoFromActiveVacanci(place=place)
            except:
                print("не удалось получить информацию")

        # for card in cardsVacanci:

        #     try:
        #         print(card.text)
        #         print(card)
        #         print("\n\n")
        #     except:
        #         print("не могу прочитать текст")

        #     try:
        #         ActionChains(self.driver).scroll_to_element(card).perform()
        #     except:
        #         print("не могу прокрутить")

        #     time.sleep(2)

        #     try:
        #         card.click()
        #     except:
        #         print("не могу нажать")

        #     time.sleep(2)

        # for card in cardsVacanci:
        #     print(card.text)
        #     ActionChains(self.driver).scroll_to_element(card).perform()
        #     time.sleep(2)
        #     card.click()
        #     #time.sleep(5)
        #     #self.getInfoFromActiveVacanci(place=place)

        print(len(cardsVacanci))

        return self.vacancies


    #метод для получения всех вакансий с сайта trudvsem.ru
    def getAllVacancies(self, path : str, place : str) -> None:
        self.driver.get(path)
        self.driver.set_window_size(1920, 1080)
        time.sleep(5)

        #self.counterVacancies = self.getCounterVacancies()

        time.sleep(2)

        self.pressingProcess()

        time.sleep(5)

        self.getInfoFromVacanciCards(place=place)

        time.sleep(5)


        self.driver.quit

    def getAllVacanciesFromMurmanRegion(self):
        for partOfRegion in self.partOfMurmansk:
            self.getAllVacancies(
                path=partOfRegion["path"],
                place=partOfRegion["name"]
            )

vh = VacanciesHandler()

vh.getAllVacanciesFromMurmanRegion()
