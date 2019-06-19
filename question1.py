# coding: UTF-8
import RPi.GPIO as GPIO
from time import sleep

LED = 25

qlist = [
    ['第1問：昨日巨人が勝ったか？', 1],
    ['第2問：私の大好物は焼肉である？', 0],
    ['第3問：ビッグデータとはビックリするようなデータである', 0],
    ['第4問：javaとjavascriptは同じだ', 0],
    ['第5問：RasbianはLinuxベースのOSである', 1],
    ['第6問：今日の昼ごはんはそばだった', 1],
    ['第7問：朝ごはんは食べた', 1],
    ['第8問：unixよりlinuxの方が先に作られた', 0],
    ['第9問：ラズパイは1990年代に初めて作られた', 0],
    ['第10問：ウナギの完全養殖はまだ出来ていない', 1]
]

def lchika():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)

    for i in range(5):
        GPIO.output(LED, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(LED, GPIO.LOW)
        sleep(0.5)
    
    GPIO.cleanup()

try:
    for l in qlist:
        print(l[0])
        answer = input()
        if answer == l[1]:
            print('正解')
            lchika()
        elif:
            print('間違い')    
except KeyboardInterrupt:
    pass

