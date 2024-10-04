from sys import exit #biblioteca utilizada para acessar funcao "exit" que aborta o programa

try:
    import numpy as np #pip install numpy
except: 
    print("numpy não instalada")
    exit()

try:
    from tkinter import * #pip install tk
except: 
    print("tkinter não instalada")
    exit()

try:
    import cv2 #pip install opencv-python
except: 
    print("cv2 não instalada")
    exit()

try:
    import FormatArq as formatacao #biblioteca de autoria propria para acessar formatacoes e padroes de leitura para os arquivos exportados
except: 
    print("FormatArq não instalada")
    exit()

try:
    import Class
except: 
    print("numpy não instalada")
    exit()

try:
    import time
except: 
    print("time não instalada")
    exit()