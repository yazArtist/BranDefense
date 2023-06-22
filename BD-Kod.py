#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import praw
import sqlite3

try:
    # Reddit API kullanmak için kullanıcıdan login bilgilerini istedim ve bilgileri Reddit API ile bağladım.
    client_id = input("Reddit Client ID'nizi giriniz: ")
    client_secret = input("Reddit Client Secret'ınızı giriniz: ")
    user_agent = input("User Agent'ınızı giriniz: ")

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    subreddit_names = ['python']  # Birden fazla

    connection = sqlite3.connect('veritabani.db')
    cursor = connection.cursor()

    # Tablo oluşturmak için ,ps:(tablo daha önceden oluşturulmuşsa hata almaz) :
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
            # Verilerin tipleri :
            title = str(post.title)
            author = str(post.author)
            score = int(post.score)
            url = str(post.url)

            # Veriyi veritabanına eklemek için :
            query = "INSERT INTO posts (title, author, score, url) VALUES (?, ?, ?, ?)"
            values = (title, author, score, url)
            cursor.execute(query, values)
            connection.commit()
            print('Başlık:', title)
            print('Yazar:', author)
            print('Puan:', score)
            print('URL:', url)
            print('---------------------')

    # Veritabanını sorgulamak ve görüntülemek için :
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

    connection.close()

except praw.exceptions.ClientException:
    print("Hatalı Reddit API kimlik bilgileri. Lütfen doğru bilgileri girin.")
except Exception as e:
    print("Bir hata oluştu:", str(e))


# In[ ]:




