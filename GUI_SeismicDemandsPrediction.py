# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 21:44:21 2020

@author: USER
"""

import PySimpleGUI as sg
import numpy as np
from pickle import load

# ADD TITLE COLOUR ,title_color='white'
sg.theme('DefaultNoMoreNagging')	# Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Developed by Hoang D. Nguyen, and Myoungsu Shin')],
            [sg.Text('Ulsan National Institute of Science and Technology (UNIST)')],
            [sg.Text('Ulsan, South Korea')],
            [sg.Text('Email: nguyenhoangkt712@unist.ac.kr')],
            #[sg.Text('Input parameters')],
              
            [sg.Frame(layout=[
            [sg.Text('PGA - Peak ground acceleration (g)',size=(28, 1)),sg.InputText(key='-f1-',size=(30, 1))],
            [sg.Text('S1s - Spectral acceleration at 1 s (g)',size=(28, 1)),sg.InputText(key='-f2-',size=(30, 1))],
            [sg.Text('S2s - Spectral acceleration at 2 s (g)',size=(28, 1)), sg.InputText(key='-f3-',size=(30, 1))],
            [sg.Text('S3s - Spectral acceleration at 3 s (g)',size=(28, 1)), sg.InputText(key='-f4-',size=(30, 1))],
            [sg.Text('Tm1 - First natural period (s)',size=(28, 1)), sg.InputText(key='-f5-',size=(30, 1))],
            [sg.Text('Tm2 - Second natural period (s)',size=(28, 1)), sg.InputText(key='-f6-',size=(30, 1))],
            [sg.Text('Tm3 - Third natural period (s)',size=(28, 1)),sg.InputText(key='-f7-',size=(30, 1))]],title='Input variables')],
            [sg.Frame(layout=[   
            [sg.Text('Maximum top drift (%)',size=(28, 1)), sg.InputText(key='-OP1-',size=(30, 1))],
            [sg.Text('peak floor acceleration (g)',size=(28, 1)), sg.InputText(key='-OP2-',size=(30, 1))]],title='Output variables')],
            [sg.Button('Predict'),sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Predicting Seismic Demands of Steel Moment Frames', layout)


filename = 'BestModel_XGB.sav'
loaded_model = load(open(filename, 'rb'))

filename1 = 'BestModel_GBRT.sav'
loaded_model1 = load(open(filename1, 'rb'))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    #window['-OP-'].update('Please fill all the input parameters')
    if event == 'Predict':
        #window['-OP-'].update(values[0])
        #break
        if values['-f1-'] == '' or values['-f2-'] == '' or values['-f3-'] == '' or values['-f4-'] == '' or values['-f5-'] == '' or values['-f6-'] == '' or values['-f7-'] == '':

            window['-OP1-'].update('Please fill all the input variables')
            window['-OP2-'].update('Please fill all the input variables')
        else:

            x_test=np.array([[float(values['-f1-']),float(values['-f2-']), float(values['-f3-']),float(values['-f4-']),float(values['-f5-']),values['-f6-'],values['-f7-']]])
            
            y_pred_disp = loaded_model.predict(x_test)
            window['-OP1-'].update(np.round((y_pred_disp[0]*100),4))
            
            y_pred_acc = loaded_model1.predict(x_test)
            window['-OP2-'].update(np.round((y_pred_acc[0])/9.81,4))    
window.close()
