from datetime import datetime
import ifaddr
import ipaddress
import logging
import soco
import socket


_LOG = logging.getLogger(__name__)

def _find_ipv4_networks(min_netmask):
    """Discover attached IP networks.

    Helper function to return a set of IPv4 networks to which
    the network interfaces on this node are attached.
    Exclude public, loopback and link local network ranges.

    Args:
        min_netmask(int): The minimum netmask to be used.

    Returns:
        set: A set of `ipaddress.ip_network` instances.
    """

    ipv4_net_list = set()
    adapters = ifaddr.get_adapters()
    for adapter in adapters:
        for ifaddr_network in adapter.ips:
            try:
                ipaddress.IPv4Network(ifaddr_network.ip)
            except ValueError:
                # Not an IPv4 address
                continue

            ipv4_network = ipaddress.ip_network(ifaddr_network.ip)
            # Restrict to private networks, and exclude loopback and link local
            if (
                ipv4_network.is_private
                and not ipv4_network.is_loopback
                and not ipv4_network.is_link_local
            ):
                # Constrain the size of network that will be searched
                netmask = ifaddr_network.network_prefix
                if netmask < min_netmask:
                    _LOG.debug(
                        "%s: Constraining netmask from %d to %d",
                        ifaddr_network.ip,
                        ifaddr_network.network_prefix,
                        min_netmask,
                    )
                    netmask = min_netmask
                network = ipaddress.ip_network(
                    ifaddr_network.ip + "/" + str(netmask),
                    False,
                )
                ipv4_net_list.add(network)

    _LOG.debug("Set of networks to search: %s", str(ipv4_net_list))
    return ipv4_net_list

def detect_ip_address():
    """Return the local ip-address"""
    # Rather hackish way to get the local ip-address, recipy from
    # https://stackoverflow.com/a/166589
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def getZone(networkName:str):
    index = 1;
    zones = [];
    for zone in soco.discover():
        # if the network name is found then don't allow user to choose the network
        if networkName != None and zone.player_name == networkName:
            return zone
        zones.append(zone);
        print(index, zone.player_name)
        index += 1

    print(index, "Exit")
    selected = int(input("Select the network you want to connect : "))
    if (selected >= index or selected < 1):
        return None
    else:
        return zones[selected - 1];