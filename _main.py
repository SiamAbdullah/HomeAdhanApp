from threading import Thread
from time import sleep
from xmlrpc.client import boolean
import schedule
import SonosNetwork
import PrayerTime
import HttpServer
import argparse
import signal


shouldRunning = True

def playAzanOnce(prayerInfo: PrayerTime.PTime, networkName:str, urlPath:str):
    print(prayerInfo.PrayerName, "is due. Playing azan", urlPath)

    prayerInfo.IsPlayed = True
    zone = SonosNetwork.getZone(networkName)
    print(zone)
    zone.volume = 60
    number_in_queue = zone.add_uri_to_queue(urlPath)

    # play_from_queue indexes are 0-based
    zone.play_from_queue(number_in_queue - 1)
    sleep(120)
    #zone.stop()
    print("Adhan is played successfully")
    return schedule.CancelJob

def main(networkName: str, city: str, country: str, method:int, school:1, port:int, enableFileServer:bool):

    """ Get the current machine local ip address."""
    currentMachineIpAddress = SonosNetwork.detect_ip_address();

    """ if the zone is provided by comand line argument then initialize networkName with it.
     if the zon is found then we'll have soco object of the network device. """
    zone = SonosNetwork.getZone(networkName)

    if zone == None:
        print("Could not find the Soundbar network ", networkName, ". Exiting the program.")
        return

    networkName = zone.player_name

    prayerInformation = PrayerTime.PrayerTimeFetcher(country, city, method, school)
    remainingPrayerQueue = []
    currentJob:PrayerTime.PTime = None

    while shouldRunning:
        # if the queue is empty then try to fetch next day information
        if len(remainingPrayerQueue) == 0:
            remainingPrayerQueue = prayerInformation.fetch().getRemainingTodaySalah();

        # if remainingPrayerQueue is still empty then sleep 30 mins
        if len(remainingPrayerQueue) == 0:
            print("There is no prayer today so going to sleep for 1 hour")
            sleep(3600) # sleep for 1 hour
            continue

        currentJob = remainingPrayerQueue.pop(0)

        # remainingPrayerQueue is not empty now schedule for play Azan
        azanSoundUrl = "http://{}:{}/{}".format(currentMachineIpAddress, port, currentJob.AdhanFileName)
        print(currentJob.PrayerName, currentJob.TimeAsString, azanSoundUrl)
        schedule.every().day.at(currentJob.TimeAsString).do(playAzanOnce, currentJob, networkName, azanSoundUrl)
        while currentJob.IsPlayed == False:
            schedule.run_pending()
            sleep(10) #sleep 2 mins

    schedule.clear()
    print("Shutting down the Azan App")

def shutdownHandler(signal_received, frame):
    print("Ctrl-c was pressed.")
    global shouldRunning
    shouldRunning = False
    exit(1)

def TestPlayAzan():
    azanSoundUrl = "http://{}:{}/{}".format(SonosNetwork.detect_ip_address(), args.port, "Adhan.mp3")
    playAzanOnce(PrayerTime.PTime("Zuhr", "01:12"), "Living Room Sono", azanSoundUrl )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-name', type=str, help='Soundbar Network Name', default=None)
    parser.add_argument('-city', type=str, help='Soundbar Network Name', default="Seattle")
    parser.add_argument('-country', type=str, help='Soundbar Network Name', default="USA")
    parser.add_argument('-method', type=int, help='Soundbar Network Name', default=2) # 2 means Islamic Society of North America (ISNA)
    parser.add_argument('-school', type=int, help='Soundbar Network Name', default=1)
    parser.add_argument('-port', type=int, help='ServerPot', default=8000)
    parser.add_argument('-enableFileServer', type=bool, help='Should Enable File server', default=True)
    args = parser.parse_args()

    signal.signal(signal.SIGINT, shutdownHandler)
    # create server to stream Azan to Soundbar
    server = None
    try:
        server = None
        if (args.enableFileServer):
            server = HttpServer.HttpServer(args.port)
            server.start()

        main(args.name, args.city, args.country, args.method, args.school,args.port, args.enableFileServer)
        #mainThread = Thread(target=main, args=(args.name, args.city, args.country, args.method, args.school,args.port, args.enableFileServer))
        #mainThread.run()
        #while shouldRunning:
            # Do nothing and hog CPU forever until SIGINT received.
        #    pass

    except:
        print("Exception occured")
    finally:
        if args.enableFileServer and server != None:
            server.stop()
