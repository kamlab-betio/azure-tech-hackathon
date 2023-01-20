#!usr/bin/env python
# -*- coding: utf-8 -*-
import smbus
import time
import subprocess
i2c = smbus.SMBus(1) # 1 is bus number
addr02=0x3e #lcd
_command=0x00
_data=0x40
_clear=0x01
_home=0x02
display_On=0x0f
LCD_2ndline=0x40+0x80

# お皿の中身がいっぱい(full):1,　空っぽ(not full):0
plate_full = "full"
plate_enpty = "enpty"

#LCD AQM0802/1602
def command(code):
    try:
        i2c.write_byte_data(addr02, _command, code)
        time.sleep(0.5)
    except:
        time.sleep(0.1)
  
def writeLCD(message):
        time.sleep(0.1)
        mojilist=[]
        for moji in message:
                mojilist.append(ord(moji)) 
        try:
            i2c.write_i2c_block_data(addr02, _data, mojilist)
            time.sleep(0.5)
        except:
            time.sleep(0.1)


def writeLCD_2(message):
        command(LCD_2ndline)
        if message == 1:
            message = "Y N"
        elif message == 2:
            message = "N Y"
        elif message == 12:
            message = "Y Y"
        elif message == 0:
            message = "N N"
        # init()
        # command(_clear)
        time.sleep(1)

        mojilist=[]
        for moji in message:
                mojilist.append(ord(moji)) 
        # print(mojilist)
        try:
            time.sleep(0.1)
            i2c.write_i2c_block_data(addr02, _data, mojilist)
            # time.sleep(0.1)
        except:
            time.sleep(0.1)
            # i2c.write_i2c_block_data(addr02, _data, mojilist)

 
def init():
        command(0x38)
        time.sleep(0.1)
        command(0x39)
        time.sleep(0.1)
        command(0x14)
        time.sleep(0.1)
        command(0x73)
        time.sleep(0.1)
        command(0x56)
        time.sleep(0.1)
        command(0x6c)
        time.sleep(0.1)
        command(0x38)
        time.sleep(0.1)
        command(_clear)
        time.sleep(0.1)
        command(display_On)
  
#main

init()
command(_clear)
# writeLCD("1 Table:")
writeLCD("1 2")


# command(LCD_2ndline)
# res = subprocess.check_output(['vcgencmd','measure_temp'])
# print(res)
# res = plate_enpty
# writeLCD(str(res)[4:11])

# writeLCD_2(res)
# time.sleep(0.5)

