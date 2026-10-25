import requests
from bs4 import BeautifulSoup
import csv
import datetime
import re

url = "https://www.hotenavi.com/pierre/empty"

html = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
).text

soup = BeautifulSoup(html, "html.parser")

available_rooms = []
preparing_rooms = []

# h2単位で判定
for h2 in soup.find_all("h2"):

    title = h2.get_text(strip=True)

    section = h2.find_parent("section")

    if not section:
        continue

    rooms = []

    for a in section.find_all("a"):

        room = a.get_text(strip=True)

        if re.fullmatch(r"\d{3}", room):
            rooms.append(room)

    rooms = sorted(set(rooms))

    if "空室一覧" in title:
        available_rooms = rooms

    elif "準備中一覧" in title:
        preparing_rooms = rooms

print("利用可能:", available_rooms)
print("準備中:", preparing_rooms)

timestamp = datetime.datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

with open(
    "hotel_room_log.csv",
    "a",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)

    if f.tell() == 0:
        writer.writerow(
            ["取得日時", "利用可能部屋", "用意中部屋"]
        )

    writer.writerow([
        timestamp,
        ",".join(available_rooms),
        ",".join(preparing_rooms)
    ])

print("記録完了")