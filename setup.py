import SonosNetwork
import os
import subprocess

def main():
    """ Prints the name of each discovered player in the network. """
    zone = SonosNetwork.getZone(None)
    if zone != None:
      print(zone.player_name)
      #(["python3", "_main.py", " -name \""+zone.player_name+"\""])
      os.system("python3 _main.py -name \""+zone.player_name+"\"")

if __name__ == "__main__":
    main()