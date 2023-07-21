import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import cv2
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch


wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()

def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")



def get_audio():
    print("\nBot: \tĐang nghe \t --__-- \n")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=8)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text.lower()
        except:
            print("...")
            return 0


def stop():
    speak("Hẹn gặp lại bạn sau!")
    time.sleep(2)


def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak("Máy không nghe rõ. Bạn nói lại được không!")
            time.sleep(3)
    time.sleep(2)
    stop()
    return 0


def hello(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(name))
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa.".format(name))
    else:
        speak("Chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ.".format(name))
    time.sleep(5)
    speak("Bạn có khoẻ không ?")
    time.sleep(3)
    ans = get_audio()
    if ans:
        if "có" in ans:
            speak("Thật là tuyệt vời")
        else:
            speak("Bạn cần nghỉ ngơi")

#Mo Web
def open_website(text):
    regex = re.search ('mở (.+)', text)
    if regex:
        domain = regex.group(1)
        url = 'https://www.' + domain
        webbrowser.open(url)
        speak("Trang web đã được mở")
        return True
    else:
        return False


# Ham tim kiem
def google_search(text):
    search_for = text.split("kiếm", 1)[1]
    speak("Oke")
    driver = webdriver.Chrome(path)
    driver.get("http://www.google.com.vn")
    query = driver.find_element_by_xpath("//input[@name='q']")
    query.send_keys(str(search_for))
    query.send_keys(Keys.RETURN)
    time.sleep(10)

#Ham bat nhac tren YouTube

def play_youtube():
    speak("Chọn tên bài hát")
    my_song = get_text()
    while True:
        result = YoutubeSearch(my_song, max_results = 10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    speak("Bài hát đã được bật")
    time.sleep(15)


#Ham thoi gian ngay thang

def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút %d giây' % (now.hour, now.minute, now.second))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d" %
              (now.day, now.month, now.year))
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")
    time.sleep(4)


def qr_code(text):
    cam=cv2.VideoCapture(0)
    if "quét mã" in text:
        speak("Bắt đầu quét mã QR. ấn Q để quét")

    while True:
        ret,frame=cam.read()
        cv2.imshow("QR",frame)
        k=cv2.waitKey(1)
        if(k==113):
            break
    rQR=cv2.QRCodeDetector()
    v=rQR.detectAndDecode(frame)
    print("Gia tri nhan duoc là:",v[0])
    webbrowser.open(v[0],new=1)
    speak("Kết quả vừa được quét đang được mở")
    time.sleep(5)
    cam.release()
    cv2.destroyAllWindows()

#Ham ket noi camera
def cam(text):
    url = input("Camera's IP address: ")
    video = cv2.VideoCapture(url)
    if "camera" in text:
        speak("Kết nối camera, nhấn phím x để ngừng truy cập camera")
    while True:
        ret, frame = video.read()
        if ret:
            cv2.imshow("IPCam", frame)
        if cv2.waitKey(1) == ord("x"):
            break
    video.release()
    cv2.destroyAllWindows()


#Ham du bao thoi tiet
def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    time.sleep(3)
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute, 
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        speak(content)
        time.sleep(28)
    else:
        speak("Không tìm thấy địa chỉ của bạn")
        time.sleep(2)

#Ham mo cac ung dung
def open_app(text):
    if"google" in text:
        speak ("Mở google chrome")
        os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe')
        speak("Phần mềm chưa được cài đặt")

#Ham nhan dien
def open_nhandien(text):
    if "nhận diện" in text:
        speak("Mở trang web nhận diện")

        webbrowser.open('https://sour-verdant-cactus.glitch.me/',new=1)
        speak("Ok!Trang nhận diện đang được mở")
        time.sleep(30)

#Ham wikipedia
def wiki():
    try:
        speak("Bạn muốn biết gì nhỉ?")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(20)
        for content in contents[1:]:
            speak("Bạn muốn nghe tiếp về chủ đề này hay không")
            ans = get_text()
            if "không" in ans:
                break
            speak(content)
            time.sleep(20)
        speak("Kết quả tìm kiếm đã được đọc")
    except:
        speak("Bot không rõ dữ liệu cần tìm kiếm")
        


#Ham chay tro ly
def assistant():
    speak("Xin chào, bạn tên là gì nhỉ?")
    time.sleep(2)
    name = get_text()
    if name:
        speak("Chào bạn {}".format(name))
        speak("Bạn cần Bot có thể giúp gì ạ?")
        time.sleep(3)
        while True:
            text = get_text()
            if not text:
                break
            elif "trò chuyện" in text or "nói chuyện" in text:
                hello(name)

            elif "dừng" in text or "tạm biệt" in text or "chào robot" in text or "ngủ thôi" in text:
                stop()
                break
            elif "mở" in text:
                if "mở và tìm kiếm" in text:
                    google_search(text)  
                elif "." in text:
                    open_website(text)
                else:
                    open_app(text)


            elif "ngày" in text or "giờ" in text:
                get_time(text)
            elif "bật nhạc" in text:
                play_youtube()
            elif "thời tiết" in text:
                current_weather()
            elif "định nghĩa" in text:
                wiki()
            elif "nhận diện" in text:
                open_nhandien(text)

            elif "quét mã" in text:
                qr_code(text)
            elif "camera" in text:
                cam(text)
assistant()