import requests
import json
import datetime
import time
import pytz


def get_time_data(url="https://yandex.com/time/sync.json?geo=213"):
    try:
        start_time = datetime.datetime.now(datetime.timezone.utc).timestamp()

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        end_time = datetime.datetime.now(datetime.timezone.utc).timestamp()
        rtt = end_time - start_time

        return data, rtt

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к ресурсу: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"Ошибка при разборе JSON: {e}")
        return None, None


def format_time_data(data):
    if not data:
        return None, None

    timestamp = data.get("timestamp")
    timezone_id = data.get("timezone_id")

    if timestamp is None or timezone_id is None:
        print("Отсутствуют необходимые данные о времени или временной зоне.")
        return None, None

    timezone = pytz.timezone(timezone_id)
    dt_object = datetime.datetime.fromtimestamp(timestamp, tz=timezone)

    formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    return formatted_time, timezone_id


def calculate_time_delta(data):
    if not data:
        return None

    timestamp = data.get("timestamp")

    if timestamp is None:
        print("Отсутствует timestamp в ответе.")
        return None

    now_utc = datetime.datetime.now(datetime.timezone.utc).timestamp()
    time_delta = timestamp - now_utc
    return time_delta


def run_series_of_requests(num_requests=5):
    deltas = []
    rtts = []

    for i in range(num_requests):
        print(f"Запрос #{i + 1}:")
        data, rtt = get_time_data()

        if data:
            time_delta = calculate_time_delta(data)
            if time_delta is not None:
                deltas.append(time_delta)
                rtts.append(rtt)
                print(f"  Дельта времени: {time_delta:.4f} сек.")
            else:
                print("  Не удалось вычислить дельту времени.")
        else:
            print("  Ошибка получения данных.")

        time.sleep(1)

    if deltas:
        average_delta = sum(deltas) / len(deltas)
        print(f"\nСредняя дельта времени: {average_delta:.4f} сек.")
        print(f"Среднее время затраченное на запрос : {sum(rtts) / len(rtts)}")
    else:
        print("\nНе удалось получить данные для вычисления средней дельты.")


if __name__ == "__main__":
    data, rtt = get_time_data()

    if data:
        print("\nСырой ответ:")
        print(json.dumps(data, indent=4))

        formatted_time, timezone_id = format_time_data(data)
        if formatted_time and timezone_id:
            print(f"\nВремя в понятном формате: {formatted_time}")
            print(f"Временная зона: {timezone_id}")

        time_delta = calculate_time_delta(data)
        if time_delta is not None:
            print(f"\nДельта времени: {time_delta:.4f} сек.")

        print("\nЗапуск серии запросов...")
        run_series_of_requests()
    else:
        print("Не удалось получить данные.")
