import praw
import sqlite3

 # Reddit API kullanmak için kullanıcıdan login bilgilerini istedim ve bilgileri Reddit API ile bağladım.
def get_reddit_credentials():
    client_id = input("Reddit Client ID'nizi giriniz: ")
    client_secret = input("Reddit Client Secret'ınızı giriniz: ")
    user_agent = input("User Agent'ınızı giriniz: ")
    return client_id, client_secret, user_agent

#Kullanıcıdan takip etmek istediği subreddit isminin girdisinin alınması
def get_subreddit_name():
    subreddit_name = input("Takip etmek istediğiniz subreddit ismini giriniz (örnek: python): ")
    return subreddit_name

# DB İle bağlantı kurulması.
def create_database_connection():
    connection = sqlite3.connect('veritabani.db')
    cursor = connection.cursor()
    return connection, cursor

# Veritabanına elde edilen verinin yazılması.
def insert_post_to_database(cursor, title, author, score, url):
    query = "INSERT INTO posts (title, author, score, url) VALUES (?, ?, ?, ?)"
    values = (title, author, score, url)
    cursor.execute(query, values)

# Veritabanı içerisinden verilerin çekilmesi ve ekrana yazılması.
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
    # Kullanıcıdan reddit kimlik bilgilerinin alınması.
    client_id, client_secret, user_agent = get_reddit_credentials()

    # Reddit API Bağlantısı
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    # Takip edilecek subreddit isminin alınması
    subreddit_name = get_subreddit_name()
    subreddit_names = [subreddit_name]

    # Veritabanı bağlantısının oluşturulması.
    connection, cursor = create_database_connection()

    # Eğer tablo oluşturulmamışsa tablonun oluşturulması.
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    score INTEGER,
                    url TEXT)''')

    # Subredditlerin postlarını anlık olarak takip etmek için stream kullandım.
    for subreddit_name in subreddit_names:
        subreddit = reddit.subreddit(subreddit_name)
        print(f"Takip edilen subreddit: {subreddit_name}")
        print("-------------------------------------")
        for post in subreddit.stream.submissions():
            title = str(post.title)
            author = str(post.author)
            score = int(post.score)
            url = str(post.url)

            # Veriyi veritabanına eklenmesi.
            insert_post_to_database(cursor, title, author, score, url)
            connection.commit()
            
            print('Başlık:', title)
            print('Yazar:', author)
            print('Puan:', score)
            print('URL:', url)
            print('---------------------')

    # Veritabanındaki kayıtların görüntülenmesi.
    display_database_records(cursor)

    # Veritabanı bağlantısının sonlandırılması.
    connection.close()

except praw.exceptions.ClientException:
    print("Hatalı Reddit API kimlik bilgileri. Lütfen doğru bilgileri girin.")
except Exception as e:
    print("Bir hata oluştu:", str(e))
