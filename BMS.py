import time
from selenium import webdriver
from settings import API_KEY, URL, movie_url, chatId1, chatId2
from selenium. common. exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from telebot import types, apihelper
import telebot

API_KEY = API_KEY
bot = telebot.TeleBot(API_KEY)
apihelper.SESSION_TIME_TO_LIVE = 60 * 5

capabilities = {
    "browserName": "chrome",
    "version": "80.0",
    "enableVNC": True,
    "enableVideo": False
}

driver = webdriver.Remote(
    command_executor= URL,
    desired_capabilities=capabilities)

def startbms():

    theatre_list = ['Bhramaramba 70MM A/C Dts: Kukatpally', 'Mallikarjuna 70mm A/C DTS: Kukatpally', 'Sai Ranga: Miyapur']
    dict_theatre = {}

    for theatre in theatre_list:

        dict_theatre[theatre] = 0 

    url = movie_url

    url_string = url.split('/')

    movie_name = url_string[4].split('-')
    movie_name.remove('hyderabad')

    driver.get(url)

    i = 1
    extracted = 0
    theatreDone = False
    isDone = False

    while not isDone:

        time.sleep(1)

        while not theatreDone:

            try:

                theatre_name = driver.find_element(By.XPATH, '//*[@id="venuelist"]/li[' + str(i) + ']/div[1]/div[2]/div/div[1]/a').text

                for theatre in theatre_list:

                    if theatre == theatre_name:
                        
                        dict_theatre[theatre] = i
                        extracted += 1

                i += 1

                if extracted == 6:

                    theatreDone = True

            except NoSuchElementException:

                i = 1
                theatreDone = True

        for theatre in theatre_list:
            
            j = 1

            if dict_theatre[theatre] > 0:

                theatre_name = driver.find_element(By.XPATH, '//*[@id="venuelist"]/li[' + str(dict_theatre[theatre]) + ']/div[1]/div[2]/div/div[1]/a').text

                if theatre_name == theatre:

                    while j < 9:

                        try:

                            driver.find_element(By.XPATH, '//*[@id="wzrk-cancel"]').click()
                    
                        except NoSuchElementException:

                            try:

                                show_button = driver.find_element(By.XPATH, '//*[@id="venuelist"]/li[' + str(dict_theatre[theatre]) + ']/div[2]/div[2]/div[' + str(j) + ']/a')

                                driver.execute_script("arguments[0].click();", show_button)

                                show_time = driver.find_element(By.XPATH, '//*[@id="venuelist"]/li[' + str(dict_theatre[theatre]) + ']/div[2]/div[2]/div[' + str(j) + ']/a').text

                                j += 1

                                time.sleep(0.5)

                                popup_button = driver.find_element(By.XPATH, '//*[@id="btnPopupCancel"]')
                                select_seat = driver.find_element(By.XPATH, '//*[@id="proceed-Qty"]')
                                back_button = driver.find_element(By.XPATH, '//*[@id="disback"]')

                                if popup_button.is_displayed():

                                    driver.execute_script("arguments[0].click();", popup_button)
                                    bot.send_message(chatId1, "For " + ' '.join(movie_name).upper() + " on " + url_string[6] + "\nTickets available at " + theatre_name + "\nShow time: " + show_time)
                                    bot.send_message(chatId2, "For " + ' '.join(movie_name).upper() + " on " + url_string[6] + "\nTickets available at " + theatre_name + "\nShow time: " + show_time)

                                elif select_seat.is_displayed():
                                    
                                    driver.execute_script("arguments[0].click();", select_seat)
                                    back_button = driver.find_element(By.XPATH, '//*[@id="disback"]')
                                    driver.execute_script("arguments[0].click();", back_button)
                                    bot.send_message(chatId1, "For " + ' '.join(movie_name).upper() + " on " + url_string[6] + "\nTickets available at " + theatre_name + "\nShow time: " + show_time)
                                    bot.send_message(chatId2, "For " + ' '.join(movie_name).upper() + " on " + url_string[6] + "\nTickets available at " + theatre_name + "\nShow time: " + show_time)

                                elif back_button.is_displayed():

                                    driver.execute_script("arguments[0].click();", back_button)
                                    bot.send_message(chatId1, "For " + ' '.join(movie_name).upper() + " on " + url_string[6] + "\nTickets available at " + theatre_name + "\nShow time: " + show_time)
                                    bot.send_message(chatId2, "For " + ' '.join(movie_name).upper() + " on " + url_string[6] + "\nTickets available at " + theatre_name + "\nShow time: " + show_time)

                            except NoSuchElementException:

                                j = 9
                                
                        time.sleep(1)

                else:

                    theatreDone = False

            else:

                theatreDone = False

        time.sleep(20)

        driver.refresh()

startbms()

bot.polling(none_stop=False, interval=0, timeout=20)
