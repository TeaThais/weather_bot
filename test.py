code_to_smile = {
    'Clear': '☀️ ️Clear ☀️',
    'Clouds': '☁️ Clouds ☁️',
    'Rain': '🌧️ Rain 🌧️',
    'Drizzle': '💧 Drizzle 💧',
    'Thunderstorm': '⛈️ Thunderstorm ⛈️',
    'Snow': '🌨️ Snow 🌨️',
    'Mist': '🌫️ Mist 🌫️',
    'Fog': '🌫️ Fog 🌫️'
}



def change():
    latitude = '55°03′N'
    lat = latitude.replace('°', '-').replace('′', '-').replace('″', '') if '″' in latitude else latitude.replace('°', '-').replace('′', '-00')
    N = 'N' in lat
    d, m, s = map(float, lat[:-1].split('-'))
    latitude = (d + m / 60. + s / 3600.) * (1 if N else -1)

    longitude = '82°57′E'
    lon = longitude.replace('°', '-').replace('′', '-').replace('″', '') if '″' in longitude else longitude.replace('°', '-').replace('′', '-00')
    W = 'W' in lon
    d, m, s = map(float, lon[:-1].split('-'))
    longitude = (d + m / 60. + s / 3600.) * (-1 if W else 1)



change()