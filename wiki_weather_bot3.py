from pprint import pprint

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from auth_data import token
from asyncio import run
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from auth_data import open_weather_token
from test import code_to_smile

bot = Bot(token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_bot(message: types.Message):
    await message.reply(f'Hi, {message.from_user.full_name}! Please type the name of the city!\n e.g. Saint_Petersburg')


@dp.message()
async def get_geo(message: types.Message):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'
        }
        url = f'https://en.wikipedia.org/wiki/{message.text}'

        r = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')
        latitude = soup.find(name='span', attrs={'class': 'latitude'}).text
        lat = latitude.replace('°', '-').replace('′', '-').replace('″', '') if '″' in latitude else latitude.replace(
            '°', '-').replace('′', '-00')
        N = 'N' in lat
        d, m, s = map(float, lat[:-1].split('-'))
        latitude = (d + m / 60. + s / 3600.) * (1 if N else -1)

        # lt = lat.replace('°', '-').replace('′', '-').replace('″', '')

        longitude = soup.find(name='span', attrs={'class': 'longitude'}).text
        lon = longitude.replace('°', '-').replace('′', '-').replace('″', '') if '″' in longitude else longitude.replace(
            '°', '-').replace('′', '-00')
        W = 'W' in lon
        d, m, s = map(float, lon[:-1].split('-'))
        longitude = (d + m / 60. + s / 3600.) * (-1 if W else 1)
        # ln = lon.replace('°', '-').replace('′', '-').replace('″', '')

        lat_data = round(latitude, 2)
        lon_data = round(longitude, 2)

        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat_data}&lon={lon_data}&exclude=alerts&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        city_distirict = data['name']
        date = datetime.date(datetime.fromtimestamp(data['sys']['sunrise']))
        temp = data['main']['temp']
        weather_descr = data['weather'][0]['main']
        if weather_descr in code_to_smile:
            wd = code_to_smile[weather_descr]
        else:
            wd = 'Please check in your window.'
        weather = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        day_length = datetime.fromtimestamp(data['sys']['sunset']) - datetime.fromtimestamp(data['sys']['sunrise'])
        await message.reply(
            f'***{date}***\n'
            f'{wd}\n'
            f'The weather in: {city_distirict}\n'
            f'The temperature is {temp}°C, {weather}\n'
            f'💧 Humidity is {humidity}\n'
            f'The wind speed is {wind} m/s\n'
            f'🌄 Lenght of the day is {day_length} 🌇'
        )


    except Exception as ex:
        await message.reply('Sorry, no city with this name!')
        print(ex)


if __name__ == '__main__':
    run(dp.start_polling(bot))

#
#         # here supposed the first part of forecast
#         sunrise_h = datetime.fromtimestamp(data['sys']['sunrise']).hour
#         sunrise_m = datetime.fromtimestamp(data['sys']['sunrise']).minute
#         sunrise = f'{sunrise_h}h:{sunrise_m}m'
#         # sunrise = f'{sunrise_h + 2}h:{sunrise_m}m'
#         sunset_h = datetime.fromtimestamp(data['sys']['sunset']).hour
#         sunset_m = datetime.fromtimestamp(data['sys']['sunset']).minute
#         sunset = f'{sunset_h}h:{sunset_m}m'
#         # sunset = f'{sunset_h + 2}h:{sunset_m}m'
#         day_length = datetime.fromtimestamp(data['sys']['sunset']) - datetime.fromtimestamp(data['sys']['sunrise'])
#         await message.reply(
#             f'***{date}***\n'
#             f'{wd}\n'
#             f'The weather in: {city_distirict}\n'
#             f'The temperature is {temp}°C, {weather}\n'
#             f'💧 Humidity is {humidity}\n'
#             f'The wind speed is {wind} m/s\n'
#             f'🌄 The sunrise is at {sunrise} 🌄\n'
#             f'🌇 The sunset is at {sunset} 🌇\n'
#             f'Lenght of the day is {day_length}')
#
# elif city_distirict == 'Novaya Gollandiya' or city_distirict == 'Orekhovo-Borisovo Severnoye':
#     sunrise_h = datetime.fromtimestamp(data['sys']['sunrise']).hour
#     sunrise_m = datetime.fromtimestamp(data['sys']['sunrise']).minute
#     sunrise = f'{sunrise_h + 2}h:{sunrise_m}m'
#     sunset_h = datetime.fromtimestamp(data['sys']['sunset']).hour
#     sunset_m = datetime.fromtimestamp(data['sys']['sunset']).minute
#     sunset = f'{sunset_h + 2}h:{sunset_m}m'
#     day_length = datetime.fromtimestamp(data['sys']['sunset']) - datetime.fromtimestamp(data['sys']['sunrise'])
#
#     print(
#         f'🌄 The sunrise is at {sunrise} 🌄\n'
#         f'🌇 The sunset is at {sunset} 🌇\n'
#         f'Lenght of the day is {day_length}')
#
# elif city_distirict == 'Novosibirsk':
#     sunrise_h = datetime.fromtimestamp(data['sys']['sunrise']).hour
#     sunrise_m = datetime.fromtimestamp(data['sys']['sunrise']).minute
#     sunrise = f'{sunrise_h + 6}h:{sunrise_m}m'
#     sunset_h = datetime.fromtimestamp(data['sys']['sunset']).hour
#     sunset_m = datetime.fromtimestamp(data['sys']['sunset']).minute
#     sunset = f'{sunset_h + 6}h:{sunset_m}m'
#     day_length = datetime.fromtimestamp(data['sys']['sunset']) - datetime.fromtimestamp(data['sys']['sunrise'])
#     print(
#         f'🌄 The sunrise is at {sunrise} 🌄\n'
#         f'🌇 The sunset is at {sunset} 🌇\n'
#         f'Lenght of the day is {day_length}')


