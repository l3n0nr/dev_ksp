#!/usr/bin/env python
import os

def calculate():
    value = raw_input("Time[HH:MM:SS]: ")       # 040506 = 04h 05m 06s

    # convert numbers
    hours = int(value[0:2])
    minute = int(value[2:4])
    second = int(value[4:6])

    hours_conv = (hours * 3600)
    minute_conv = (minute * 60)
    second_conv = (hours_conv + minute_conv + second)

    print second_conv, "seconds"

def main():
    calculate()

# call main function
main()