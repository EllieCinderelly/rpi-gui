import sys
import time
#import spidev
from PyQt5.QtWidgets import QGridLayout, QApplication, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QRadioButton, QScrollArea, QVBoxLayout, QHBoxLayout, QTabWidget, QComboBox
from PyQt5.QtCore import QRect, Qt
import pandas as pd
import os
import shutil
#import RPi.GPIO as gpio


button_width = 100
button_height = 20
pin_grid_start = 2

gpio_headers = ['pin11','pin12','pin13','pin15','pin16','pin18','pin22','pin29','pin31','pin32','pin33','pin35','pin36','pin37','pin38','pin40']
gpio_numbers = [11,12,13,15,16,18,22,29,31,32,33,35,36,37,38,40]
address_count = 0 #global variable for keeping track of the number of register addresses for this device

spi_address_sets = [] # array for storing the address info of each created register (SPI)
spi_message_sets = [] # array for storing the message info of each created register (SPI)
spi_label_sets = []


# it's all just widgets inside of widgets...always has been.
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #window settings
        self.setWindowTitle('Q-XMW RPI Test Panel')
        #self.setMinimumHeight(250)
        #self.setMinimumWidth(800)
        #self.setMaximumHeight(250)
        #self.setMaximumWidth(800)
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        self.setStyleSheet('background-color: rgb(38,38,38);')
        self.setFixedHeight(900)
        self.setFixedWidth(1000)

        #layout settings
        layout = QGridLayout()
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(layout)
        QGridLayout.setVerticalSpacing(layout,12)
        QGridLayout.setHorizontalSpacing(layout,12)
        self.grid_widget.setStyleSheet('background-color: rgb(64,64,64);')





        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll_layout,12)

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget.setLayout(self.scroll_layout)
        self.scroll.setStyleSheet('background-color: rgb(64,64,64);')

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll1_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll1_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll1_layout,12)

        self.scroll1 = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget1 = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget1.setLayout(self.scroll1_layout)
        self.scroll1.setStyleSheet('background-color: rgb(64,64,64);')

        #Scroll Area Properties
        self.scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll1.setWidgetResizable(True)
        self.scroll1.setWidget(self.widget1)

        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll2_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll2_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll2_layout,12)

        self.scroll2 = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget2 = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget2.setLayout(self.scroll2_layout)
        self.scroll2.setStyleSheet('background-color: rgb(64,64,64);')

        #Scroll Area Properties
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setWidget(self.widget2)

        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll3_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll3_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll3_layout,12)

        self.scroll3 = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget3 = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget3.setLayout(self.scroll3_layout)
        self.scroll3.setStyleSheet('background-color: rgb(64,64,64);')

        #Scroll Area Properties
        self.scroll3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll3.setWidgetResizable(True)
        self.scroll3.setWidget(self.widget3)
        
        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll4_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll4_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll4_layout,12)

        self.scroll4 = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget4 = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget4.setLayout(self.scroll4_layout)
        self.scroll4.setStyleSheet('background-color: rgb(64,64,64); border: 1px green;')

        #Scroll Area Properties
        self.scroll4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll4.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll4.setWidgetResizable(True)
        self.scroll4.setWidget(self.widget4)


        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.addTab(self.scroll,'SPI')
        tabs.addTab(self.scroll1,'I2C')
        tabs.addTab(self.scroll2,'UART')
        tabs.addTab(self.scroll3,'CLK Gen')
        tabs.addTab(self.scroll4,'About')
        tabs.setStyleSheet('background-color: white; color: black; font-size: 16pt;')


        #spi0_ce1_button = QPushButton('Send Data', self)
        #self.spi0_ce0_button.setFixedWidth(130)
        #self.spi0_ce0_button.setFixedHeight(35)
        #spi0_ce1_button.toggled.connect(self.update)


        #rpi pinout labels
        pin1_label = QLabel('1',self)
        pin1_label.setStyleSheet("color: white; font: 16px;")
        pin2_label = QLabel('2',self)
        pin2_label.setStyleSheet("color: white; font: 16px;")        
        pin3_label = QLabel('3',self)
        pin3_label.setStyleSheet("color: white; font: 16px;")
        pin4_label = QLabel('4',self)
        pin4_label.setStyleSheet("color: white; font: 16px;")
        pin5_label = QLabel('5',self)
        pin5_label.setStyleSheet("color: white; font: 16px;")
        pin6_label = QLabel('6',self)
        pin6_label.setStyleSheet("color: white; font: 16px;")
        pin7_label = QLabel('7',self)
        pin7_label.setStyleSheet("color: white; font: 16px;")
        pin8_label = QLabel('8',self)
        pin8_label.setStyleSheet("color: white; font: 16px;")
        pin9_label = QLabel('9',self)
        pin9_label.setStyleSheet("color: white; font: 16px;")
        pin10_label = QLabel('10',self)
        pin10_label.setStyleSheet("color: white; font: 16px;")
        pin11_label = QLabel('11',self)
        pin11_label.setStyleSheet("color: white; font: 16px;")
        pin12_label = QLabel('12',self)
        pin12_label.setStyleSheet("color: white; font: 16px;")
        pin13_label = QLabel('13',self)
        pin13_label.setStyleSheet("color: white; font: 16px;")
        pin14_label = QLabel('14',self)
        pin14_label.setStyleSheet("color: white; font: 16px;")
        pin15_label = QLabel('15',self)
        pin15_label.setStyleSheet("color: white; font: 16px;")
        pin16_label = QLabel('16',self)
        pin16_label.setStyleSheet("color: white; font: 16px;")
        pin17_label = QLabel('17',self)
        pin17_label.setStyleSheet("color: white; font: 16px;")
        pin18_label = QLabel('18',self)
        pin18_label.setStyleSheet("color: white; font: 16px;")
        pin19_label = QLabel('19',self)
        pin19_label.setStyleSheet("color: white; font: 16px;")
        pin20_label = QLabel('20',self)
        pin20_label.setStyleSheet("color: white; font: 16px;")
        pin21_label = QLabel('21',self)
        pin21_label.setStyleSheet("color: white; font: 16px;")
        pin22_label = QLabel('22',self)
        pin22_label.setStyleSheet("color: white; font: 16px;")
        pin23_label = QLabel('23',self)
        pin23_label.setStyleSheet("color: white; font: 16px;")
        pin24_label = QLabel('24',self)
        pin24_label.setStyleSheet("color: white; font: 16px;")
        pin25_label = QLabel('25',self)
        pin25_label.setStyleSheet("color: white; font: 16px;")
        pin26_label = QLabel('26',self)
        pin26_label.setStyleSheet("color: white; font: 16px;")
        pin27_label = QLabel('27',self)
        pin27_label.setStyleSheet("color: white; font: 16px;")
        pin28_label = QLabel('28',self)
        pin28_label.setStyleSheet("color: white; font: 16px;")
        pin29_label = QLabel('29',self)
        pin29_label.setStyleSheet("color: white; font: 16px;")
        pin30_label = QLabel('30',self)
        pin30_label.setStyleSheet("color: white; font: 16px;")
        pin31_label = QLabel('31',self)
        pin31_label.setStyleSheet("color: white; font: 16px;")
        pin32_label = QLabel('32',self)
        pin32_label.setStyleSheet("color: white; font: 16px;")
        pin33_label = QLabel('33',self)
        pin33_label.setStyleSheet("color: white; font: 16px;")
        pin34_label = QLabel('34',self)
        pin34_label.setStyleSheet("color: white; font: 16px;")
        pin35_label = QLabel('35',self)
        pin35_label.setStyleSheet("color: white; font: 16px;")
        pin36_label = QLabel('36',self)
        pin36_label.setStyleSheet("color: white; font: 16px;")
        pin37_label = QLabel('37',self)
        pin37_label.setStyleSheet("color: white; font: 16px;")
        pin38_label = QLabel('38',self)
        pin38_label.setStyleSheet("color: white; font: 16px;")
        pin39_label = QLabel('39',self)
        pin39_label.setStyleSheet("color: white; font: 16px;")
        pin40_label = QLabel('40',self)
        pin40_label.setStyleSheet("color: white; font: 16px;")


        #ground pins
        ground6_pin = QLabel('GND',self)
        ground6_pin.setStyleSheet("color: white; font: bold 16px;")
        ground9_pin = QLabel('GND',self)
        ground9_pin.setStyleSheet("color: white; font: bold 16px;")
        ground14_pin = QLabel('GND',self)
        ground14_pin.setStyleSheet("color: white; font: bold 16px;")
        ground20_pin = QLabel('GND',self)
        ground20_pin.setStyleSheet("color: white; font: bold 16px;")
        ground25_pin = QLabel('GND',self)
        ground25_pin.setStyleSheet("color: white; font: bold 16px;")
        ground30_pin = QLabel('GND',self)
        ground30_pin.setStyleSheet("color: white; font: bold 16px;")
        ground34_pin = QLabel('GND',self)
        ground34_pin.setStyleSheet("color: white; font: bold 16px;")
        ground39_pin = QLabel('GND',self)
        ground39_pin.setStyleSheet("color: white; font: bold 16px;")


        #3.3V Pins
        p3V_1 = QLabel('3.3V',self)
        p3V_1.setStyleSheet('color: rgb(255,128,213); font: bold 16px;')
        p3V_17 = QLabel('3.3V',self)
        p3V_17.setStyleSheet('color: rgb(255,128,213); font: bold 16px;')

        #5V Pins
        p5V_2 = QLabel('5V',self)
        p5V_2.setStyleSheet('color: rgb(255,128,213); font: bold 16px;')
        p5V_4 = QLabel('5V',self)
        p5V_4.setStyleSheet('color: rgb(255,128,213); font: bold 16px;')

        #Comm Pins
        
        comm3_pin = QLabel('I2C-SDA',self)
        comm3_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')        
        comm5_pin = QLabel('I2C-SCL',self)
        comm5_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm7_pin = QLabel('GLCK',self)
        comm7_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm8_pin = QLabel('UART-TX',self)
        comm8_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm10_pin = QLabel('UART-RX',self)
        comm10_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm19_pin = QLabel('SPI-MOSI',self)
        comm19_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm21_pin = QLabel('SPI-MISO',self)
        comm21_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm23_pin = QLabel('SPI-CLK',self)
        comm23_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm24_pin = QLabel('SPI-CE0',self)
        comm24_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm26_pin = QLabel('SPI-CE1',self)
        comm26_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm27_pin = QLabel('SD (NC)',self)
        comm27_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')
        comm28_pin = QLabel('SC (NC)',self)
        comm28_pin.setStyleSheet('color: rgb(0,255,255); font: bold 16px;')












        #rpi GPIO buttons - 16 pins that are toggleable - they are labeled by rpi pin number instead of the BCM SoC pin number (GPIO#)
        self.GPIO11_button = QCheckBox('GPIO',self)
        self.GPIO11_button.setChecked(False)
        self.GPIO11_button.toggled.connect(self.update)
        self.GPIO11_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO12_button = QCheckBox('GPIO',self)
        self.GPIO12_button.setChecked(False)
        self.GPIO12_button.toggled.connect(self.update)
        self.GPIO12_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO13_button = QCheckBox('GPIO',self)
        self.GPIO13_button.setChecked(False)
        self.GPIO13_button.toggled.connect(self.update)
        self.GPIO13_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO15_button = QCheckBox('GPIO',self)
        self.GPIO15_button.setChecked(False)
        self.GPIO15_button.toggled.connect(self.update)
        self.GPIO15_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO16_button = QCheckBox('GPIO',self)
        self.GPIO16_button.setChecked(False)
        self.GPIO16_button.toggled.connect(self.update)
        self.GPIO16_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO18_button = QCheckBox('GPIO',self)
        self.GPIO18_button.setChecked(False)
        self.GPIO18_button.toggled.connect(self.update)
        self.GPIO18_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO22_button = QCheckBox('GPIO',self)
        self.GPIO22_button.setChecked(False)
        self.GPIO22_button.toggled.connect(self.update)
        self.GPIO22_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO29_button = QCheckBox('GPIO',self)
        self.GPIO29_button.setChecked(False)
        self.GPIO29_button.toggled.connect(self.update)
        self.GPIO29_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO31_button = QCheckBox('GPIO',self)
        self.GPIO31_button.setChecked(False)
        self.GPIO31_button.toggled.connect(self.update)
        self.GPIO31_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO32_button = QCheckBox('GPIO',self)
        self.GPIO32_button.setChecked(False)
        self.GPIO32_button.toggled.connect(self.update)
        self.GPIO32_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO33_button = QCheckBox('GPIO',self)
        self.GPIO33_button.setChecked(False)
        self.GPIO33_button.toggled.connect(self.update)
        self.GPIO33_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO35_button = QCheckBox('GPIO',self)
        self.GPIO35_button.setChecked(False)
        self.GPIO35_button.toggled.connect(self.update)
        self.GPIO35_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO36_button = QCheckBox('GPIO',self)
        self.GPIO36_button.setChecked(False)
        self.GPIO36_button.toggled.connect(self.update)
        self.GPIO36_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO37_button = QCheckBox('GPIO',self)
        self.GPIO37_button.setChecked(False)
        self.GPIO37_button.toggled.connect(self.update)
        self.GPIO37_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO38_button = QCheckBox('GPIO',self)
        self.GPIO38_button.setChecked(False)
        self.GPIO38_button.toggled.connect(self.update)
        self.GPIO38_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')
        self.GPIO40_button = QCheckBox('GPIO',self)
        self.GPIO40_button.setChecked(False)
        self.GPIO40_button.toggled.connect(self.update)
        self.GPIO40_button.setStyleSheet('color: rgb(0,204,0); font: bold 16px;')



        #load state
        load_button = QPushButton('Load',self)
        load_button.clicked.connect(self.update)
        load_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 16px;')
        load_button.clicked.connect(self.load_part)

        save_button = QPushButton('Save',self)
        save_button.clicked.connect(self.update)
        save_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 16px;')
        save_button.clicked.connect(self.save_part)

        self.part_name = QLineEdit()
        self.part_name.setText('Enter Part Name')
        self.part_name.setFixedWidth(250)
        self.part_name.setFixedHeight(30)
        self.part_name.setStyleSheet('background-color: white; font: 18px')
        #self.part_name.setStyleSheet('border: 4px: border-color: green;')


        #apply states button
        apply_button = QPushButton('Apply',self)
        apply_button.clicked.connect(self.update)
        apply_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 16px;')
        #apply_button.clicked.connect(self.apply_pins)

        spi_write_button = QPushButton('WRITE',self)
        spi_write_button.clicked.connect(self.update)
        spi_write_button.setFixedHeight(30)
        spi_write_button.setFixedWidth(160)
        spi_write_button.setStyleSheet('color: black; background-color: rgb(255,153,0); font: bold 16px;')
        spi_write_button.clicked.connect(self.spi_write)



        ##SPI address and message widgets for generating with + buttons
        generate_button = QPushButton('Add Register',self)
        generate_button.clicked.connect(self.update)
        generate_button.setFixedWidth(160)
        generate_button.setFixedHeight(30)
        generate_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 16px;')
        generate_button.clicked.connect(self.generate)

        remove_button = QPushButton('Delete Register',self)
        remove_button.clicked.connect(self.update)
        remove_button.setFixedWidth(160)
        remove_button.setFixedHeight(30)
        remove_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 16px;')
        remove_button.clicked.connect(self.delete)

        self.hold_le = QCheckBox('Toggle CE?',self)
        self.hold_le.setChecked(False)
        self.hold_le.toggled.connect(self.update)
        self.hold_le.setStyleSheet('color: white; font: 18px;')

        mode_label = QLabel('SPI Mode:',self)
        mode_label.setFixedWidth(160)
        mode_label.setFixedHeight(30)
        mode_label.setStyleSheet('color: white; font: 18px;')

        speed_label = QLabel('Speed (Hz):',self)
        speed_label.setFixedWidth(160)
        speed_label.setFixedHeight(30)
        speed_label.setStyleSheet('color: white; font: 18px;')

        self.mode_box = QComboBox()
        self.mode_box.addItem('0')
        self.mode_box.addItem('1')
        self.mode_box.addItem('2')
        self.mode_box.addItem('3')
        self.mode_box.currentIndexChanged.connect(self.update)
        self.mode_box.setStyleSheet('background-color: white; font: 18px;')

        device_label = QLabel('Chip Select:',self)
        device_label.setFixedWidth(160)
        device_label.setFixedHeight(30)
        device_label.setStyleSheet('color: white; font: 18px;')

        self.device_box = QComboBox()
        self.device_box.addItem('CE0')
        self.device_box.addItem('CE1')
        self.device_box.currentIndexChanged.connect(self.update)
        self.device_box.setStyleSheet('background-color: white; font: 18px;')

        self.speed = QLineEdit()
        self.speed.setText('25000')
        self.speed.setFixedWidth(160)
        self.speed.setFixedHeight(30)
        self.speed.setStyleSheet('background-color: white; font: 18px')

        about_label = QLabel('SPI: "Toggle LE" box can be selected to toggle \n       CE0 or CE1 between words. \n\n\nThis program is maintained by Ellie. \nBug reports, functionality requests, etc. contact at:\nEllie.Roth@quanticxmw.com',self)
        about_label.setStyleSheet('color: white; font: 18px;')

        I2C_label = QLabel('The RPi can handle i2c communication on pins 3(SDA) and 5(SCL). \n ~There is a second i2c bus on the EEPROM lines but,\n   those should be reserved for the internal HAT. \n ~HAT config can be looked into as well.',self)
        I2C_label.setStyleSheet('color: white; font: 18px;')

        UART_label = QLabel('The RPi can handle UART communication on pins 8(TX) and 10(RX) \n ~To be implemented.',self)
        UART_label.setStyleSheet('color: white; font: 18px;')

        clockgen_label = QLabel('Pin 7 "GCLK" is capable of generating a square wave up to 125MHz. \n ~To be implemented.',self)
        clockgen_label.setStyleSheet('color: white; font: 18px;')


        self.gpio_names = [self.GPIO11_button,self.GPIO12_button,self.GPIO13_button,self.GPIO15_button,self.GPIO16_button,self.GPIO18_button,self.GPIO22_button,self.GPIO29_button,self.GPIO31_button,self.GPIO32_button,self.GPIO33_button,self.GPIO35_button,self.GPIO36_button,self.GPIO37_button,self.GPIO38_button,self.GPIO40_button]

        #layout reference because why follow common-sense coding conventions
        ## tabs.addTab(self.scroll,'SPI')
        ## tabs.addTab(self.scroll1,'I2C')
        ## tabs.addTab(self.scroll2,'UART')
        ## tabs.addTab(self.scroll3,'CLK Gen')
        ## tabs.addTab(self.scroll4,'About')

        self.scroll_layout.addWidget(spi_write_button,0,0,1,1)
        self.scroll_layout.addWidget(remove_button,1,0,1,1)
        self.scroll_layout.addWidget(self.hold_le,0,3,1,1)

        self.scroll_layout.addWidget(mode_label,0,1,1,1)
        self.scroll_layout.addWidget(self.mode_box,0,2,1,1)
        self.scroll_layout.addWidget(self.speed,1,2,1,1)
        self.scroll_layout.addWidget(speed_label,1,1,1,1)
        self.scroll_layout.addWidget(generate_button,2,0,1,1)
        self.scroll_layout.addWidget(self.device_box,2,2,1,1)
        self.scroll_layout.addWidget(device_label,2,1,1,1)

        self.scroll1_layout.addWidget(I2C_label,0,0,6,3)
        self.scroll2_layout.addWidget(UART_label,0,0,6,3)
        self.scroll3_layout.addWidget(clockgen_label,0,0,6,3)
        self.scroll4_layout.addWidget(about_label,0,0,6,3)



        layout.addWidget(load_button,pin_grid_start - 2, 0,1,2)
        layout.addWidget(save_button,pin_grid_start - 2, 2,1,2)
        layout.addWidget(apply_button,pin_grid_start - 2, 4,1,2)
        layout.addWidget(self.part_name,pin_grid_start - 1,0,1,6)

        layout.addWidget(pin1_label,pin_grid_start + 0,0)
        layout.addWidget(p3V_1,pin_grid_start + 0,1,1,2)

        layout.addWidget(pin2_label,pin_grid_start + 0,3)
        layout.addWidget(p5V_2,pin_grid_start + 0,4,1,2)

        layout.addWidget(pin3_label,pin_grid_start + 1,0)
        layout.addWidget(comm3_pin,pin_grid_start + 1,1,1,2)

        layout.addWidget(pin4_label,pin_grid_start + 1,3)
        layout.addWidget(p5V_4,pin_grid_start + 1,4,1,2)

        layout.addWidget(pin5_label,pin_grid_start + 2,0)
        layout.addWidget(comm5_pin,pin_grid_start + 2,1,1,2)

        layout.addWidget(pin6_label,pin_grid_start + 2,3)
        layout.addWidget(ground6_pin,pin_grid_start + 2,4,1,2)

        layout.addWidget(pin7_label,pin_grid_start + 3,0)
        layout.addWidget(comm7_pin,pin_grid_start + 3,1,1,2)

        layout.addWidget(pin8_label,pin_grid_start + 3,3)
        layout.addWidget(comm8_pin,pin_grid_start + 3,4,1,2)

        layout.addWidget(pin9_label,pin_grid_start + 4,0)
        layout.addWidget(ground9_pin,pin_grid_start + 4,1,1,2)

        layout.addWidget(pin10_label,pin_grid_start + 4,3)
        layout.addWidget(comm10_pin,pin_grid_start + 4,4,1,2)

        layout.addWidget(pin11_label,pin_grid_start + 5,0)
        layout.addWidget(self.GPIO11_button,pin_grid_start + 5,1,1,2)

        layout.addWidget(pin12_label,pin_grid_start + 5,3)
        layout.addWidget(self.GPIO12_button,pin_grid_start + 5,4,1,2)

        layout.addWidget(pin13_label,pin_grid_start + 6,0)
        layout.addWidget(self.GPIO13_button,pin_grid_start + 6,1,1,2)

        layout.addWidget(pin14_label,pin_grid_start + 6,3)
        layout.addWidget(ground14_pin,pin_grid_start + 6,4,1,2)

        layout.addWidget(pin15_label,pin_grid_start + 7,0)
        layout.addWidget(self.GPIO15_button,pin_grid_start + 7,1,1,2)

        layout.addWidget(pin16_label,pin_grid_start + 7,3)
        layout.addWidget(self.GPIO16_button,pin_grid_start + 7,4,1,2)

        layout.addWidget(pin17_label,pin_grid_start + 8,0)
        layout.addWidget(p3V_17,pin_grid_start + 8,1,1,2)

        layout.addWidget(pin18_label,pin_grid_start + 8,3)
        layout.addWidget(self.GPIO18_button,pin_grid_start + 8,4,1,2)

        layout.addWidget(pin19_label,pin_grid_start + 9,0)
        layout.addWidget(comm19_pin,pin_grid_start + 9,1,1,2)

        layout.addWidget(pin20_label,pin_grid_start + 9,3)
        layout.addWidget(ground20_pin,pin_grid_start + 9,4,1,2)

        layout.addWidget(pin21_label,pin_grid_start + 10,0)
        layout.addWidget(comm21_pin,pin_grid_start + 10,1,1,2)

        layout.addWidget(pin22_label,pin_grid_start + 10,3)
        layout.addWidget(self.GPIO22_button,pin_grid_start + 10,4,1,2)

        layout.addWidget(pin23_label,pin_grid_start + 11,0)
        layout.addWidget(comm23_pin,pin_grid_start + 11,1,1,2)

        layout.addWidget(pin24_label,pin_grid_start + 11,3)
        layout.addWidget(comm24_pin,pin_grid_start + 11,4,1,2)

        layout.addWidget(pin25_label,pin_grid_start + 12,0)
        layout.addWidget(ground25_pin,pin_grid_start + 12,1,1,2)

        layout.addWidget(pin26_label,pin_grid_start + 12,3)
        layout.addWidget(comm26_pin,pin_grid_start + 12,4,1,2)

        layout.addWidget(pin27_label,pin_grid_start + 13,0)
        layout.addWidget(comm27_pin,pin_grid_start + 13,1,1,2)

        layout.addWidget(pin28_label,pin_grid_start + 13,3)
        layout.addWidget(comm28_pin,pin_grid_start + 13,4,1,2)
        
        layout.addWidget(pin29_label,pin_grid_start + 14,0)
        layout.addWidget(self.GPIO29_button,pin_grid_start + 14,1,1,2)

        layout.addWidget(pin30_label,pin_grid_start + 14,3)
        layout.addWidget(ground30_pin,pin_grid_start + 14,4,1,2)

        layout.addWidget(pin31_label,pin_grid_start + 15,0)
        layout.addWidget(self.GPIO31_button,pin_grid_start + 15,1,1,2)

        layout.addWidget(pin32_label,pin_grid_start + 15,3)
        layout.addWidget(self.GPIO32_button,pin_grid_start + 15,4,1,2)

        layout.addWidget(pin33_label,pin_grid_start + 16,0)
        layout.addWidget(self.GPIO33_button,pin_grid_start + 16,1,1,2)

        layout.addWidget(pin34_label,pin_grid_start + 16,3)
        layout.addWidget(ground34_pin,pin_grid_start + 16,4,1,2)

        layout.addWidget(pin35_label,pin_grid_start + 17,0)
        layout.addWidget(self.GPIO35_button,pin_grid_start + 17,1,1,2)

        layout.addWidget(pin36_label,pin_grid_start + 17,3)
        layout.addWidget(self.GPIO36_button,pin_grid_start + 17,4,1,2)

        layout.addWidget(pin37_label,pin_grid_start + 18,0)
        layout.addWidget(self.GPIO37_button,pin_grid_start + 18,1,1,2)

        layout.addWidget(pin38_label,pin_grid_start + 18,3)
        layout.addWidget(self.GPIO38_button,pin_grid_start + 18,4,1,2)

        layout.addWidget(pin39_label,pin_grid_start + 19,0)
        layout.addWidget(ground39_pin,pin_grid_start + 19,1,1,2)

        layout.addWidget(pin40_label,pin_grid_start + 19,3)
        layout.addWidget(self.GPIO40_button,pin_grid_start + 19,4,1,2)

        



        main_layout.addWidget(self.grid_widget)
        main_layout.addWidget(tabs)
        self.generate()
        self.whitespace()
        #set GPIO for output and set all LOW at startup - uncomment on rpi
        """
        for i in range(len(gpio_numbers)):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(gpio_numbers[i], GPIO.OUT)
            GPIO.output(gpio_numbers[i], 0)
        """
        self.show()


    def load_part(self):
        global address_count
        global spi_address_sets
        global spi_message_sets
        global spi_label_sets

        name = self.part_name.text()
        if(name=='base'):
            self.part_name.setText('INVALID NAME')
        else:
            try: 
                df = pd.read_csv('part_config\\%s.csv' % (name))
            except:
                self.part_name.setText('FILE NOT FOUND')
            else:

                for i in range(address_count): #if the load is possible we need to delete the currently created register locations
                    self.scroll_layout.removeWidget(spi_address_sets[i])
                    self.scroll_layout.removeWidget(spi_message_sets[i])
                    self.scroll_layout.removeWidget(spi_label_sets[i])



                address_count = int(df.loc[0].at['SPI_count'])
                spi_address_sets = [] #these need reset on a successful load otherwise we append onto already loaded arrays
                spi_message_sets = []
                spi_label_sets = []

                for i in range(len(self.gpio_names)):
                    state = df.loc[i].at['GPIO_pins']
                    if(state == 0): self.gpio_names[i].setChecked(False)
                    if(state == 1): self.gpio_names[i].setChecked(True)

                for i in range(address_count):
                    labelName = "REG"+str(i)
                    self.labelName = QLabel(self)
                    self.labelName.setText("REG %s" % (i))
                    self.labelName.setFixedWidth(160)
                    self.labelName.setFixedHeight(30)
                    self.labelName.setStyleSheet('color: white; font: 18px;')
                    address = "address"+str(i)
                    self.address = QLineEdit(self)
                    self.address.setFixedWidth(160)
                    self.address.setFixedHeight(30)
                    self.address.setText(str(hex(int(df.loc[i,'SPI_Address']))))
                    self.address.setStyleSheet('background-color: white; color: black; font: 18px;')
                    msg = "message"+str(i)
                    self.msg = QLineEdit(self)
                    self.msg.setFixedWidth(160)
                    self.msg.setFixedHeight(30)
                    self.msg.setText(str(hex(int(df.loc[i,'SPI_Message']))))
                    self.msg.setStyleSheet('background-color: white; color: black; font: 18px;')
                    #add widget to layout
                    self.scroll_layout.addWidget(self.labelName,i + 3,0)
                    self.scroll_layout.addWidget(self.address,i + 3,1)
                    self.scroll_layout.addWidget(self.msg,i + 3,2)
                    #still need to store these for local access on a load operation
                    spi_address_sets.append(self.address)
                    spi_message_sets.append(self.msg)
                    spi_label_sets.append(self.labelName)

                mode = int(df.loc[0,'SPI_settings'])
                self.mode_box.setCurrentIndex(mode)

                speed = str(int(df.loc[1,'SPI_settings']))
                self.speed.setText(speed)

                ce = int(df.loc[2,'SPI_settings'])
                self.device_box.setCurrentIndex(ce)

                tg = int(df.loc[3,'SPI_settings'])
                if(tg == 0): self.hold_le.setChecked(False)
                if(tg == 1): self.hold_le.setChecked(True)

                
                
                

    def save_part(self):
        global address_count
        global spi_address_sets
        global spi_message_sets
        name = self.part_name.text()
        if(name=='base'):
            self.part_name.setText('INVALID NAME')
        else:
            if(os.path.exists('part_config\\%s.csv' % (name))): os.remove('part_config\\%s.csv' % (name))                       
            shutil.copyfile('part_config\\base.csv', 'part_config\\%s.csv' % (name))
            df = pd.read_csv('part_config\\%s.csv' % (name))

            for i in range(len(self.gpio_names)):
                state = self.gpio_names[i].isChecked()
                if(state == False): state = 0
                if(state == True): state = 1
                df.loc[i,'GPIO_pins'] = state
                
            df.loc[0,'SPI_count'] = int(address_count)

            #print(address_count)
            for i in range(address_count):
                df.loc[i,'SPI_Address'] = int(spi_address_sets[i].text(),16)
                df.loc[i,'SPI_Message'] = int(spi_message_sets[i].text(),16)

            #save SPI mode state
            cindex = self.mode_box.currentIndex()
            df.loc[0,'SPI_settings'] = cindex #SPI mode

            #save SPI speed text
            df.loc[1,'SPI_settings'] = int(self.speed.text()) #SPI speed

            #save SPI CE pin selected state
            cindex = self.device_box.currentIndex()
            df.loc[2,'SPI_settings'] = cindex #SPI CE pin

            #save CE toggle state
            state = self.hold_le.isChecked()
            if(state == False): state = 0
            if(state == True): state = 1
            df.loc[3,'SPI_settings'] = state #SPI toggle CE pin

            df.to_csv('part_config\\%s.csv' % (name),index=False)



    #apply settings from loaded pins - uncomment for rpi
    """
    def apply_pins(self):
        for i in range(len(gpio_names)):
            state = self.gpio_names[i].isChecked()    
            if(state == False): 
                GPIO.output(gpio_numbers[i], 0)
            if(state == True): 
                GPIO.output(gpio_numbers[i], 1)
    """

    def generate(self):
        
        global spi_address_sets
        global spi_message_sets
        global spi_label_sets
        global address_count
        labelName = "REG"+str(address_count)
        self.labelName = QLabel(self)
        self.labelName.setText("REG %s" % address_count)
        self.labelName.setFixedWidth(160)
        self.labelName.setFixedHeight(30)
        self.labelName.setStyleSheet('color: white; font: 18px;')
        address = "address"+str(address_count)
        self.address = QLineEdit(self)
        self.address.setFixedWidth(160)
        self.address.setFixedHeight(30)
        self.address.setText('0xff')
        self.address.setStyleSheet('background-color: white; color: black; font: 18px;')
        msg = "message"+str(address_count)
        self.msg = QLineEdit(self)
        self.msg.setFixedWidth(160)
        self.msg.setFixedHeight(30)
        self.msg.setText('0xff')
        self.msg.setStyleSheet('background-color: white; color: black; font: 18px;')
        #add widget to layout
        self.scroll_layout.addWidget(self.labelName,address_count + 3,0)
        self.scroll_layout.addWidget(self.address,address_count + 3,1)
        self.scroll_layout.addWidget(self.msg,address_count + 3,2)
        spi_label_sets.append(self.labelName)
        spi_address_sets.append(self.address)
        spi_message_sets.append(self.msg)
        address_count = int(address_count) + int(1)
        self.whitespace()
                

    def whitespace(self):
        global address_count
        for i in range(20 - address_count):
            spacerName = "REGW"+str(i)
            self.spacerName = QLabel(self)
            self.spacerName.setFixedWidth(200)
            self.scroll_layout.addWidget(self.spacerName,address_count + 5 + i,0,1,3)

    def delete(self):
        global spi_address_sets
        global spi_message_sets
        global spi_label_sets
        global address_count

        index = address_count - 1

        if(address_count==1):
            print('cannot remove any more registers')#maybe add output console later?
        else:            
            self.scroll_layout.removeWidget(spi_address_sets[index])
            self.scroll_layout.removeWidget(spi_message_sets[index])
            self.scroll_layout.removeWidget(spi_label_sets[index])
            spi_address_sets[index].setParent(None)
            spi_message_sets[index].setParent(None)
            spi_label_sets[index].setParent(None)
            del spi_address_sets[index]
            del spi_message_sets[index]
            del spi_label_sets[index]
            address_count = address_count - 1
            





    def spi_write(self):
        global spi_address_sets
        global spi_message_sets
        global spi_label_sets
        global address_count



        spi_send = [] #Generate an empty array to handle what message we are sending

        mode = int(self.mode_box.currentIndex())
        speed = int(self.speed.text())
        chip = int(self.device_box.currentIndex())

        print(mode,speed,chip)

        #if the address skip box is checked, we don't append addresses and just send the message. otherwise we need to combine the address+message
        print(address_count)
        for i in range(address_count):
            spi_send.append(int(spi_address_sets[i].text(),16) + int(spi_message_sets[i].text(),16))
            print(spi_send[i])


        #spi = spidev.SpiDev()
        #spi.open(0,chip)
        #spi.max_speed_hz = speed
        #spi.mode = mode
            
        for i in range(len(spi_send)):
                if(self.hold_le.isChecked()):
                    #spi.xfer3([spi_send[i]])
                    print(hex(spi_send[i]))
                    output = format(spi_send[i],'08b')
                    print('%s -cmd%s' % (output,i+1)) 
                else:
                    #spi.xfer([spi_send[i]])
                    output = format(int(spi_send[i],16),'#010b')
                    print('%s -cmd%s' % (output,i+1))  
                    
        print('sent %s' % (spi_send))
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
