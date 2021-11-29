#!/usr/bin/python3

import argparse
import logging
import logging.handlers
import random
import requests
import sys
import time

# Setup LOG
logging.basicConfig()
LOG = logging.getLogger(__name__)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)

LOG.setLevel(logging.DEBUG)

class EosLights():

    def __init__(self, controller_ip=None, api_id=None):
        self.controller_ip = controller_ip
        self.api_id = api_id
        self.base_url = f"http://{controller_ip}/api/{api_id}"
        LOG.debug("Initialized")

    def switch_on(self, light_id=None):
        url = f"{self.base_url}/lights/{light_id}/state"
        d = { "on": True }
        LOG.debug(f"-->calling {url}")
        LOG.debug(f"-->data {d}")
        r = requests.put(url=url, json=d)

    def switch_off(self, light_id=None):
        url = f"{self.base_url}/lights/{light_id}/state"
        d = { "on": False }
        LOG.debug(f"-->calling {url}")
        LOG.debug(f"-->data {d}")
        r = requests.put(url=url, json=d)

    def is_on(self, light_id=None):
        url = f"{self.base_url}/lights/{light_id}"
        LOG.debug(f"-->calling {url}")
        r = requests.get(f"{url}")
        return(r.json()["state"]["on"])

    def get_light_info(self, light_id=None):
        url = f"{self.base_url}/lights/{light_id}"
        LOG.debug(f"-->calling {url}")
        r = requests.get(f"{url}")
        return(r.json())

    def set_hue(self, light_id=None, hue=None):
        url = f"{self.base_url}/lights/{light_id}/state"
        d = { "hue": hue }
        LOG.debug(f"-->calling {url}")
        LOG.debug(f"-->data {d}")
        r = requests.put(url=url, json=d)

    def party(self, light_id=None, n=30, interval=0.2):
        for i in range(0,n):
            n = random.randrange(0,65535)
            self.set_hue(light_id=light_id, hue=n)
            time.sleep(interval)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="eos lights")

    parser.add_argument("--loglevel", type = str, nargs = "?",
                        default="DEBUG",
                        help = "CRITICAL|ERROR|WARNING|INFO|DEBUG")

    parser.add_argument("--controller", type = str, nargs = "?",
                        help = "Controller IP address")

    parser.add_argument("--key", type = str, nargs = "?",
                        help = "API key")

    parser.add_argument("--on", type = str, nargs = "?",
                        help = "Switch on Light ID")

    parser.add_argument("--off", type = str, nargs = "?",
                        help = "Switch off Light ID")

    parser.add_argument("--color", type = str, nargs = "?",
                        help = "Set 0-65535 color. Format is LightID,color")

    parser.add_argument("--party", type = str, nargs = "?",
                        help = "Make a party on Light ID")

    args = parser.parse_args()

    # modify log level if required
    ll = {"CRITICAL": logging.CRITICAL,
          "ERROR": logging.ERROR,
          "WARNING": logging.WARNING,
          "INFO": logging.INFO,
          "DEBUG": logging.DEBUG}
    LOG.setLevel(ll[args.loglevel])

    lights = EosLights(controller_ip=args.controller, api_id=args.key)

    if args.on is not None:
        lights.switch_on(light_id=args.on)
    if args.off is not None:
        lights.switch_off(light_id=args.off)
    if args.color is not None:
        (lid, color) = args.color.split(",")
        lights.set_hue(light_id=lid, hue=int(color))
    if args.party is not None:
        lights.party(light_id=args.party)

    LOG.info("EXITED")

    sys.exit(0)
