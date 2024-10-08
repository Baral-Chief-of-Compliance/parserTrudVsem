from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options #добавляем для опций
import time
import db_tools
import json
import clean

CONFIG_PATH = 'volume/config.json'


class VacanciesHandler():

    vacancies = []

    min_range = 1280
    max_range = 1380

    partOfMurmansk = [
        {
            "name": "Терский район",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100600000000&page=0&salary=0&salary=999999"
        },
        {
            "name" : "Кировск",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000500000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Мончегорск",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000600000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Кандалакшский район",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100100000000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Североморск",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100001100000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Кольский район",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100300000000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Печенгский район",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100500000000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Ковдорский район",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100200000000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Гаджиево",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100001200000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Полярный",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100001000000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Снежногорск",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100001300000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Мурманск",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000100000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Апатиты",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000200000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Оленегорск",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&page=0&districts=5100000700000&districts=5100001500000&districts=5100001600000&salary=0&salary=999999"
        },
        {
            "name": "Ловозерский район",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100400000000&page=0&salary=0&salary=999999"
        },
        {
            "name": "Полярные Зори",
            "path": "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100000900000&page=0&salary=0&salary=999999"
        }
    ]

    #path = "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&page=0&salary=0&salary=999999"

    #тестовый url для Терского райна
    pathTest = "https://trudvsem.ru/vacancy/search?_regionIds=5100000000000&_districts=5100600000000&page=0&salary=0&salary=999999"

    driver : webdriver

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


    #по сути config.js это своего рода состояние парсера, пока он не закончил сбор данных
    #чтобы каждый раз запуская selenium мы могли обращаться к моменту где остановился наш сбор
    #или на каком моменте лучше прервать сессию бота и запустить по новой, чтобы не грузить бразуре
    #по 1гб на вкладку, что соответсвено сказывается на работе парсера и браузера 
    #функция для прочтения конфига для парсера в формате json
    def readJsonConfig(self) -> dict:
        f = open(CONFIG_PATH)
        data = json.load(f)
        f.close()
        return data

    
    #функция для записи конфига в формате json
    def setJsonConfig(self, config: dict) -> None:
        f = open(CONFIG_PATH, 'w')
        json.dump(config, f)
        f.close()
    
    #установка занчения в json файл сколько карточек с вакансиями по региону
    def setCardsCount(self, cards_count: int) -> None:
        config = self.readJsonConfig()
        config['cards_count'] = cards_count
        self.setJsonConfig(config)


    #установка базового значения конфига для парсинга
    def setBaseSettingConfig(self) -> None:
        self.setJsonConfig(
            {
                "region": "Терский район",
                "region_index": 0,
                "min_range": 0,
                "max_range": 100,
                "delta_range": 100,
                "cards_count": 0,
                "work_status": True
            }
        )
    
    #метод для нажатия кнопки, пока она не пропадёт   
    def pressingProcess(self) -> None:
        workCondition = True
        counter = 0

        #берем конфиг, тобишь возвращаемся к стейту приложения
        config = self.readJsonConfig()

        self.min_range = config['min_range']
        self.max_range = config['max_range']
        delta = config['delta_range']


        while (workCondition) and (counter <= self.max_range):
             
            button = self.driver.find_element(By.XPATH, self.buttonMoreXPath)
            vacancies = self.driver.find_elements(By.XPATH, self.cardVacanciXPath)

            if len(vacancies) > self.max_range:
                #это именно тот момент где мы двигаем каретку в конфиге
                #увеличивая min и max значения на delta
                config["max_range"] = self.max_range + delta
                config["min_range"] = self.min_range + delta
                self.setJsonConfig(config=config)
                workCondition = False

            else:
                counter = len(vacancies)
                print(f"len(vacancies): {len(vacancies)}")
                if button.get_attribute("class") == self.buttonMoreActivClass:
                    self.pressButtonDowmloadMore()
                    nowVacancies = self.driver.find_elements(By.XPATH, self.cardVacanciXPath)
                    print(f"nowVacancies: {len(nowVacancies)}")
                    print(f"vacancies: {len(vacancies)}")
                    if vacancies == nowVacancies:
                        #здесть имеется виду количество вкансий равно количество вакансий
                        config["work_status"] = False
                        self.setJsonConfig(config=config)
                        workCondition = False
                elif button.get_attribute("class") == self.buttonMoreDeactiveClass:
                    #если кнопки нет, то и начаша работа здесь окончена
                    config["work_status"] = False
                    self.setJsonConfig(config=config)
                    workCondition = False

        print(f"закончил нажимать на кнопку вот, столько вакансий {counter}")

        #установка в конфиг количества карт с вакансиями в регионе
        self.setCardsCount(counter)



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

        counter = 0
        for uid in cardsUid:
            if counter > self.min_range:
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

                counter = counter + 1
                print(counter)
            
            else:
                counter = counter + 1
                print("\n\n")
                print(counter)
                print("слишком маленкий индекс")

            if counter >= self.max_range:
                break

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

        work_status : bool = True

        #цикл работы парсера
        while work_status:
            config = self.readJsonConfig()
            work_status = config['work_status']

            #точка выхода из цикла
            if not(work_status):
                print("вырубаю драйвер")
                self.driver.quit()
                break
            
            #опции
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--headless=new')
            options.add_argument('--start-maximized')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--ignore-certificate-errors')

            self.driver = webdriver.Chrome(options=options)
            self.driver.get(path)
            #self.driver.set_window_size(1920, 1080)
            time.sleep(5)

            #self.counterVacancies = self.getCounterVacancies()

            time.sleep(2)


            #в данной части кода мы нажимаем кнопку "Загрузить еще"
            #чтобы получить на странице все карточки с вакансиями.
            #по которым мы сможем передвигаться и собирать информацию
            self.pressingProcess()

            time.sleep(5)

            #а в этой части коды мы собираем информацию с карточек
            #которые есть на сайте, по средством нажатия на эти карточки
            #и собирания с них полной информации
            self.getInfoFromVacanciCards(place=place)

            time.sleep(5)

            self.driver.quit()

            time.sleep(10)
        
        #по окончании процесса сбора вакансий с региона, мы сбрасываем
        config = self.readJsonConfig()
        config["cards_count"] = 0
        config["region_index"] = config["region_index"] + 1
        self.setJsonConfig(config=config)

    def getAllVacanciesFromMurmanRegion(self):
        #устанавливаем стратовый конфиг для парсера
        #self.setBaseSettingConfig()


        #приступаем к сбору вакансий 
        for index, partOfRegion in enumerate(self.partOfMurmansk):


            print(f"count: {index}; partOfRegion: {partOfRegion}")

            #на каждой итерации нашего списка регионов
            #мы должны грубо говоря сбрасывать config
            config = self.readJsonConfig()

            if config["region_index"] != index:
                continue
            
            else:
                if config["cards_count"] != 0:
                    print("не равно нулю")
                    pass
                else:
                    config["region"] = partOfRegion["name"]
                    config["region_index"] = index
                    config["work_status"] = True
                    config["min_range"] = 0
                    config["max_range"] = 100
                    config["delta_range"] = 100
                    config["cards_count"] = 0

            print("запуск ппроцесса получения всех вакансий")
            self.setJsonConfig(config=config)

            self.getAllVacancies(
                path=partOfRegion["path"],
                place=partOfRegion["name"]
            )

#запуск скрипта
if __name__ == "__main__":

    vh = VacanciesHandler()

    vh.getAllVacanciesFromMurmanRegion()
    vh.setBaseSettingConfig()

    # чистим полученные вакансии от говна
    clean.clean_db()
    clean.del_db("dbs/vacancies.db")
