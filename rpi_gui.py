import sys
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import spidev
from PyQt6.QtWidgets import (QGridLayout, QApplication, QWidget, QLabel, QPushButton,
                             QLineEdit, QCheckBox, QRadioButton, QScrollArea, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QComboBox)
from PyQt6.QtCore import QRect, Qt

import pandas as pd
import os
import shutil
import RPi.GPIO as GPIO


button_width = 100
button_height = 20
pin_grid_start = 2
gpio_bcm_names = ['17','18','27','22','23','24','25','5','6','12','13','19','16','26','20','21']

comm_pin_names = ['I2C-SDA','I2C-SCL','GLCK','UART-TX','UART-RX','SPI-MOSI','SPI-MISO','SPI-CLK','SPI-CE0','SPI-CE1','SD (NC)','SC (NC)']
comm_pin_numbers = [3,5,7,8,10,19,21,23,24,26,27,28]
gpio_numbers = [11,12,13,15,16,18,22,29,31,32,33,35,36,37,38,40]
ground_numbers = [6,9,14,20,25,30,34,39]
v5_numbers = [2,4]
v3v3_numbers = [1,17]

address_count = 0 #global variable for keeping track of the number of register addresses for this device

gpio_sets = []
gpio_labels = []
spi_address_sets = [] # stores the address info of each created register (SPI)
spi_message_sets = [] # stores the message info of each created register (SPI)
spi_label_sets = []   # stores the custom register label
spi_reg_write_button_sets = []   # stores the write button sets
spi_reg_read_button_sets = []   # stores the read button sets
spi_reg_readback_sets = []   # stores the read button sets



# it's all just widgets inside of widgets...always has been.
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #window settings
        self.setWindowTitle('RPi Control Panel')
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        self.setStyleSheet('background-color: rgb(38,38,38);')
        self.setFixedHeight(700)
        self.setFixedWidth(900)

        #layout settings
        layout = QGridLayout()
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(layout)
        QGridLayout.setVerticalSpacing(layout,8)
        QGridLayout.setHorizontalSpacing(layout,8)
        self.grid_widget.setStyleSheet('background-color: rgb(64,64,64);')
        self.grid_widget.setFixedWidth(300)
        

        ### This next section creates the scoll areas -- to be implemented in a generative function
        ########################################
        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll_layout,8)

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget.setLayout(self.scroll_layout)
        self.scroll.setStyleSheet('background-color: rgb(64,64,64);')

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        ########################################
        ########################################
        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll1_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll1_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll1_layout,8)

        self.scroll1 = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget1 = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget1.setLayout(self.scroll1_layout)
        self.scroll1.setStyleSheet('background-color: rgb(64,64,64);')

        #Scroll Area Properties
        self.scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll1.setWidgetResizable(True)
        self.scroll1.setWidget(self.widget1)
        ########################################
        ########################################
        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll2_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll2_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll2_layout,8)

        self.scroll2 = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget2 = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget2.setLayout(self.scroll2_layout)
        self.scroll2.setStyleSheet('background-color: rgb(64,64,64);')

        #Scroll Area Properties
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setWidget(self.widget2)
        ########################################
        ########################################
        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll3_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll3_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll3_layout,8)

        self.scroll3 = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget3 = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget3.setLayout(self.scroll3_layout)
        self.scroll3.setStyleSheet('background-color: rgb(64,64,64);')

        #Scroll Area Properties
        self.scroll3.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll3.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll3.setWidgetResizable(True)
        self.scroll3.setWidget(self.widget3)
        ########################################
        ########################################  
        #this creates a layout type, scroll area, and widget. The layout is assigned to the widget, set the vertical scroll box set to always on, horizontal to off, make it resizeable, assign the widget to the scroll area
        self.scroll4_layout = QGridLayout()           #
        QGridLayout.setVerticalSpacing(self.scroll4_layout,8)
        QGridLayout.setHorizontalSpacing(self.scroll4_layout,8)

        self.scroll4 = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget4 = QWidget()                 # Widget that contains the collection of Vertical Box           
        self.widget4.setLayout(self.scroll4_layout)
        self.scroll4.setStyleSheet('background-color: rgb(64,64,64); border: 1px green;')

        #Scroll Area Properties
        self.scroll4.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll4.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll4.setWidgetResizable(True)
        self.scroll4.setWidget(self.widget4)
        ########################################
        ########################################

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.addTab(self.scroll,'SPI')
        tabs.addTab(self.scroll1,'I2C')
        tabs.addTab(self.scroll2,'UART')
        tabs.addTab(self.scroll3,'CLK Gen')
        tabs.addTab(self.scroll4,'About')
        tabs.setStyleSheet('background-color: white; color: black; font-size: 10pt;')

        #generate the 40 RPi Pin Labels and populate them on the grid
        for i in range(40):
            self.pinLabel = QLabel(self)
            self.pinLabel.setText("%s" % (i+1))
            self.pinLabel.setFixedWidth(20)
            self.pinLabel.setFixedHeight(10)
            self.pinLabel.setStyleSheet('color: white; font: 10px;')
            
            if i % 2 == 0:
                layout.addWidget(self.pinLabel,pin_grid_start + int(i/2),0,1,1)
            else:
                layout.addWidget(self.pinLabel,pin_grid_start + int(i/2),3,1,1)

        for i in range(len(v3v3_numbers)):
            self.v3_label = QLabel(self)
            self.v3_label.setText("3.3V")
            self.v3_label.setFixedWidth(60)
            self.v3_label.setFixedHeight(30)
            self.v3_label.setStyleSheet('color: rgb(255,128,213); font: bold 10px;')
            print(int(v3v3_numbers[i]/2))
            layout.addWidget(self.v3_label,pin_grid_start + int(v3v3_numbers[i]/2),1,1,2)

        for i in range(len(v5_numbers)):
            self.v5_label = QLabel(self)
            self.v5_label.setText("5V")
            self.v5_label.setFixedWidth(60)
            self.v5_label.setFixedHeight(30)
            self.v5_label.setStyleSheet('color: rgb(255,128,213); font: bold 10px;')
            print(int(v5_numbers[i]/2))
            layout.addWidget(self.v5_label,pin_grid_start + int(v5_numbers[i]/2) - 1,4,1,2)

        for i in range(len(ground_numbers)):
            self.ground_label = QLabel(self)
            self.ground_label.setText("Ground")
            self.ground_label.setFixedWidth(60)
            self.ground_label.setFixedHeight(30)
            self.ground_label.setStyleSheet('color: white; font: bold 10px;')
            print(int(ground_numbers[i]/2),i % 2)
            if ground_numbers[i] % 2 == 1:
                layout.addWidget(self.ground_label,pin_grid_start + int(ground_numbers[i]/2),1,1,2)
            else:
                layout.addWidget(self.ground_label,pin_grid_start + int(ground_numbers[i]/2) - 1,4,1,2)
  
        for i in range(len(comm_pin_numbers)):
            self.comm_pin = QLabel(self)
            self.comm_pin.setText("%s" % (comm_pin_names[i]))
            self.comm_pin.setFixedWidth(60)
            self.comm_pin.setFixedHeight(30)
            self.comm_pin.setStyleSheet('color: rgb(0,255,255); font: bold 10px;')
            print(int(comm_pin_numbers[i]/2),i % 2)
            if comm_pin_numbers[i] % 2 == 1:
                layout.addWidget(self.comm_pin,pin_grid_start + int(comm_pin_numbers[i]/2),1,1,2)
            else:
                layout.addWidget(self.comm_pin,pin_grid_start + int(comm_pin_numbers[i]/2) - 1,4,1,2)

        for i in range(len(gpio_numbers)):
            self.gpio_label = QLineEdit()
            self.gpio_label.setText('GPIO %s' % gpio_bcm_names[i])
            self.gpio_label.setFixedWidth(60)
            self.gpio_label.setFixedHeight(30)
            self.gpio_label.setStyleSheet('color: rgb(0,204,0); font: bold 10px;')
            self.gpio_pin = QCheckBox(self)
            self.gpio_pin.setFixedWidth(10)
            self.gpio_pin.setFixedHeight(10)
            self.gpio_pin.setStyleSheet('color: rgb(0,204,0); background-color: rgb(255,255,255); font: bold 10px;')
            gpio_labels.append(self.gpio_label)
            gpio_sets.append(self.gpio_pin)
            print(gpio_numbers[i],i,i%2)
            if gpio_numbers[i] % 2 == 1:
                layout.addWidget(self.gpio_label,pin_grid_start + int(gpio_numbers[i]/2),1,1,1)
                layout.addWidget(self.gpio_pin,pin_grid_start + int(gpio_numbers[i]/2),2,1,1)
                
            else:
                layout.addWidget(self.gpio_label,pin_grid_start + int(gpio_numbers[i]/2) - 1,4,1,1)
                layout.addWidget(self.gpio_pin,pin_grid_start + int(gpio_numbers[i]/2) - 1,5,1,1)


        #load state
        load_button = QPushButton('Load',self)
        load_button.clicked.connect(self.update)
        load_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
        load_button.clicked.connect(self.load_part)

        save_button = QPushButton('Save',self)
        save_button.clicked.connect(self.update)
        save_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
        save_button.clicked.connect(self.save_part)

        self.part_name = QLineEdit()
        self.part_name.setText('Enter Part Name')
        self.part_name.setFixedWidth(240)
        self.part_name.setFixedHeight(30)
        self.part_name.setStyleSheet('background-color: white; font: 10px')
        #self.part_name.setStyleSheet('border: 4px: border-color: green;')

        #apply states button
        apply_button = QPushButton('Apply',self)
        apply_button.clicked.connect(self.update)
        apply_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
        #apply_button.clicked.connect(self.apply_pins)

        spi_write_button = QPushButton('WRITE',self)
        spi_write_button.clicked.connect(self.update)
        spi_write_button.setFixedHeight(30)
        spi_write_button.setFixedWidth(80)
        spi_write_button.setStyleSheet('color: black; background-color: rgb(255,153,0); font: bold 10px;')
        spi_write_button.clicked.connect(self.spi_write)

        ##SPI address and message widgets for generating with + buttons
        generate_button = QPushButton('Add Reg',self)
        generate_button.clicked.connect(self.update)
        generate_button.setFixedWidth(80)
        generate_button.setFixedHeight(30)
        generate_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
        generate_button.clicked.connect(self.generate)

        remove_button = QPushButton('Delete Reg',self)
        remove_button.clicked.connect(self.update)
        remove_button.setFixedWidth(80)
        remove_button.setFixedHeight(30)
        remove_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
        remove_button.clicked.connect(self.delete)

        readback_all_button = QPushButton('Readback All',self)
        readback_all_button.clicked.connect(self.update)
        readback_all_button.setFixedWidth(80)
        readback_all_button.setFixedHeight(30)
        readback_all_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
        readback_all_button.clicked.connect(self.spi_read)

        self.hold_le = QCheckBox('Toggle CE?',self)
        self.hold_le.setChecked(False)
        self.hold_le.toggled.connect(self.update)
        self.hold_le.setStyleSheet('color: white; font: 10px;')

        mode_label = QLabel('SPI Mode:',self)
        mode_label.setFixedWidth(80)
        mode_label.setFixedHeight(30)
        mode_label.setStyleSheet('color: white; font: 10px;')

        speed_label = QLabel('Speed (Hz):',self)
        speed_label.setFixedWidth(80)
        speed_label.setFixedHeight(30)
        speed_label.setStyleSheet('color: white; font: 10px;')

        single_write_label = QLabel('',self)
        single_write_label.setFixedWidth(80)
        single_write_label.setFixedHeight(30)
        single_write_label.setStyleSheet('color: white; font: 10px;')

        single_read_label = QLabel('',self)
        single_read_label.setFixedWidth(80)
        single_read_label.setFixedHeight(30)
        single_read_label.setStyleSheet('color: white; font: 10px;')

        readback_label = QLabel('Readback Values',self)
        readback_label.setFixedWidth(80)
        readback_label.setFixedHeight(30)
        readback_label.setStyleSheet('color: white; font: 10px;')

        self.mode_box = QComboBox()
        self.mode_box.addItem('0')
        self.mode_box.addItem('1')
        self.mode_box.addItem('2')
        self.mode_box.addItem('3')
        self.mode_box.currentIndexChanged.connect(self.update)
        self.mode_box.setStyleSheet('background-color: white; font: 10px;')

        device_label = QLabel('Chip Select:',self)
        device_label.setFixedWidth(80)
        device_label.setFixedHeight(30)
        device_label.setStyleSheet('color: white; font: 10px;')

        self.device_box = QComboBox()
        self.device_box.addItem('CE0')
        self.device_box.addItem('CE1')
        self.device_box.currentIndexChanged.connect(self.update)
        self.device_box.setStyleSheet('background-color: white; font: 10px;')

        self.speed = QLineEdit()
        self.speed.setText('25000')
        self.speed.setFixedWidth(80)
        self.speed.setFixedHeight(30)
        self.speed.setStyleSheet('background-color: white; font: 10px')

        about_label = QLabel('SPI: "Toggle LE" box can be selected to toggle \n       CE0 or CE1 between words. \n\n\n',self)
        about_label.setStyleSheet('color: white; font: 10px;')

        I2C_label = QLabel('The RPi can handle i2c communication on pins 3(SDA) and 5(SCL). \n ~There is a second i2c bus on the EEPROM lines but,\n   those should be reserved for the internal HAT. \n ~HAT config can be looked into as well.',self)
        I2C_label.setStyleSheet('color: white; font: 10px;')

        UART_label = QLabel('The RPi can handle UART communication on pins 8(TX) and 10(RX) \n ~To be implemented.',self)
        UART_label.setStyleSheet('color: white; font: 10px;')

        clockgen_label = QLabel('Pin 7 "GCLK" is capable of generating a square wave up to 125MHz. \n ~To be implemented.',self)
        clockgen_label.setStyleSheet('color: white; font: 10px;')

        self.scroll_layout.addWidget(spi_write_button,0,0,1,1)
        self.scroll_layout.addWidget(remove_button,1,0,1,1)
        self.scroll_layout.addWidget(self.hold_le,0,3,1,1)
        self.scroll_layout.addWidget(readback_all_button,1,5,1,1)

        self.scroll_layout.addWidget(mode_label,0,1,1,1)
        self.scroll_layout.addWidget(self.mode_box,0,2,1,1)
        self.scroll_layout.addWidget(self.speed,1,2,1,1)
        self.scroll_layout.addWidget(speed_label,1,1,1,1)
        self.scroll_layout.addWidget(generate_button,2,0,1,1)
        self.scroll_layout.addWidget(self.device_box,2,2,1,1)
        self.scroll_layout.addWidget(device_label,2,1,1,1)
        self.scroll_layout.addWidget(single_write_label,2,3,1,2)
        self.scroll_layout.addWidget(single_read_label,2,4,1,2)
        self.scroll_layout.addWidget(readback_label,2,5,1,1)

        self.scroll1_layout.addWidget(I2C_label,0,0,6,3)
        self.scroll2_layout.addWidget(UART_label,0,0,6,3)
        self.scroll3_layout.addWidget(clockgen_label,0,0,6,3)
        self.scroll4_layout.addWidget(about_label,0,0,6,3)

        layout.addWidget(load_button,pin_grid_start - 2, 0,1,2)
        layout.addWidget(save_button,pin_grid_start - 2, 2,1,2)
        layout.addWidget(apply_button,pin_grid_start - 2, 4,1,2)
        layout.addWidget(self.part_name,pin_grid_start - 1,0,1,6)

        main_layout.addWidget(self.grid_widget)
        main_layout.addWidget(tabs)
        self.generate()
        self.whitespace()
        #set GPIO for output and set all LOW at startup - uncomment on rpi
        
        for i in range(len(gpio_numbers)):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(gpio_numbers[i], GPIO.OUT)
            GPIO.output(gpio_numbers[i], 0)
        
        self.show()
    

    def load_part(self):
        global address_count
        global spi_address_sets
        global spi_message_sets
        global spi_label_sets
        global spi_reg_write_button_sets
        global spi_reg_read_button_sets
        global spi_reg_readback_sets
        global gpio_sets
        global gpio_labels

        name = self.part_name.text()
        if(name=='base'):
            self.part_name.setText('INVALID NAME')
        else:
            try:        
                df = pd.read_csv('part_config/%s.csv' % (name))
            except:
                self.part_name.setText('FILE NOT FOUND')
            else:

                for i in range(address_count): #if the load is possible we need to delete the currently created register locations
                    self.scroll_layout.removeWidget(spi_address_sets[i])
                    self.scroll_layout.removeWidget(spi_message_sets[i])
                    self.scroll_layout.removeWidget(spi_label_sets[i])
                    self.scroll_layout.removeWidget(spi_reg_write_button_sets[i])
                    self.scroll_layout.removeWidget(spi_reg_read_button_sets[i])
                    self.scroll_layout.removeWidget(spi_reg_readback_sets[i])


                address_count = int(df.loc[0].at['SPI_count'])
                #these need reset on a successful load otherwise we append onto already loaded arrays
                spi_address_sets = [] 
                spi_message_sets = []
                spi_label_sets = []
                spi_reg_write_button_sets = []   
                spi_reg_read_button_sets = []  
                spi_reg_readback_sets = [] 

                for i in range(len(gpio_sets)):
                    state = df.loc[i].at['GPIO_pins']
                    gpio_labels[i].setText('%s' % (df.loc[i].at['GPIO_names']))
                    if(state == 0): 
                        gpio_sets[i].setChecked(False)
                    if(state == 1): 
                        gpio_sets[i].setChecked(True)


                for i in range(address_count):

                    self.labelName = QLineEdit(self)
                    self.labelName.setText(str(df.loc[i,'SPI_Label']))
                    self.labelName.setFixedWidth(80)
                    self.labelName.setFixedHeight(30)
                    self.labelName.setStyleSheet('color: white; font: 10px;')
                    spi_label_sets.append(self.labelName)

                    self.address = QLineEdit(self)
                    self.address.setFixedWidth(80)
                    self.address.setFixedHeight(30)
                    self.address.setText(str(df.loc[i,'SPI_Address']))
                    self.address.setStyleSheet('background-color: white; color: black; font: 10px;')
                    spi_address_sets.append(self.address)

                    self.msg = QLineEdit(self)
                    self.msg.setFixedWidth(80)
                    self.msg.setFixedHeight(30)
                    self.msg.setText(str(df.loc[i,'SPI_Message']))
                    self.msg.setStyleSheet('background-color: white; color: black; font: 10px;')
                    spi_message_sets.append(self.msg)

                    self.spi_reg_write_button = QPushButton('Write',self)
                    self.spi_reg_write_button.clicked.connect(self.update)
                    self.spi_reg_write_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
                    spi_reg_write_button_sets.append(self.spi_reg_write_button)
                    self.spi_reg_write_button.setFixedWidth(80)
                    self.spi_reg_write_button.setFixedHeight(30)
                    self.spi_reg_write_button.clicked.connect(lambda _, j = i: self.single_spi_write(j))

                    self.spi_reg_read_button = QPushButton('Read',self)
                    self.spi_reg_read_button.clicked.connect(self.update)
                    self.spi_reg_read_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
                    spi_reg_read_button_sets.append(self.spi_reg_read_button)
                    self.spi_reg_read_button.setFixedWidth(80)
                    self.spi_reg_read_button.setFixedHeight(30)
                    self.spi_reg_read_button.clicked.connect(lambda _, j = i:self.single_spi_read(j))

                    
                    self.spi_reg_readback = QLineEdit(self)
                    self.spi_reg_readback.setText('')
                    self.spi_reg_readback.setFixedWidth(80)
                    self.spi_reg_readback.setFixedHeight(30)
                    self.spi_reg_readback.setStyleSheet('background-color: white; color: black; font: 10px;')
                    spi_reg_readback_sets.append(self.spi_reg_readback)

                    #add widget to layout
                    self.scroll_layout.addWidget(self.labelName,i + 3,0)
                    self.scroll_layout.addWidget(self.address,i + 3,1)
                    self.scroll_layout.addWidget(self.msg,i + 3,2)
                    self.scroll_layout.addWidget(self.spi_reg_write_button,i + 3,3)
                    self.scroll_layout.addWidget(self.spi_reg_read_button,i + 3,4)
                    self.scroll_layout.addWidget(self.spi_reg_readback,i + 3,5)
   

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
        global spi_label_sets
        global gpio_sets

        name = self.part_name.text()
        loc = 'part_config/%s.csv' % (name)
        if(name=='base'):
            self.part_name.setText('INVALID NAME')
        else:
            if(os.path.exists(loc)): os.remove(loc)                       
            shutil.copyfile('part_config/base.csv', loc)
            df = pd.read_csv(loc)

            for i in range(len(gpio_sets)):
                state = gpio_sets[i].isChecked()
                txt = gpio_labels[i].text()
                if(state == False): state = 0
                if(state == True): state = 1
                df.loc[i,'GPIO_pins'] = state
                df.loc[i,'GPIO_names'] = txt
                
                
            df.loc[0,'SPI_count'] = int(address_count)

            #print(address_count)
            for i in range(address_count):
                df.loc[i,'SPI_Label'] = str(spi_label_sets[i].text())
                df.loc[i,'SPI_Address'] = str(spi_address_sets[i].text())
                df.loc[i,'SPI_Message'] = str(spi_message_sets[i].text())

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

            df.to_csv(loc,index=False)



    #apply settings from loaded pins - uncomment for rpi
    
    def apply_pins(self):
        for i in range(len(self.gpio_names)):
            state = self.gpio_names[i].isChecked()   
            if(state == False): 
                GPIO.output(gpio_numbers[i], 0)
            if(state == True): 
                GPIO.output(gpio_numbers[i], 1)
    

    def generate(self):
        
        global spi_address_sets
        global spi_message_sets
        global spi_label_sets
        global address_count
        global spi_reg_readback_sets

        self.labelName = QLineEdit(self)
        self.labelName.setText("REG %s" % address_count)
        self.labelName.setFixedWidth(80)
        self.labelName.setFixedHeight(30)
        self.labelName.setStyleSheet('color: white; font: 10px;')

        self.address = QLineEdit(self)
        self.address.setFixedWidth(80)
        self.address.setFixedHeight(30)
        if(address_count == 0):
            self.address.setText('0xFF')
        else:
            self.address.setText(str(spi_address_sets[address_count - 1].text()))
        self.address.setStyleSheet('background-color: white; color: black; font: 10px;')

        self.msg = QLineEdit(self)
        self.msg.setFixedWidth(80)
        self.msg.setFixedHeight(30)
        if(address_count == 0):
            self.msg.setText('0xFF')
        else:
            self.msg.setText(str(spi_message_sets[address_count - 1].text()))
        self.msg.setStyleSheet('background-color: white; color: black; font: 10px;')
        
        spi_label_sets.append(self.labelName)
        spi_address_sets.append(self.address)
        spi_message_sets.append(self.msg)

        self.spi_reg_write_button = QPushButton('Write',self)
        self.spi_reg_write_button.clicked.connect(self.update)
        self.spi_reg_write_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
        self.spi_reg_write_button.setFixedWidth(80)
        self.spi_reg_write_button.setFixedHeight(30)
        spi_reg_write_button_sets.append(self.spi_reg_write_button)
        self.spi_reg_write_button.clicked.connect(lambda _, i = address_count: self.single_spi_write(i))

        self.spi_reg_read_button = QPushButton('Read',self)
        self.spi_reg_read_button.clicked.connect(self.update)
        self.spi_reg_read_button.setStyleSheet('color: black; background-color: rgb(255,255,0); font: bold 10px;')
        self.spi_reg_read_button.setFixedWidth(80)
        self.spi_reg_read_button.setFixedHeight(30)
        spi_reg_read_button_sets.append(self.spi_reg_read_button)
        self.spi_reg_read_button.clicked.connect(lambda _, i = address_count: self.single_spi_read(i))

        self.spi_reg_readback = QLineEdit(self)
        self.spi_reg_readback.setText('')
        self.spi_reg_readback.setFixedWidth(80)
        self.spi_reg_readback.setFixedHeight(30)
        self.spi_reg_readback.setStyleSheet('background-color: white; color: black; font: 10px;')

        #add widget to layout
        self.scroll_layout.addWidget(self.labelName,address_count + 3,0)
        self.scroll_layout.addWidget(self.address,address_count + 3,1)
        self.scroll_layout.addWidget(self.msg,address_count + 3,2)
        self.scroll_layout.addWidget(self.spi_reg_write_button,address_count + 3,3)
        self.scroll_layout.addWidget(self.spi_reg_read_button,address_count + 3,4) 
        self.scroll_layout.addWidget(self.spi_reg_readback,address_count + 3,5)


        spi_reg_readback_sets.append(self.spi_reg_readback)

        address_count = int(address_count) + int(1)

        self.whitespace()
                

    def whitespace(self):
        global address_count
        if(address_count < 0):
            pass
        else:
            for i in range(20 - address_count):
                self.spacerName = QLabel(self)
                self.spacerName.setFixedWidth(80)
                self.scroll_layout.addWidget(self.spacerName,address_count + 5 + i,0,1,3)

    def delete(self):
        global spi_address_sets
        global spi_message_sets
        global spi_label_sets
        global address_count
        global spi_reg_readback_sets
        global spi_reg_write_button_sets
        global spi_reg_read_button_sets
        
        index = address_count - 1
        
        if(address_count==1):
            print('cannot remove any more registers')#maybe add output console later?
        else:            
            self.scroll_layout.removeWidget(spi_address_sets[index])
            self.scroll_layout.removeWidget(spi_message_sets[index])
            self.scroll_layout.removeWidget(spi_label_sets[index])
            self.scroll_layout.removeWidget(spi_reg_read_button_sets[index])
            self.scroll_layout.removeWidget(spi_reg_write_button_sets[index])
            self.scroll_layout.removeWidget(spi_reg_readback_sets[index])
            
            spi_address_sets[index].setParent(None)
            spi_message_sets[index].setParent(None)
            spi_label_sets[index].setParent(None)
            spi_reg_read_button_sets[index].setParent(None)
            spi_reg_write_button_sets[index].setParent(None)
            spi_reg_readback_sets[index].setParent(None)
            
            del spi_address_sets[index]
            del spi_message_sets[index]
            del spi_label_sets[index]
            del spi_reg_read_button_sets[index]
            del spi_reg_write_button_sets[index]
            del spi_reg_readback_sets[index]
            
            address_count = address_count - 1
            

    def single_spi_write(self, spi_index):
        global spi_address_sets
        global spi_message_sets
        global address_count
        global spi_reg_write_button_sets
        
        print(spi_index)

        mode = int(self.mode_box.currentIndex())
        speed = int(self.speed.text())
        chip = int(self.device_box.currentIndex())

        
        spi = spidev.SpiDev()
        spi.open(0,chip)
        spi.max_speed_hz = speed
        spi.mode = mode
        
        spi_send = [] #Generate an empty array to handle what message we are sending
        msg = spi_address_sets[spi_index].text()
        for j in range(2,len(spi_address_sets[spi_index].text()) - 1,2):
            word = msg[j] + msg[j + 1]
            spi_send.append(int(word,16))

        msg = spi_message_sets[spi_index].text()
        for j in range(2,len(spi_message_sets[spi_index].text()) - 1,2):
            word = msg[j] + msg[j + 1]
            spi_send.append(int(word,16))

        spi.xfer3(spi_send)

        print('\n sent %s \n' % (spi_send))

        spi.close()
        
    
    def single_spi_read(self,spi_index):
        global spi_address_sets
        global spi_message_sets
        global spi_reg_readback_sets
        global address_count

        mode = int(self.mode_box.currentIndex())
        speed = int(self.speed.text())
        chip = int(self.device_box.currentIndex())
        
        spi = spidev.SpiDev()
        spi.open(0,chip)
        spi.max_speed_hz = speed
        spi.mode = mode
        
        spi_send = [] #Generate an empty array to handle what message we are sending
        msg = spi_address_sets[spi_index].text()
        for j in range(2,len(spi_address_sets[spi_index].text()) - 1,2):
            word = msg[j] + msg[j + 1]
            spi_send.append(int(word,16))

        msg = spi_message_sets[spi_index].text()
        for j in range(2,len(spi_message_sets[spi_index].text()) - 1,2):
            word = msg[j] + msg[j + 1]
            spi_send.append(int(word,16))

        readback = spi.xfer3(spi_send)
        readback_text = ''
        for i in range(len(readback)):
                readback_text = readback_text + str(readback[i]) + ','
        spi_reg_readback_sets[spi_index].setText('%s' % readback_text)

        print('\n read %s \n' % (spi_send))

        spi.close()
        

    def spi_read(self):
        global spi_address_sets
        global spi_message_sets
        global spi_reg_readback_sets
        global address_count

        mode = int(self.mode_box.currentIndex())
        speed = int(self.speed.text())
        chip = int(self.device_box.currentIndex())

        
        spi = spidev.SpiDev()
        spi.open(0,chip)
        spi.max_speed_hz = speed
        spi.mode = mode
        
        for i in range(address_count):
                spi_send = [] #Generate an empty array to handle what message we are sending
                msg = spi_address_sets[i].text()
                for j in range(2,len(spi_address_sets[i].text()) - 1,2):
                    word = msg[j] + msg[j + 1]
                    spi_send.append(int(word,16))

                msg = spi_message_sets[i].text()
                for j in range(2,len(spi_message_sets[i].text()) - 1,2):
                    ## using standard b1000 for first R/W identifier
                    if(j == 2):
                        word = '8' + msg[j + 1]
                    else:
                        word = msg[j] + msg[j + 1]
                        spi_send.append(int(word,16))

                
                readback = spi.xfer3(spi_send)
                print(readback)
                readback_text = ''
                for j in range(len(readback)):
                        readback_text = readback_text + str(readback[j]) + ','
                spi_reg_readback_sets[i].setText('%s' % readback_text)

        spi.close()
        


    def spi_write(self):
        global spi_address_sets
        global spi_message_sets
        global address_count

        mode = int(self.mode_box.currentIndex())
        speed = int(self.speed.text())
        chip = int(self.device_box.currentIndex())

        
        spi = spidev.SpiDev()
        spi.open(0,chip)
        spi.max_speed_hz = speed
        spi.mode = mode
        
        for i in range(address_count):
                spi_send = [] #Generate an empty array to handle what message we are sending
                msg = spi_address_sets[i].text()
                for j in range(2,len(spi_address_sets[i].text()) - 1,2):
                    word = msg[j] + msg[j + 1]
                    spi_send.append(int(word,16))

                msg = spi_message_sets[i].text()
                for j in range(2,len(spi_message_sets[i].text()) - 1,2):
                    word = msg[j] + msg[j + 1]
                    spi_send.append(int(word,16))
                spi.xfer3(spi_send)

                print('\n sent %s \n' % (spi_send))

        spi.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
