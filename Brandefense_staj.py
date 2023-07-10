import sqlite3
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_user_credentials():
    client_id = input("Reddit API Client ID'yi giriniz: ")
    client_secret = input("Reddit API Client Secret'ı giriniz: ")
    return client_id, client_secret


def get_subreddit_name():
    subreddit_name = input("Takip etmek istediğiniz subreddit ismini giriniz (örnek: python): ")
    return subreddit_name


def create_database_connection():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    return connection, cursor
def crawl_posts_and_save_to_database():
    client_id, client_secret = get_user_credentials()

    subreddit_name = get_subreddit_name()

    # Reddit API için kimlik doğrulama işlemi
    auth_url = "https://www.reddit.com/api/v1/access_token"
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    auth_res = requests.post(auth_url, auth=auth, data=auth_data, headers=auth_headers)
    auth_res.raise_for_status()
    access_token = auth_res.json()['access_token']

    connection, cursor = create_database_connection()
    # Tabloyu oluştur (eğer oluşturulmamışsa)
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT,
                       author TEXT,
                       score INTEGER,
                       url TEXT)''')

    # Subreddit postlarını anlık olarak çekmek için Playwright
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(f"https://www.reddit.com/r/{subreddit_name}")
        page.wait_for_selector("h3")

        while True:
            soup = BeautifulSoup(str(page.content), "html.parser")
            posts = soup.select("div.Post")

            for post in posts:
                title_element = post.select_one("h3")
                author_element = post.select_one("span.PostAuthor")
                score_element = post.select_one("div.PostScore")
                url_element = post.select_one("a.PostTitle")

                if title_element and author_element and score_element and url_element:
                    title = str(title_element.get_text(strip=True))
                    author = str(author_element.get_text(strip=True))
                    score = int(score_element.get_text(strip=True))
                    url = url_element["href"]

                    # Veritabanına kaydet
                    insert_post_to_database(cursor, title, author, score, url)
                    connection.commit()

                    print('Başlık:', title)
                    print('Yazar:', author)
                    print('Puan:', score)
                    print('URL:', url)
                    print('---------------------')

            next_button = page.query_selector("a.Button--PaginationNext")
            if not next_button:
                break

            next_button.click()
            page.wait_for_selector("h3")
            browser.close()
            display_database_records(cursor)

            connection.close()

def insert_post_to_database(cursor, title, author, score, url):
    query = "INSERT INTO posts (title, author, score, url) VALUES (?, ?, ?, ?)"
    values = (title, author, score, url)
    cursor.execute(query, values)


def display_database_records(cursor):
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()

    print("Veritabanı Kayıtları:")
    for row in rows:
        print('ID:', row[0])
        print('Başlık:', row[1])
        print('Yazar:', row[2])
        print('Puan:', row[3])
        print('URL:', row[4])
        print('---------------------')



try:
    crawl_posts_and_save_to_database()
except Exception as e:
    print("Bir hata oluştu:", repr(e))

"""
get_user_credentials() fonksiyonu, kullanıcıdan Reddit API kimlik bilgilerini alır.
get_subreddit_name() fonksiyonu, kullanıcıdan takip edilecek subreddit'in ismini alır.
create_database_connection() fonksiyonu, SQLite veritabanı bağlantısı oluşturur ve bir imleç (cursor) döndürür.
insert_post_to_database() fonksiyonu, verilen başlık, yazar, puan ve URL değerlerini kullanarak veritabanına bir gönderi ekler.
display_database_records() fonksiyonu, veritabanındaki kayıtları alır ve ekrana yazdırır.
crawl_posts_and_save_to_database() fonksiyonu, Reddit API'ya kimlik doğrulama yapar, subreddit postlarını Playwright kullanarak anlık olarak çeker, her bir postu veritabanına kaydeder ve ekrana yazdırır.
crawl_posts_and_save_to_database() fonksiyonunu çalıştırarak, postları takip ediyoruz.
"""
