# BranDefense
Brandefese  2023 Staj Kampı | Şahinde Ceren OMRAK


Usage: python Brandefense_staj.py
Write your reddit creds.


Docker usage:
docker pull yazartist/brandefense_staj


docker run -it yazartist/brandefense_staj

Playwright ile tarayıcı başlatılır ve belirtilen subreddit'in sayfasına gidilir.
Sayfa içeriği BeautifulSoup kütüphanesiyle analiz edilir ve gerekli veriler seçilir.
Seçilen veriler veritabanına kaydedilir ve ekrana yazdırılır.
Bir sonraki sayfaya geçilir ve işlem tekrarlanır.
Tüm postlar çekildikten sonra tarayıcı kapatılır.
