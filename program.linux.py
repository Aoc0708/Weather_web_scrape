from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import bs4
import os


def main():
    first_run()
    persistent_run()


def weather_net(options):  # function to pull source from weather network
    weather_network_url = "https://www.theweathernetwork.com/ca/weather/ontario/williamstown"
    w_dvr = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver',
                             options=options)
    w_dvr.get(weather_network_url)
    w_soup = bs4.BeautifulSoup(w_dvr.page_source, 'html.parser')
    w_soup.find("div", {"class": "wxRow wx_detailed-metrics stripeable wx_rain_long"}).text
    w_dvr.quit()

    return w_soup


def yahoo_weather(options):  # function to pull source from yahoo weather
    yahoo_url = "https://ca.news.yahoo.com/weather/canada/ontario/williamstown-23397397"
    y_dvr = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver',
                             options=options)
    y_dvr.get(yahoo_url)
    y_soup = bs4.BeautifulSoup(y_dvr.page_source, 'html.parser')
    y_dvr.quit()

    return y_soup


def get_from_web():
    # Opening web page and getting beautiful soup info
    options = Options()  # loads options for chrome
    options.add_argument("--headless")  # Tells Chrome to run headless (No Gui)
    y_html = yahoo_weather(options)
    w_html = weather_net(options)

    return y_html, w_html


def first_run():  # Initial run of the program to get baseline of time and weather after startup
    my_time = time.localtime()
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears screen of old information
    print("Information Gathered at: {}".format(time.asctime(my_time)))
    y_html, w_html = get_from_web()
    format_data(y_html, w_html)


def persistent_run():  # If statement grabs minutes of the hour and modulo divides to run every 10 minutes
    while True:
        my_time = time.localtime()
        if my_time[4] % 10 == 0:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clears screen of old information
            print("Information Gathered at: {}".format(time.asctime(my_time)))
            y_html, w_html = get_from_web()
            format_data(y_html, w_html)
            time.sleep(540)  # sleeps for 9 minutes
        else:
            time.sleep(1)  # starts checking the time to be ready for when the mod swaps over to 10 minute mark


def format_data(y_data, w_data):  # Function accepts source code from sites and filters through to pull necessary data
    loc = y_data.select("div h1[data-reactid*='7']")[0].text
    temp = y_data.select("div span[data-reactid*='37']")[0].text
    feels_like = y_data.select("div [data-reactid*='477']")[0].text
    high = y_data.select("div span[data-reactid*='29']")[0].text
    low = y_data.select("div span[data-reactid*='33']")[0].text
    condition = y_data.find('div', {'class': 'wind'})
    condition = condition.find('p').get_text()
    skies = y_data.select("div span[data-reactid*='26']")[0].text
    try:  # try / except because weather network removes div when not necessary. If no snow, look for rain
        snow = w_data.find("div", {"class": "wxRow wx_detailed-metrics stripeable wx_snow_long wx_24h_xlong"}).text
        if snow == '-':
            snow = ' 0 mm'
        snow = snow + ' of Snow'
    except AttributeError:
        try:
            snow = w_data.find("div", {"class": "wxRow wx_detailed-metrics stripeable wx_snow_long"}).text
            if snow == '-':
                snow = ' 0 mm'
            snow = snow + ' of Snow'
        except AttributeError:
            snow = 'Information unavailable'
    try:  # try / except because weather network removes div when not necessary. If no rain, look for snow
        precip = w_data.find("div", {"class": "wxRow wx_detailed-metrics stripeable wx_rain_long"}).text
        if precip == '-':
            precip = ' 0 mm'
        precip = precip + ' of Rain'
    except AttributeError:
        try:
            precip = w_data.find("div", {"class": "wxRow wx_detailed-metrics stripeable wx_rain_long wx_24h_xlong"}).text
            if precip == '-':
                precip = ' 0 mm'
            precip = precip + ' of Rain'
        except AttributeError:
            precip = 'Information unavailable'

    # Multiple Days forecast
    # Forecast for tomorrow
    forecast_01_day = y_data.select("div span[data-reactid*='221']")[0].text
    forecast_01_high = y_data.select("div span[data-reactid*='231']")[0].text
    forecast_01_low = y_data.select("div span[data-reactid*='234']")[0].text
    forecast_01_rain = y_data.select("div span[data-reactid*='227']")[0].text

    # Forecast for 2 days from today
    forecast_02_day = y_data.select("div span[data-reactid*='241']")[0].text
    forecast_02_high = y_data.select("div span[data-reactid*='251']")[0].text
    forecast_02_low = y_data.select("div span[data-reactid*='254']")[0].text
    forecast_02_rain = y_data.select("div span[data-reactid*='247']")[0].text

    # Forecast for 3 days from today
    forecast_03_day = y_data.select("div span[data-reactid*='261']")[0].text
    forecast_03_high = y_data.select("div span[data-reactid*='271']")[0].text
    forecast_03_low = y_data.select("div span[data-reactid*='274']")[0].text
    forecast_03_rain = y_data.select("div span[data-reactid*='267']")[0].text

    # Forecast for 4 days from today
    forecast_04_day = y_data.select("div span[data-reactid*='281']")[0].text
    forecast_04_high = y_data.select("div span[data-reactid*='291']")[0].text
    forecast_04_low = y_data.select("div span[data-reactid*='294']")[0].text
    forecast_04_rain = y_data.select("div span[data-reactid*='287']")[0].text

    # Forecast for 5 days from today
    forecast_05_day = y_data.select("div span[data-reactid*='301']")[0].text
    forecast_05_high = y_data.select("div span[data-reactid*='311']")[0].text
    forecast_05_low = y_data.select("div span[data-reactid*='314']")[0].text
    forecast_05_rain = y_data.select("div span[data-reactid*='307']")[0].text

    print("""
    Your Current location is: {}
    The temperature in your area is: {}
    It feels like: {}
    The High for today is: {}
    The Low for today is: {}
    Wind conditions are: {}
    Skies are currently: {}
    Estimated amount of rain over 24 hours: {}
    Estimated amount of snow over 24 hours: {}
    """.format(loc, temp, feels_like, high, low, condition, skies, precip, snow))

    print("Your Five Day Forecast")
    print("""
    Day 1: On {} the high will be {} the low will be {} with {} chance of precipitation.
    Day 2: On {} the high will be {} the low will be {} with {} chance of precipitation.
    Day 3: On {} the high will be {} the low will be {} with {} chance of precipitation.
    Day 4: On {} the high will be {} the low will be {} with {} chance of precipitation.
    Day 5: On {} the high will be {} the low will be {} with {} chance of precipitation.
    """.format(forecast_01_day, forecast_01_high, forecast_01_low, forecast_01_rain,
               forecast_02_day, forecast_02_high, forecast_02_low, forecast_02_rain,
               forecast_03_day, forecast_03_high, forecast_03_low, forecast_03_rain,
               forecast_04_day, forecast_04_high, forecast_04_low, forecast_04_rain,
               forecast_05_day, forecast_05_high, forecast_05_low, forecast_05_rain))


if __name__ == '__main__':
    main()
