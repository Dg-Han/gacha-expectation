#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *

class Ui(Frame):
    global step_model
    global fixed_model
    global mode
    global file

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master.title('抽卡期望计算器')
        self.master.geometry('1280x720')

        mn=Menu(self.master)
        choosemn=Menu(mn,tearoff=False)
        choosemn.add_command(label='概率递增卡池',command=self.createWidgets_step)
        choosemn.add_command(label='固定概率卡池',command=self.createWidgets_fixed)
        choosemn.add_command(label='收藏品',command=self.createWidgets_collection)
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
            self.info.lb2=Label(self.info,text='当前版本: 1.0.1 (ver20220512)')
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

        label_list=['最高稀有度出率','up占最高稀有度比例','up角色数量','触发概率递增机制抽数','必出抽数/每抽递增概率','大保底歪几必出\n0为无大保底机制']

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
        self.lb7.place(relx=0.1,rely=0.4,relwidth=0.1,relheight=0.05)
        self.lb8.place(relx=0.25,rely=0.4,relwidth=0.2,relheight=0.05)
        self.lb9=Label(self.master,text='期望结果概率\n默认为95%')
        self.lb9.place(relx=0.5,rely=0.4,relwidth=0.1,relheight=0.05)
        self.ety7=Entry(self.master)
        self.ety8=Entry(self.master)
        self.ety9=Entry(self.master)
        self.ety7.place(relx=0.1,rely=0.475,relwidth=0.1,relheight=0.05)
        self.ety8.place(relx=0.3,rely=0.475,relwidth=0.1,relheight=0.05)
        self.ety9.place(relx=0.5,rely=0.475,relwidth=0.1,relheight=0.05)
        self.ety7.bind('<KeyRelease>',self.check_step)
        self.ety8.bind('<FocusOut>',self.test)
        self.ety9.bind('<FocusOut>',self.check_step)

        self.btn1=Button(self.master,text='计算',command=lambda: self.step_output())
        self.btn1.place(relx=0.7,rely=0.45,relwidth=0.2,relheight=0.1)
        self.btn1.bind('<Return>',lambda: self.step_output())
        self.btn2=Button(self.master,text='保存模板',command=lambda: self.save_step_model())
        self.btn2.place(relx=0.85,rely=0.05,relwidth=0.1,relheight=0.05)
        self.btn3=Button(self.master,text='删除模板',command=lambda: self.delete_step_model())
        self.btn3.place(relx=0.85,rely=0.15,relwidth=0.1,relheight=0.05)

        self.lb10=Label(self.master,text='')
        self.lb10.place(relx=0.25,rely=0.7,relwidth=0.5,relheight=0.1)
        
    def set_step_para(self,event=None):
        self.ety1.config(state='normal')
        self.ety2.config(state='normal')
        self.ety3.config(state='normal')
        self.ety4.config(state='normal')
        self.ety5.config(state='normal')
        self.ety6.config(state='normal')
        self.ety1.delete(0,END)
        self.ety2.delete(0,END)
        self.ety3.delete(0,END)
        self.ety4.delete(0,END)
        self.ety5.delete(0,END)
        self.ety6.delete(0,END)
        self.ety7.delete(0,END)
        self.ety8.delete(0,END)
        self.ety9.delete(0,END)
        
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
        global up
        global up_result
        '''
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
        if self.ety9.get():
            target=eval(self.ety9.get()) if eval(self.ety9.get())<=1 else eval(self.ety9.get())/100
        else:
            target=0.95
        
        if ups==1:
            result=step(p,p_up,ups,thres,most,mg).calc(n,e,None)
            #nx=step(p,p_up,ups,thres,most,mg).interplt(e,target)
            lower=0
            upper=sum(e)*int((most if most>1 else thres+round((1-p)/most))/p_up)
            fdis=upper-lower
            while True:
                n=int(lower+(upper-lower)*(target+0.5)/2)
                p1=step(p,p_up,ups,thres,most,mg).calc(n,e)
                p2=step(p,p_up,ups,thres,most,mg).calc(n+1,e)
                if p1<target<=p2:
                    nx=n+1
                    break
                elif p2<target:
                    lower=n
                    self.lb10.config(text='计算中... 计算进度 %.2f %%'%(100*(1-(upper-lower)/fdis)))
                    self.update()
                else:
                    upper=n
                    self.lb10.config(text='计算中... 计算进度 %.2f %%'%(100*(1-(upper-lower)/fdis)))
                    self.update()
                
            self.lb10.config(text='达到预期抽卡结果的概率是 %.2f %%\n达到 %d%% 出率的所需抽数为 %d'%(100*result,int(100*target),nx))
        else:
            self.lb10.config(text='达到预期抽卡结果的概率是 %.2f %%'%(100*step(p,p_up,ups,thres,most,mg).smlt(n,e)))
        '''
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
                elif c not in [' ']:
                    raise TypeError
            #print(p,p_up,ups,thres,most,mg,n,e)
            if self.ety9.get():
                target=eval(self.ety9.get()) if eval(self.ety9.get())<=1 else eval(self.ety9.get())/100
            else:
                target=0.95
            
            if ups==1:
                para_set=step(p,p_up,ups,thres,most,mg)
                result=para_set.calc(n,e)
                self.lb10.config(text='计算中... 计算进度 %.2f %%'%(10+10*random.random()))
                self.update()
                #nx=step(p,p_up,ups,thres,most,mg).interplt(e,target)
                lower=0
                upper=sum(e)*int((most if most>1 else thres+round((1-p)/most))/p_up)
                fdis=upper-lower
                while True:
                    n=int(lower+(upper-lower)*(target+0.5)/2)
                    p1=para_set.calc(n,e)
                    p2=para_set.calc(n+1,e)
                    #print(lower,upper,n,p1,p2)
                    if p1<target<=p2:
                        nx=n+1
                        break
                    elif p2<target:
                        lower=n
                        self.lb10.config(text='计算中... 计算进度 %.2f %%'%(100*(1-(upper-lower)/fdis)))
                        self.update()
                    else:
                        upper=n
                        self.lb10.config(text='计算中... 计算进度 %.2f %%'%(100*(1-(upper-lower)/fdis)))
                        self.update()
                    
                self.lb10.config(text='达到预期抽卡结果的概率是 %.2f %%\n达到 %d%% 出率的所需抽数为 %d'%(100*result,int(100*target),nx))
            else:
                self.lb10.config(text='达到预期抽卡结果的概率是 %.2f %%'%(100*step(p,p_up,ups,thres,most,mg).smlt(n,e)))
        except SyntaxError:
            showerror('Error','存在参数值为空！')
        except TypeError:
            showerror('Error','期望结果输入格式错误！')

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
                showwarning('Warning','4请输入数字！')
                self.ety4.delete(len(self.ety4.get())-1,END)
        if self.ety5.get():
            try:
                eval(self.ety5.get())
            except:
                showwarning('Warning','数据类型错误！请输入数字')
                self.ety5.delete(len(self.ety5.get())-1,END)
        if self.ety6.get():
            if not self.ety6.get()[-1].isnumeric():
                showwarning('Warning','6请输入整数！')
                self.ety6.delete(len(self.ety6.get())-1,END)
        if self.ety7.get():
            if not self.ety7.get()[-1].isnumeric():
                showwarning('Warning','7请输入整数！')
                self.ety7.delete(len(self.ety7.get())-1,END)
        if self.ety9.get():
            try:
                if eval(self.ety9.get())>100 or eval(self.ety9.get())<0:
                    showwarning('Warning','请输入百分比或概率！')
                    self.ety9.delete(0,END)
            except:
                showerror('Error','数据类型错误！请输入百分比或概率')
                self.ety9.delete(0,END)

    def test(self,event):
        try:
            if self.ety8.get():
                list=input2nlist(self.ety8.get())
                if len(list)!=eval(self.ety3.get()):
                    showwarning('Warning','输入期望数量与up角色数量不符！')
        except:
            pass

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
                self.set_step_para()
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
            self.set_step_para()
            
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
        self.lb2=Label(self.master,text='up角色出率')
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
        self.ety1.bind('<KeyRelease>',self.check_fixed)
        self.ety2.bind('<KeyRelease>',self.check_fixed)
        self.ety3.bind('<KeyRelease>',self.check_fixed)

        self.lb4=Label(self.master,text='总抽数')
        self.lb5=Label(self.master,text='期望结果')
        self.lb4.place(relx=0.2,rely=0.4,relwidth=0.1,relheight=0.05)
        self.lb5.place(relx=0.4,rely=0.4,relwidth=0.1,relheight=0.05)
        self.ety4=Entry(self.master)
        self.ety5=Entry(self.master)
        self.ety4.place(relx=0.2,rely=0.5,relwidth=0.1,relheight=0.05)
        self.ety5.place(relx=0.4,rely=0.5,relwidth=0.1,relheight=0.05)
        self.ety4.bind('<KeyRelease>',self.check_fixed)
        self.ety5.bind('<KeyRelease>',self.check_fixed)

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

    def createWidgets_collection(self):
        for widget in self.master.winfo_children():
            if (widget.winfo_class()!='Frame')and(widget.winfo_class()!='Menu'):
                widget.destroy()

        self.lb1=Label(self.master,text='收藏品总数')
        self.lb2=Label(self.master,text='收藏品获得概率')
        self.lb3=Label(self.master,text='兑换new所需token')
        self.lb4=Label(self.master,text='重复收藏品获得token')
        self.lb1.place(relx=0.1,rely=0.2,relwidth=0.1,relheight=0.05)
        self.lb2.place(relx=0.3,rely=0.2,relwidth=0.1,relheight=0.05)
        self.lb3.place(relx=0.5,rely=0.2,relwidth=0.1,relheight=0.05)
        self.lb4.place(relx=0.7,rely=0.2,relwidth=0.1,relheight=0.05)

        self.ety1=Entry(self.master)
        self.ety2=Entry(self.master)
        self.ety3=Entry(self.master)
        self.ety4=Entry(self.master)
        self.ety1.place(relx=0.1,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety2.place(relx=0.3,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety3.place(relx=0.5,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety4.place(relx=0.7,rely=0.3,relwidth=0.1,relheight=0.05)
        self.ety1.bind('<FocusOut>',self.check_collection)
        self.ety2.bind('<FocusOut>',self.check_collection)
        self.ety3.bind('<FocusOut>',self.check_collection)
        self.ety4.bind('<FocusOut>',self.check_collection)

        self.lb5=Label(self.master,text='总抽数')
        self.lb6=Label(self.master,text='已有收藏品情况')
        self.lb7=Label(self.master,text='重复收藏品情况/token数量')
        self.lb5.place(relx=0.1,rely=0.4,relwidth=0.1,relheight=0.05)
        self.lb6.place(relx=0.3,rely=0.4,relwidth=0.1,relheight=0.05)
        self.lb7.place(relx=0.45,rely=0.4,relwidth=0.2,relheight=0.05)

        self.ety5=Entry(self.master)
        self.ety6=Entry(self.master)
        self.ety7=Entry(self.master)
        self.ety5.place(relx=0.1,rely=0.5,relwidth=0.1,relheight=0.05)
        self.ety6.place(relx=0.3,rely=0.5,relwidth=0.1,relheight=0.05)
        self.ety7.place(relx=0.5,rely=0.5,relwidth=0.1,relheight=0.05)
        self.ety5.bind('<FocusOut>',self.check_collection)
        self.ety6.bind('<FocusOut>',self.check_collection)
        self.ety7.bind('<FocusOut>',self.check_collection)

        self.lb8=Label(self.master,text='')
        self.lb8.place(relx=0.25,rely=0.7,relwidth=0.5,relheight=0.1)

        self.btn1=Button(self.master,text='计算',command=lambda: self.collection_output())
        self.btn1.place(relx=0.7,rely=0.45,relwidth=0.2,relheight=0.1)
        self.btn2=Button(self.master,text='添加收藏品属性',command=lambda: self.collect_collection())
        self.btn2.place(relx=0.8,rely=0.1,relwidth=0.1,relheight=0.05)

    def collect_collection(self):
        if not self.ety1.get():
            showwarning('Warning!','请先输入收藏品总数！')
            return None
        
        self.top=Toplevel()
        self.top.title('收藏品属性')
        self.top.geometry('720x480')
        self.top.lb1=Label(self.top,text='同稀有度收藏品件数')
        self.top.lb2=Label(self.top,text='同稀有度收藏品获得总概率/各件概率')
        self.top.lb3=Label(self.top,text='兑换未获得同稀有度收藏品所需token数')
        self.top.lb4=Label(self.top,text='获得重复同稀有度收藏品获得token数')
        self.top.lb1.place(relx=0.1,rely=0.1,relwidth=0.3,relheight=0.1)
        self.top.lb2.place(relx=0.6,rely=0.1,relwidth=0.3,relheight=0.1)
        self.top.lb3.place(relx=0.1,rely=0.4,relwidth=0.3,relheight=0.1)
        self.top.lb4.place(relx=0.6,rely=0.4,relwidth=0.3,relheight=0.1)

        self.top.ety1=Entry(self.top)
        self.top.ety2=Entry(self.top)
        self.top.ety3=Entry(self.top)
        self.top.ety4=Entry(self.top)
        self.top.ety1.place(relx=0.1,rely=0.2,relwidth=0.3,relheight=0.1)
        self.top.ety2.place(relx=0.6,rely=0.2,relwidth=0.3,relheight=0.1)
        self.top.ety3.place(relx=0.1,rely=0.5,relwidth=0.3,relheight=0.1)
        self.top.ety4.place(relx=0.6,rely=0.5,relwidth=0.3,relheight=0.1)

        self.top.btn=Button(self.top, text='添加',command=lambda: self.add_collection())
        self.top.btn.place(relx=0.4,rely=0.8,relwidth=0.2,relheight=0.1)

    def add_collection(self):
        self.ety2.insert(END,(',' if self.ety2.get() else '')+'['+self.top.ety1.get()+','+self.top.ety2.get()+']')
        self.ety3.insert(END,(',' if self.ety3.get() else '')+self.top.ety3.get())
        self.ety4.insert(END,(',' if self.ety4.get() else '')+self.top.ety4.get())

        self.check_collection()
        
        self.top.destroy()

    def check_collection(self,event=None):
        if self.ety1.get():
            try:
                if eval(self.ety1.get())!=int(eval(self.ety1.get())):
                    print('请输入正整数！')
            except:
                showwarning('Warning','数据类型错误！请输入正整数')
        if self.ety2.get():
            pass
        if self.ety3.get():
            input2nlist(self.ety3.get())
        if self.ety4.get():
            input2nlist(self.ety4.get())
        if self.ety5.get():
            try:
                if eval(self.ety5.get())!=int(eval(self.ety5.get())):
                    print('请输入正整数！')
            except:
                showwarning('Warning','数据类型错误！请输入正整数')
        if self.ety6.get():
            input2nlist(self.ety6.get())
        if self.ety7.get():
            input2nlist(self.ety7.get())
        
    def collection_output(self):
        '''
        num=eval(self.ety1.get())
        if self.ety2.get():
            if '[' not in self.ety2.get():
                cache=self.ety2.get().split(',')
                if len(cache)==1:
                    p=[float(cache)/num for _ in range(num)]
                elif len(cache)==num:
                    p=[float(_) for _ in cache]
            else:
                p=[]
                for s in self.ety2.get():
                    if s=='[':
                        p.append([])
                        cache=''
                    elif s==']':
                        cache=cache.split(',')
                        for i in cache:
                            p[-1].append(int(float(i)) if int(float(i))==eval(i) else eval(i))
                        cache=''
                    else:
                        cache=cache+s
        else:
            p=None
        cost=input2nlist(self.ety3.get()) if self.ety3.get() else None
        value=input2nlist(self.ety4.get()) if self.ety4.get() else None
        n=eval(self.ety5.get())
        res=input2nlist(self.ety6.get()) if self.ety6.get() else None
        rp=input2nlist(self.ety7.get()) if self.ety7.get() else None

        self.lb8.config(text='达到全收藏的概率是 %.2f %%'%(100*collection(num,p,cost,value).smlt(n,res,rp)))
        '''
        try:
            num=eval(self.ety1.get())
            if self.ety2.get():
                if '[' not in self.ety2.get():
                    cache=self.ety2.get().split(',')
                    if len(cache)==1:
                        p=[float(cache)/num for _ in range(num)]
                    elif len(cache)==num:
                        p=[float(_) for _ in cache]
                else:
                    p=[]
                    for s in self.ety2.get():
                        if s=='[':
                            p.append([])
                            cache=''
                        elif s==']':
                            cache=cache.split(',')
                            for i in cache:
                                p[-1].append(int(float(i)) if int(float(i))==eval(i) else eval(i))
                            cache=''
                        else:
                            cache=cache+s
            else:
                p=None
            cost=input2nlist(self.ety3.get()) if self.ety3.get() else None
            value=input2nlist(self.ety4.get()) if self.ety4.get() else None
            n=eval(self.ety5.get())
            res=input2nlist(self.ety6.get()) if self.ety6.get() else None
            rp=input2nlist(self.ety7.get()) if self.ety7.get() else None

            self.lb8.config(text='达到全收藏的概率是 %.2f %%'%(100*collection(num,p,cost,value).smlt(n,res,rp)))
        except:
            showwarning('Warning','存在参数值为空或参数格式存在错误！')

def input2nlist(text):
    cache=text.split(',')
    list=[]
    for i in cache:
        try:
            list.append(eval(i))
        except:
            showerror('Error','数据格式错误！请输入以英文逗号分隔的数字')
            return None
    return list

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

class step(Ui):
    def __init__(self,p,p_up,ups,thres,most,mg,*args,**kwargs):
        '''
        p:最高稀有度出率
        p_up:up占最高稀有度比例
        ups:up角色数量
        thres:触发保底机制下限
        most:必出抽数/触发保底机制后每抽递增概率
        mg:大保底歪几必出 (minimum guarantee); 0为无大保底机制
        '''
        step.p=p
        step.p_up=p_up
        step.ups=ups
        step.thres=thres
        step.mg=mg
        step.most=most

        global up
        global up_result
        up=None
        up_result=dict()

    def prob(self,n):
        if n<self.thres:
            return self.p
        elif self.most>1:
            return (1-self.p)*(n-self.thres)/(self.most-self.thres)+self.p
        else:
            return self.p+(n-self.thres)*self.most if self.p+(n-self.thres)*self.most<1 else 1

    def smlt(self,n,e,detail=False,times=100000):
        '''
        n为总抽数
        e为期望抽卡结果（数组形式表示）
        times为重复模拟次数
        '''
        #start=time.time()
        
        up=dict()
        for i in range(times):                                  #新狗哥入场
            insur=0                                             #非酋计数器（大保底计数器）
            turn=0                                              #小保底计数器
            s=0
            count=[0 for i in range(self.ups)]                  #up计数器
            for j in range(n):
                turn+=1
                pt=self.prob(turn)
                cache=random.random()                           #抽卡！
                if cache<pt:                                    #抽中五星
                    mg_b=True
                    for k in range(self.ups):                   #判断是否是第(k+1)个up
                        if k<=cache*self.ups/pt/self.p_up<(k+1):
                            count[k]+=1
                            insur=0
                            mg_b=False
                            break
                    if self.mg and mg_b:
                        if insur==self.mg:                      #非酋的强运！（大保底）
                            for k in range(self.ups):
                                if (k+(self.ups-k)*self.p_up)<=cache*self.ups/pt<(k+1+(self.ups-k-1)*self.p_up):
                                    count[k]+=1
                                    break
                            insur=0                             #大保底重置
                        else:
                            insur+=1                            #非酋复活甲（大保底激活）
                            s+=1                                #歪计数器+1                          
                    turn=0                                      #新轮回开始（保底计数器清零）
                    
                    if (not detail)and(sum(count)>=sum(e)):
                        if judge_exp(count,e):
                            break

            count=tuple(count)
            up[count]=up.get(count,0)+1

        result=times
        for key in up.keys():
            if not judge_exp(key,e):
                result-=up[key]

        #end=time.time()
        #print('%d: Running time: %s seconds.'%(n,end-start))
        
        return eval('%.4f'%(result/times))

    def interplt(self,e,target=0.95,lower=0,upper=None):
        if upper==None:
            upper=sum(e)*int((self.most if self.most>1 else self.thres+round((1-p)/self.most))/self.p_up)
        n=int(lower+(upper-lower)*(target+0.5)/2)
        p1=self.calc(n,e)
        p2=self.calc(n+1,e)
        print(lower,upper,n,p1,p2)
        if p1<=target<p2:
            return n+1
        elif p2<target:
            return self.interplt(e,target,n,upper,fd)
        else:
            return self.interplt(e,target,lower,n,fd)

    def calc(self,n,e,rel_exp=6):
        global up
        global up_result
        
        if up==None:
            up=[[tuple([0 for i in range(len(e))]),0,0,0,1]]
        '''
        up[0]: up结果
        up[1]: 总抽数
        up[2]: 该轮抽数
        up[3]: 保底结果
        up[4]: 概率
        '''
        #start=time.time()

        if self.mg and (n>=(self.mg+1)*(self.most if self.most>1 else self.thres+round((1-p)/self.most))*sum(e)):
            return 1
        else:
            if tuple([tuple(e),n]) in up_result:
                return up_result[tuple([tuple(e),n])]
            
            cache_dict=dict()
            result=0
            max_p=0
            
            if len(up)==1:
                i=0
            else:
                i=len(up)-1
                while up[i][1]==up[i-1][1]:
                    i-=1
                    if i==0:
                        break
                result=up_result.get(tuple([tuple(e),up[i][1]]),0)
                    
            while up[i][1]<=n-1:
                cache_dict[tuple([up[i][0],up[i][1]+1,up[i][2]+1,up[i][3]])]=cache_dict.get(tuple([up[i][0],up[i][1]+1,up[i][2]+1,up[i][3]]),0)+up[i][4]*(1-self.prob(up[i][2]+1))      #未抽中最高稀有度
                if self.mg and (up[i][3]==self.mg):                                                                                                                                     #大保底
                    for j in range(len(e)):
                        cache=[]
                        for k in range(len(e)):                                                                                                                                         #判断大保底角色
                            if j==k:
                                cache.append(up[i][0][k]+1)
                            else:
                                cache.append(up[i][0][k])
                        if judge_exp(cache,e):                                                                                                                                          #判断是否达到期望
                            cache_p=up[i][4]*self.prob(up[i][2]+1)/self.ups
                            if cache_p>max_p:
                                max_p=cache_p
                            result+=cache_p
                        else:
                            cache_dict[tuple([tuple(cache),up[i][1]+1,0,0])]=cache_dict.get(tuple([tuple(cache),up[i][1]+1,0,0]),0)+up[i][4]*self.prob(up[i][2]+1)/self.ups             #未达到期望记录分支
                else:
                    cache_dict[tuple([up[i][0],up[i][1]+1,0,up[i][3]+1])]=cache_dict.get(tuple([up[i][0],up[i][1]+1,0,up[i][3]+1]),0)+up[i][4]*self.prob(up[i][2]+1)*(1-self.p_up)      #歪
                    for j in range(len(e)):
                        cache=[]
                        for k in range(len(e)):                                                                                                                                         #判断up角色
                            if j==k:
                                cache.append(up[i][0][k]+1)
                            else:
                                cache.append(up[i][0][k])
                        if judge_exp(cache,e):
                            cache_p=up[i][4]*self.prob(up[i][2]+1)*self.p_up/self.ups
                            if cache_p>max_p:
                                max_p=cache_p
                            result+=cache_p
                        else:
                            cache_dict[tuple([tuple(cache),up[i][1]+1,0,0])]=cache_dict.get(tuple([tuple(cache),up[i][1]+1,0,0]),0)+up[i][4]*self.prob(up[i][2]+1)*self.p_up/self.ups
                
                if (i+1==len(up)):
                    for key in cache_dict.keys():
                        if rel_exp:
                            if cache_dict[key]>max_p*10**(-rel_exp):
                                cache=list(key)
                                cache.append(cache_dict[key])
                                up.append(cache)
                        else:
                            if cache_dict[key]:
                                cache=list(key)
                                cache.append(cache_dict[key])
                                up.append(cache)
                    up_result[tuple([tuple(e),up[i][1]+1])]=result
                    cache_dict=dict()
                i+=1

                if i>=len(up):
                    break

            #end=time.time()
            #print('Calc %d: Running time: %s seconds.'%(n,end-start))
                
            return eval('%.4f'%result)

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
            return 1
        else:
            p=1
            for i in range(e-math.floor(n/self.most)):
                p-=((1-self.p_up)**(n-i))*(self.p_up**i)*math.comb(n,i)
            return p

def judge_exp(key,e):
    for i in range(len(key)):
        if key[i]<e[i]:
            return False
    return True

class collection():
    def __init__(self,num,p=None,cost=None,value=None,*args,**kwargs):
        '''
        num: 收藏品总数
        p: 收藏品（累计）获取概率
        cost: 兑换未获得物品所需token数量 (默认为4)
        value: 重复获得物品时获得token数量 (默认为1), 如无重复收藏品兑换机制输入0
        level: 收藏品等级数(同等级兑换&重复获得token数相等, 获得概率可不同)
        '''
        self.num=num
        
        if p is None:
            self.p=[(_+1)/num for _ in range(num)]
        else:
            if type(p[0])==float:
                self.level=[1 for _ in range(num)]
                if 0<sum(p)<=1:
                    self.p=[sum(list(p[:(_+1)])) for _ in range(len(p))]
                elif sum(p)-1>10**(-9):
                    showwarning('Warning','获取概率总和大于1!')
            elif type(p[0])==list:
                self.p=[]
                self.level=[]
                for ps in p:
                    self.level.append(ps[0])
                    if len(ps)==2:
                        for i in range(ps[0]):
                            self.p.append((self.p[-1] if self.p else 0)+ps[1]/ps[0])
                    else:
                        for i in ps[1:]:
                            self.p.append((self.p[-1] if self.p else 0)+i)
                if self.p[-1]-1>10**(-9):
                    showwarning('Warning','获取概率总和大于1!')
                    self.p=None
        
        if cost is None:
            self.cost=[4 for _ in range(num)]
        else:
            if type(cost)==int:
                self.cost=[cost for _ in range(num)]
            elif len(cost)==self.num:
                self.cost=cost
            elif len(cost)==len(self.level):
                self.cost=[]
                for i in range(len(self.level)):
                    for j in range(self.level[i]):
                        self.cost.append(cost[i])

        if value is None:
            self.value=[1 for _ in range(num)]
        else:
            if type(value)==int:
                self.value=[value for _ in range(num)]
            elif len(value)==self.num:
                self.value=value
            elif len(value)==len(self.level):
                self.value=[]
                for i in range(len(self.level)):
                    for j in range(self.level[i]):
                        self.value.append(value[i])

    def smlt(self,n,res=None,rp=None,times=100000):
        '''
        n: 抽数
        res: 已有收藏品
        rp: 已有重复收藏品
        '''
        #start=time.time()
        
        if res is None:
            res=[0 for _ in range(self.num)]
        else:
            cache=res
            if len(cache)==len(self.level):
                res=[]
                for i in range(len(cache)):
                    for j in range(self.level[i]):
                        res.append(1 if j<int(cache[i]) else 0)
            elif len(cache)==self.num:
                res=[int(cache[_]) for _ in range(self.num)]
        if rp is None:
            rp=0
        else:
            if type(rp)==int:
                pass
            elif type(rp)==list:
                cache=rp
                rp=0
                if len(cache)==1:
                    rp=cache[0]
                elif len(cache)==len(self.level):
                    for i in range(len(self.level)):
                        rp+=cache[i]*self.value[sum(list(self.level[:i]))]
                elif len(cache)==self.num:
                    for i in range(len(self.num)):
                        rp+=cache[i]*self.value[i]
        
        result=0
        for i in range(times):
            c=[1 if _ else 0 for _ in res]
            rp_cache=rp
            for j in range(n):
                cache=random.random()
                k=0
                while self.p[k]<cache:
                    k+=1
                    if k==self.num:
                        break
                if k<self.num:
                    if c[k]:
                        rp_cache+=self.value[k]
                    else:
                        c[k]=1
            if sum([self.cost[_] if c[_] else 0 for _ in range(self.num)])+rp_cache>=sum(self.cost):
                result+=1

        #end=time.time()
        #print('%d: Running time: %s seconds.'%(n,end-start))
        
        return eval('%.4f'%(result/times))

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
    up=None
    up_result=dict()

    try:
        with open(file,'r',encoding='utf-8') as f:
            lines=f.readlines()
        for line in lines:
            cache=line[:-1].split(',')
            if cache[0]=='step':
                step_model[cache[1]]=cache[2:]
            elif cache[0]=='fixed':
                fixed_model[cache[1]]=cache[2:]
    except:
        pass
    
    top=Tk()
    mode=StringVar()
    Ui(top).mainloop()
