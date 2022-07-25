import threading
import time
from random import randrange
from flask import Flask, render_template
from bridge import Bridge
from csv_file import *
from config import CONFIGS

result_file = CSV_File(CONFIGS.CSV_PATH)  # select CSV file.
csv_file_limit = CONFIGS.CSV_LIMIT  # Set limit of CSV file.

app = Flask(__name__)  # create Flask application.

generator = threading.Condition()  # create threading condition.

first_number = Bridge()  # create object to transmit data of first number between threads.
second_number = Bridge()  # create object to transmit data of second number between threads.
web_info = Bridge()  # create object to send last generated numbers to Flask server.
web_info.send([result_file.read_csv(index=-1)[0], result_file.read_csv(index=-1)[1]])


def thread_generator():
    """
    Wait until notify is getted to generate number.
    """
    while True:
        with generator:
            generator.wait()
            second_random_number = randrange(CONFIGS.SECOND_RANGE_LIMITS[0], CONFIGS.SECOND_RANGE_LIMITS[1])
            print("__________________________",
                  f"second random number from ({CONFIGS.SECOND_RANGE_LIMITS[0]},{CONFIGS.SECOND_RANGE_LIMITS[1]}) ",
                  f"[{second_random_number}]")
            second_number.send(second_random_number)


def thread_printer(number):
    """
    First Thread to wait 1 minute and send number.
    """
    print(f"thread started.{number}")
    time.sleep(CONFIGS.TIMER_1MIN)
    first_number.send(number)
    with generator:
        generator.notify()


def main_thread():
    """
    Main thread to generate number each 5 seconds.
    Run other threads by condition.
    """
    thread_status = False
    while True:
        time.sleep(CONFIGS.TIMER_5SEC)
        first_random_number = randrange(CONFIGS.FIRST_RANGE_LIMITS[0], CONFIGS.FIRST_RANGE_LIMITS[1])
        print(
            f"first random number from ({CONFIGS.FIRST_RANGE_LIMITS[0]}, {CONFIGS.FIRST_RANGE_LIMITS[1]})",
            f" [{first_random_number}]")
        if first_random_number > CONFIGS.CONDITION:
            if not thread_status:
                thr = threading.Thread(target=thread_printer, args=(first_random_number,), name="thread_printer")
                thr.start()
                thread_status = not thread_status
            else:
                thread_status = thr.is_alive()
        if not first_number.is_empty() and not second_number.is_empty():
            print("send to scv file>", f" first [{first_number}], second [{second_number}]")
            web_info.receive()
            web_info.send([first_number.item[0], second_number.item[0]])
            result_file.send_to_csv(
                send_data={"first_number": first_number.receive(), "second_number": second_number.receive()})
            result_file.csv_limit(limit=csv_file_limit)


@app.route("/")
def home():
    """
    Home page of Flask server.
    http://127.0.0.1:5000/
    """
    values = result_file.read_csv()[-10:]  # send last 10 values to webpage.
    data = {"title": "Flask Threads",
            "first_number": web_info.item[0][0],
            "second_number": web_info.item[0][1]
            }
    return render_template("home.html", data=data, values=values)


def server_thread():
    """
    Thread to run Flask server.
    """
    app.run()


def main():
    threading.Thread(target=thread_generator, name="generator").start()  # start generator thread.
    threading.Thread(target=server_thread, name="web").start()  # start Flask server thread.
    main_thread()  # open main thread.


if __name__ == "__main__":
    main()
