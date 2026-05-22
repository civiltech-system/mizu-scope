"""
初期データ投入スクリプト
使い方:
  python seed.py
"""
import asyncio
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select

from app.core.config import settings
from app.core.database import Base
from app.models.models import WaterRegion, WaterQuality, CommercialWater

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

# (country_code, prefecture, city, slug, lat, lng, population, water_source, utility_name)
REGIONS = [
    ("jpn", "東京都",   "千代田区",   "jp/tokyo/chiyoda",         35.6940, 139.7536,   66680, "利根川・荒川水系",     "東京都水道局"),
    ("jpn", "大阪府",   "大阪市",     "jp/osaka/osaka",           34.6937, 135.5023, 2690000, "琵琶湖・淀川水系",     "大阪市水道局"),
    ("jpn", "愛知県",   "名古屋市",   "jp/aichi/nagoya",          35.1815, 136.9066, 2300000, "木曽川水系",           "名古屋市上下水道局"),
    ("jpn", "福岡県",   "福岡市",     "jp/fukuoka/fukuoka",       33.5904, 130.4017, 1610000, "筑後川・山系",         "福岡市水道局"),
    ("jpn", "北海道",   "札幌市",     "jp/hokkaido/sapporo",      43.0642, 141.3469, 1960000, "豊平川水系",           "札幌市水道局"),
    ("jpn", "宮城県",   "仙台市",     "jp/miyagi/sendai",         38.2688, 140.8721, 1090000, "広瀬川水系",           "仙台市水道局"),
    ("jpn", "広島県",   "広島市",     "jp/hiroshima/hiroshima",   34.3853, 132.4553, 1200000, "太田川水系",           "広島市水道局"),
    ("jpn", "京都府",   "京都市",     "jp/kyoto/kyoto",           35.0116, 135.7681, 1460000, "琵琶湖・鴨川水系",     "京都市上下水道局"),
    ("jpn", "神奈川県", "横浜市",     "jp/kanagawa/yokohama",     35.4437, 139.6380, 3750000, "相模川水系",           "横浜市水道局"),
    ("jpn", "埼玉県",   "さいたま市", "jp/saitama/saitama",       35.8617, 139.6455, 1340000, "荒川・利根川水系",     "さいたま市水道局"),
    ("jpn", "千葉県",   "千葉市",     "jp/chiba/chiba",           35.6073, 140.1063,  980000, "利根川水系",           "千葉市水道局"),
    ("jpn", "静岡県",   "静岡市",     "jp/shizuoka/shizuoka",     34.9769, 138.3831,  690000, "安倍川・大井川水系",   "静岡市上下水道局"),
    ("jpn", "新潟県",   "新潟市",     "jp/niigata/niigata",       37.9161, 139.0364,  790000, "信濃川水系",           "新潟市水道局"),
    ("jpn", "長野県",   "長野市",     "jp/nagano/nagano",         36.6513, 138.1810,  370000, "犀川・千曲川水系",     "長野市上下水道局"),
    ("jpn", "石川県",   "金沢市",     "jp/ishikawa/kanazawa",     36.5944, 136.6256,  460000, "手取川水系",           "金沢市水道局"),
    ("jpn", "岡山県",   "岡山市",     "jp/okayama/okayama",       34.6618, 133.9350,  720000, "旭川水系",             "岡山市水道局"),
    ("jpn", "熊本県",   "熊本市",     "jp/kumamoto/kumamoto",     32.8031, 130.7079,  740000, "阿蘇山系地下水",       "熊本市上下水道局"),
    ("jpn", "沖縄県",   "那覇市",     "jp/okinawa/naha",          26.2124, 127.6809,  320000, "ダム湖・地下水",       "沖縄県企業局"),
    ("jpn", "鹿児島県", "鹿児島市",   "jp/kagoshima/kagoshima",   31.5966, 130.5571,  600000, "鹿児島湾流域地下水",   "鹿児島市水道局"),
    ("jpn", "青森県",   "青森市",     "jp/aomori/aomori",         40.8246, 140.7401,  280000, "浅虫水系",             "青森市企業局"),
]

# (slug, hardness, ph, calcium, magnesium, sodium, tds, chlorine)
QUALITIES = [
    ("jp/tokyo/chiyoda",       60.0, 7.1, 15.0,  4.2,  8.5,  80.0, 0.3),
    ("jp/osaka/osaka",         87.0, 7.2, 21.0,  6.0, 12.0, 110.0, 0.4),
    ("jp/aichi/nagoya",        65.0, 7.0, 16.0,  4.8,  9.0,  85.0, 0.3),
    ("jp/fukuoka/fukuoka",     31.0, 6.9,  7.5,  2.5,  6.0,  45.0, 0.2),
    ("jp/hokkaido/sapporo",    40.0, 7.0, 10.0,  2.8,  5.0,  55.0, 0.2),
    ("jp/miyagi/sendai",       53.0, 7.1, 13.0,  3.8,  7.5,  70.0, 0.3),
    ("jp/hiroshima/hiroshima", 43.0, 7.0, 10.5,  3.2,  6.5,  60.0, 0.2),
    ("jp/kyoto/kyoto",         72.0, 7.2, 17.5,  5.2, 10.0,  90.0, 0.3),
    ("jp/kanagawa/yokohama",   75.0, 7.1, 18.5,  5.5, 11.0,  95.0, 0.4),
    ("jp/saitama/saitama",     68.0, 7.0, 16.5,  5.0,  9.5,  88.0, 0.3),
    ("jp/chiba/chiba",         83.0, 7.1, 20.5,  6.0, 12.0, 105.0, 0.4),
    ("jp/shizuoka/shizuoka",   38.0, 7.0,  9.5,  2.8,  5.5,  52.0, 0.2),
    ("jp/niigata/niigata",     30.0, 7.0,  7.5,  2.2,  4.5,  42.0, 0.2),
    ("jp/nagano/nagano",       52.0, 7.1, 12.5,  3.8,  7.0,  68.0, 0.2),
    ("jp/ishikawa/kanazawa",   48.0, 7.0, 11.5,  3.5,  6.8,  65.0, 0.2),
    ("jp/okayama/okayama",     56.0, 7.1, 13.5,  4.0,  8.0,  73.0, 0.3),
    ("jp/kumamoto/kumamoto",   63.0, 7.2, 15.5,  4.5,  8.8,  82.0, 0.2),
    ("jp/okinawa/naha",       125.0, 7.3, 31.0,  8.5, 18.0, 155.0, 0.5),
    ("jp/kagoshima/kagoshima", 45.0, 7.1, 11.0,  3.3,  6.5,  62.0, 0.2),
    ("jp/aomori/aomori",       42.0, 7.0, 10.5,  3.0,  6.0,  58.0, 0.2),
]

# (name, brand, country_code, water_source, hardness, ph, calcium, magnesium, sodium, tds, water_type, coffee_score)
COMMERCIAL_WATERS = [
    ("南アルプスの天然水", "サントリー",     "jpn", "南アルプス",           30.0,   7.0,   8.0,  1.3,  1.7,   21.0, "soft",      4),
    ("エビアン",           "エビアン",       "fra", "アルプス・シャブレー", 291.0,   7.2,  80.0, 26.0,  6.5,  309.0, "very_hard", 3),
    ("ヴォルビック",       "ヴォルビック",   "fra", "オーヴェルニュ火山帯",  60.0,   7.0,  11.5,  8.0, 11.6,  130.0, "soft",      5),
    ("コントレックス",     "コントレックス", "fra", "ヴォージュ山脈",      1468.0,   7.4, 468.0, 84.0,  9.1, 2032.0, "very_hard", 1),
    ("六甲のおいしい水",   "アサヒ飲料",     "jpn", "六甲山系",             86.0,   7.2,  20.0,  7.0,  8.0,  120.0, "medium",    4),
    ("クリスタルガイザー", "クリスタルガイザー", "usa", "シャスタ山",        38.0,   7.4,   9.0,  3.0,  2.0,   56.0, "soft",      4),
    ("富士山の天然水",     "大塚食品",       "jpn", "富士山麓",             21.0,   7.0,   5.0,  1.5,  1.8,   18.0, "soft",      3),
    ("い・ろ・は・す",     "コカ・コーラ",   "jpn", "日本各地の自然水",     27.0,   7.2,   7.0,  1.8,  1.5,   25.0, "soft",      4),
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession() as session:
        existing = await session.execute(select(WaterRegion))
        if existing.scalars().first():
            print("Data already exists. Skipping seed.")
            return

        slug_to_id: dict[str, int] = {}
        for row in REGIONS:
            country, prefecture, city, slug, lat, lng, population, water_source, utility_name = row
            region = WaterRegion(
                country_code=country,
                prefecture=prefecture,
                city=city,
                slug=slug,
                lat=lat,
                lng=lng,
                population=population,
                water_source=water_source,
                utility_name=utility_name,
            )
            session.add(region)
            await session.flush()
            slug_to_id[slug] = region.id

        for row in QUALITIES:
            slug, hardness, ph, calcium, magnesium, sodium, tds, chlorine = row
            session.add(WaterQuality(
                region_id=slug_to_id[slug],
                hardness=hardness,
                ph=ph,
                calcium=calcium,
                magnesium=magnesium,
                sodium=sodium,
                tds=tds,
                chlorine=chlorine,
                drinkable=True,
                boil_recommended=False,
                confidence_score="official",
                measured_at=datetime(2024, 4, 1),
            ))

        for row in COMMERCIAL_WATERS:
            name, brand, country_code, water_source, hardness, ph, calcium, magnesium, sodium, tds, water_type, coffee_score = row
            session.add(CommercialWater(
                name=name,
                brand=brand,
                country_code=country_code,
                water_source=water_source,
                hardness=hardness,
                ph=ph,
                calcium=calcium,
                magnesium=magnesium,
                sodium=sodium,
                tds=tds,
                water_type=water_type,
                coffee_score=coffee_score,
            ))

        await session.commit()
        print(f"Seeded {len(REGIONS)} regions, {len(QUALITIES)} quality records, {len(COMMERCIAL_WATERS)} commercial waters.")


if __name__ == "__main__":
    asyncio.run(seed())
