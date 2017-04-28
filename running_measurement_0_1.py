import sys, os, os.path
from ctypes import *
import serial
import operator
import ctypes
import threading
import PyQt4
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import urllib2
from Tkinter import *
import tkFont
import glob
import threading
import imageio
import Queue
import time
from pygame import mixer # Load the required library
mixer.init()
#mixer.music.load('Kalimba.mp3')
#mixer.music.play()
#time.sleep(5)
#mixer.music.stop()
#time.sleep(5)

sys.path.append('D:\Dropbox\MANIP\Code_for_Develop\Bat771_P9\Bat771_P9_Libraries')
sys.path.append('C:\python lab\qubit_setup\instruments')
sys.path.append('C:\python lab\libs\pyview\lib')
sys.path.append('C:\python lab\Bat771_P9\Bat771_P9_Libraries')
import pyttsx
import Logging
reload(Logging)
import Logging as log
import calib
reload(calib)
import calib as ca
import recondense
reload(recondense)
import recondense as recon

from mpl_toolkits.axes_grid1 import make_axes_locatable

engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 100)
engine = pyttsx.init()
voices = engine.getProperty('voices')


import pyvisa
#import os, sys
import itc1_oxford # ITC controls Library
import itc2_oxford # ITC controls Library
import yokogawa # Yokogawa 7651 programmable source
import adlink9826 # ADLINK 9826 DAQ board
import stepper  # step motor control for valve
import awg33250 # high-Freq current  measurement
import lockin_signalrecovery_7265 # lockin amplifier
import teracontrol # Thz source Library

path1=os.path.realpath(__file__+'../../../')
#lockin=lockin_signalrecovery_7265.Instr()
#lockin.initialize()
#itc1 = itc1_oxford.Instr()
#itc1.initialize()
#itc2 = itc2_oxford.Instr()
#itc2.initialize()

####################
#import matplotlib.pyplot as plt


from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

####################

from Measurement_Controller_0_1 import *

from PyQt4 import QtCore, QtGui

from matplotlibwidget import MatplotlibWidget

import scipy.integrate as integrate
import time
import numpy
import numpy as np
import math
import cmath

kb=1.3806485279e-23
#f1=2899169;f2=3814697
charge_e = -1.60217656535e-19
Planck_constant = 6.62607004081e-34
f1 = 3809169
f2 = 3814697

from scipy.optimize import fsolve

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

import threading
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

class Temp_itc_1(QtCore.QThread):

    Temps_sorb = QtCore.pyqtSignal(str)
    Temps_He3Low = QtCore.pyqtSignal(str)
    Temps_He3High = QtCore.pyqtSignal(str)
    Power_ITC_1 = QtCore.pyqtSignal(str)
    Temps_HeatSW = QtCore.pyqtSignal(str)
    Temps_PT2 = QtCore.pyqtSignal(str)
    Power_ITC_2 = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Temp_itc_1, self).__init__(parent)
    def run(self):
        itc1Temp_sorb = str(itc1.Temp_1())
        self.Temps_sorb.emit(itc1Temp_sorb)
        time.sleep(0.2)
        itc1Temp_He3Low = str(itc1.Temp_2())
        self.Temps_He3Low.emit(itc1Temp_He3Low)
        time.sleep(0.2)
        itc1Temp_He3High = str(itc1.Temp_3())
        self.Temps_He3High.emit(itc1Temp_He3High)
        time.sleep(0.2)
        output_power_ITC_1 = itc1.r5()
        self.Power_ITC_1.emit(output_power_ITC_1[2:])
        time.sleep(0.2)
        itc2Temp_HeatSW = str(itc2.Temp_4())
        self.Temps_HeatSW.emit(itc2Temp_HeatSW)
        time.sleep(0.2)
        itc2Temp_PT2 = str(itc2.Temp_5())
        self.Temps_PT2.emit(itc2Temp_PT2)
        time.sleep(0.2)
        output_power_ITC_2 = itc2.r5()
        self.Power_ITC_2.emit(output_power_ITC_2[2:])
        time.sleep(0.2)

class fridge_control:
    import time
    import Logging
    reload(Logging)
    import Logging as log

    def sorb_Temp(itc1):
        S1_temp = itc1.r1()
        SorbTemp = float(S1_temp[1:])
        return SorbTemp

    def Heat_Sorb_off(itc1):
        itc1.clear()
        itc1.C3()
        time.sleep(0.1)
        itc1.A0()
        time.sleep(0.1)
        itc1.O(0)  # output 0
        time.sleep(0.1)

        msg = ' - Heat Sorb Off' + '\n'
        log.Save_log(msg)

    def Heat_Sorb_on(itc1):
        itc2.clear()
        itc1.C3()
        itc1.A0()
        itc1.O(07)
        msg = ' - Heat Sorb On, Wait several hours' + '\n'
        log.Save_log(msg)

    def Heat_SW_On(itc2):
        itc2.clear()
        itc2.C3()
        itc2.A0()
        itc2.O(99)  # Set 99% of Max power, 100% doesn't work
        time.sleep(0.1)
        msg = ' - Heat SW On' + '\n'
        log.Save_log(msg)

    def Heat_SW_off(itc2):
        itc2.clear()
        itc2.C3()
        itc2.A0()
        itc2.O(0)
        msg = ' - heat SW OFF, Wait until heat SW is cold' + '\n'
        log.Save_log(msg)

    def V1_Open(valve):
        valve.OPEN_V1()
        msg = ' - V1 Opened, Wait 1 hour' + '\n'
        log.Save_log(msg)

    def V1_Close(valve):
        valve.CLOSE_V1()
        time.sleep(0.5)
        timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
        msg = timestr + '-V1 Closed' + '\n'
        log.Save_log(msg)

    def Goto_Temp(itc1, Set_Temp):

        def itc1_He3_Low_Temp():
            S2temp = itc1.r2()
            He3LowTemp = float(S2temp[1:])
            return He3LowTemp

        '''
        def itc2_SW_Temp():
            time.sleep(0.5)
            temp_SW=itc2.r1()
            SW_Temp=float(temp_SW[1:])
            return SW_Temp
        '''

        def currentTempDeviation():
            ReadTemperror = itc1.r4()
            Deviation = abs(float(ReadTemperror[1:]))
            return Deviation

        itc1.TargetTemp(2, Set_Temp)
        msg = ' - Go to ' + str(Set_Temp) + ' K' + '\n'
        log.Save_log(msg)
        time.sleep(0.5)

        # Parameters
        MaxdeviationtoTconsigne = 0.002
        waitTime = 15  # sec
        Nbrep = 10
        j = 0
        while j < Nbrep:
            time.sleep(waitTime)
            Deviation = currentTempDeviation()
            time.sleep(0.1)
            if Deviation > MaxdeviationtoTconsigne:
                j = 0
            else:
                j += 1

        y = itc1_He3_Low_Temp()
        time.sleep(0.5)
        msg = ' - Now, He3 Low Temperature is ' + str(y) + ' K' + '\n'
        log.Save_log(msg)

    def itc1_sorb_Temp(itc1):
        S1_temp = itc1.r1()
        time.sleep(0.1)
        SorbTemp = float(S1_temp[1:])
        return SorbTemp

    def itc1_He3_Low_Temp(itc1):
        S2_temp = itc1.r2()
        time.sleep(0.1)
        He3LowTemp = float(S2_temp[1:])
        return He3LowTemp

    def itc1_He3_High_Temp(itc1):
        S3_temp = itc1.r3()
        time.sleep(0.1)
        He3HighTemp = float(S3_temp[1:])
        return He3HighTemp

    def itc2_SW_Temp(itc1):
        temp_SW = itc2.r1()
        time.sleep(0.1)
        SW_Temp = float(temp_SW[1:])
        return SW_Temp

    def itc2_Pt2_Temp(itc1):
        temp_Pt2 = itc2.r2()
        time.sleep(0.1)
        Pt2_Temp = float(temp_Pt2[1:])
        return Pt2_Temp

    def currentTempDeviation(itc1):
        ReadTemperror = itc1.r4()
        time.sleep(0.1)
        Deviation = abs(float(ReadTemperror[1:]))
        return Deviation

    def recondensation(self, Start_Temp, collecting_time, condensation_hour, Set_Temp, itc1, itc2, valve,
                       log_path='D:\Dropbox\MANIP\He3_log.txt', step=0):

        itc1.clear()
        time.sleep(0.1)
        itc2.clear()
        time.sleep(0.1)
        y = itc1_He3_Low_Temp()
        time.sleep(0.1)

        if y > Start_Temp:
            time.sleep(1.1)

        if itc1_He3_Low_Temp() > Start_Temp:
            time.sleep(1.1)

        if itc1_He3_Low_Temp() > Start_Temp:
            time.sleep(1.1)

        if itc1_He3_Low_Temp() > Start_Temp:
            y = itc1_He3_Low_Temp()
            sorb_T = itc1_sorb_Temp()
            He3_high = itc1_He3_High_Temp()
            z = itc2_SW_Temp()
            Pt2 = itc2_Pt2_Temp()
            msg = ' - He3 Temp: ' + str(y) + ' K, Start Recondensing He3' + '-Sorb : ' + str(
                sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                Pt2) + ' K' + '\n'
            log.Save_log(msg)

            ### Heat Sorb OFF  : Step 0 ###
            if step == 0:
                itc1.C3()
                time.sleep(0.1)
                itc1.A0()
                time.sleep(0.1)
                itc1.O(0)  # output 0
                time.sleep(0.1)
                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()
                msg = ' - Step ' + str(step) + ' - Heat Sorb Off - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)
                step += 1

                ### heat SW ON : Step 1  ###
            if step == 1:
                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                itc2.C3()
                time.sleep(0.1)
                itc2.A0()
                time.sleep(0.1)
                itc2.O(99)  # Set 99% of Max power, 100% doesn't work
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()
                msg = ' - Step ' + str(step) + ' - Heat SW On - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)
                step += 1

                ### V1 Open Wait 2 hour : Step 2  ###
            if step == 2:
                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()

                msg = ' - Step ' + str(step) + ' - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)

                valve.OPEN_V1()

                msg = ' - Step ' + str(step) + ' - V1 Opened, Wait ' + str(collecting_time) + ' hour' + '\n'
                log.Save_log(msg)
                time.sleep(collecting_time * 3600)
                step += 1
                ###  V1 Close : Step 3 ###
            if step == 3:
                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()

                msg = ' - Step ' + str(step) + ' - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)

                valve.CLOSE_V1()

                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()

                msg = ' - Step ' + str(step) + ' - V1 Closed - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)
                step += 1

                ### Heat SW OFF : Step 4 ###
            if step == 4:
                itc2.clear()
                time.sleep(0.1)
                itc2.C3()
                time.sleep(0.1)
                itc2.A0()
                time.sleep(0.1)
                itc2.O(0)
                time.sleep(0.1)
                msg = ' - Step ' + str(step) + ' - heat SW OFF, Wait until heat SW is cold' + '\n'
                log.Save_log(msg)
                ###  Waiting... ###
                j = 0
                while j < 1:
                    z = itc2_SW_Temp()
                    if z < 6:
                        j = 2
                    else:
                        j = 0
                    time.sleep(5)

                msg = ' - Step ' + str(step) + ' - Now SW is cold, Wait 5 min' + '\n'
                log.Save_log(msg)
                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(300)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()

                msg = ' - Step ' + str(step) + ' - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)
                step += 1


                ###  Heat Sorb ON : Step 5 ###
            if step == 5:
                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()

                msg = ' - Step ' + str(step) + ' - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)

                itc1.C3()
                time.sleep(0.1)
                itc1.A0()
                time.sleep(0.1)
                itc1.O(07)
                time.sleep(0.1)
                msg = ' - Step ' + str(step) + ' - Heat Sorb On, Wait ' + str(condensation_hour) + ' hour' + '\n'
                log.Save_log(msg)
                ###  Wait hour  ###
                time.sleep(condensation_hour * 3600)
                ###  Measure He3 Low Temp  ###
                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()
                msg = ' - Step ' + str(step) + ' - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)
                step += 1

                ### Heat Sorb OFF : Step 6  ###
            if step == 6:
                itc1.C3()
                time.sleep(0.1)
                itc1.A0()
                time.sleep(0.1)
                itc1.O(0)
                time.sleep(0.1)
                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()
                msg = ' - Step ' + str(step) + ' - Heat Sorb Off - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)
                step += 1

                ###  Open V1, Wait 1 min : Step 7  ###
            if step == 7:
                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()
                msg = ' - Step ' + str(step) + ' - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)

                valve.OPEN_V1()

                msg = ' - Step ' + str(step) + ' - V1 Opened, Wait 1 min' + '\n'
                log.Save_log(msg)
                time.sleep(55)
                step += 1

                ###  Close V1, heat SW ON : Step 8 ###
            if step == 8:
                valve.CLOSE_V1()
                itc2.C3()
                time.sleep(0.1)
                itc2.A0()
                time.sleep(0.1)
                itc2.O(99)  # Set 100% power is not working. 99% works
                time.sleep(0.1)
                msg = ' - Step ' + str(
                    step) + ' - V1 Closed, heater Switch On, Wait until He3 Low temperature is below 350 mK' + '\n'
                log.Save_log(msg)

                itc1.clear()
                time.sleep(0.1)
                itc2.clear()
                time.sleep(0.1)
                sorb_T = itc1_sorb_Temp()
                y = itc1_He3_Low_Temp()
                He3_high = itc1_He3_High_Temp()
                z = itc2_SW_Temp()
                Pt2 = itc2_Pt2_Temp()
                msg = ' - Step ' + str(step) + ' - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                    sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                    Pt2) + ' K' + '\n'
                log.Save_log(msg)
                step += 1
                ###  Waiting...  Until He3 Low_Temp below 350mK : Step 9 ###

            if step == 9:
                if Set_Temp < 0.35:
                    while itc1_He3_Low_Temp() > Set_Temp:
                        itc1.clear()
                        time.sleep(0.1)
                        itc2.clear()
                        time.sleep(0.1)
                        sorb_T = itc1_sorb_Temp()
                        y = itc1_He3_Low_Temp()
                        He3_high = itc1_He3_High_Temp()
                        z = itc2_SW_Temp()
                        Pt2 = itc2_Pt2_Temp()
                        msg = ' - Step ' + str(step) + ' - He3 Temp: ' + str(y) + ' K, Sorb : ' + str(
                            sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(z) + ' K, Pt2: ' + str(
                            Pt2) + ' K' + '\n'
                        log.Save_log(msg)
                        time.sleep(120)

                    itc1.clear()
                    time.sleep(0.1)
                    itc2.clear()
                    time.sleep(0.1)
                    sorb_T = itc1_sorb_Temp()
                    y = itc1_He3_Low_Temp()
                    He3_high = itc1_He3_High_Temp()
                    z = itc2_SW_Temp()
                    Pt2 = itc2_Pt2_Temp()
                    msg = ' - Step ' + str(step) + ' - He3 recondensation finish - He3 Temp: ' + str(
                        y) + ' K, Sorb : ' + str(sorb_T) + ' K, He3 High : ' + str(He3_high) + ' K, Heat SW: ' + str(
                        z) + ' K, Pt2: ' + str(Pt2) + ' K' + '\n'
                    log.Save_log(msg)

                elif Set_Temp > 0.35:
                    itc1.TargetTemp(2, Set_Temp)
                    msg = ' - Step ' + str(step) + ' - Go to ' + str(Set_Temp) + ' K' + '\n'
                    log.Save_log(msg)
                    time.sleep(0.5)

                    # Parameters
                    MaxdeviationtoTconsigne = 0.002
                    waitTime = 15  # sec
                    Nbrep = 10
                    j = 0
                    while j < Nbrep:
                        time.sleep(waitTime)
                        Deviation = currentTempDeviation()
                        time.sleep(0.1)
                        if Deviation > MaxdeviationtoTconsigne:
                            j = 0
                        else:
                            j += 1

                    y = itc1_He3_Low_Temp()
                    time.sleep(0.5)
                    msg = ' - Step ' + str(step) + ' -He3 recondensation finish. Now, He3 Low Temperature is ' + str(
                        y) + ' K' + '\n'
                    log.Save_log(msg)

class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):

        QtGui.QWidget.__init__(self,parent)
        super(QMainWindow, self).__init__()
        # super(Ui_MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.Equip_Setup_list = []

        self.subfig_list = []
        self.valve_status = 0
        self.ScanofDimension = 0
        self.measure_axis=np.zeros([4, 1])
        #self.measure_axis[:] = np.NAN
        self.subfig_list=np.zeros([3, 3])
        self.parameter_list_for_figure = [' ', 'SiA', 'SiB', 'SiCross', 'X_lockin', 'Rsample', 'Temp_He3', 'Gsample',
                                          'Auto A', 'Auto B', 'CrossAB', 'ImAB', 'Theory_Cross', 'Difference',
                                          'Gain_Cross', 'Gain_A', 'Gain_B']
        self.MeasureTemp_1 = Temp_itc_1(self)
        self.MeasureTemp_1.Temps_sorb.connect(self.Temps_display_lcd_1)
        self.MeasureTemp_1.Temps_He3Low.connect(self.Temps_display_lcd_2)
        self.MeasureTemp_1.Temps_He3High.connect(self.Temps_display_lcd_3)
        self.MeasureTemp_1.Power_ITC_1.connect(self.ITC_1_power_gauge)
        self.MeasureTemp_1.Temps_HeatSW.connect(self.Temps_display_lcd_4)
        self.MeasureTemp_1.Power_ITC_2.connect(self.ITC_2_power_gauge)
        self.MeasureTemp_1.Temps_PT2.connect(self.Temps_display_lcd_5)
        self.ui.checkBox_Vsd.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_1.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_2.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_3.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_4.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_5.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_6.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_7.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_8.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_9.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_10.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_11.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Vg_12.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_ITC_1.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_ITC_2.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_lockin_7265.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_awg_33210.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_adlink9826.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_mmr3_1.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_mmr3_2.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_Magnet.stateChanged.connect(self.checkBoxState_Equip_Setup)
        self.ui.checkBox_subfig_1.stateChanged.connect(self.checkBoxState_subfig)
        self.ui.checkBox_subfig_2.stateChanged.connect(self.checkBoxState_subfig)
        self.ui.checkBox_subfig_3.stateChanged.connect(self.checkBoxState_subfig)
        self.ui.checkBox_subfig_4.stateChanged.connect(self.checkBoxState_subfig)
        self.ui.checkBox_subfig_5.stateChanged.connect(self.checkBoxState_subfig)
        self.ui.checkBox_subfig_6.stateChanged.connect(self.checkBoxState_subfig)
        self.ui.checkBox_subfig_7.stateChanged.connect(self.checkBoxState_subfig)
        self.ui.checkBox_subfig_8.stateChanged.connect(self.checkBoxState_subfig)
        self.ui.checkBox_subfig_9.stateChanged.connect(self.checkBoxState_subfig)
        self.ui.checkBox_subfig_9.stateChanged.connect(self.checkBoxState_subfig)

        #self.connect(self.ui.pushButton_quit, SIGNAL("clicked()"), self.quit_btn_clicked)
        #self.connect(self.ui.pushButton_run, SIGNAL("clicked()"), self.run_btn_clicked)
        QtCore.QObject.connect(self.ui.pushButton_run, QtCore.SIGNAL(_fromUtf8("clicked()")), self.run_btn_clicked)
        #self.connect(self.ui.pushButton_pause, SIGNAL("clicked()"), self.terminate_thread())
        self.connect(self.ui.pushButton_stop, SIGNAL("clicked()"), self.stop_btn_clicked)
        QtCore.QObject.connect(self.ui.pushButton_Recon_On_ITC, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Auto_Recon_btn_clicked)
        #self.connect(self.ui.pushButton_Recon_On_ITC, SIGNAL("clicked()"), self.Auto_Recon_btn_clicked)
        self.connect(self.ui.pushButton_Valve_open_ITC, SIGNAL("clicked()"), self.V1open_btn_clicked)
        self.connect(self.ui.pushButton_Valve_Close_ITC, SIGNAL("clicked()"), self.V1close_btn_clicked)
        self.connect(self.ui.actionQuit, SIGNAL("triggered()"), self.Close_application)

        #self.connect(self.pushButton_Temp_REC_on, SIGNAL("clicked()"), self.REC_on_btn_clicked)
        #self.connect(self.pushButton_Temp_REC_off, SIGNAL("clicked()"), self.REC_off_btn_clicked)
        #self.connect(self.Recondense_checkBox, SIGNAL("clicked()"), self.checkBoxState)
        #self.connect(self.Recondense_checkBox_2, SIGNAL("clicked()"), self.checkBoxState)
        #self.connect(self.Recondense_checkBox_3, SIGNAL("clicked()"), self.checkBoxState)
        #self.connect(self.dial_refresh_rate_1, SIGNAL("valueChanged(int)"), self.checkDialState_1)
        #self.connect(self.dial_refresh_rate_2, SIGNAL("valueChanged(int)"), self.checkDialState_2)
        #self.connect(self.dial_refresh_rate_3, SIGNAL("valueChanged(int)"), self.checkDialState_3)
        #self.connect(self.dial_refresh_rate_4, SIGNAL("valueChanged(int)"), self.checkDialState_4)
        #self.connect(self.dial_refresh_rate_5, SIGNAL("valueChanged(int)"), self.checkDialState_5)
        #self.connect(self.dial_power_heatSW, SIGNAL("valueChanged(int)"), self.check_power_DialState_heatSW)
        #self.connect(self.dial_power_sorb, SIGNAL("valueChanged(int)"), self.check_power_DialState_sorb)
        #self.connect(self.actionNew,SIGNAL("clicked()"), self.V1open_btn_clicked)

        timer_2 = QtCore.QTimer(self)
        timer_2.timeout.connect(self.run_tempearature_background)
        timer_2.start(3000)
        self.run_tempearature_background()
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.show()
        self.checkBoxState_Equip_Setup()
        self.checkBoxState_subfig()
        self.Initial_Valve_status_check()
        #self.check_measurement_axis
    ####
    def addmpl(self,fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
    ####

    def combobox_load(self, combo_handle, combo_data):
        combo_handle.clear()  # delete all items from comboBox
        combo_handle.addItems(combo_data)  # add the actual content of self.comboData
        combo_handle.update()

    def Temps_display_lcd_1(self, TempsMeasured):
        self.ui.lcdNumber_ITC_Sorb.display(TempsMeasured)
    def Temps_display_lcd_2(self, TempsMeasured):
        self.ui.lcdNumber_ITC_He3Low.display(TempsMeasured)
    def Temps_display_lcd_3(self,TempsMeasured):
        self.ui.lcdNumber_ITC_He3High.display(TempsMeasured)
    def Temps_display_lcd_4(self,TempsMeasured):
        self.ui.lcdNumber_ITC_HeatSW.display(TempsMeasured)
    def Temps_display_lcd_5(self,TempsMeasured):
        self.ui.lcdNumber_ITC_PT2.display(TempsMeasured)
    def ITC_1_power_gauge(self,TempsMeasured):
        self.ui.Gauge_sorb_power_ITC.setValue(float(TempsMeasured))
    def ITC_2_power_gauge(self,TempsMeasured):
        self.ui.Gauge_Heat_power_ITC.setValue(float(TempsMeasured))
    def run_tempearature_background(self):
        self.MeasureTemp_1.start()

    def checkBoxState_Equip_Setup(self):
        self.Equip_Setup_list=[' ']
        self.Equip_address_list = [' ']
        msg = ""
        if self.ui.checkBox_Vsd.isChecked() == True:
            self.Equip_Setup_list.append('Vsd')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vsd.value())
        if self.ui.checkBox_Vg_1.isChecked() == True:
            self.Equip_Setup_list.append('Vg_1')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_1.value())
        if self.ui.checkBox_Vg_2.isChecked() == True:
            self.Equip_Setup_list.append('Vg_2')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_2.value())
        if self.ui.checkBox_Vg_3.isChecked() == True:
            self.Equip_Setup_list.append('Vg_3')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_3.value())
        if self.ui.checkBox_Vg_4.isChecked() == True:
            self.Equip_Setup_list.append('Vg_4')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_4.value())
        if self.ui.checkBox_Vg_5.isChecked() == True:
            self.Equip_Setup_list.append('Vg_5')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_5.value())
        if self.ui.checkBox_Vg_6.isChecked() == True:
            self.Equip_Setup_list.append('Vg_6')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_6.value())
        if self.ui.checkBox_Vg_7.isChecked() == True:
            self.Equip_Setup_list.append('Vg_7')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_7.value())
        if self.ui.checkBox_Vg_8.isChecked() == True:
            self.Equip_Setup_list.append('Vg_8')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_8.value())
        if self.ui.checkBox_Vg_9.isChecked() == True:
            self.Equip_Setup_list.append('Vg_9')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_9.value())
        if self.ui.checkBox_Vg_10.isChecked() == True:
            self.Equip_Setup_list.append('Vg_10')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_10.value())
        if self.ui.checkBox_Vg_11.isChecked() == True:
            self.Equip_Setup_list.append('Vg_11')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_11.value())
        if self.ui.checkBox_Vg_12.isChecked() == True:
            self.Equip_Setup_list.append('Vg_12')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Vg_12.value())
        if self.ui.checkBox_ITC_1.isChecked() == True:
            self.Equip_Setup_list.append('Temp_ITC')
            self.Equip_address_list.append(self.ui.spinBox_GPIB_ITC_1.value())
        if self.ui.checkBox_ITC_2.isChecked() == True:
            pass
        if self.ui.checkBox_lockin_7265.isChecked() == True:
            pass
            #self.Equip_Setup_list.append("lockin_7265")
        if self.ui.checkBox_awg_33210.isChecked() == True:
            self.Equip_Setup_list.append("AWG33210")
            self.Equip_address_list.append(self.ui.spinBox_GPIB_awg_33210.value())
        if self.ui.checkBox_Magnet.isChecked() == True:
            self.Equip_Setup_list.append("Magnet")
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Magnet.value())
        if self.ui.checkBox_Toptica.isChecked() == True:
            self.Equip_Setup_list.append("Toptica")
            self.Equip_address_list.append(self.ui.spinBox_GPIB_Toptica.value())
        if self.ui.checkBox_adlink9826.isChecked() == True:
            # self.Equip_Setup_list.append("Adlink9826")
            pass
        if self.ui.checkBox_mmr3_1.isChecked() == True:
            self.Equip_Setup_list.append("Temp_mmr")
            self.Equip_address_list.append(str(self.ui.textEdit_mmr3_1_address.currentText()))
        if self.ui.checkBox_mmr3_2.isChecked() == True:
            pass
        self.statusBar.showMessage(msg)
        self.combobox_load(self.ui.comboBox_x_axis, self.Equip_Setup_list)
        self.combobox_load(self.ui.comboBox_y_axis, self.Equip_Setup_list)
        self.combobox_load(self.ui.comboBox_z_axis, self.Equip_Setup_list)
        self.combobox_load(self.ui.comboBox_r_axis, self.Equip_Setup_list)

    def checkBoxState_subfig(self):
        msg = ""
        if self.ui.checkBox_subfig_1.isChecked() == 0:
            self.subfig_list[0, 0] = 0
            self.combobox_load(self.ui.comboBox_subfig_1, self.parameter_list_for_figure)
        elif self.ui.checkBox_subfig_1.isChecked() == 1:
            self.subfig_list[0, 0] = 1
            self.combobox_load(self.ui.comboBox_subfig_1, self.parameter_list_for_figure)
            msg += "subfig_1 "

        if self.ui.checkBox_subfig_2.isChecked() == 0:
            self.subfig_list[0, 1] = 0
            self.combobox_load(self.ui.comboBox_subfig_2, self.parameter_list_for_figure)
        elif self.ui.checkBox_subfig_2.isChecked() == 1:
            self.subfig_list[0, 1] = 1
            self.combobox_load(self.ui.comboBox_subfig_2, self.parameter_list_for_figure)
            msg += "subfig_2 "

        if self.ui.checkBox_subfig_3.isChecked() == 0:
            self.subfig_list[0, 2] = 0
            self.combobox_load(self.ui.comboBox_subfig_3, self.parameter_list_for_figure)
        elif self.ui.checkBox_subfig_3.isChecked() == 1:
            self.subfig_list[0, 2] = 1
            self.combobox_load(self.ui.comboBox_subfig_3, self.parameter_list_for_figure)
            msg += "subfig_3 "

        if self.ui.checkBox_subfig_4.isChecked() == 0:
            self.subfig_list[1, 0] = 0
            self.combobox_load(self.ui.comboBox_subfig_4, self.parameter_list_for_figure)
        elif self.ui.checkBox_subfig_4.isChecked() == 1:
            self.subfig_list[1, 0] = 1
            self.combobox_load(self.ui.comboBox_subfig_4, self.parameter_list_for_figure)
            msg += "subfig_4 "

        if self.ui.checkBox_subfig_5.isChecked() == 0:
            self.subfig_list[1, 1] = 0
            self.combobox_load(self.ui.comboBox_subfig_5, self.parameter_list_for_figure)
        elif self.ui.checkBox_subfig_5.isChecked() == 1:
            self.subfig_list[1, 1] = 1
            self.combobox_load(self.ui.comboBox_subfig_5, self.parameter_list_for_figure)
            msg += "subfig_5 "

        if self.ui.checkBox_subfig_6.isChecked() == 0:
            self.subfig_list[1, 2] = 0
            self.combobox_load(self.ui.comboBox_subfig_6, self.parameter_list_for_figure)
        elif self.ui.checkBox_subfig_6.isChecked() == 1:
            self.subfig_list[1, 2] = 1
            self.combobox_load(self.ui.comboBox_subfig_6, self.parameter_list_for_figure)
            msg += "subfig_6 "

        if self.ui.checkBox_subfig_7.isChecked() == 0:
            self.subfig_list[2, 0] = 0
            self.combobox_load(self.ui.comboBox_subfig_7, self.parameter_list_for_figure)
        elif self.ui.checkBox_subfig_7.isChecked() == 1:
            self.subfig_list[2, 0] = 1
            self.combobox_load(self.ui.comboBox_subfig_7, self.parameter_list_for_figure)
            msg += "subfig_7 "

        if self.ui.checkBox_subfig_8.isChecked() == 0:
            self.subfig_list[2, 1] = 0
            self.combobox_load(self.ui.comboBox_subfig_8, self.parameter_list_for_figure)
        elif self.ui.checkBox_subfig_8.isChecked() == 1:
            self.subfig_list[2, 1] = 1
            self.combobox_load(self.ui.comboBox_subfig_8, self.parameter_list_for_figure)
            msg += "subfig_8 "

        if self.ui.checkBox_subfig_9.isChecked() == 0:
            self.subfig_list[2, 2] = 0
            self.combobox_load(self.ui.comboBox_subfig_9, self.parameter_list_for_figure)
        elif self.ui.checkBox_subfig_9.isChecked() == 1:
            self.subfig_list[2, 2] = 1
            self.combobox_load(self.ui.comboBox_subfig_9, self.parameter_list_for_figure)
            msg += "subfig_9 "

        self.define_figure_setup()
        self.statusBar.showMessage(msg)


    def run_btn_clicked(self):
        #ask_Run_or_Not = self.check_measurement_axis()
        if self.check_measurement_axis() == True:
            choice = QtGui.QMessageBox.question(self, 'Warning!',
                                            "Measurement start???",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if choice == QtGui.QMessageBox.Yes:
                print("Just Do It!!!!")
                t = threading.Thread(target=self.run_measurements)
                t.start()
            else:
                pass

    def run_measurements(self):
        a=1
        #if load_Instr_ != True:
        self.fig_map_color = ['jet','jet','jet','jet','jet','jet','jet','jet','jet','jet','jet','jet','jet','jet','jet','jet']
        lockin = lockin_signalrecovery_7265.Instr()
        lockin.initialize()
        adlink = adlink9826.Instr()
        adlink.initialize()
        awg = awg33250.Instr()
        awg.initialize()

        if self.measure_axis[0, 0] != 0:
            #print(self.measure_axis[0, 0])
            #print(self.Equip_Setup_list[int(self.measure_axis[0, 0])])
            Instr_gpib_name_xaxis = self.Equip_Setup_list[int(self.measure_axis[0, 0])]
            j_0 = map(operator.eq, Instr_gpib_name_xaxis, "Vsd").count(True)
            j_1 = map(operator.eq, Instr_gpib_name_xaxis, "Vg").count(True)
            j_2 = map(operator.eq, Instr_gpib_name_xaxis, "Temp_ITC").count(True)
            j_3 = map(operator.eq, Instr_gpib_name_xaxis, "AWG33210").count(True)
            j_4 = map(operator.eq, Instr_gpib_name_xaxis, "Magnet").count(True)
            j_5 = map(operator.eq, Instr_gpib_name_xaxis, "Toptica").count(True)
            j_6 = map(operator.eq, Instr_gpib_name_xaxis, "Temp_mmr").count(True)
            Instr_gpib_address_xaxis = self.Equip_address_list[int(self.measure_axis[0, 0])]


            if self.ui.radioButton_step.isChecked() == True:
                self.sweep_range_x_array = np.linspace(self.ui.doubleSpinBox_x_start.value(), self.ui.doubleSpinBox_x_stop.value(),((self.ui.doubleSpinBox_x_stop.value() - self.ui.doubleSpinBox_x_start.value()) / self.ui.doubleSpinBox_x_step.value()))
            elif self.ui.radioButton_datapoint.isChecked() == True:
                self.sweep_range_x_array = np.linspace(self.ui.doubleSpinBox_x_start.value(), self.ui.doubleSpinBox_x_stop.value(),self.ui.spinBox_x_datapoint.value())

            if  j_0 >= 3 or j_1 >= 2:
                self.Instr_xaxis = yokogawa.Instr('GPIB0::'+str(Instr_gpib_address_xaxis)+'::INSTR')
                self.Instr_xaxis.initialize()
            elif j_2 >=8:
                pass
            elif j_3 >= 8:
                self.Instr_xaxis = awg33250.Instr('GPIB0::'+str(Instr_gpib_address_xaxis)+'::INSTR')
                self.Instr_xaxis.initialize()
            elif j_4 >= 6:
                raise Exception("Unsupported Instrument")
            elif j_5 >= 7:
                raise Exception("Unsupported Instrument")
            elif j_6 >= 7:
                raise Exception("Unsupported Instrument")
        if self.measure_axis[1, 0] != 0:
            Instr_gpib_name_yaxis = self.Equip_Setup_list[int(self.measure_axis[1, 0])]
            j_0 = map(operator.eq, Instr_gpib_name_yaxis, "Vsd").count(True)
            j_1 = map(operator.eq, Instr_gpib_name_yaxis, "Vg").count(True)
            j_2 = map(operator.eq, Instr_gpib_name_yaxis, "Temp_ITC").count(True)
            j_3 = map(operator.eq, Instr_gpib_name_yaxis, "AWG33210").count(True)
            j_4 = map(operator.eq, Instr_gpib_name_yaxis, "Magnet").count(True)
            j_5 = map(operator.eq, Instr_gpib_name_yaxis, "Toptica").count(True)
            j_6 = map(operator.eq, Instr_gpib_name_yaxis, "Temp_mmr").count(True)
            Instr_gpib_address_yaxis = self.Equip_address_list[int(self.measure_axis[1, 0])]
            if self.ui.radioButton_step.isChecked() == True:
                self.sweep_range_y_array = np.linspace(self.ui.doubleSpinBox_y_start.value(), self.ui.doubleSpinBox_y_stop.value(),
                                                  ((self.ui.doubleSpinBox_y_stop.value() - self.ui.doubleSpinBox_y_start.value()) / self.ui.doubleSpinBox_y_step.value()))
            elif self.ui.radioButton_datapoint.isChecked() == True:
                self.sweep_range_y_array=np.linspace(self.ui.doubleSpinBox_y_start.value(), self.ui.doubleSpinBox_y_stop.value(),self.ui.spinBox_y_datapoint.value())

            if  j_0 >= 3 or j_1 >= 2:
                self.Instr_yaxis = yokogawa.Instr('GPIB0::'+str(Instr_gpib_address_yaxis)+'::INSTR')
                self.Instr_yaxis.initialize()
            elif j_2 >=8:
                pass
            elif j_3 >= 8:
                self.Instr_yaxis = awg33250.Instr('GPIB0::'+str(Instr_gpib_address_yaxis)+'::INSTR')
                self.Instr_yaxis.initialize()
            elif j_4 >= 6:
                raise Exception("Unsupported Instrument")
            elif j_5 >= 7:
                raise Exception("Unsupported Instrument")
            elif j_6 >= 7:
                raise Exception("Unsupported Instrument")
        if self.measure_axis[2, 0] != 0:
            Instr_gpib_name_zaxis = self.Equip_Setup_list[int(self.measure_axis[2, 0])]
            j_0 = map(operator.eq, Instr_gpib_name_zaxis, "Vsd").count(True)
            j_1 = map(operator.eq, Instr_gpib_name_zaxis, "Vg").count(True)
            j_2 = map(operator.eq, Instr_gpib_name_zaxis, "Temp_ITC").count(True)
            j_3 = map(operator.eq, Instr_gpib_name_zaxis, "AWG33210").count(True)
            j_4 = map(operator.eq, Instr_gpib_name_zaxis, "Magnet").count(True)
            j_5 = map(operator.eq, Instr_gpib_name_zaxis, "Toptica").count(True)
            j_6 = map(operator.eq, Instr_gpib_name_zaxis, "Temp_mmr").count(True)
            Instr_gpib_address_zaxis = self.Equip_address_list[int(self.measure_axis[2, 0])]
            if self.ui.radioButton_step.isChecked() == True:
                self.sweep_range_z_array = np.linspace(self.ui.doubleSpinBox_z_start.value(), self.ui.doubleSpinBox_z_stop.value(),
                                                  ((self.ui.doubleSpinBox_z_stop.value() - self.ui.doubleSpinBox_z_start.value()) / self.ui.doubleSpinBox_z_step.value()))
            elif self.ui.radioButton_datapoint.isChecked() == True:
                self.sweep_range_z_array=np.linspace(self.ui.doubleSpinBox_z_start.value(), self.ui.doubleSpinBox_z_stop.value(),self.ui.spinBox_z_datapoint.value())

            if  j_0 >= 3 or j_1 >= 2:
                self.Instr_zaxis = yokogawa.Instr('GPIB0::'+str(Instr_gpib_address_zaxis)+'::INSTR')
                self.nstr_zaxis.initialize()
            elif j_2 >=8:
                pass
            elif j_3 >= 8:
                self.Instr_zaxis = awg33250.Instr('GPIB0::'+str(Instr_gpib_address_zaxis)+'::INSTR')
                self.Instr_zaxis.initialize()
            elif j_4 >= 6:
                raise Exception("Unsupported Instrument")
            elif j_5 >= 7:
                raise Exception("Unsupported Instrument")
            elif j_6 >= 7:
                raise Exception("Unsupported Instrument")
        if self.measure_axis[3, 0] != 0:
            Instr_gpib_name_raxis = self.Equip_Setup_list[int(self.measure_axis[3, 0])]
            j_0 = map(operator.eq, Instr_gpib_name_raxis, "Vsd").count(True)
            j_1 = map(operator.eq, Instr_gpib_name_raxis, "Vg").count(True)
            j_2 = map(operator.eq, Instr_gpib_name_raxis, "Temp_ITC").count(True)
            j_3 = map(operator.eq, Instr_gpib_name_raxis, "AWG33210").count(True)
            j_4 = map(operator.eq, Instr_gpib_name_raxis, "Magnet").count(True)
            j_5 = map(operator.eq, Instr_gpib_name_raxis, "Toptica").count(True)
            j_6 = map(operator.eq, Instr_gpib_name_raxis, "Temp_mmr").count(True)
            Instr_gpib_address_raxis = self.Equip_address_list[int(self.measure_axis[3, 0])]
            if self.ui.radioButton_step.isChecked() == True:
                self.sweep_range_r_array = np.linspace(self.ui.doubleSpinBox_r_start.value(), self.ui.doubleSpinBox_r_stop.value(),
                                                  ((self.ui.doubleSpinBox_r_stop.value() - self.ui.doubleSpinBox_r_start.value()) / self.ui.doubleSpinBox_r_step.value()))
            elif self.ui.radioButton_datapoint.isChecked() == True:
                self.sweep_range_r_array=np.linspace(self.ui.doubleSpinBox_r_start.value(), self.ui.doubleSpinBox_r_stop.value(),self.ui.spinBox_r_datapoint.value())

            if  j_0 >= 3 or j_1 >= 2:
                self.Instr_raxis = yokogawa.Instr('GPIB0::'+str(Instr_gpib_address_raxis)+'::INSTR')
                self.Instr_raxis.initialize()
            elif j_2 >=8:
                pass
            elif j_3 >= 8:
                self.Instr_raxis = awg33250.Instr('GPIB0::'+str(Instr_gpib_address_raxis)+'::INSTR')
                self.Instr_raxis.initialize()
            elif j_4 >= 6:
                raise Exception("Unsupported Instrument")
            elif j_5 >= 7:
                raise Exception("Unsupported Instrument")
            elif j_6 >= 7:
                raise Exception("Unsupported Instrument")
        if self.ScanofDimension == 1:
            xsize = self.ui.spinBox_x_repeat.value()
            ysize = len(self.sweep_range_x_array)
            self.array_Vgate_plot = self.Make_NaN_array(ysize, xsize)
            self.array_Vsd_plot = self.Make_NaN_array(ysize, xsize)
            self.Vds_sample_plot = self.Make_NaN_array(ysize, xsize)
            self.SiA_plot = self.Make_NaN_array(ysize, xsize)
            self.SiB_plot = self.Make_NaN_array(ysize, xsize)
            self.Auto_A_plot = self.Make_NaN_array(ysize, xsize)
            self.Auto_B_plot = self.Make_NaN_array(ysize, xsize)
            self.SiCross_plot = self.Make_NaN_array(ysize, xsize)
            self.X_lockin_plot = self.Make_NaN_array(ysize, xsize)
            self.Rsample_plot = self.Make_NaN_array(ysize, xsize)
            self.Temp_He3_plot = self.Make_NaN_array(ysize, xsize)
            self.Gsample_plot = self.Make_NaN_array(ysize, xsize)
            self.CrossAB_plot = self.Make_NaN_array(ysize, xsize)
            self.ImAB_plot = self.Make_NaN_array(ysize, xsize)
            self.Theory_Cross_plot = self.Make_NaN_array(ysize, xsize)
            self.Difference_plot = self.Make_NaN_array(ysize, xsize)
            self.Gain_Cross_plot = self.Make_NaN_array(ysize, xsize)
            self.Gain_A_plot = self.Make_NaN_array(ysize, xsize)
            self.Gain_B_plot = self.Make_NaN_array(ysize, xsize)
            self.data_plot = [self.array_Vgate_plot, self.array_Vsd_plot, self.Vds_sample_plot, self.SiA_plot,
                              self.SiB_plot, self.Auto_A_plot, self.Auto_B_plot, self.SiCross_plot, self.X_lockin_plot,
                              self.Rsample_plot, self.Temp_He3_plot, self.Gsample_plot, self.CrossAB_plot,
                              self.ImAB_plot,
                              self.Theory_Cross_plot, self.Difference_plot, self.Gain_Cross_plot, self.Gain_A_plot,
                              self.Gain_B_plot]

        elif self.ScanofDimension == 2 or self.ScanofDimension == 3 or self.ScanofDimension == 4:
            xsize = len(self.sweep_range_x_array)
            ysize = len(self.sweep_range_y_array)
            self.array_Vgate_plot = self.Make_NaN_array(ysize, xsize)
            self.array_Vsd_plot = self.Make_NaN_array(ysize, xsize)
            self.Vds_sample_plot = self.Make_NaN_array(ysize, xsize)
            self.SiA_plot = self.Make_NaN_array(ysize, xsize)
            self.SiB_plot = self.Make_NaN_array(ysize, xsize)
            self.Auto_A_plot = self.Make_NaN_array(ysize, xsize)
            self.Auto_B_plot = self.Make_NaN_array(ysize, xsize)
            self.SiCross_plot = self.Make_NaN_array(ysize, xsize)
            self.X_lockin_plot = self.Make_NaN_array(ysize, xsize)
            self.Rsample_plot = self.Make_NaN_array(ysize, xsize)
            self.Temp_He3_plot = self.Make_NaN_array(ysize, xsize)
            self.Gsample_plot = self.Make_NaN_array(ysize, xsize)
            self.CrossAB_plot = self.Make_NaN_array(ysize, xsize)
            self.ImAB_plot = self.Make_NaN_array(ysize, xsize)
            self.Theory_Cross_plot = self.Make_NaN_array(ysize, xsize)
            self.Difference_plot = self.Make_NaN_array(ysize, xsize)
            self.Gain_Cross_plot = self.Make_NaN_array(ysize, xsize)
            self.Gain_A_plot = self.Make_NaN_array(ysize, xsize)
            self.Gain_B_plot = self.Make_NaN_array(ysize, xsize)

            self.array_Vgate_D2 = self.Make_zero_array(ysize, xsize)
            self.array_Vsd_D2 = self.Make_zero_array(ysize, xsize)
            self.Vds_sample_D2 = self.Make_zero_array(ysize, xsize)
            self.SiA_D2 = self.Make_zero_array(ysize, xsize)
            self.SiB_D2 = self.Make_zero_array(ysize, xsize)
            self.Auto_A_D2 = self.Make_zero_array(ysize, xsize)
            self.Auto_B_D2 = self.Make_zero_array(ysize, xsize)
            self.SiCross_D2 = self.Make_zero_array(ysize, xsize)
            self.X_lockin_D2 = self.Make_zero_array(ysize, xsize)
            self.Rsample_D2 = self.Make_zero_array(ysize, xsize)
            self.Temp_He3_D2 = self.Make_zero_array(ysize, xsize)
            self.Gsample_D2 = self.Make_zero_array(ysize, xsize)
            self.CrossAB_D2 = self.Make_zero_array(ysize, xsize)
            self.ImAB_D2 = self.Make_zero_array(ysize, xsize)
            self.Theory_Cross_D2 = self.Make_zero_array(ysize, xsize)
            self.Difference_D2 = self.Make_zero_array(ysize, xsize)
            self.Gain_Cross_D2 = self.Make_zero_array(ysize, xsize)
            self.Gain_A_D2 = self.Make_zero_array(ysize, xsize)
            self.Gain_B_D2 = self.Make_zero_array(ysize, xsize)
            self.data_plot = [self.array_Vgate_plot, self.array_Vsd_plot, self.Vds_sample_plot, self.SiA_plot,
                              self.SiB_plot, self.Auto_A_plot, self.Auto_B_plot, self.SiCross_plot, self.X_lockin_plot,
                              self.Rsample_plot, self.Temp_He3_plot, self.Gsample_plot, self.CrossAB_plot,
                              self.ImAB_plot,
                              self.Theory_Cross_plot, self.Difference_plot, self.Gain_Cross_plot, self.Gain_A_plot,
                              self.Gain_B_plot]
            self.data_D2 = [self.array_Vgate_D2, self.array_Vsd_D2, self.Vds_sample_D2, self.SiA_D2, self.SiB_D2,
                            self.Auto_A_D2, self.Auto_B_D2, self.SiCross_D2, self.X_lockin_D2, self.Rsample_D2,
                            self.Temp_He3_D2, self.Gsample_D2, self.CrossAB_D2, self.ImAB_D2, self.Theory_Cross_D2,
                            self.Difference_D2, self.Gain_Cross_D2, self.Gain_A_D2, self.Gain_B_D2]
            '''
            array_Vgate_D2 = np.zeros([len(sweep_range_y_array), len(sweep_range_x_array)])
            array_Vsd_D2 = np.zeros([len(sweep_range_y_array), len(sweep_range_x_array)])
            Vds_sample_D2 = np.zeros([len(sweep_range_y_array), len(sweep_range_x_array)])
            SiA_D2 = np.zeros([len(sweep_range_y_array), len(sweep_range_x_array)])
            SiB_D2 = np.zeros([len(sweep_range_y_array), len(sweep_range_x_array)])
            SiCross_D2 = np.zeros([len(sweep_range_y_array), len(sweep_range_x_array)])
            X_lockin_D2 = np.zeros([len(sweep_range_y_array), len(sweep_range_x_array)])
            Rsample_D2 = np.zeros([len(sweep_range_y_array), len(sweep_range_x_array)])
            Temp_He3_D2 = np.zeros([len(sweep_range_y_array), len(sweep_range_x_array)])
            Gsample = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            auto_A = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            auto_B = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            CrossAB = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            ImAB = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            Theory_Cross = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            Difference = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            Gain_Cross = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            Gain_A = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            Gain_B = np.zeros([self.ui.spinBox_x_repeat.value(), len(sweep_range_x_array)])
            'Vgate', 'Vsd', 'Vds_sample', 'SiA', 'SiB', 'SiCross', 'X_lockin', 'Rsample', 'Temp_He3', 'Gsample', 'Auto A', 'Auto B', 'CrossAB', 'ImAB', 'Theory_Cross', 'Difference', 'Gain_Cross', 'Gain_A', 'Gain_B'
            '''


        #try:
        #    self.data_plot = [self.array_Vgate_plot, self.array_Vsd_plot,self.Vds_sample_plot, self.SiA_plot,self.SiB_plot,self.Auto_A_plot,self.Auto_B_plot,self.SiCross_plot,self.X_lockin_plot, self.Rsample_plot,self.Temp_He3_plot, self.Gsample_plot, self.CrossAB_plot, self.ImAB_plot, self.Theory_Cross_plot, self.Difference_plot, self.Gain_Cross_plot, self.Gain_A_plot, self.Gain_B_plot]
        #    self.data_D2 = [self.array_Vgate_D2, self.array_Vsd_D2,self.Vds_sample_D2, self.SiA_D2,self.SiB_D2,self.Auto_A_D2,self.Auto_B_D2,self.SiCross_D2,self.X_lockin_D2, self.Rsample_D2,self.Temp_He3_D2, self.Gsample_D2, self.CrossAB_D2, self.ImAB_D2, self.Theory_Cross_D2, self.Difference_D2, self.Gain_Cross_D2, self.Gain_A_D2, self.Gain_B_D2]
        #except:
        #    pass
        #V3.yoko_rewind(set_Yoko3, time_wait=2)
        #print(self.data_plot)
        count_l=0
        if self.ScanofDimension == 4:
            for r in self.sweep_range_r_array:
                count_k=0
                self.Instr_raxis.rewind(r)
                time.sleep(self.ui.doubleSpinBox_r_wait_time.value())
                for z in self.sweep_range_z_array:
                    count_j=0
                    self.Instr_zaxis.rewind(z)
                    time.sleep(self.ui.dobuleSpinBox_z_wait_time.value())
                    for y in self.sweep_range_y_array:
                        count_i=0
                        self.Instr_yaxis.rewind(y)
                        time.sleep(self.ui.doubleSpinBox_y_wait_time.value())
                        for x in self.sweep_range_x_array:
                            if self.ui.Lamp_Recon_On_ITC.value() == True:
                                pass
                            else:
                                pass
                            time.sleep(self.ui.doubleSpinBox_x_wait_time.value())
                            #Value_lockin_10hz = ca.lockin_x(lockin)
                            #xlockin_2Darray_10hz[j, i] = Value_lockin_10hz
                            #xlockin_2Darray_10hz_plot[j, i] = Value_lockin_10hz
                            if self.ui.checkBox_Measure_lockin.isChecked() == True:
                                self.X_lockin_plot[count_j, count_i] = ca.lockin_x(lockin)
                            if self.ui.checkBox_Measure_Noise.isChecked() == True:
                                arr = np.zeros(4, dtype=float)
                                timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
                                adlink.acqire_n_FFT(name='FullSpectrum_' + timestr[:-2], average=self.ui.doubleSpinBox_ADLINK_avgnum.value(), start=self.ui.doubleSpinBox_ADLINK_start.value(),
                                                stop=self.ui.doubleSpinBox_ADLINK_stop.value(), arr=arr, save=self.ui.checkBox_ADLINK_save.checkState())

                            if count_i < len(self.sweep_range_x_array) - 1:
                                self.Instr_xaxis.rewind(self.sweep_range_x_array[count_i + 1], time_wait=1)
                                #V2.yoko_rewind(self.sweep_range_x_array[i + 1], time_wait=1)
                            else:
                                pass

                            self.array_Vgate_plot[count_j, count_i]= x
                            if self.ui.checkBox_Measure_lockin.isChecked() == True:
                                self.Rsample_plot[count_j, count_i] = ca.Rs(self.X_lockin_plot[count_j, count_i])
                                self.Gsample_plot[count_j, count_i] = ca.Gs(self.X_lockin_plot[count_j, count_i])


                            self.Temp_He3_plot [count_j, count_i] = self.MeasureTemp_1.Temps_He3Low()

                            if self.ScanofDimension == 2 or self.ScanofDimension == 3 or self.ScanofDimension == 4:
                                self.array_Vsd_plot[count_j, count_i] = y
                                if self.ui.checkBox_Measure_lockin.isChecked() == True:
                                    self.Vds_sample_plot[count_j, count_i] = ca.Vds(self.Rsample_plot[count_j, count_i], y)
                            if self.ui.checkBox_Measure_Noise.isChecked() == True:
                                self.Auto_A_plot[count_j, count_i] = (arr[0])
                                self.Auto_B_plot[count_j, count_i] = (arr[1])
                                self.CrossAB_plot[count_j, count_i] = (arr[2])
                                self.ImAB_plot[count_j, count_i] = (arr[3])
                                if self.ui.checkBox_Measure_lockin.isChecked() == True:
                                    self.Theory_Cross_plot[count_j, count_i] = ca.theory(self.Rsample_plot[count_j, count_i], self.array_Vsd_plot[count_j, count_i], self.Temp_He3_plot [count_j, count_i])
                                    self.Gain_Cross_plot[count_j, count_i] = ca.gain(self.Rsample_plot[count_j, count_i], Cross=1)
                                    self.Gain_A_plot[count_j, count_i] = ca.gain(self.Rsample_plot[count_j, count_i], AutoA=1)
                                    self.Gain_B_plot[count_j, count_i] = ca.gain(self.Rsample_plot[count_j, count_i], AutoB=1)
                                    self.SiCross_plot[count_j, count_i] = abs(arr[2]) / self.Gain_Cross_plot[count_j, count_i]
                                    self.SiA_plot[count_j, count_i] = (arr[0]) / self.Gain_A_plot[count_j, count_i]
                                    self.SiB_plot[count_j, count_i] = (arr[0]) / self.Gain_B_plot[count_j, count_i]
                                    self.Difference_plot[count_j, count_i] = (abs(arr[2]) / self.Gain_Cross_plot[count_j, count_i]) - (self.Theory_Cross_plot[count_j, count_i])
                            count_i +=1
                        count_j += 1
                    count_k += 1
                count_l += 1
        elif self.ScanofDimension == 3:
            count_k = 0
            for z in self.sweep_range_z_array:
                count_j = 0
                self.Instr_zaxis.rewind(z)
                time.sleep(self.ui.doubleSpinBox_z_wait_time.value())
                for y in self.sweep_range_y_array:
                    count_i = 0
                    self.Instr_yaxis.rewind(y)
                    time.sleep(self.ui.doubleSpinBox_y_wait_time.value())

                    for x in self.sweep_range_x_array:
                        if self.ui.Lamp_Recon_On_ITC.value() == True:
                            pass
                        else:
                            pass
                        time.sleep(self.ui.doubleSpinBox_x_wait_time.value())
                        # Value_lockin_10hz = ca.lockin_x(lockin)
                        # xlockin_2Darray_10hz[j, i] = Value_lockin_10hz
                        # xlockin_2Darray_10hz_plot[j, i] = Value_lockin_10hz
                        if self.ui.checkBox_Measure_lockin.isChecked() == True:
                            self.X_lockin_plot[count_j, count_i] = ca.lockin_x(lockin)
                        if self.ui.checkBox_Measure_Noise.isChecked() == True:
                            arr = np.zeros(4, dtype=float)
                            timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
                            adlink.acqire_n_FFT(name='FullSpectrum_' + timestr[:-2],
                                                average=self.ui.doubleSpinBox_ADLINK_avgnum.value(),
                                                start=self.ui.doubleSpinBox_ADLINK_start.value(),
                                                stop=self.ui.doubleSpinBox_ADLINK_stop.value(),
                                                arr=arr,
                                                save=self.ui.checkBox_ADLINK_save.checkState())

                        if count_i < len(self.sweep_range_x_array) - 1:
                            self.Instr_xaxis.rewind(self.sweep_range_x_array[count_i + 1],
                                                    time_wait=1)
                            # V2.yoko_rewind(self.sweep_range_x_array[i + 1], time_wait=1)
                        else:
                            pass

                        self.array_Vgate_plot[count_j, count_i] = x
                        if self.ui.checkBox_Measure_lockin.isChecked() == True:
                            self.Rsample_plot[count_j, count_i] = ca.Rs(self.X_lockin_plot[count_j, count_i])
                            self.Gsample_plot[count_j, count_i] = ca.Gs(self.X_lockin_plot[count_j, count_i])

                        self.Temp_He3_plot[count_j, count_i] = self.ui.lcdNumber_ITC_He3Low.value()

                        if self.ScanofDimension == 2 or self.ScanofDimension == 3 or self.ScanofDimension == 4:
                            self.array_Vsd_plot[count_j, count_i] = y
                            if self.ui.checkBox_Measure_lockin.isChecked() == True:
                                self.Vds_sample_plot[count_j, count_i] = ca.Vds(
                                    self.Rsample_plot[count_j, count_i], y)
                        if self.ui.checkBox_Measure_Noise.isChecked() == True:
                            self.Auto_A_plot[count_j, count_i] = (arr[0])
                            self.Auto_B_plot[count_j, count_i] = (arr[1])
                            self.CrossAB_plot[count_j, count_i] = (arr[2])
                            self.ImAB_plot[count_j, count_i] = (arr[3])
                            if self.ui.checkBox_Measure_lockin.isChecked() == True:
                                self.Theory_Cross_plot[count_j, count_i] = ca.theory(
                                    self.Rsample_plot[count_j, count_i],
                                    self.array_Vsd_plot[count_j, count_i],
                                    self.Temp_He3_plot[count_j, count_i])
                                self.Gain_Cross_plot[count_j, count_i] = ca.gain(
                                    self.Rsample_plot[count_j, count_i], Cross=1)
                                self.Gain_A_plot[count_j, count_i] = ca.gain(
                                    self.Rsample_plot[count_j, count_i], AutoA=1)
                                self.Gain_B_plot[count_j, count_i] = ca.gain(
                                    self.Rsample_plot[count_j, count_i], AutoB=1)
                                self.SiCross_plot[count_j, count_i] = abs(arr[2]) / \
                                                                      self.Gain_Cross_plot[
                                                                          count_j, count_i]
                                self.SiA_plot[count_j, count_i] = (arr[0]) / self.Gain_A_plot[
                                    count_j, count_i]
                                self.SiB_plot[count_j, count_i] = (arr[0]) / self.Gain_B_plot[
                                    count_j, count_i]
                                self.Difference_plot[count_j, count_i] = (abs(arr[2]) /
                                                                          self.Gain_Cross_plot[
                                                                              count_j, count_i]) - (
                                                                             self.Theory_Cross_plot[
                                                                                 count_j, count_i])
                        count_i+=1
                    count_j+=1
                count_k+=1
        elif self.ScanofDimension == 2:
            count_j = 0
            for y in self.sweep_range_y_array:
                count_i = 0
                time.sleep(self.ui.doubleSpinBox_y_wait_time.value())
                for x in self.sweep_range_x_array:
                    if self.ui.Lamp_Recon_On_ITC.value() == True:
                        pass
                    else:
                        pass
                    time.sleep(self.ui.doubleSpinBox_x_wait_time.value())
                    # Value_lockin_10hz = ca.lockin_x(lockin)
                    # xlockin_2Darray_10hz[j, i] = Value_lockin_10hz
                    # xlockin_2Darray_10hz_plot[j, i] = Value_lockin_10hz
                    if self.ui.checkBox_Measure_lockin.isChecked() == True:
                        self.X_lockin_plot[count_j, count_i] = ca.lockin_x(lockin)
                    if self.ui.checkBox_Measure_Noise.isChecked() == True:
                        arr = np.zeros(4, dtype=float)
                        timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
                        adlink.acqire_n_FFT(name='FullSpectrum_' + timestr[:-2],
                                            average=self.ui.doubleSpinBox_ADLINK_avgnum.value(),
                                            start=self.ui.doubleSpinBox_ADLINK_start.value(),
                                            stop=self.ui.doubleSpinBox_ADLINK_stop.value(),
                                            arr=arr,
                                            save=self.ui.checkBox_ADLINK_save.checkState())

                    if count_i < len(self.sweep_range_x_array) - 1:
                        self.Instr_xaxis.rewind(self.sweep_range_x_array[count_i + 1],
                                                time_wait=1)
                        # V2.yoko_rewind(self.sweep_range_x_array[i + 1], time_wait=1)
                    else:
                        pass

                    self.array_Vgate_plot[count_j, count_i] = x
                    if self.ui.checkBox_Measure_lockin.isChecked() == True:
                        self.Rsample_plot[count_j, count_i] = ca.Rs(self.X_lockin_plot[count_j, count_i])
                        self.Gsample_plot[count_j, count_i] = ca.Gs(self.X_lockin_plot[count_j, count_i])

                    self.Temp_He3_plot[count_j, count_i] = self.ui.lcdNumber_ITC_He3Low.value()

                    if self.ScanofDimension == 2 or self.ScanofDimension == 3 or self.ScanofDimension == 4:
                        self.array_Vsd_plot[count_j, count_i] = y
                        if self.ui.checkBox_Measure_lockin.isChecked() == True:
                            self.Vds_sample_plot[count_j, count_i] = ca.Vds(
                                self.Rsample_plot[count_j, count_i], y)
                    if self.ui.checkBox_Measure_Noise.isChecked() == True:
                        self.Auto_A_plot[count_j, count_i] = (arr[0])
                        self.Auto_B_plot[count_j, count_i] = (arr[1])
                        self.CrossAB_plot[count_j, count_i] = (arr[2])
                        self.ImAB_plot[count_j, count_i] = (arr[3])
                        if self.ui.checkBox_Measure_lockin.isChecked() == True:
                            self.Theory_Cross_plot[count_j, count_i] = ca.theory(
                                self.Rsample_plot[count_j, count_i],
                                self.array_Vsd_plot[count_j, count_i],
                                self.Temp_He3_plot[count_j, count_i])
                            self.Gain_Cross_plot[count_j, count_i] = ca.gain(
                                self.Rsample_plot[count_j, count_i], Cross=1)
                            self.Gain_A_plot[count_j, count_i] = ca.gain(
                                self.Rsample_plot[count_j, count_i], AutoA=1)
                            self.Gain_B_plot[count_j, count_i] = ca.gain(
                                self.Rsample_plot[count_j, count_i], AutoB=1)
                            self.SiCross_plot[count_j, count_i] = abs(arr[2]) / \
                                                                  self.Gain_Cross_plot[
                                                                      count_j, count_i]
                            self.SiA_plot[count_j, count_i] = (arr[0]) / self.Gain_A_plot[
                                count_j, count_i]
                            self.SiB_plot[count_j, count_i] = (arr[0]) / self.Gain_B_plot[
                                count_j, count_i]
                            self.Difference_plot[count_j, count_i] = (abs(arr[2]) /
                                                                      self.Gain_Cross_plot[
                                                                          count_j, count_i]) - (
                                                                         self.Theory_Cross_plot[
                                                                             count_j, count_i])
                    count_i+=1
                count_j += 1
        elif self.ScanofDimension == 1:
            count_j = 0
            for y in range(0, self.ui.spinBox_x_repeat.value(), 1):
                count_i = 0
                self.Instr_xaxis.rewind(self.sweep_range_x_array[0], time_wait=1)
                time.sleep(self.ui.doubleSpinBox_y_wait_time.value())


                for x in self.sweep_range_x_array:
                    if self.ui.Lamp_Recon_On_ITC.value() == True:
                        pass
                    else:
                        pass
                    time.sleep(self.ui.doubleSpinBox_x_wait_time.value())

                    if self.ui.checkBox_Measure_lockin.isChecked() == True:
                        self.X_lockin_plot[count_j, count_i] = ca.lockin_x(lockin)

                    if self.ui.checkBox_Measure_Noise.isChecked() == True:
                        arr = np.zeros(4, dtype=float)
                        timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
                        adlink.acqire_n_FFT(name='FullSpectrum_' + timestr[:-2],
                                            average=self.ui.doubleSpinBox_ADLINK_avgnum.value(),
                                            start=self.ui.doubleSpinBox_ADLINK_start.value(),
                                            stop=self.ui.doubleSpinBox_ADLINK_stop.value(),
                                            arr=arr,
                                            save=self.ui.checkBox_ADLINK_save.checkState())

                    if count_i < len(self.sweep_range_x_array) - 1:
                        self.Instr_xaxis.rewind(self.sweep_range_x_array[count_i + 1], time_wait=1)

                    else:
                        pass

                    self.array_Vgate_plot[count_j, count_i] = x
                    if self.ui.checkBox_Measure_lockin.isChecked() == True:
                        self.Rsample_plot[count_j, count_i] = ca.Rs(self.X_lockin_plot[count_j, count_i])
                        self.Gsample_plot[count_j, count_i] = ca.Gs(self.X_lockin_plot[count_j, count_i])

                    self.Temp_He3_plot[count_j, count_i] = self.ui.lcdNumber_ITC_He3Low.value()
                    #temp = str(self.MeasureTemp_1.Temps_sorb())
                    #print(self.Temp_He3)
                    if self.ScanofDimension == 2 or self.ScanofDimension == 3 or self.ScanofDimension == 4:
                        self.array_Vsd_plot[count_j, count_i] = y
                        if self.ui.checkBox_Measure_lockin.isChecked() == True:
                            self.Vds_sample_plot[count_j, count_i] = ca.Vds(
                                self.Rsample_plot[count_j, count_i], y)
                    if self.ui.checkBox_Measure_Noise.isChecked() == True:
                        self.Auto_A_plot[count_j, count_i] = (arr[0])
                        self.Auto_B_plot[count_j, count_i] = (arr[1])
                        self.CrossAB_plot[count_j, count_i] = (arr[2])
                        self.ImAB_plot[count_j, count_i] = (arr[3])
                        if self.ui.checkBox_Measure_lockin.isChecked() == True:
                            self.Theory_Cross_plot[count_j, count_i] = ca.theory(
                                self.Rsample_plot[count_j, count_i],
                                self.array_Vsd_plot[count_j, count_i],
                                self.Temp_He3_plot[count_j, count_i])
                            self.Gain_Cross_plot[count_j, count_i] = ca.gain(
                                self.Rsample_plot[count_j, count_i], Cross=1)
                            self.Gain_A_plot[count_j, count_i] = ca.gain(
                                self.Rsample_plot[count_j, count_i], AutoA=1)
                            self.Gain_B_plot[count_j, count_i] = ca.gain(
                                self.Rsample_plot[count_j, count_i], AutoB=1)
                            self.SiCross_plot[count_j, count_i] = abs(arr[2]) / \
                                                                  self.Gain_Cross_plot[
                                                                      count_j, count_i]
                            self.SiA_plot[count_j, count_i] = (arr[0]) / self.Gain_A_plot[
                                count_j, count_i]
                            self.SiB_plot[count_j, count_i] = (arr[0]) / self.Gain_B_plot[
                                count_j, count_i]
                            self.Difference_plot[count_j, count_i] = (abs(arr[2]) /
                                                                      self.Gain_Cross_plot[
                                                                          count_j, count_i]) - (
                                                                         self.Theory_Cross_plot[
                                                                             count_j, count_i])
                    #subplot_num = int(str(int(self.figure_array_size[0])) + str(int(self.figure_array_size[1])) + str(int(self.subfig_num[0, 1])))
                    #print(subplot_num)
                    #print(self.subfig_list)
                    #print(self.subfig_num)
                    self.make_figure()
                    count_i += 1
                count_j += 1

    def make_figure(self):
        if self.subfig_list[0, 0] != 0:
            if self.ui.checkBox_subfig_1_img_type.isChecked() == 0:
                self.D1_plot_figure(self.figure_array_size[0], self.figure_array_size[1], self.subfig_num[0, 0],
                                str(self.ui.comboBox_subfig_1.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                self.sweep_range_x_array, self.data_plot[self.ui.comboBox_subfig_1.currentIndex()+1][0])
            elif self.ScanofDimension > 1 and self.ui.checkBox_subfig_1_img_type.isChecked() == 1:
                self.D2_plot_figure(self.figure_array_size[0], self.figure_array_size[1],  self.subfig_num[0, 0],
                                    str(self.ui.comboBox_subfig_1.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                    str(self.ui.comboBox_y_axis.currentText()), self.sweep_range_x_array,
                                    self.sweep_range_y_array, self.data_plot[self.ui.comboBox_subfig_1.currentIndex()+1], self.fig_map_color[1])
        if self.subfig_list[0, 1] != 0:
            if self.ui.checkBox_subfig_2_img_type.isChecked() == 0:
                self.D1_plot_figure(self.figure_array_size[0], self.figure_array_size[1], self.subfig_num[0, 1],
                                str(self.ui.comboBox_subfig_2.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                self.sweep_range_x_array, self.data_plot[self.ui.comboBox_subfig_2.currentIndex()+1])
            elif self.ScanofDimension > 1 and self.ui.checkBox_subfig_2_img_type.isChecked() == 1:
                self.D2_plot_figure(self.figure_array_size[0], self.figure_array_size[1],  self.subfig_num[0, 1],
                                    str(self.ui.comboBox_subfig_2.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                    str(self.ui.comboBox_y_axis.currentText()), self.sweep_range_x_array,
                                    self.sweep_range_y_array, self.data_plot[self.ui.comboBox_subfig_2.currentIndex()+1], self.fig_map_color[2])
        if self.subfig_list[0, 2] != 0:
            if self.ui.checkBox_subfig_3_img_type.isChecked() == 0:
                self.D1_plot_figure(self.figure_array_size[0], self.figure_array_size[1], self.subfig_num[0, 2],
                                str(self.ui.comboBox_subfig_3.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                self.sweep_range_x_array, self.data_plot[self.ui.comboBox_subfig_3.currentIndex()+1])
            elif self.ScanofDimension > 1 and self.ui.checkBox_subfig_3_img_type.isChecked() == 1:
                self.D2_plot_figure(self.figure_array_size[0], self.figure_array_size[1],  self.subfig_num[0, 2],
                                    str(self.ui.comboBox_subfig_3.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                    str(self.ui.comboBox_y_axis.currentText()), self.sweep_range_x_array,
                                    self.sweep_range_y_array, self.data_plot[self.ui.comboBox_subfig_3.currentIndex()+1], self.fig_map_color[3])
        if self.subfig_list[1, 0] != 0:
            if self.ui.checkBox_subfig_4_img_type.isChecked() == 0:
                self.D1_plot_figure(self.figure_array_size[0], self.figure_array_size[1], self.subfig_num[1, 0],
                                str(self.ui.comboBox_subfig_4.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                self.sweep_range_x_array, self.data_plot[self.ui.comboBox_subfig_4.currentIndex()+1])
            elif self.ScanofDimension > 1 and self.ui.checkBox_subfig_4_img_type.isChecked() == 1:
                self.D2_plot_figure(self.figure_array_size[0], self.figure_array_size[1],  self.subfig_num[1, 0],
                                    str(self.ui.comboBox_subfig_4.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                    str(self.ui.comboBox_y_axis.currentText()), self.sweep_range_x_array,
                                    self.sweep_range_y_array, self.data_plot[self.ui.comboBox_subfig_4.currentIndex()+1], self.fig_map_color[4])
        if self.subfig_list[1, 1] != 0:
            if self.ui.checkBox_subfig_5_img_type.isChecked() == 0:
                self.D1_plot_figure(self.figure_array_size[0], self.figure_array_size[1], self.subfig_num[1, 1],
                                str(self.ui.comboBox_subfig_5.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                self.sweep_range_x_array, self.data_plot[self.ui.comboBox_subfig_5.currentIndex()+1])
            elif self.ScanofDimension > 1 and self.ui.checkBox_subfig_5_img_type.isChecked() == 1:
                self.D2_plot_figure(self.figure_array_size[0], self.figure_array_size[1],  self.subfig_num[1, 1],
                                    str(self.ui.comboBox_subfig_5.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                    str(self.ui.comboBox_y_axis.currentText()), self.sweep_range_x_array,
                                    self.sweep_range_y_array, self.data_plot[self.ui.comboBox_subfig_5.currentIndex()+1], self.fig_map_color[5])
        if self.subfig_list[1, 2] != 0:
            if self.ui.checkBox_subfig_6_img_type.isChecked() == 0:
                self.D1_plot_figure(self.figure_array_size[0], self.figure_array_size[1], self.subfig_num[1, 2],
                                str(self.ui.comboBox_subfig_6.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                self.sweep_range_x_array, self.data_plot[self.ui.comboBox_subfig_6.currentIndex()+1])
            elif self.ScanofDimension > 1 and self.ui.checkBox_subfig_6_img_type.isChecked() == 1:
                self.D2_plot_figure(self.figure_array_size[0], self.figure_array_size[1],  self.subfig_num[0, 1],
                                    str(self.ui.comboBox_subfig_6.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                    str(self.ui.comboBox_y_axis.currentText()), self.sweep_range_x_array,
                                    self.sweep_range_y_array, self.data_plot[self.ui.comboBox_subfig_6.currentIndex()+1], self.fig_map_color[6])
        if self.subfig_list[2, 0] != 0:
            if self.ui.checkBox_subfig_7_img_type.isChecked() == 0:
                self.D1_plot_figure(self.figure_array_size[0], self.figure_array_size[1], self.subfig_num[2, 0],
                                str(self.ui.comboBox_subfig_7.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                self.sweep_range_x_array, self.data_plot[self.ui.comboBox_subfig_7.currentIndex()+1])
            elif self.ScanofDimension > 1 and self.ui.checkBox_subfig_7_img_type.isChecked() == 1:
                self.D2_plot_figure(self.figure_array_size[0], self.figure_array_size[1],  self.subfig_num[0, 1],
                                    str(self.ui.comboBox_subfig_7.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                    str(self.ui.comboBox_y_axis.currentText()), self.sweep_range_x_array,
                                    self.sweep_range_y_array, self.data_plot[self.ui.comboBox_subfig_7.currentIndex()+1], self.fig_map_color[7])
        if self.subfig_list[2, 1] != 0:
            if self.ui.checkBox_subfig_8_img_type.isChecked() == 0:
                self.D1_plot_figure(self.figure_array_size[0], self.figure_array_size[1], self.subfig_num[2, 1],
                                str(self.ui.comboBox_subfig_8.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                self.sweep_range_x_array, self.data_plot[self.ui.comboBox_subfig_8.currentIndex()+1])
            elif self.ScanofDimension > 1 and self.ui.checkBox_subfig_8_img_type.isChecked() == 1:
                self.D2_plot_figure(self.figure_array_size[0], self.figure_array_size[1],  self.subfig_num[2, 1],
                                    str(self.ui.comboBox_subfig_8.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                    str(self.ui.comboBox_y_axis.currentText()), self.sweep_range_x_array,
                                    self.sweep_range_y_array, self.data_plot[self.ui.comboBox_subfig_8.currentIndex()+1], self.fig_map_color[8])
        if self.subfig_list[2, 2] != 0:
            if self.ui.checkBox_subfig_9_img_type.isChecked() == 0:
                self.D1_plot_figure(self.figure_array_size[0], self.figure_array_size[1], self.subfig_num[2, 2],
                                str(self.ui.comboBox_subfig_9.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                self.sweep_range_x_array, self.data_plot[self.ui.comboBox_subfig_9.currentIndex()+1])
            elif self.ScanofDimension > 1 and self.ui.checkBox_subfig_9_img_type.isChecked() == 1:
                self.D2_plot_figure(self.figure_array_size[0], self.figure_array_size[1],  self.subfig_num[2, 2],
                                    str(self.ui.comboBox_subfig_9.currentText()), str(self.ui.comboBox_x_axis.currentText()),
                                    str(self.ui.comboBox_y_axis.currentText()), self.sweep_range_x_array,
                                    self.sweep_range_y_array, self.data_plot[self.ui.comboBox_subfig_9.currentIndex()+1], self.fig_map_color[2])
    def define_figure_setup(self):
        row_array_num = []
        col_array_num = []
        self.subfig_num=np.zeros([3,3])
        for i in range(0,3):
            row_array_num.append(sum(self.subfig_list[:, i]))
            col_array_num.append(sum(self.subfig_list[i, :]))
        k=1
        for j in range(0,3):
            for i in range(0, 3):
                if self.subfig_list[j, i] != 0:
                    self.subfig_num[j, i] = self.subfig_num[j, i] + k
                    k+=1
                else:
                    pass


        figure_row = max(row_array_num)
        figure_column = max(col_array_num)
        self.figure_array_size=[figure_row, figure_column]

    def D1_plot_figure(self, figure_row, figure_column, fig_num, title, fig_xlabel, xaxis, caxis):
        #mw = MatplotlibWidget()
        print('figure')

        subplot_num = int(str(int(figure_row))+str(int(figure_column))+str(int(fig_num)))
        print(subplot_num)
        #fig_handle =self.ui.mplwidget_fig_1


        #subplot = fig_handle.getFigure.add_subplot(subplot_num)
        #subplot = fig_handle
        #subplot.plot(xaxis, caxis)
        #fig_handle.axes.draw()
        print xaxis
        print len(xaxis)
        print caxis
        print len(caxis)
        fig1=Figure()
        ax1f1 = fig1.add_subplot(subplot_num)
        ax1f1.plot(xaxis, caxis)
        self.addmpl(fig1)
        print(title)
        print(fig_xlabel)

        '''
        fig_handle=self.ui.mplwidget_fig_1.axes
        fig, ax = fig_handle.subplots(figure_row, figure_column)#, facecolor='w', figsize=(12, 8))
        #for fig_num, ax in enumerate(ax.flat, start=1):
        ax.set_title('{}'.format(title[fig_num]))
        ax.set_xlabel('{}'.format(fig_xlabel[fig_num]))
        #ax.set_ylabel('{}'.format(fig_ylabel[fig_num]))
        ax.tick_params(labelsize=7)
        ax.plot(xaxis, caxis)
        ax.hold(True)
        ax.axis('tight')
        #fig_handle.tight_layout()
        fig_handle.darw(fig)
        #fig_handle.savefig(target_directory + 'html\\figures\\' + Global_file_name + '.png', dpi=image_resolution)
        '''

    def D2_plot_figure(self, figure_row, figure_column, fig_num, title, fig_xlabel, fig_ylabel, xaxis, yaxis, caxis, map_color):
        fig_handle=self.ui.mplwidget_fig_1
        fig, ax = fig_handle.subplots(figure_row, figure_column)#, facecolor='w', figsize=(12, 8))
        # fig.suptitle('Title of fig', fontsize=24)
        #for fig_num, ax in enumerate(ax.flat, start=1):
        ax.set_title('{}'.format(title[fig_num]))
        ax.set_xlabel('{}'.format(fig_xlabel[fig_num]))
        ax.set_ylabel('{}'.format(fig_ylabel[fig_num]))
        ax.tick_params(labelsize=7)
        img = ax.pcolor(xaxis, yaxis, caxis, cmap=map_color)
        ax.axis('tight')
        div = make_axes_locatable(ax)
        cax = div.append_axes("right", size="8%", pad=0.05)
        cbar = fig_handle.colorbar(img, cax=cax)
        #fig_handle.tight_layout()
        fig_handle.darw(fig)
        #fig_handle.savefig(target_directory + 'html\\figures\\' + Global_file_name + '.png', dpi=image_resolution)

    def Make_zero_array(self, xsize, ysize):
        array_handel = np.zeros([ysize, xsize])
        return array_handel
    def Make_NaN_array(self, xsize, ysize):
        array_handel = np.empty([ysize, xsize])
        array_handel[:]=np.NaN
        return array_handel
    def check_measurement_axis(self):
        self.measure_axis[0, 0] = self.ui.comboBox_x_axis.currentIndex()
        self.measure_axis[1, 0] = self.ui.comboBox_y_axis.currentIndex()
        self.measure_axis[2, 0] = self.ui.comboBox_z_axis.currentIndex()
        self.measure_axis[3, 0] = self.ui.comboBox_r_axis.currentIndex()
        self.correct_axis = False
        if self.measure_axis[0, 0] != 0 and self.measure_axis[1, 0] == 0 and self.measure_axis[2, 0] == 0 and self.measure_axis[3, 0] == 0:
            self.correct_axis = True
            self.ScanofDimension=1
        elif self.measure_axis[0, 0] != 0 and self.measure_axis[1, 0] != 0 and self.measure_axis[0, 0] != self.measure_axis[1, 0] and self.measure_axis[2, 0] == 0 and self.measure_axis[3, 0] == 0:
            self.correct_axis = True
            self.ScanofDimension = 2
        elif self.measure_axis[0, 0] != 0 and self.measure_axis[1, 0] != 0 and self.measure_axis[2, 0] != 0 \
                and self.measure_axis[0, 0] != self.measure_axis[1, 0] and self.measure_axis[1, 0] != self.measure_axis[2, 0] \
                and self.measure_axis[0, 0] != self.measure_axis[2, 0] and self.measure_axis[3, 0] == 0:
            self.correct_axis = True
            self.ScanofDimension = 3
        elif self.measure_axis[0, 0] != 0 and self.measure_axis[1, 0] != 0 and self.measure_axis[2, 0] != 0 and self.measure_axis[3, 0] != 0 \
                and self.measure_axis[0, 0] != self.measure_axis[1, 0] and self.measure_axis[0, 0] != self.measure_axis[2, 0] \
                and self.measure_axis[0, 0] != self.measure_axis[3, 0] and self.measure_axis[1, 0] != self.measure_axis[2, 0] \
                and self.measure_axis[1, 0] != self.measure_axis[3, 0] and self.measure_axis[2, 0] != self.measure_axis[3, 0]:
            self.correct_axis = True
            self.ScanofDimension = 4
        else:
            self.axis_wrong_msg()
        print(self.ScanofDimension)
        return self.correct_axis
    def axis_wrong_msg(self):
        QtGui.QMessageBox.question(self, 'Warning!', "Check Measurement Axis", QtGui.QMessageBox.Ok)
    def pause_btn_clicked(self):
        choice = QtGui.QMessageBox.question(self, 'Warning!',
                                            "Quit without save???",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Measurement paused!!!!")

        else:
            pass
    def stop_btn_clicked(self):
        choice = QtGui.QMessageBox.question(self, 'Warning!',
                                            "Measurement Cancel???",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Measurement Canceled!!!!")

        else:
            pass
    def quit_btn_clicked(self):
        choice = QtGui.QMessageBox.question(self, 'Warning!',
                                            "Quit without save???",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Bye Bye!!!!")
            sys.exit()
        else:
            pass
    def Auto_Recon_btn_clicked(self):
        choice = QtGui.QMessageBox.question(self, 'Warning!',
                                            "Set Recondensation Auto?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Set  the   Recondesation    Auto ")
            for voice in voices:
                engine.setProperty('voice', voice.id)
                engine.say("Set  the    Automatical      Recondesation")
            engine.runAndWait()
            self.ui.Lamp_Recon_On_ITC.setValue(1)
        else:
            pass
    def Initial_Valve_status_check(self):
        choice = QtGui.QMessageBox.question(self, 'Warning!',
                                            "What is Valve status?",
                                            QtGui.QMessageBox.Open | QtGui.QMessageBox.Close)
        if choice == QtGui.QMessageBox.Open:
            self.ui.Lamp_Valve_Open_ITC.setValue(1)
            self.ui.Lamp_Valve_Close_ITC.setValue(0)
            self.valve_status = 1
        else:
            self.ui.Lamp_Valve_Open_ITC.setValue(0)
            self.ui.Lamp_Valve_Close_ITC.setValue(1)
            self.valve_status = 0
    def V1open_btn_clicked(self):
        if self.valve_status == 1:
            choice = QtGui.QMessageBox.question(self, 'Warning!',
                                                "Valve is already open, Do you want to proceed?",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        else:
            choice = QtGui.QMessageBox.question(self, 'Warning!',
                                                "Do you want to open the Valve manually?",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            valve = stepper.Instr()
            valve.initialize()
            valve.OPEN_V1()
            print("Open the Valve manually  ")
            for voice in voices:
                engine.setProperty('voice', voice.id)
                engine.say('Open    the    Valve    manually ')
            engine.runAndWait()
            self.ui.Lamp_Valve_Open_ITC.setValue(1)
            self.ui.Lamp_Valve_Close_ITC.setValue(0)
        self.valve_status = 1
    def V1close_btn_clicked(self):
        if self.valve_status == 0:
            choice = QtGui.QMessageBox.question(self, 'Warning!',
                                                "Valve is already close, Do you want to proceed?",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        else:
            choice = QtGui.QMessageBox.question(self, 'Warning!',
                                                "Do you want to close the Valve manually?",
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            valve = stepper.Instr()
            valve.initialize()
            valve.CLOSE_V1()
            print("Close the Valve manually")
            for voice in voices:
                engine.setProperty('voice', voice.id)
                engine.say('Close    the    Valve    manually ')
            engine.runAndWait()
            self.ui.Lamp_Valve_Open_ITC.setValue(0)
            self.ui.Lamp_Valve_Close_ITC.setValue(1)
        self.valve_status = 0
    def REC_on_btn_clicked(self):
        choice = QtGui.QMessageBox.question(self, 'Warning!',
                                            "Recording ITC Temperatures?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            self.progressBar_4.setValue(100)
            print("Recording Temperatures")
            print(self.progressBar_4.Value())

        else:
            pass
            #self.progressBar_4.setValue(0)
    def REC_off_btn_clicked(self):
        choice = QtGui.QMessageBox.question(self, 'Warning!',
                                            "STOP the Recording ITC Temperatures?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            self.progressBar_4.setValue(0)
            print("STOP the Recording")


        else:
            pass
            #self.progressBar_4.setValue(100)
    def Close_application(self):
        msg = "Leave the Application???"
        msgBox = QtGui.QMessageBox(QMessageBox.Warning, "Warning!!!",
                                            msg, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if msgBox.exec_() == QtGui.QMessageBox.Yes:
            print("Bye Bye!!!!")
            sys.exit()
        else:
            pass

    def terminate_thread(thread):
        """Terminates a python thread from another thread.

        :param thread: a threading.Thread instance
        """
        if not thread.isAlive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    #app.exec_()
    sys.exit(app.exec_())
'''
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #myWindow = MyWindow()
    #myWindow.show()
    MainWindow.show()

    sys.exit(app.exec_())
'''