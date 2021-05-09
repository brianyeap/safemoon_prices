import requests
import time
from playsound import playsound
from win32com.client import Dispatch
import numpy as np


def bit_mart_sfm():
    bit_mart_url = "https://api-cloud.bitmart.com/spot/v1/ticker?symbol=SAFEMOON_USDT"
    bit_mart_response = requests.request("GET", bit_mart_url).json()
    bit_mart_price = bit_mart_response["data"]["tickers"][0]["last_price"]
    print(f"Bitmart - OK ({bit_mart_price})")
    return bit_mart_price


def pancake_sfm():
    pancake_url = "https://api.pancakeswap.info/api/tokens"
    pancake_request = requests.request("GET", pancake_url).json()
    pancake_address = "0x8076C74C5e3F5852037F31Ff0093Eeb8c8ADd8D3"
    pancake_price = pancake_request["data"][pancake_address]["price"]
    print(f"Pancake - OK ({float(pancake_price):.8f})")
    return pancake_price


def gate_sfm():
    gate_url = "https://data.gateapi.io/api2/1/tickers"
    gate_request = requests.request("GET", gate_url).json()
    gate_price = gate_request["safemoon_usdt"]["last"]
    print(f"Gate.io - OK ({gate_price})")
    return gate_price


def whitebit_sfm():
    whitebit_url = "https://whitebit.com/api/v1/public/ticker?market=SFM_USDT"
    whitebit_request = requests.request("GET", whitebit_url).json()
    whitebit_price = whitebit_request["result"]["last"]
    print(f"Whitebit - OK ({whitebit_price})")
    return whitebit_price


def mxc_sfm():
    mxc_url = "https://www.mxc.com/open/api/v2/market/ticker"
    mxc_request = requests.request("GET", mxc_url).json()
    mxc_exchanges = mxc_request["data"]

    for exchange in mxc_exchanges:
        if exchange["symbol"] == "SAFEMOON_USDT":
            print(f"MXC - OK ({exchange['last']})")
            return exchange["last"]


def zbg_sfm():
    zbg_url = "https://www.zbg.com/exchange/config/controller/website/pricecontroller/getassistprice?coins=usdt,safemoon"
    zbg_response = requests.request("POST", zbg_url).json()
    zbg_price = zbg_response['datas']['usd']['safemoon']
    print(f"ZBG - OK ({zbg_price})")
    return zbg_price


def alert(loop, interval):
    count = 0
    while count < loop:
        playsound('./src/audio/alarm.mp3')
        time.sleep(interval)
        count += 1


def robot_speak(stuff):
    speak = Dispatch("SAPI.SpVoice").Speak
    speak(stuff)


def opportunity(dif, pancake, bit_mart, gate, whitebit, mxc, zbg):
    pancake_price = float(pancake)
    bit_mart_price = float(bit_mart)
    gate_price = float(gate)
    whitebit_price = float(whitebit)
    mxc_price = float(mxc)
    zbg_price = float(zbg)
    exchanges = [["Pancake", pancake_price], ["Bitmart", bit_mart_price], ["Gate.io", gate_price],
                 ["Whitebit", whitebit_price], ["MXC", mxc_price], ["ZBG", zbg_price]]
    exchange_dif = []
    price_dif = []

    for exchange1 in exchanges:
        for exchange2 in exchanges:
            if exchange1[0] != exchange2[0]:
                if exchange1[1] > exchange2[1]:
                    exchange_dif.append(
                        [exchange1[0], exchange2[0], ((exchange1[1] - exchange2[1]) / exchange1[1]) * 100,
                         [exchange1[1], exchange2[1]]])
                    price_dif.append(exchange1[1] - exchange2[1])
                else:
                    exchange_dif.append(
                        [exchange2[0], exchange1[0], ((exchange2[1] - exchange1[1]) / exchange2[1]) * 100,
                         [exchange2[1], exchange1[1]]])
                    price_dif.append(exchange2[1] - exchange1[1])

    max_price_dif_index = np.argmax(price_dif, axis=0)
    max_dif_exchange = exchange_dif[max_price_dif_index]

    if max_dif_exchange[2] > dif:
        print("\n")
        print("--------------------CAN DO!--------------------")
        print(f"{max_dif_exchange[1]} -> {max_dif_exchange[0]}")
        print(f"{max_dif_exchange[1]}: {max_dif_exchange[3][1]:.8f}")
        print(f"{max_dif_exchange[0]}: {max_dif_exchange[3][0]:.8f}")
        print(f"Difference: {round(max_dif_exchange[2], 2)}%")
        print("--------------------CAN DO!--------------------")
        print("\n")
        robot_speak(f"{max_dif_exchange[1]} to {max_dif_exchange[0]}, difference {round(max_dif_exchange[2], 2)}%")
        robot_speak(f"{max_dif_exchange[0]}, {round(max_dif_exchange[3][0] * 100000000)}")
        # alert(3, 1)
    else:
        print("\n")
        print("--------------------CAN'T DO!--------------------")
        print(f"{max_dif_exchange[1]} -> {max_dif_exchange[0]}")
        print(f"{max_dif_exchange[1]}: {max_dif_exchange[3][1]:.8f}")
        print(f"{max_dif_exchange[0]}: {max_dif_exchange[3][0]:.8f}")
        print(f"Difference: {round(max_dif_exchange[2], 2)}%")
        print("--------------------CAN'T DO!--------------------")
        print("\n")
        robot_speak(f"{max_dif_exchange[0]}, {round(max_dif_exchange[3][0] * 100000000)}")


def wait(sec):
    count = 1
    while count <= sec:
        print(count)
        time.sleep(1)
        count += 1


target_dif = input("Enter % dif: ")
while True:
    try:
        opportunity(int(target_dif), pancake_sfm(), bit_mart_sfm(), gate_sfm(), whitebit_sfm(), mxc_sfm(), zbg_sfm())
        wait(25)
    except requests.exceptions.ConnectionError:
        wait(25)
