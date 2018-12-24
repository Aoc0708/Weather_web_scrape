from selenium import webdriver
import time
import bs4


def main():
    while True:
        my_time = time.localtime()
        # If statement grabs minutes of the hour and modulo divides to run every 15 minutes
        if my_time[4] % 10 == 0:
            print("Information Gathered at: {}".format(time.asctime(my_time)))
            html, driver = get_from_web()
            format_data(html)
            driver.quit()
            time.sleep(540)  # sleeps for 9 minutes
        else:
            time.sleep(1)  # starts checking the time to be ready for when the mod swaps over to 10 minute mark


def get_from_web():
    # Opening web page and getting beautiful soup info
    url = "Web_address_to_scrape_frome"
    driver = webdriver.Chrome(executable_path =r'Insert_path_to_web_driver_here')
    driver.get(url)
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    return soup, driver


def format_data(soup):
    loc = soup.select("div h1[data-reactid*='7']")[0].text
    temp = soup.select("div span[data-reactid*='37']")[0].text
    feels_like = soup.select("div [data-reactid*='477']")[0].text
    high = soup.select("div span[data-reactid*='29']")[0].text
    low = soup.select("div span[data-reactid*='33']")[0].text
    condition = soup.find('div', {'class': 'wind'})
    condition = condition.find('p').get_text()
    skies = soup.select("div span[data-reactid*='26']")[0].text

    # Multiple Days forecast
    # Forecast for tomorrow
    forecast_01_day = soup.select("div span[data-reactid*='221']")[0].text
    forecast_01_high = soup.select("div span[data-reactid*='231']")[0].text
    forecast_01_low = soup.select("div span[data-reactid*='234']")[0].text
    forecast_01_rain = soup.select("div span[data-reactid*='227']")[0].text

    # Forecast for 2 days from today
    forecast_02_day = soup.select("div span[data-reactid*='241']")[0].text
    forecast_02_high = soup.select("div span[data-reactid*='251']")[0].text
    forecast_02_low = soup.select("div span[data-reactid*='254']")[0].text
    forecast_02_rain = soup.select("div span[data-reactid*='247']")[0].text

    # Forecast for 3 days from today
    forecast_03_day = soup.select("div span[data-reactid*='261']")[0].text
    forecast_03_high = soup.select("div span[data-reactid*='271']")[0].text
    forecast_03_low = soup.select("div span[data-reactid*='274']")[0].text
    forecast_03_rain = soup.select("div span[data-reactid*='267']")[0].text

    # Forecast for 4 days from today
    forecast_04_day = soup.select("div span[data-reactid*='281']")[0].text
    forecast_04_high = soup.select("div span[data-reactid*='291']")[0].text
    forecast_04_low = soup.select("div span[data-reactid*='294']")[0].text
    forecast_04_rain = soup.select("div span[data-reactid*='287']")[0].text

    # Forecast for 5 days from today
    forecast_05_day = soup.select("div span[data-reactid*='301']")[0].text
    forecast_05_high = soup.select("div span[data-reactid*='311']")[0].text
    forecast_05_low = soup.select("div span[data-reactid*='314']")[0].text
    forecast_05_rain = soup.select("div span[data-reactid*='307']")[0].text

    print("""
    Your Current location is: {}
    The temperature in your area is: {}
    It feels like: {}
    The High for today is: {}
    The Low for today is: {}
    Wind conditions are: {}
    Skies are currently: {}
    """.format(loc, temp, feels_like, high, low, condition, skies))

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
