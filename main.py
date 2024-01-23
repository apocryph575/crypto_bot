import requests
import json
import telebot


def get_api_tele():
    with open('config.txt', 'r') as file:
        lines = file.readlines()

    bot_token = lines[0].split('"')[1]
    user_id = lines[1].split('"')[1]

    bot = telebot.TeleBot(bot_token)
    return user_id, bot


def read_info_json():
    with open("info.json", "r") as file:
        data = json.load(file)
    return data


def message(ID, bot, text):
    bot.send_message(ID, text)


def get_info(name_crypto):
    base = "https://fapi.binance.com"
    path = "/fapi/v1/ticker/price"
    url = base+path
    param = {'symbol': name_crypto}
    r = requests.get(url, params=param)
    return r.json()


def main():
    data_info = read_info_json()
    ID, bot = get_api_tele()
    message(ID, bot,f" Bot is started")
    crypto_list = []
    for i in data_info["prices"]:
        crypto_list.append("true")
    while True:
        for item in data_info["prices"]:
            try:
                correct_name = item["symbol"]
                info = get_info(correct_name)
                correct_price = info["price"]
                in_t = data_info["prices"].index(item)
                if (((float(correct_price) > float(item["buy"])) and (float(correct_price) < float(item["sell"]))) and (crypto_list[in_t] == "false")):
                    crypto_list[in_t] = "true"
                if (((float(correct_price) < float(item["buy"])) or (float(correct_price) > float(item["sell"]))) and (crypto_list[in_t] == "true")):
                    if (float(correct_price) < float(item["buy"])):
                        message(ID, bot, f" ↘ Waluta {correct_name} - spadła, trzeba kupować, cena - {correct_price} | {item['buy']} ~ {item['sell']} ")
                    elif (float(correct_price) > float(item["sell"])):
                        message(ID, bot, f"↗ Waluta {correct_name} - wzrosła, trzeba sprzedawać, cena - {correct_price} | {item['buy']} ~ {item['sell']} ")
                    crypto_list[in_t] = "false"
            except:
                continue


if __name__ == "__main__":
    main()