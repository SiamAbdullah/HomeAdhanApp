from datetime import datetime
import SonosNetwork

def main():
    """ Prints the name of each discovered player in the network. """
    zone = SonosNetwork.getZone(None)
    if zone != None:
      print(zone.player_name)

if __name__ == "__main__":
    main()