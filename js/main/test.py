import os
import schedule
import win10toast

os.system('cls')

toast = win10toast.ToastNotifier()


def task():
    toast.show_toast(
                    title='Wake up, bruh...',
                    msg='The Matrix has you...',
                    duration=15
                )


schedule.every(1).seconds.do(task)

while True:
    schedule.run_pending()
