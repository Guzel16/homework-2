import requests
from bs4 import BeautifulSoup
import pandas as pd

# Шаг 1: Сбор ссылок на страницы с новостями
all_page = ['https://sysblok.ru']
for i in range(2, 17):
    url = f'https://sysblok.ru/page/{i}'
    all_page.append(url)


# Шаг 2: Сбор ссылок на отдельные новости
news_file = open('links.txt', 'w') #запишем новости в файл
all_links = []
for page in all_page:
    response = requests.get(page)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href and 'sysblok.ru' in href:
            all_links.append(href)
            news_file.write(href + '\n')
 

# Шаг 3: Функция для сбора информации о новости
def parse_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #дата
    date_element = soup.find('time')
    date = date_element.text.strip()
    
    #заголовок
    title_element = soup.find('h1')
    title = title_element.text.strip()
    
    #текст
    text_elements = soup.find_all('p')
    text = ' '.join([element.text.strip() for element in text_elements])
    
    #автор
    author_element = soup.find('a', {'rel': 'author'})
    if author_element:
        author = author_element.text.strip()
    else:
        author = ''
    
    #категории
    categories = []
    category_elements = soup.find_all('a', {'rel': 'category tag'})
    for element in category_elements:
        category = element.text.strip()
        categories.append(category)
    
    return {
        'Title': title,
        'Author': author,
        'Date': date,
        'Text': text,
        'Categories': categories
    }

def writeNewsInFile(file_, news): #дополнительно записала информацию в файл, чтобы отслеживать 
    file_.write('Заголовок: '+news['Title']+'\n')
    file_.write('Автор: '+news['Author']+'\n')
    file_.write('Дата: '+news['Date']+'\n')
    file_.write('Текст: '+news['Text']+'\n')

    if len(news['Categories'])!=0: #запись категорий
        file_.write('Категории: ')
        for i in range(len(news['Categories'])):
            file_.write(news['Categories'][i])
            if i!=len(news['Categories'])-1:
                file_.write(', ')
        file_.write('\n')

    file_.write('\n')

# Шаг 4: Сбор информации для всех новостей
#parsed_news = parse_news(all_links[0])
news_file2 = open('news.txt', 'w', encoding="utf-8")  
all_news = []
tLink = 1 #для отслеживания выполнения программы (всего 5622 ссылок)
for link in all_links:
    print(tLink)
    try:
        news_info = parse_news(link)
        all_news.append(news_info)
        #print(news_info)
        writeNewsInFile(news_file2, news_info)
    except:
        pass
    tLink+=1

# Шаг 5: Создание датафрейма
df = pd.DataFrame(all_news)
print(df)
