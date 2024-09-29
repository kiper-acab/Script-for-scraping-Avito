from selenium import webdriver
from selenium.webdriver.common.by import By
from multiprocessing import Pool
import json
import argparse



def main(product):
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    links = []
    characteristics = {}

    try:
        driver.get('https://www.avito.ru/')
        driver.implicitly_wait(5)
        print("Делаем запрос....")

        input_search = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div/div[3]/div[2]/div[1]/div/div/label/div/div/input')
        input_search.send_keys(product)
        find = driver.find_element(By.CLASS_NAME, 'desktop-xp6ezn')
        find.click()

        driver.implicitly_wait(5)

        driver.find_element(By.CLASS_NAME, 'styles-module-root-EEwdX').click()
        products = driver.find_elements(By.CLASS_NAME, 'iva-item-root-_lk9K')

        print('Cобираем все ссылки на товар...')
        for id, product in enumerate(products):
            link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
            links.append(link)
    
        for id, link in enumerate(links):
            product = driver.get(link)
            print(f'Собираем информацию с ссылки №{id}...')

            try:
                price = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/div/span/span/span[1]').text
            except:
                price = 'Бесплатно'

            try:
                raiting = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div/div[3]/div[2]/div/div/div/div[1]/div/div[1]/div/div[2]/span[1]').text
            except:
                raiting = 'Неизвестно'
            
            try:
                name = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div/div[3]/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/div/div/div/h3/a/span').text
            except:
                name = 'Anon'

            try:
                result = []
                infos = driver.find_elements(By.CLASS_NAME, 'params-paramsList__item-_2Y2O')
                for info in infos:
                    p = info.find_element(By.TAG_NAME, 'p').text.split(": ")
                    p = {p[0]: p[1]}
                    result.append(p)        
            except:
                info = 'Пусто'

            characteristics[str(id)] = {'Информация о продавце': {'Рейтинг': raiting, 'Имя': name}}, {'Цена': price}, {'Ссылка на товар': link}, {'Характеристики товара': result}

        
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(characteristics, f, indent=4, ensure_ascii=False)
        print('Файл успешно сохранён в json')


    except Exception:
        print('Что то пошло не так....')


    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('product', help='Впишите название товара, который хотите спарсить', nargs='*')
    args = parser.parse_args()
    main(' '.join(args.product))
