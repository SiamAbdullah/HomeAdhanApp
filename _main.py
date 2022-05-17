from threading import Thread
from time import sleep
import schedule
import SonosNetwork
import PrayerTime
import HttpServer
import argparse
import signal


shouldRunning = True

def playAzanOnce(prayerInfo: PrayerTime.PTime, zone, urlPath:str):
    print(prayerInfo.PrayerName, "is due. Playing azan", urlPath)

    number_in_queue = zone.add_uri_to_queue(urlPath)
    zone.volume = 55
    # play_from_queue indexes are 0-based
    zone.play_from_queue(number_in_queue - 1)
    sleep(180)
    prayerInfo.IsPlayed = True
    print("Adhan is played successfully")
    return schedule.CancelJob

def main(networkName: str, city: str, country: str, method:int, school:1, port:int):

    """ if the zone is provided by comand line argument then initialize networkName with it.
     if the zon is found then we'll have soco object of the network device. """
    zone = SonosNetwork.getZone(networkName)

    if zone == None:
        print("Could not find the Soundbar network ", networkName, ". Exiting the program.")
        return

    print("Found the Soundbar network :", zone)

    # create server to stream Azan to Soundbar
    server = HttpServer.HttpServer(port)
    server.start()

    """ Get the current machine local ip address."""
    currentMachineIpAddress = SonosNetwork.detect_ip_address();

    prayerInformation = PrayerTime.PrayerTimeFetcher(country, city, method, school)
    remainingPrayerQueue = []
    currentJob:PrayerTime.PTime = None

    while shouldRunning:
        # if the queue is empty then try to fetch next day information
        if len(remainingPrayerQueue) == 0:
            remainingPrayerQueue = prayerInformation.fetch().getRemainingTodaySalah();

        # if remainingPrayerQueue is still empty then sleep 30 mins
        if len(remainingPrayerQueue) == 0:
            sleep(1800) # sleep for 1 hour
            continue

        currentJob = remainingPrayerQueue.pop(0)

        # remainingPrayerQueue is not empty now schedule for play Azan
        azanSoundUrl = "http://{}:{}/{}".format(currentMachineIpAddress, port, currentJob.AdhanFileName)
        print(currentJob.PrayerName, currentJob.TimeAsString, azanSoundUrl)
        schedule.every().day.at("22:20").do(playAzanOnce, currentJob, zone, azanSoundUrl)
        while currentJob.IsPlayed == False:
            schedule.run_pending()
            sleep(10) #sleep 2 mins

    schedule.clear()
    server.stop();
    print("Shutting down the Azan App")

def shutdownHandler(signal_received, frame):
    print("Ctrl-c was pressed.")
    global shouldRunning
    shouldRunning = False
    exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-name', type=str, help='Soundbar Network Name', default=None)
    parser.add_argument('-city', type=str, help='Soundbar Network Name', default="Seattle")
    parser.add_argument('-country', type=str, help='Soundbar Network Name', default="USA")
    parser.add_argument('-method', type=int, help='Soundbar Network Name', default=1)
    parser.add_argument('-school', type=int, help='Soundbar Network Name', default=1)
    parser.add_argument('-port', type=int, help='ServerPot', default=8000)
    args = parser.parse_args()

    signal.signal(signal.SIGINT, shutdownHandler)
    mainThread = Thread(target=main, args=(args.name, args.city, args.country, args.method, args.school,args.port))
    mainThread.run()
    while True:
        # Do nothing and hog CPU forever until SIGINT received.
        pass
