## 温度管理アプリ
このアプリは商品棚の**温度**を管理します。

## ER図
```mermaid
erDiagram
user {
    int user_id PK
    char name
    char password
    char address
}

shop {
    int shop_id PK
    int user_id FK
    char shop_name
    char shop_adress
}

shelf {
    int shelf_id PK
    int shop_id FK
    int reference_temperature
    int temperature
    date temperature_at
}

item {
    int item_id PK
    int shelf_id FK
    char item_name
    int price
    int stock
    date expiration_date
}

user ||--o{ shop : ""
shop |o--o{ shelf : ""
shelf |o--o{ item : ""
```

## テーブルについて
user : ユーザの個人情報<br>
shop : 店舗情報<br>
shelf : 商品棚の温度情報<br>
item : 商品棚に置いてある商品についての情報

## API仕様書
Webサイトにアクセスした**時間**を返します

## GET /api/time
**出力例**<br>
{<br>
　"1.year": 2023,<br>
　"2.month": 11,<br>
　"3.month_name": "November",<br>
　"4.day": 11,<br>
　"5.weekday": "Saturday",<br>
　"6.hour": 2,<br>
　"7.minute": 46,<br>
　"8.second": 51,<br>
　"9.now": "2023-11-11T02:46:51.047523"<br>
}<br>

**説明**<br>
year : 現在の年<br>
month : 現在の月<br>
month_name : 現在の月(英語の名称)<br>
day : 現在の日付<br>
weekday : 現在の曜日<br>
hour : 現在の時間(時)<br>
minute : 現在の時間(分)<br>
second : 現在の時間(秒)<br>
now : 現在の時間(年、月、日、時間、分、秒、マイクロ秒)<br>
