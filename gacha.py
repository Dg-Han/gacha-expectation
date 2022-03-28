#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *

'''     
    if mode=='4' or 'collection':
        p=1/eval(print('请输入套装收藏品件数:'))
        r=eval(input("请输入重复收藏品兑换新收藏品的比例:"))
'''

class Ui(Frame):
    global step_model
    global file

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master.title('抽卡期望计算器')
        self.master.geometry('1280x720')

        mn=Menu(self.master)
        choosemn=Menu(mn,tearoff=False)
        choosemn.add_command(label='概率递增卡池',command=self.createWidgets_step)
        choosemn.add_command(label='固定概率卡池',command=self.createWidgets_fixed)
        mn.add_cascade(label='卡池类型选择',menu=choosemn)
        helpmn=Menu(mn,tearoff=False)
        helpmn.add_command(label='Q&A',command=self.show_help)
        helpmn.add_command(label='有关信息',command=self.show_info)
        mn.add_cascade(label='帮助',menu=helpmn)
        self.master.config(menu=mn)
        
        self.createWidgets_step()

    def show_help(self):
        with open('gacha_doc.txt','r',encoding='utf-8') as f:
            doc=f.read()
        
        hlp=Tk()
        hlp.title('使用说明和常见问题')
        hlp.geometry('720x480')
        txt=Text(hlp,width=700,height=480)
        txt.insert('1.0',doc)
        sb=Scrollbar(hlp)
        sb.pack(side='right',fill='y')
        txt.pack(side='left')
        sb.config(command=txt.yview)
        txt.config(yscrollcommand=sb.set,state='disabled')

        hlp.mainloop()

    def show_info(self):
        if 'Toplevel' in [widget.winfo_class() for widget in self.master.winfo_children()]:
            pass
        else:
            self.info=Toplevel()
            self.info.title('有关信息')
            self.info.geometry('320x240')
            self.info.lb1=Label(self.info,text='抽卡期望计算器')
            self.info.lb2=Label(self.info,text='当前版本: 0.1.5 (ver20220328)')
            self.info.lb3=Label(self.info,text='Copyright by Dg_Han. All Rights Reserved.')
            self.info.lb4=Label(self.info,text='github: https://github.com/Dg-Han')
            self.info.lb1.pack()
            self.info.lb2.pack()
            self.info.lb3.pack()
            self.info.lb4.pack()
            
    def createWidgets_step(self):
        for widget in self.master.winfo_children():
            if (widget.winfo_class()!='Frame')and(widget.winfo_class()!='Menu'):
                widget.destroy()

        self.cmb=ttk.Combobox(self.master, textvariable=mode, state='readonly')
        name_list=self.step_cmb_value()
        self.cmb['value']=name_list
        self.cmb.bind('<<ComboboxSelected>>', self.set_step_para)
        self.cmb.place(relx=0.7,rely=0.1,relwidth=0.1,relheight=0.05)
        self.cmb.set('')

        label_list=['最高稀有度出率','up占最高稀有度比例','up角色数量','触发概率递增机制抽数','必出抽数/每抽递增概率','大保底歪几必出,0为无大保底机制']

        for i in range(6):
            self.lb=Label(self.master,text=label_list[i])
            self.lb.place(relx=0.15*i+0.025,rely=0.225,relwidth=0.15,relheight=0.05)

        self.ety1=Entry(self.master)
        self.ety2=Entry(self.master)
        self.ety3=Entry(self.master)
        self.ety4=Entry(self.master)
        self.ety5=Entry(self.master)
        self.ety6=Entry(self.master)
        self.ety1.place(relx=0.05,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety2.place(relx=0.2,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety3.place(relx=0.35,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety4.place(relx=0.5,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety5.place(relx=0.65,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety6.place(relx=0.8,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety1.bind('<KeyRelease>',self.check_step)
        self.ety2.bind('<KeyRelease>',self.check_step)
        self.ety3.bind('<KeyRelease>',self.check_step)
        self.ety4.bind('<KeyRelease>',self.check_step)
        self.ety5.bind('<KeyRelease>',self.check_step)
        self.ety6.bind('<KeyRelease>',self.check_step)

        self.lb7=Label(self.master,text='总抽数')
        self.lb8=Label(self.master,text='期望结果\n多up角色数量间用逗号分隔')
        self.lb7.place(relx=0.2,rely=0.4,relwidth=0.1,relheight=0.05)
        self.lb8.place(relx=0.35,rely=0.4,relwidth=0.2,relheight=0.05)
        self.ety7=Entry(self.master)
        self.ety8=Entry(self.master)
        self.ety7.place(relx=0.2,rely=0.475,relwidth=0.1,relheight=0.05)
        self.ety8.place(relx=0.4,rely=0.475,relwidth=0.1,relheight=0.05)
        self.ety7.bind('<KeyRelease>',self.check_step)
        self.ety8.bind('<FocusOut>',self.test)

        self.btn1=Button(self.master,text='计算',command=lambda: self.step_output())
        self.btn1.place(relx=0.7,rely=0.45,relwidth=0.2,relheight=0.1)
        self.btn2=Button(self.master,text='保存模板',command=lambda: self.save_step_model())
        self.btn2.place(relx=0.85,rely=0.05,relwidth=0.1,relheight=0.05)
        self.btn3=Button(self.master,text='删除模板',command=lambda: self.delete_step_model())
        self.btn3.place(relx=0.85,rely=0.15,relwidth=0.1,relheight=0.05)

        self.lb9=Label(self.master,text='')
        self.lb9.place(relx=0.25,rely=0.7,relwidth=0.5,relheight=0.1)
        
    def set_step_para(self,event):
        self.ety1.config(state='normal')
        self.ety2.config(state='normal')
        self.ety3.config(state='normal')
        self.ety4.config(state='normal')
        self.ety5.config(state='normal')
        self.ety6.config(state='normal')
        self.ety7.config(state='normal')
        self.ety8.config(state='normal')
        self.ety1.delete(0,END)
        self.ety2.delete(0,END)
        self.ety3.delete(0,END)
        self.ety4.delete(0,END)
        self.ety5.delete(0,END)
        self.ety6.delete(0,END)
        self.ety7.delete(0,END)
        self.ety8.delete(0,END)
        
        m=mode.get()
        if m in step_model.keys():
            self.ety1.insert(END,str(step_model[m][0]))
            self.ety1.config(state='readonly')
            self.ety2.insert(END,str(step_model[m][1]))
            self.ety2.config(state='readonly')
            self.ety3.insert(END,str(step_model[m][2]))
            self.ety3.config(state='readonly')
            self.ety4.insert(END,str(step_model[m][3]))
            self.ety4.config(state='readonly')
            self.ety5.insert(END,str(step_model[m][4]))
            self.ety5.config(state='readonly')
            self.ety6.insert(END,str(step_model[m][5]))
            self.ety6.config(state='readonly')
            self.cmb.config(state='readonly')
        else:
            self.cmb.config(state='normal')

    def step_output(self):
        try:
            p=eval(self.ety1.get())
            p_up=eval(self.ety2.get())
            ups=eval(self.ety3.get())
            thres=eval(self.ety4.get())
            most=eval(self.ety5.get())
            mg=eval(self.ety6.get())
            n=eval(self.ety7.get())
            e=[0]
            for c in self.ety8.get():
                if (48<=ord(c)<=57):
                    e[-1]=10*e[-1]+eval(c)
                elif c==',':
                    e.append(0)
            #print(p,p_up,ups,thres,most,mg,n,e)
            self.lb9.config(text='达到预期抽卡结果的概率是 %.2f %%'%(100*step(p,p_up,ups,thres,most,mg).smlt(n,e)))
        except:
            showerror('Error','期望目标格式错误！')

    def check_step(self,event):
        if self.ety1.get():
            try:
                if eval(self.ety1.get())>1:
                    showwarning('Warning','请输入0-1之间的数')
                    self.ety1.delete(0,END)
            except:
                showwarning('Warning','数据类型错误！请输入0-1之间的数')
                self.ety1.delete(len(self.ety1.get())-1,END)
        if self.ety2.get():
            try:
                if eval(self.ety2.get())>1:
                    showwarning('Warning','请输入0-1之间的数')
                    self.ety2.delete(0,END)
            except:
                showwarning('Warning','数据类型错误！请输入0-1之间的数')
                self.ety2.delete(len(self.ety2.get())-1,END)
        if self.ety3.get():
            if not self.ety3.get()[-1].isnumeric():
                showwarning('Warning','请输入整数！')
                self.ety3.delete(len(self.ety3.get())-1,END)
        if self.ety4.get():
            if not self.ety4.get()[-1].isnumeric():
                showwarning('Warning','请输入整数！')
                self.ety4.delete(len(self.ety4.get())-1,END)
        if self.ety5.get():
            try:
                eval(self.ety5.get())
            except:
                showwarning('Warning','数据类型错误！请输入数字')
                self.ety5.delete(len(self.ety5.get())-1,END)
        if self.ety6.get():
            if not self.ety6.get()[-1].isnumeric():
                showwarning('Warning','请输入整数！')
                self.ety6.delete(len(self.ety6.get())-1,END)
        if self.ety7.get():
            if not self.ety7.get()[-1].isnumeric():
                showwarning('Warning','请输入整数！')
                self.ety7.delete(len(self.ety7.get())-1,END)

    def test(self,event):
        try:
            cache=self.ety8.get().split(',')
            if len(cache)==eval(self.ety3.get()):
                for item in cache:
                    try:
                        eval(item)
                    except:
                        showerror('Error','请输入数字！')
            else:
                showwarning('Warning','输入期望数量与up角色数量不符！')
        except:
            showerror('Error','输入期望角色数量格式错误！')

    def save_step_model(self):
        if self.cmb.get() in step_model.keys():
            showwarning('Warning','保存模板名称与已有模板重复！')
        else:
            if self.cmb.get() and self.ety1.get() and self.ety2.get() and self.ety3.get() and self.ety4.get() and self.ety5.get() and self.ety6.get():
                with open(file,'a',encoding='utf-8') as f:
                    f.write(','.join(['step',self.cmb.get(),
                                      self.ety1.get(),
                                      self.ety2.get(),
                                      self.ety3.get(),
                                      self.ety4.get(),
                                      self.ety5.get(),
                                      self.ety6.get()]))
                    f.write('\n')
                step_model[self.cmb.get()]=[self.ety1.get(),self.ety2.get(),self.ety3.get(),self.ety4.get(),self.ety5.get(),self.ety6.get()]
                
                name_list=self.step_cmb_value()
                self.cmb['value']=name_list
                self.cmb.current(len(name_list)-2)
                self.set_step_para(None)
            else:
                showwarning('Warning','存在卡池参数值为空！')

    def delete_step_model(self):
        if self.cmb.get() not in step_model.keys():
            showerror('Error','无已有模板！')
        elif self.cmb.get() in ['原神','明日方舟单up','明日方舟双up']:
            showwarning('Warning','初始模板不可删除！')
        else:                                               #self.cmb.get() in step_model.keys()
            with open(file,'r',encoding='utf-8') as f:
                lines=f.readlines()
            with open(file,'w',encoding='utf-8') as f:
                for line in lines:
                    if self.cmb.get() not in line:
                        f.write(line)
            del step_model[self.cmb.get()]

            name_list=self.step_cmb_value()
            self.cmb['value']=name_list
            self.cmb.set('')
            self.set_step_para(None)
            
    def step_cmb_value(self):
        global step_model
        
        cache=[item for item in step_model.keys()]
        cache.append('自定义')
        name_list=tuple(cache)
        return name_list

    def createWidgets_fixed(self):
        for widget in self.master.winfo_children():
            if (widget.winfo_class()!='Frame')and(widget.winfo_class()!='Menu'):
                widget.destroy()

        self.cmb=ttk.Combobox(self.master, textvariable=mode, state='readonly')
        name_list=self.fixed_cmb_value()
        self.cmb['value']=name_list
        self.cmb.bind('<<ComboboxSelected>>', self.set_fixed_para)
        self.cmb.place(relx=0.7,rely=0.1,relwidth=0.1,relheight=0.05)
        self.cmb.set('')

        self.lb1=Label(self.master,text='最高稀有度出率')
        self.lb2=Label(self.master,text='up占最高稀有度比例')
        self.lb3=Label(self.master,text='保底抽数,0为无保底机制')
        self.lb1.place(relx=0.1,rely=0.2,relwidth=0.1,relheight=0.05)
        self.lb2.place(relx=0.3,rely=0.2,relwidth=0.1,relheight=0.05)
        self.lb3.place(relx=0.5,rely=0.2,relwidth=0.1,relheight=0.05)

        self.ety1=Entry(self.master)
        self.ety2=Entry(self.master)
        self.ety3=Entry(self.master)
        self.ety1.place(relx=0.1,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety2.place(relx=0.3,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety3.place(relx=0.5,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety1.bind('KeyRelease',self.check_fixed)
        self.ety2.bind('KeyRelease',self.check_fixed)
        self.ety3.bind('KeyRelease',self.check_fixed)

        self.lb4=Label(self.master,text='总抽数')
        self.lb5=Label(self.master,text='期望结果')
        self.lb4.place(relx=0.2,rely=0.4,relwidth=0.1,relheight=0.05)
        self.lb5.place(relx=0.4,rely=0.4,relwidth=0.1,relheight=0.05)
        self.ety4=Entry(self.master)
        self.ety5=Entry(self.master)
        self.ety4.place(relx=0.2,rely=0.5,relwidth=0.1,relheight=0.05)
        self.ety5.place(relx=0.4,rely=0.5,relwidth=0.1,relheight=0.05)
        self.ety4.bind('KeyRelease',self.check_fixed)
        self.ety5.bind('KeyRelease',self.check_fixed)

        self.lb6=Label(self.master,text='')
        self.lb6.place(relx=0.25,rely=0.7,relwidth=0.5,relheight=0.1)

        self.btn1=Button(self.master,text='计算',command=lambda: self.fixed_output())
        self.btn1.place(relx=0.7,rely=0.45,relwidth=0.2,relheight=0.1)

    def set_fixed_para(self,event):
        self.ety1.config(state='normal')
        self.ety2.config(state='normal')
        self.ety3.config(state='normal')

        self.ety1.delete(0,END)
        self.ety2.delete(0,END)
        self.ety3.delete(0,END)

        m=mode.get()
        if m in fixed_model.keys():
            self.ety1.insert(END,str(fixed_model[m][0]))
            self.ety1.config(state='readonly')
            self.ety2.insert(END,str(fixed_model[m][1]))
            self.ety2.config(state='readonly')
            self.ety3.insert(END,str(fixed_model[m][2]))
            self.ety3.config(state='readonly')
            self.cmb.config(state='readonly')
        else:
            self.cmb.config(state='normal')

    def check_fixed(self,event):
        if self.ety1.get():
            try:
                if eval(self.ety1.get())>1:
                    showwarning('Warning','请输入0-1之间的数')
                    self.ety1.delete(0,END)
            except:
                showwarning('Warning','数据类型错误！请输入0-1之间的数')
                self.ety1.delete(len(self.ety1.get())-1,END)
        if self.ety2.get():
            try:
                if eval(self.ety2.get())>1:
                    showwarning('Warning','请输入0-1之间的数')
                    self.ety2.delete(0,END)
            except:
                showwarning('Warning','数据类型错误！请输入0-1之间的数')
                self.ety2.delete(len(self.ety2.get())-1,END)
        if self.ety3.get():
            if not self.ety3.get()[-1].isnumeric():
                showwarning('Warning','请输入整数！')
                self.ety3.delete(len(self.ety3.get())-1,END)
        if self.ety4.get():
            if not self.ety4.get()[-1].isnumeric():
                showwarning('Warning','请输入整数！')
                self.ety4.delete(len(self.ety3.get())-1,END)
        if self.ety5.get():
            if not self.ety5.get()[-1].isnumeric():
                showwarning('Warning','请输入整数！')
                self.ety5.delete(len(self.ety3.get())-1,END)

    def fixed_output(self):
        try:
            p=eval(self.ety1.get())
            p_up=eval(self.ety2.get())
            most=eval(self.ety3.get())
            n=eval(self.ety4.get())
            e=eval(self.ety5.get())
            self.lb6.config(text='达到预期抽卡结果的概率是 %.2f %%'%(100*fixed(p,p_up,most).prob(n,e)))
        except:
            showerror('Error','存在参数值输入错误！')

    def fixed_cmb_value(self):
        global fixed_model
        
        cache=[item for item in fixed_model.keys()]
        cache.append('自定义')
        name_list=tuple(cache)
        return name_list

def prob_ys(n):
    if n<=73:
        return 0.006
    else:
        return 0.994*(n-73)/17+0.006

def prob_mrfz(n):
    if n<=50:
        return 0.02
    else:
        return 0.02*n-0.98                          #0.02*(n-50)+0.02

class step():
    def __init__(self,p,p_up,ups,thres,most,mg,*args,**kwargs):
        '''
        p:最高稀有度出率
        p_up:up占最高稀有度比例
        ups:up角色数量
        thres:触发保底机制下限
        most:必出抽数
        mg:大保底歪几必出 (minimum guarantee); 0为无大保底机制
        '''
        step.p=p
        step.p_up=p_up
        step.ups=ups
        step.thres=thres
        step.mg=mg
        if most>1:
            step.most=most
        else:
            step.most=round(thres+(1-p)/most)

    def prob(self,n):
        if n<self.thres:
            return self.p
        else:
            return (1-self.p)*(n-self.thres)/(self.most-self.thres)+self.p

    def smlt(self,n,e,times=100000):
        '''
        n为总抽数
        e为期望抽卡结果（数组形式表示）
        times为重复模拟次数
        '''
        s=0
        up=dict()
        for i in range(times):                              #新狗哥入场
            insur=0                                         #非酋计数器（大保底计数器）
            turn=0                                          #小保底计数器
            count=[0 for i in range(self.ups)]              #up计数器
            for j in range(n):
                turn+=1
                pt=self.prob(turn)
                cache=random.random()                       #抽卡！
                if cache<pt:                                #抽中五星
                    mg_b=True
                    for k in range(self.ups):
                        if k<=cache*self.ups/pt/self.p_up<(k+1):
                            count[k]+=1
                            insur=0
                            mg_b=False
                            break
                    if self.mg and mg_b:
                        if insur==self.mg:                  #非酋的强运！（大保底）
                            for k in range(self.ups):
                                if (k+(self.ups-k)*self.p_up)<=cache*self.ups/pt<(k+1+(self.ups-k-1)*self.p_up):
                                    count[k]+=1
                                    break
                            insur=0                         #大保底重置
                        else:
                            insur+=1                        #非酋复活甲（大保底激活）
                            s+=1                            #歪计数器+1                          
                    turn=0                                  #新轮回开始（保底计数器清零）
            count=tuple(count)
            up[count]=up.get(count,0)+1
        result=times

        for key in up.keys():
            for i in range(len(key)):
                if key[i]<e[i]:
                    result-=up[key]
                    break
        
        return eval('%.4f'%(result/times))

    def output_list(self,up):
        for i in sorted(up.keys()):
            print(i,up[i])

class fixed():
    def __init__(self,p,p_up,most,*args,**kwargs):
        '''
        p:最高稀有度出率
        p_up:up角色出率
        most:保底抽数, 0为无保底机制
        '''
        self.p=p
        self.p_up=p_up
        self.most=most

    def smlt(self,n,e,times):
        s=0
        up=dict()
        for i in range(times):
            count=0
            c=0
            turn=0
            for j in range(n):
                turn+=1
                cache=random.random()
                if cache<self.p:
                    if cache<self.p_up:
                        count+=1
                    else:
                        s+=1
            up[count]=up.get(count,0)+1
        for i in range(e):
            result-=up.get(i,0)
        return eval('%.4f'%(result/times))

    def prob(self,n,e):
        if self.most and (n>=e*self.most):
            return 0
        else:
            p=1
            for i in range(e-math.floor(n/self.most)):
                p-=((1-self.p_up)**(n-i))*(self.p_up**i)*math.comb(n,i)
            return p

def ct(text,Default=True):
    cache=input(text+'(Y/N):')
    if (cache=='Y') or (cache=='y') or (not cache and Default):
        return True
    elif (cache=='N') or (cache=='n') or (not cache and not Default):
        return False
    else:
        ct(text,Default)

def check_input(text,require=''):                       #酒馆防爆机制（输入合法性检查）
    '''
    'N':自然数
    'p':0-1
    '''
    cache=input(text)
    if require:
        if require=='N':
            try:
                if (eval(cache)==int(eval(cache))) and (eval(cache)>=0):
                    return eval(cache)
                else:
                    print('请输入自然数！')
                    return check_input(text,require)
            except:
                print('数据格式错误！请输入自然数！')
                return check_input(text,require)
        if require=='p':
            try:
                if 0<=eval(cache)<=1:
                    return eval(cache)
                else:
                    print('请输入0-1之间的数！')
                    return check_input(text,require)
            except:
                print('数据格式错误！请输入0-1之间的数！')
                return check_input(text,require)
    else:
        try:
            return eval(cache)
        except:
            return cache

if __name__=="__main__":
    step_model={'原神':[0.006,0.5,1,73,90,1],
                '明日方舟单up':[0.02,0.5,1,50,0.02,0],
                '明日方舟双up':[0.02,0.7,2,50,0.02,0]
                }

    fixed_model={'PCR':[0.025,0.006,300],
                 'blhx':[0.07,0.02,200]
                 }
    
    file="gacha_data.dll"

    try:
        with open(file,'r',encoding='utf-8') as f:
            lines=f.readlines()
        for line in lines:
            cache=line.split(',')
            if cache[0]=='step':
                step_model[cache[1]]=cache[2:]
            elif cache[0]=='fixed':
                fixed_model[cache[1]]=cache[2:]
    except:
        pass
    
    top=Tk()
    mode=StringVar()
    Ui(top).mainloop()

'''
p_ys=[]
ys=step(0.006,0.5,1,73,90,1)
for i in range(360):
    p_ys.append(ys(i).smlt(n,[2],100000))
    print('%3d %.5f'%(i,p_ys[-1]))
print(p_ys)

p_mrfz=[]
mrfz2=step(0.02,0.7,2,50,99,0)
for i in range(1,401):
    p_mrfz.append(mrfz2.smlt(i,[1,1]))
    print('%3d %.5f'%p_mrfz[-1])
print(p_mrfz)
'''
