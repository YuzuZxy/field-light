# Gold 融金时刻
A trilingual astronomical time-tracking project

> Treasure the moments of watching the sunrise/sunset with that person.
> Golden light, pink clouds,
> a beauty that is fleeting, yet luminous.

> Schätze die Zeit, in der du mit dieser Person den Sonnenaufgang/-untergang betrachtest.
> Goldenes Abendlicht, rosafarbene Wolken
> schöne Momente, flüchtig und leuchtend.

## 🌅 About
**融金时刻（DD in Gold）** is a small command-line program that tracks  
**sunrise, sunset, and current weather** for a given city.

Light rises and falls each day
sometimes witnessed alone, sometimes shared.

This project is both a tool and a quiet record:  
of light in a field,  
and of the moments spent watching it together.

The program supports **three language tracks**:
- 中文 (Chinese)
- English
- Deutsch (German)

At runtime, the user selects one language, and the entire program runs along that single linguistic path.

---

## ✨ Features

- 🌍 City-based location input (no need for latitude/longitude)
- 🌅 Accurate sunrise & sunset calculation
- 🌦️ Current weather information:
  - Temperature
  - Feels-like temperature
  - Precipitation
  - Wind speed
  - Cloud cover
- 🗣️ Trilingual interface with language-track selection
- 🧭 Automatic timezone detection

---

## 🛠️ How It Works

1. The user selects a language at program start.
2. The user enters a date (or uses today by default).
3. The user enters a city name.
4. The program:
   - Geocodes the city (Open-Meteo Geocoding API)
   - Determines timezone automatically
   - Calculates sunrise and sunset (Astral)
   - Fetches current weather data (Open-Meteo Weather API)

All language content is centrally managed and separated from program logic.

---

## ▶️ Usage

### Install dependencies
```bash
pip install astral requests
