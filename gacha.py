#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk

from gacha_UI import Ui

if __name__=="__main__":
    step_model={'原神':[0.006,0.5,1,73,90,1],
                '明日方舟单up':[0.02,0.5,1,50,0.02,0],
                '明日方舟双up':[0.02,0.7,2,50,0.02,300],
                'PCR':[0.025,[0.006],0,0,0,300],
                'blhx':[0.07,[0.02],0,0,0,200]
                }
    
    file="gacha_data.dll"

    try:
        with open(file,'r',encoding='utf-8') as f:
            lines=f.readlines()
        for line in lines:
            cache=line[:-1].split(',')
            step_model[cache[0]]=cache[1:]
    except:
        pass
    
    top=tk.Tk()
    mode=tk.StringVar()
    Ivar1=tk.IntVar()
    Ivar2=tk.IntVar()
    Ivar3=tk.IntVar()
    Ui(top,mode=mode,I1=Ivar1,I2=Ivar2,I3=Ivar3,step_model=step_model).mainloop()
