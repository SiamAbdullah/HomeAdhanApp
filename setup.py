from datetime import datetime
import os
import ifaddr
import ipaddress
import logging
import soco
import socket
import SonosNetwork

def main():
    """ Prints the name of each discovered player in the network. """
    zone = SonosNetwork.getZone()
    if zone != None:
      print(zone.player_name)


if __name__ == "__main__":
    main()