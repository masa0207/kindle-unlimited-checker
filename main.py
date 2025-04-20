import requests
from bs4 import BeautifulSoup

def fetch_new_magazines():
    url = "https://www.amazon.co.jp/s?i=digital-text&rh=n%3A2275256051"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    books = soup.select(".s-title-instructions-style")
    new_books = []
    for book in books:
        title = book.get_text(strip=True)
        link = book.find_parent("a")["href"]
        new_books.append(f"{title}\nhttps://www.amazon.co.jp{link}")
    return new_books

def send_line_notify(message):
    token = "YOUR_LINE_NOTIFY_TOKEN"  # GitHub Secretsで設定
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

if __name__ == "__main__":
    books = fetch_new_magazines()
    if books:
        message = "\n\n".join(books[:5])  # 上位5件だけ通知
        send_line_notify("📚 Kindle Unlimited 新着雑誌：\n\n" + message)
