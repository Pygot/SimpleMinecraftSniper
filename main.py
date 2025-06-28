"""
╔════════════════════════════════════════════════════════════╗
║  Author  : pygot                                           ║
║  GitHub  : https://github.com/pygot                        ║
╚════════════════════════════════════════════════════════════╝
"""
# main.py

from tzlocal import get_localzone
from datetime import datetime
from requests import put
from secret import token
from time import sleep

import pytz

local_tz = get_localzone()

# - CONFIG -
# Go to: namemc.com/minecraft-names?sort=asc&length_op=&length=3&lang=&searches=100
time_left = "2025-07-05T20:11:56.790Z"
# Then right-click the date and grab the datetime="XXX-XXX0Z"
target = "Eternal"  # Target username


def snipe(name):
    """
    Sends a PUT request to the Minecraft Services API to update a player's username.

    The function interacts with the official Minecraft API to change the username
    associated with the currently authenticated user. It requires a valid
    authorization token to execute successfully. Make sure to replace the placeholder
    `token` with an actual authorized token prior to execution. It handles the request
    via a PUT method to communicate with the specific API endpoint.

    :param name: The desired Minecraft username to be set.
    :type name: str
    :return: The response object from the PUT request.
    :rtype: requests.Response
    """
    return put(
        f"https://api.minecraftservices.com/minecraft/profile/name/{name}",
        headers={
        "accept": "*/*",
        "accept-language": "cs-CZ,cs;q=0.9,en;q=0.8",
        "authorization": token
    })


def sleeptime():
    """
    Calculates the sleep time in seconds between the current time and a target
    time by subtracting 0.8 seconds from the computed difference. The target
    time is assumed to be in UTC and converted to the local time zone before
    calculating the difference.

    :raises ValueError: If the `time_left` cannot be parsed into a datetime
        object due to an invalid format.
    :raises OverflowError: If the calculated sleep time exceeds the allowable
        numeric range for floating-point values.
    :return: The calculated sleep time in seconds as a floating-point number.
    :rtype: float
    """
    now = datetime.now(local_tz)
    then_utc = datetime.strptime(time_left, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
    then_local = then_utc.astimezone(local_tz)
    return (then_local - now).total_seconds() - 0.8


def main():
    """
    Main function responsible for executing a continuous sniping process.

    This function initiates by determining the sleep time using the `sleeptime`
    function. It then enters a repetitive loop, where it performs the sniping
    operation by calling `snipe(target)` and evaluating the responses. Based
    on specific response details (e.g., "DUPLICATE" status), the loop adjusts
    its behavior, including varying sleep intervals. The process runs until
    interrupted by external signals such as a keyboard interrupt or an
    unexpected error.

    :raises KeyboardInterrupt: If the program is manually stopped by the user.
    :raises Exception: When any error other than a keyboard interrupt occurs.
    """
    try:
        index = 0
        seconds = sleeptime()
        print("Sleeping for", seconds, "seconds...")
        sleep(seconds)
        print("Sniping...")
        while True:
            response = snipe(target).json()
            details = response.get("details", {})
            if details.get("status") == "DUPLICATE":
                if index == 0: index_sleep = 0.7
                elif index == 1: index_sleep = 0.11
                else: continue
                sleep(index_sleep)
                index += 1
                continue
            sleep(1)
    except KeyboardInterrupt: print("Program stopped.")
    except Exception as e: print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()