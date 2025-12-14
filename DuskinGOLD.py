from __future__ import annotations
from datetime import date, datetime
from zoneinfo import ZoneInfo

import requests
from astral import LocationInfo
from astral.sun import sun


APP1_NAME_ZH = "融金时刻"
APP1_NAME_EN = "Dawn & Dusk in Gold"

TEXT = {
    "title": {
        "zh": "记录光的升起与落下。",
        "en": "Tracking the rising and fading of light.",
        "de": "Beobachtung des Auf- und Untergangs des Lichts."
    },
    "input_date": {
        "zh": "输入日期（YYYY-MM-DD，直接回车=今天）：",
        "en": "Enter date (YYYY-MM-DD, press Enter for today): ",
        "de": "Datum eingeben (YYYY-MM-DD, Enter = heute): "
    },
    "input_city": {
        "zh": "输入城市名（中文或英文，如：慕尼黑 / Munich / 北京 / Beijing）：",
        "en": "Enter city name (Chinese or English, e.g. Munich / Beijing): ",
        "de": "Stadtname eingeben (Chinesisch oder Englisch, z.B. München / Beijing): "
    },
    "date": {"zh": "日期", "en": "Date", "de": "Datum"},
    "timezone": {"zh": "时区", "en": "Time zone", "de": "Zeitzone"},
    "location": {"zh": "地点", "en": "Location", "de": "Ort"},
    "coordinates": {"zh": "坐标", "en": "Coordinates", "de": "Koordinaten"},
    "sunrise": {"zh": "日出", "en": "Sunrise", "de": "Sonnenaufgang"},
    "sunset": {"zh": "日落", "en": "Sunset", "de": "Sonnenuntergang"},
    "temperature": {"zh": "当前气温", "en": "Temperature", "de": "Temperatur"},
    "feels_like": {"zh": "体感温度", "en": "Feels like", "de": "Gefühlte Temperatur"},
    "precipitation": {"zh": "降水", "en": "Precipitation", "de": "Niederschlag"},
    "wind": {"zh": "风速", "en": "Wind speed", "de": "Windgeschwindigkeit"},
    "cloud": {"zh": "云量", "en": "Cloud cover", "de": "Bewölkung"},
}


def get_sunrise_sunset(lat: float, lon: float, tz: str, d: date) -> dict:
    loc = LocationInfo(name="Here", region="Earth", timezone=tz, latitude=lat, longitude=lon)
    s = sun(loc.observer, date=d, tzinfo=ZoneInfo(tz))
    return {"sunrise": s["sunrise"], "sunset": s["sunset"]}


def get_weather_open_meteo(lat: float, lon: float, tz: str) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,precipitation,wind_speed_10m,cloud_cover",
        "timezone": tz,
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    return data.get("current", {})

# 地理编码辅助函数
def geocode_city(city: str) -> dict:
    """
    使用 Open-Meteo 的地理编码 API：
    输入城市名（中英文），返回 lat / lon / timezone
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    if "results" not in data or not data["results"]:
        raise ValueError("未找到该城市，请检查城市名输入。")
    res = data["results"][0]
    return {
        "name": res.get("name"),
        "country": res.get("country"),
        "lat": res.get("latitude"),
        "lon": res.get("longitude"),
        "timezone": res.get("timezone"),
    }

def main():
    print("请选择语言 / Select language / Sprache wählen")
    print("1. 中文")
    print("2. English")
    print("3. Deutsch")
    lang_choice = input("请输入数字 / Enter number / Nummer eingeben: ").strip()

    if lang_choice == "1":
        LANG = "zh"
    elif lang_choice == "2":
        LANG = "en"
    elif lang_choice == "3":
        LANG = "de"
    else:
        print("输入无效，默认使用 English.")
        LANG = "en"

    print(f"{TEXT['title'][LANG]}\n")

    date_str = input(TEXT["input_date"][LANG]).strip()
    d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()

    city = input(TEXT["input_city"][LANG]).strip()
    info = geocode_city(city)

    lat = info["lat"]
    lon = info["lon"]
    tz = info["timezone"]

    ss = get_sunrise_sunset(lat, lon, tz, d)
    w = get_weather_open_meteo(lat, lon, tz)

    print("\n==============================")
    print(f"📅 {TEXT['date'][LANG]}: {d.isoformat()}")
    print(f"🕒 {TEXT['timezone'][LANG]}: {tz}")
    print(f"📍 {TEXT['location'][LANG]}: {info['name']}, {info['country']}")
    print(f"📐 {TEXT['coordinates'][LANG]}: lat={lat:.3f}, lon={lon:.3f}")
    print("------------------------------")
    print(f"🌅 {TEXT['sunrise'][LANG]}: {ss['sunrise'].strftime('%H:%M')}")
    print(f"🌇 {TEXT['sunset'][LANG]}: {ss['sunset'].strftime('%H:%M')}")

    if w:
        print("------------------------------")
        print(f"🌡️ {TEXT['temperature'][LANG]}: {w.get('temperature_2m', 'NA')}°C")
        print(f"🤗 {TEXT['feels_like'][LANG]}: {w.get('apparent_temperature', 'NA')}°C")
        print(f"🌧️ {TEXT['precipitation'][LANG]}: {w.get('precipitation', 'NA')} mm")
        print(f"💨 {TEXT['wind'][LANG]}: {w.get('wind_speed_10m', 'NA')} km/h")
        print(f"☁️ {TEXT['cloud'][LANG]}: {w.get('cloud_cover', 'NA')} %")
    else:
        print("⚠️ 天气数据获取失败（请检查网络/坐标/时区输入）")

    print("==============================\n")


if __name__ == "__main__":
    main()