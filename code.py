{
    "BOT_TOKEN": "6673412321:AAGh4Y7DTZfnkQs9JYLai81S4mlmkoME9J8",
    "CHAT_ID": "6312386599",
    "BAUDRATE": 115200,
    "UART_INTERFACE": 0,
    "TX_PIN": 12,
    "RX_PIN": 13,
    "APN": "JioNet"
}
from machine import UART, Pin
from time import sleep
import ujson
# import config
class A7600X:
    def __init__(self, interface, baudrate, txpin, rxpin):
        self.uart = UART(interface,
                         baudrate=baudrate,
                         bits=8,
                         parity=None,
                         stop=1,
                         tx=Pin(txpin),
                         rx=Pin(rxpin))
    def _exe_command(self, command):
        self.uart.write(command+'\r\n')
        sleep(2)
        response = self.uart.read()
        print(response.decode('utf-8'))
        return response
    
    def _http_post(self, url, type, data):
        json_data = ujson.dumps(data)
        data_length = len(json_data)
        uart_commands = [
            'AT+HTTPINIT',
            'AT+HTTPPARA="URL","' + url + '"',
            'AT+HTTPPARA="CONTENT","' + type + '"',
            'AT+HTTPDATA={},10000'.format(data_length),
            json_data,
            'AT+HTTPACTION=1',
            'AT+HTTPHEAD',
            'AT+HTTPTERM'
        ]

        for command in uart_commands:
            self._exe_command(command)
import A7600X
from time import sleep
import ujson
# import config
class Main:
    def __init__(self, config_file_path='config.json'):
        with open(config_file_path) as config_file:
            self.config_json = ujson.load(config_file)
            
        self.gsm = A7600X.A7600X(self.config_json['UART_INTERFACE'],
                                 self.config_json['BAUDRATE'],
                                 self.config_json['TX_PIN'],
                                 self.config_json['RX_PIN'])
        self.telegram_url = 'https://api.telegram.org/bot' + \
            self.config_json['BOT_TOKEN'] + '/sendMessage'
        self.http_type = 'application/json'
        sleep(10)
        response = self.gsm._exe_command('AT')
        response += self.gsm._exe_command('ATE')
        response += self.gsm._exe_command('ATI')
        response += self.gsm._exe_command('AT+CIMI')
        response += self.gsm._exe_command('AT+CNUM')
        response += self.gsm._exe_command('AT+COPS?')
        response += self.gsm._exe_command('AT+CPIN?')
        self.gsm._http_post(
            self.telegram_url,
            self.http_type,
            self._telegram_payload(response))

        while True:
            self.gsm._exe_command('AT+CMGF=1')
            sms_response = self.gsm._exe_command('AT+CMGL="REC UNREAD"')
            sms_messages = sms_response.decode('utf-8').split('+CMGL: ')[1:]
#             text.decode("utf-8").encode("windows-1252").decode("utf-8")
#             text.encode("windows-1252").decode("utf-8")
            print(sms_messages)
            for sms_message in sms_messages:
                message_lines = sms_message.split('\r\n')
                timestamp = message_lines[0].split(',')[4].replace('"', '')
                message = message_lines[1]
                formatted_message = "<b>Time: </b>{}\r\n<b>Message: </b>{}".format(
                    timestamp, message)
                self.gsm._http_post(
                    self.telegram_url,
                    self.http_type,
                    self._telegram_payload(formatted_message))
                sms_index = message_lines[0].split(',')[0]
                self.gsm._exe_command('AT+CMGD={}'.format(sms_index))
                sleep(1)
            self.gsm._exe_command('AT+CMGD=1,4')
            sleep(10)
    def _telegram_payload(self, message):
        payload = {
            "chat_id": self.config_json['CHAT_ID'],
            "text": message,
            "parse_mode": "HTML"
        }
        return payload

if __name__ == "__main__":
    Main()
'''digital=Pin(0,Pin.IN)
#analog = Pin(17,Pin.IN)

while True:
    print("Digital Value:",digital.value())
    print("-----------------")
#     analog_value = gpio.input()
#     print("Analog Value:", analog_value)
    time.sleep(1)
from machine import Pin,PWM,ADC
from time import sleep,sleep_us,ticks_us,ticks_diff
#Led pinouts: R,Vcc(Common Anode=on is off, off is on),G,B
'''
Ultrasonic:
u1_tx = 16,   u2_tx = 12,   u3_tx =4
u1_rx=17,   u2_rx=13,   u3_rx=5
Noise Sensors:
front, back ==AO==26,27
left,right==DO==11,18
GSM:
tx=8 , rx=9
Led:
red1=21, blue1=19, green1=20
red2=0, blue2=1
noise_blue=6 ,
noise_red=7
#(0,1),(4,5),(8,9),(12,13),(16,17)'''
#Ultra+LED
red1=Pin(21,Pin.OUT)
blue1=Pin(19,Pin.OUT)
green1=Pin(20,Pin.OUT)
red2=Pin(0,Pin.OUT)
blue2=Pin(1,Pin.OUT)
#Sound+LED
noise_red=Pin(7,Pin.OUT)
noise_blue=Pin(6,Pin.OUT)
noise_green=Pin(3,Pin.OUT)
#sound_front= Pin(26, Pin.IN, Pin.PULL_DOWN)  DOUBT
# sound_back= Pin(6, Pin.IN, Pin.PULL_DOWN)
sound_left= Pin(11, Pin.IN, Pin.PULL_DOWN)
sound_right= Pin(18, Pin.IN, Pin.PULL_DOWN)
def led_blink(l):
    for i in range(20):
        l.value(0)
        sleep(0.08)
        l.value(1)
        sleep(0.08)
def sound_led_blink(led):
    for i in range(10):
            led.off()
            sleep(0.1)
            led.on()
            sleep(0.1)

u1_tx=Pin(16,Pin.OUT)
u1_rx=Pin(17,Pin.IN)
u2_tx=Pin(12,Pin.OUT)
u2_rx=Pin(13,Pin.IN)
u3_tx=Pin(4,Pin.OUT)
u3_rx=Pin(5,Pin.IN)
def distance(tx,rx):
    tx.on()
    sleep_us(10)
    tx.off()
    while rx.value()==0:
        start_time=ticks_us()
    while rx.value()==1:
        end_time=ticks_us()
    t=ticks_diff(end_time,start_time)
    dist=(t*0.0343)/2
    return dist

while True:
    red1.on()
    red2.on()
    blue1.on()
    blue2.on()
    green1.on()
    noise_red.on()
    noise_blue.on()
    noise_green.on()
    adc1=ADC(Pin(26))
    adc2=ADC(Pin(27))
    f=adc1.read_u16()
    b=adc2.read_u16()
    
    dr=distance(u1_tx,u1_rx)
    print("Right Distance: {:.2f} cm".format(dr))
    dl=distance(u2_tx,u2_rx)
    print("Left Distance: {:.2f} cm".format(dl))
    df=distance(u3_tx,u3_rx)
    print("Front Distance: {:.2f} cm".format(df))
    print("-------")
    
    print("Front Sound::{:.2f} Hz  Back Sound::{:.2f} Hz".format(f,b))
    print("Left  Sound::{:.2f} Hz   Right Sound::{:.2f} Hz".format(sound_left,sound_right))
    print("------------")
    
    if(dr<=30 and dl>30):
        blue1.on()
        red1.off()
        led_blink(red1)
        red1.on()
    sleep(0.5)
    if(dl<=30 and dr>30):
        blue2.on()
        red2.off()
        led_blink(red2)
        red2.on()
    sleep(0.5)
    if (dr<=30 and dl<=30):
        red1.on()
        red2.on()
        blue1.off()
        blue2.off()
        if(dr<dl):
            led_blink(blue1)
        if(dl<dr):
            led_blink(blue2)
        blue1.on()
        blue2.off()
    sleep(0.5)
    if(20<=df<=40):
        green1.off()
        sleep(2)
#     Noise Sensor
    if f>=2500:
        sound_led_blink(noise_green)
    if b >= 3000:
        sound_led_blink(noise_red)
    if left==1 or right==1:
        sound_led_blink(noise_blue)
    
    noise_red.on()
    noise_blue.on()
    noise_green.on()   
#     sleep(2)
    red1.on()
    red2.on()
    blue1.on()
    blue2.on()
    green1.on()
    sleep(1)
