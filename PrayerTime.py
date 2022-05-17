import requests
import json
from datetime import datetime

AdhanMusic = {"Fajr":"FajrAdhan.mp3", "Zuhr":"Adhan.mp3", "Asr":"Adhan.mp3", "Maghrib":"Adhan.mp3", "Eisha":"Adhan.mp3"}

class PTime:
    def __init__(self, prayerName: str, strTime: str):
        parts = strTime.split(":")
        self.PrayerName = prayerName
        self.Hour = 0
        self.Minute = 0
        self.HasValue = False
        self.TimeAsString = strTime
        self.IsPlayed = False
        self.AdhanFileName = AdhanMusic[prayerName]
        if len(parts) == 2:
            self.Hour = int(parts[0])
            self.Minute = int(parts[1])
            self.HasValue = True

    def IsPrayerTimeValid(self, currentHour, currentMinute)->bool:
        if (self.Hour < currentHour):
            return False
        elif (self.Hour == currentHour and self.Minute < currentMinute):
            return False

        return True


class PrayerTime:
    def __init__(self, date, fajr, zuhr, asr, maghrib, eisha):
        self.Date = date
        self.PrayersTime:list[PTime] = []
        self.PrayersTime.append(PTime("Fajr", fajr))
        self.PrayersTime.append(PTime("Zuhr", zuhr))
        self.PrayersTime.append(PTime("Asr", asr))
        self.PrayersTime.append(PTime("Maghrib", maghrib))
        self.PrayersTime.append(PTime("Eisha", eisha))

    def getRemainingTodaySalah(self)->list:
        availablePrayersForAzan:list[PTime] = []
        currentDateTime = datetime.now()
        if self.Date.date() != currentDateTime.date():
            return availablePrayersForAzan

        currentTime = currentDateTime.time();
        hour = currentTime.hour
        minute = currentTime.minute

        for item in self.PrayersTime:
            if item.IsPrayerTimeValid(hour, minute):
                availablePrayersForAzan.append(item)
        return availablePrayersForAzan


class PrayerTimeFetcher:
    def __init__(self, city:str, country:str, method:int, school:int):
        self.city = city
        self.country = country
        self.method = method
        self.school = school


    def fetch(self)->PrayerTime:
        print("Fetching prayer information: ")
        url = "http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method={method}&school={school}".format(city = self.city, country = self.country, method = self.method, school = self.school)
        apiRequest = requests.get(url)
        jsonContent=json.loads(apiRequest.content)

        dataDate = jsonContent["data"]["date"]["timestamp"]
        prayerDate = datetime.fromtimestamp(int(dataDate))
        fajr=jsonContent["data"]["timings"]["Fajr"]
        zuhr=jsonContent["data"]["timings"]["Dhuhr"]
        asr=jsonContent["data"]["timings"]["Asr"]
        maghrib=jsonContent["data"]["timings"]["Maghrib"]
        eisha=jsonContent["data"]["timings"]["Isha"]

        return PrayerTime(prayerDate, fajr, zuhr, asr, maghrib, eisha)
