import random
import traceback
import threading

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning, showerror, showinfo

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from gacha_type import step, fixed, collection
from gacha_func import input2nlist, check_input, p_return

class Ui(Frame):
    
    file="gacha_data.dll"
    label_font='Times\sNew\sRoman -14'

    def __init__(self,master=None,*args,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])
        
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
            self.info.lb2=Label(self.info,text='当前版本: 1.2.0 (ver20230608)')
            self.info.lb3=Label(self.info,text='Copyright by Dg_Han. All Rights Reserved.')
            self.info.lb4=Label(self.info,text='github: https://github.com/Dg-Han')
            self.info.lb1.pack()
            self.info.lb2.pack()
            self.info.lb3.pack()
            self.info.lb4.pack()
            
    def createWidgets_step(self):
        #清除控件
        for widget in self.master.winfo_children():
            if (widget.winfo_class()!='Frame')and(widget.winfo_class()!='Menu'):
                widget.destroy()

        self.cmb=ttk.Combobox(self.master, textvariable=self.mode, state='readonly')
        name_list=self.step_cmb_value()
        self.cmb['value']=name_list
        self.cmb.bind('<<ComboboxSelected>>', self.set_step_para)
        self.cmb.place(relx=0.7,rely=0.1,relwidth=0.1,relheight=0.05)
        self.cmb.set('')

        label_list=['最高稀有度出率','up占最高稀有度总比例','up角色数量','触发概率递增机制抽数','递增至必出时抽数\n或 每抽递增概率','大保底歪几必出\n或 兑换up所需抽数\n0为无大保底机制',
                    '总抽数','期望结果\n多up角色数量间用逗号分隔','未出最高稀有度角色抽数\n默认为0','期望结果概率\n默认为95%']

        for i in range(6):
            self.lb=Label(self.master,text=label_list[i],font=self.label_font)
            self.lb.place(relx=0.15*i+0.025,rely=0.25,relwidth=0.15,relheight=0.1)

        self.ety1=Entry(self.master)
        self.ety2=Entry(self.master)
        self.ety3=Entry(self.master)
        self.ety4=Entry(self.master)
        self.ety5=Entry(self.master)
        self.ety6=Entry(self.master)
        self.ety1.place(relx=0.05,rely=0.35,relwidth=0.1,relheight=0.05)
        self.ety2.place(relx=0.2,rely=0.35,relwidth=0.1,relheight=0.05)
        self.ety3.place(relx=0.35,rely=0.35,relwidth=0.1,relheight=0.05)
        self.ety4.place(relx=0.5,rely=0.35,relwidth=0.1,relheight=0.05)
        self.ety5.place(relx=0.65,rely=0.35,relwidth=0.1,relheight=0.05)
        self.ety6.place(relx=0.8,rely=0.35,relwidth=0.1,relheight=0.05)
        self.ety1.bind('<KeyRelease>',self.check_step)
        self.ety2.bind('<KeyRelease>',self.check_step)
        self.ety3.bind('<KeyRelease>',self.check_step)
        self.ety4.bind('<KeyRelease>',self.check_step)
        self.ety5.bind('<KeyRelease>',self.check_step)
        self.ety6.bind('<KeyRelease>',self.check_step)

        for i in range(4):
            self.lb=Label(self.master,text=label_list[6+i],font=self.label_font)
            self.lb.place(relx=0.15*i+0.025,rely=0.45,relwidth=0.15,relheight=0.05)

        self.ety7=Entry(self.master)
        self.ety8=Entry(self.master)
        self.ety9=Entry(self.master)
        self.ety10=Entry(self.master)
        self.ety7.place(relx=0.05,rely=0.525,relwidth=0.1,relheight=0.05)
        self.ety8.place(relx=0.2,rely=0.525,relwidth=0.1,relheight=0.05)
        self.ety9.place(relx=0.35,rely=0.525,relwidth=0.1,relheight=0.05)
        self.ety10.place(relx=0.5,rely=0.525,relwidth=0.1,relheight=0.05)
        self.ety7.bind('<KeyRelease>',self.check_step)
        self.ety8.bind('<FocusOut>',self.check_step)
        self.ety9.bind('<KeyRelease>',self.check_step)
        self.ety10.bind('<FocusOut>',self.check_step)

        self.btn1=Button(self.master,text='计算',font='Times\sNew\sRoman -20',command=lambda: threading.Thread(target=self.step_output,args=()).start())
        self.btn1.place(relx=0.7,rely=0.5,relwidth=0.2,relheight=0.1)
        self.btn2=Button(self.master,text='保存模板',command=lambda: self.save_step_model())
        self.btn2.place(relx=0.85,rely=0.025,relwidth=0.1,relheight=0.05)
        self.btn3=Button(self.master,text='删除模板',command=lambda: self.delete_step_model())
        self.btn3.place(relx=0.85,rely=0.1,relwidth=0.1,relheight=0.05)
        self.btn4=Button(self.master,text='分析卡池曲线',command=lambda: threading.Thread(target=self.analysis_set,args=()).start())
        self.btn4.place(relx=0.85,rely=0.175,relwidth=0.1,relheight=0.05)

        self.lb11=Label(self.master,text='',font='Times\sNew\sRoman -18')
        self.lb11.place(relx=0.25,rely=0.75,relwidth=0.5,relheight=0.1)
        
    def set_step_para(self,event=None):
        self.ety1.config(state='normal')
        self.ety2.config(state='normal')
        self.ety3.config(state='normal')
        self.ety4.config(state='normal')
        self.ety5.config(state='normal')
        self.ety6.config(state='normal')
        for widget in self.master.winfo_children():
            if widget.winfo_class()=='Entry':
                widget.delete(0,END)
        
        m=self.mode.get()
        if m in self.step_model.keys():
            self.ety1.insert(END,str(self.step_model[m][0]))
            self.ety1.config(state='readonly')
            self.ety2.insert(END,str(self.step_model[m][1]))
            self.ety2.config(state='readonly')
            self.ety3.insert(END,str(self.step_model[m][2]))
            self.ety3.config(state='readonly')
            self.ety4.insert(END,str(self.step_model[m][3]))
            self.ety4.config(state='readonly')
            self.ety5.insert(END,str(self.step_model[m][4]))
            self.ety5.config(state='readonly')
            self.ety6.insert(END,str(self.step_model[m][5]))
            self.ety6.config(state='readonly')
            self.cmb.config(state='readonly')
        else:
            self.cmb.config(state='normal')

        self.lb11.config(text='')

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
                elif c not in [' ']:
                    raise TypeError
            #print(p,p_up,ups,thres,most,mg,n,e)
            t=eval(self.ety9.get()) if self.ety9.get() else 0
            if self.ety10.get():
                target=eval(self.ety9.get()) if eval(self.ety9.get())<=1 else eval(self.ety9.get())/100
            else:
                target=0.95
            
            para_set=step(p,p_up,ups,thres,most,mg)
            self.lb11.config(text='计算中...')
            result=para_set.calc_numpy(n,*e,t) if ups==1 else para_set.calc_numpy_ups(n,e,t)
            self.lb11.config(text='计算中... 计算进度 %.2f %%'%(10+10*random.random()))
            self.update()
            #nx=step(p,p_up,ups,thres,most,mg).clmp_n(e,target)
            lower=0
            upper=sum(e)*int((most if most>1 else thres+round((1-p)/most))/p_up)*ups
            fdis=upper-lower
            while True:
                n=int(lower+(upper-lower)*(target+0.5)/2)
                p1=para_set.calc_numpy(n,*e) if ups==1 else para_set.calc_numpy_ups(n,e)
                p2=para_set.calc_numpy(n+1,*e) if ups==1 else para_set.calc_numpy_ups(n+1,e)
                #print(lower,upper,n,p1,p2)
                if p1<target<=p2:
                    nx=n+1
                    break
                elif p2<target:
                    lower=n
                    self.lb11.config(text='计算中... 计算进度 %.2f %%'%(100*(1-(upper-lower)/fdis)))
                    self.update()
                else:
                    upper=n
                    self.lb11.config(text='计算中... 计算进度 %.2f %%'%(100*(1-(upper-lower)/fdis)))
                    self.update()
                    
            self.lb11.config(text='达到预期抽卡结果的概率是 %.2f %%\n%s\n达到 %d%% 出率的所需抽数为 %d'%(100*result,p_return(result),int(100*target),nx))
            
        except SyntaxError:
            self.lb11.config(text='')
            showerror('Error','存在参数值为空！')
        except TypeError:
            self.lb11.config(text='')
            showerror('Error','期望结果输入格式错误！')
        except Exception as e:
            self.lb11.config(text='')
            traceback.print_exc()
            showerror('Error','未知错误！')

    def check_step(self,event=None):
        if self.ety1.get():
            try:
                if not check_input(self.ety1.get(),'p'):
                    self.ety1.delete(0,END)
            except:
                self.ety1.delete(len(self.ety1.get())-1,END)
        if self.ety2.get():
            try:
                if not check_input(self.ety2.get(),'p'):
                    self.ety2.delete(0,END)
            except:
                self.ety2.delete(len(self.ety2.get())-1,END)
        if self.ety3.get():
            try:
                if not check_input(self.ety3.get(),'N'):
                    self.ety3.delete(len(self.ety3.get())-1,END)
            except:
                self.ety3.delete(len(self.ety3.get())-1,END)
        if self.ety4.get():
            try:
                if not check_input(self.ety4.get(),'N'):
                    self.ety4.delete(len(self.ety4.get())-1,END)
            except:
                self.ety4.delete(len(self.ety4.get())-1,END)
        if self.ety5.get():
            try:
                if not check_input(self.ety5.get(),'f'):
                    self.ety5.delete(len(self.ety5.get())-1,END)
            except:
                self.ety5.delete(len(self.ety5.get())-1,END)
        if self.ety6.get():
            try:
                if not check_input(self.ety6.get(),'N'):
                    self.ety6.delete(len(self.ety6.get())-1,END)
            except:
                self.ety6.delete(len(self.ety6.get())-1,END)
        if self.ety7.get():
            try:
                if not check_input(self.ety7.get(),'N'):
                    self.ety7.delete(len(self.ety7.get())-1,END)
            except:
                self.ety7.delete(len(self.ety7.get())-1,END)
        if self.ety8.get():
            try:
                list=input2nlist(self.ety8.get())
                if len(list)!=eval(self.ety3.get()):
                    showwarning('Warning','输入期望数量与up角色数量不符！')
            except:
                pass
        if self.ety9.get():
            try:
                if not check_input(self.ety9.get(),'N'):
                    self.ety9.delete(len(self.ety9.get())-1,END)
            except:
                self.ety9.delete(len(self.ety9.get())-1,END)
        if self.ety10.get():
            try:
                if eval(self.ety10.get())>100 or eval(self.ety10.get())<0:
                    showwarning('Warning','请输入百分比或概率！')
                    self.ety10.delete(0,END)
            except:
                showerror('Error','数据类型错误！请输入百分比或概率')
                self.ety10.delete(0,END)

    def save_step_model(self):
        if self.cmb.get() in self.step_model.keys():
            showwarning('Warning','保存模板名称与已有模板重复！')
        else:
            if self.cmb.get() and self.ety1.get() and self.ety2.get() and self.ety3.get() and self.ety4.get() and self.ety5.get() and self.ety6.get():
                with open(self.file,'a',encoding='utf-8') as f:
                    f.write(','.join(['step',self.cmb.get(),
                                      self.ety1.get(),
                                      self.ety2.get(),
                                      self.ety3.get(),
                                      self.ety4.get(),
                                      self.ety5.get(),
                                      self.ety6.get()]))
                    f.write('\n')
                self.step_model[self.cmb.get()]=[self.ety1.get(),self.ety2.get(),self.ety3.get(),self.ety4.get(),self.ety5.get(),self.ety6.get()]
                
                name_list=self.step_cmb_value()
                self.cmb['value']=name_list
                self.cmb.current(len(name_list)-2)
                self.set_step_para()
            else:
                showwarning('Warning','存在卡池参数值为空！')

    def delete_step_model(self):
        if self.cmb.get() not in self.step_model.keys():
            showerror('Error','无已有模板！')
        elif self.cmb.get() in ['原神','明日方舟单up','明日方舟双up']:
            showwarning('Warning','初始模板不可删除！')
        else:                                               #self.cmb.get() in step_model.keys()
            with open(self.file,'r',encoding='utf-8') as f:
                lines=f.readlines()
            with open(self.file,'w',encoding='utf-8') as f:
                for line in lines:
                    if self.cmb.get() not in line:
                        f.write(line)
            del self.step_model[self.cmb.get()]

            name_list=self.step_cmb_value()
            self.cmb['value']=name_list
            self.cmb.set('')
            self.set_step_para()
            
    def step_cmb_value(self):
        
        cache=[item for item in self.step_model.keys()]
        cache.append('自定义')
        name_list=tuple(cache)
        return name_list

    def analysis_set(self):
        if not self.ety3.get():
            showwarning('Warning','请先设定卡池参数！')
            return
        
        self.top=Toplevel()
        self.top.title('卡池分析设置')
        self.top.geometry('960x640')

        if self.ety3.get()=='1':
            self.top.cbtn1=Checkbutton(self.top,text='1',variable=self.I1,command=lambda: self.get_e_list())
            self.top.cbtn2=Checkbutton(self.top,text='2',variable=self.I2,command=lambda: self.get_e_list())
            self.top.cbtn3=Checkbutton(self.top,text='3',variable=self.I3,command=lambda: self.get_e_list())
            self.top.cbtn1.place(relx=0.85,rely=0.1,relwidth=0.1,relheight=0.05)
            self.top.cbtn2.place(relx=0.85,rely=0.2,relwidth=0.1,relheight=0.05)
            self.top.cbtn3.place(relx=0.85,rely=0.3,relwidth=0.1,relheight=0.05)
            self.top.cbtn1.select()
            self.top.cbtn2.select()
            self.top.cbtn3.select()
        else:
            self.top.cbtn=Checkbutton(self.top,text='all',command=lambda: self.get_e_list(),variable=self.I1)
            self.top.cbtn.place(relx=0.85,rely=0.2,relwidth=0.1,relheight=0.05)
            self.top.cbtn.select()

        self.top.lb=Label(self.top,text='自定义期望\n如需同时添加多个\n以换行分隔')
        self.top.lb.place(relx=0.85,rely=0.4,relwidth=0.1,relheight=0.1)
        self.top.txt=Text(self.top)
        self.top.txt.place(relx=0.85,rely=0.5,relwidth=0.1,relheight=0.3)

        self.top.btn=Button(self.top,text='分析',command=lambda: threading.Thread(target=self.analysis_step,args=(self.get_e_list(),)).start())
        self.top.btn.place(relx=0.85,rely=0.85,relwidth=0.1,relheight=0.05)

    def get_e_list(self):
        e_list=[]
        if self.ety3.get()=='1':
            if self.I1.get()==1:
                e_list.append([1])
            if self.I2.get()==1:
                e_list.append([2])
            if self.I3.get()==1:
                e_list.append([3])
        else:
            if self.I1.get()==1:
                e_list.append([1 for _ in range(eval(self.ety3.get()))])
        cache=self.top.txt.get('1.0',END)[:-1].split('\n')
        for e in cache:
            if e=='':
                pass
            else:
                e_list.append(input2nlist(e))
        return e_list

    def analysis_step(self,e_list):
        try:
            p=eval(self.ety1.get())
            p_up=eval(self.ety2.get())
            ups=eval(self.ety3.get())
            thres=eval(self.ety4.get())
            most=eval(self.ety5.get())
            mg=eval(self.ety6.get())

            fig=plt.figure(figsize=(7.5,6),dpi=100)
            f_plot=fig.add_subplot(111)
            cv=FigureCanvasTkAgg(fig,master=self.top)
            cv.get_tk_widget().place(x=20,y=20)

            plt.rcParams['font.sans-serif']=['SimHei']
            plt.rcParams['axes.unicode_minus']=False
            f_plot.clear()
            plt.xlabel('抽数')
            plt.ylabel('达成期望概率')
            plt.title('抽卡概率曲线')
            
            for e in e_list:
                up_result=dict()
                para_set=step(p,p_up,ups,thres,most,mg,up_result=up_result)
                n=0
                if para_set.mg_type=='exc':
                    upper=mg*max(e)*1.05
                else:
                    upper=sum(e)*int((most if most>1 else thres+round((1-p)/most))/p_up)*(1+ups)/2
                while n<upper:
                    n+=1
                    if ups==1:
                        para_set.calc(n,e)
                        self.update()
                    else:
                        para_set.smlt(n,e)
                        self.update()
                up_result[tuple([tuple(e),0])]=0
                x_list=[]
                y_list=[]
                for i in sorted([_[1] for _ in up_result.keys()]):
                    x_list.append(i)
                    y_list.append(up_result[tuple([tuple(e),i])])
                
                plt.plot(x_list,y_list,label=','.join([str(e[_])+'up'+('' if len(e)==1 else chr(ord('A')+_)) for _ in range(len(e))]))

            plt.legend()
            cv.draw()
            #plt.show()
            
        except SyntaxError:
            showerror('Error','存在参数值为空！')
        except TypeError:
            traceback.print_exc()
            showerror('Error','期望结果输入格式错误！')
        except:
            traceback.print_exc()
            showerror('Error','未知错误！')

    def createWidgets_fixed(self):
        for widget in self.master.winfo_children():
            if (widget.winfo_class()!='Frame')and(widget.winfo_class()!='Menu'):
                widget.destroy()

        self.cmb=ttk.Combobox(self.master, textvariable=self.mode, state='readonly')
        name_list=self.fixed_cmb_value()
        self.cmb['value']=name_list
        self.cmb.bind('<<ComboboxSelected>>', self.set_fixed_para)
        self.cmb.place(relx=0.7,rely=0.1,relwidth=0.1,relheight=0.05)
        self.cmb.set('')

        self.lb1=Label(self.master,text='最高稀有度出率',font=self.label_font)
        self.lb2=Label(self.master,text='up角色出率',font=self.label_font)
        self.lb3=Label(self.master,text='保底抽数\n0为无保底机制',font=self.label_font)
        self.lb1.place(relx=0.1,rely=0.25,relwidth=0.1,relheight=0.05)
        self.lb2.place(relx=0.3,rely=0.25,relwidth=0.1,relheight=0.05)
        self.lb3.place(relx=0.45,rely=0.25,relwidth=0.2,relheight=0.05)

        self.ety1=Entry(self.master)
        self.ety2=Entry(self.master)
        self.ety3=Entry(self.master)
        self.ety1.place(relx=0.1,rely=0.325,relwidth=0.1,relheight=0.05)
        self.ety2.place(relx=0.3,rely=0.325,relwidth=0.1,relheight=0.05)
        self.ety3.place(relx=0.5,rely=0.325,relwidth=0.1,relheight=0.05)
        self.ety1.bind('<KeyRelease>',self.check_fixed)
        self.ety2.bind('<KeyRelease>',self.check_fixed)
        self.ety3.bind('<KeyRelease>',self.check_fixed)

        self.lb4=Label(self.master,text='总抽数',font=self.label_font)
        self.lb5=Label(self.master,text='期望结果',font=self.label_font)
        self.lb4.place(relx=0.2,rely=0.45,relwidth=0.1,relheight=0.05)
        self.lb5.place(relx=0.4,rely=0.45,relwidth=0.1,relheight=0.05)
        self.ety4=Entry(self.master)
        self.ety5=Entry(self.master)
        self.ety4.place(relx=0.2,rely=0.525,relwidth=0.1,relheight=0.05)
        self.ety5.place(relx=0.4,rely=0.525,relwidth=0.1,relheight=0.05)
        self.ety4.bind('<KeyRelease>',self.check_fixed)
        self.ety5.bind('<KeyRelease>',self.check_fixed)

        self.lb6=Label(self.master,text='',font='Times\sNew\sRoman -18')
        self.lb6.place(relx=0.25,rely=0.75,relwidth=0.5,relheight=0.1)

        self.btn1=Button(self.master,text='计算',command=lambda: self.fixed_output(),font='Times\sNew\sRoman -20')
        self.btn1.place(relx=0.7,rely=0.5,relwidth=0.2,relheight=0.1)
        self.btn2=Button(self.master,text='保存模板',command=lambda: self.save_fixed_model())
        self.btn2.place(relx=0.85,rely=0.0625,relwidth=0.1,relheight=0.05)
        self.btn3=Button(self.master,text='删除模板',command=lambda: self.delete_fixed_model())
        self.btn3.place(relx=0.85,rely=0.1375,relwidth=0.1,relheight=0.05)

    def set_fixed_para(self,event=None):
        self.ety1.config(state='normal')
        self.ety2.config(state='normal')
        self.ety3.config(state='normal')

        for widget in self.master.winfo_children():
            if widget.winfo_class()=='Entry':
                widget.delete(0,END)

        m=self.mode.get()
        if m in self.fixed_model.keys():
            self.ety1.insert(END,str(self.fixed_model[m][0]))
            self.ety1.config(state='readonly')
            self.ety2.insert(END,str(self.fixed_model[m][1]))
            self.ety2.config(state='readonly')
            self.ety3.insert(END,str(self.fixed_model[m][2]))
            self.ety3.config(state='readonly')
            self.cmb.config(state='readonly')
        else:
            self.cmb.config(state='normal')

    def check_fixed(self,event):
        if self.ety1.get():
            try:
                if not check_input(self.ety1.get(),'p'):
                    self.ety1.delete(0,END)
            except:
                self.ety1.delete(len(self.ety1.get())-1,END)
        if self.ety2.get():
            try:
                if not check_input(self.ety2.get(),'p'):
                    self.ety2.delete(0,END)
            except:
                self.ety2.delete(len(self.ety2.get())-1,END)
        if self.ety3.get():
            try:
                if not check_input(self.ety3.get(),'N'):
                    self.ety3.delete(len(self.ety3.get())-1,END)
            except:
                self.ety3.delete(len(self.ety3.get())-1,END)
        if self.ety4.get():
            try:
                if not check_input(self.ety4.get(),'N'):
                    self.ety4.delete(len(self.ety4.get())-1,END)
            except:
                self.ety4.delete(len(self.ety4.get())-1,END)
        if self.ety5.get():
            try:
                if not check_input(self.ety5.get(),'N'):
                    self.ety5.delete(len(self.ety5.get())-1,END)
            except:
                self.ety5.delete(len(self.ety5.get())-1,END)

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

    def save_fixed_model(self):
        if self.cmb.get() in self.fixed_model.keys():
            showwarning('Warning','保存模板名称与已有模板重复！')
        else:
            if self.cmb.get() and self.ety1.get() and self.ety2.get() and self.ety3.get():
                with open(self.file,'a',encoding='utf-8') as f:
                    f.write(','.join(['fixed',self.cmb.get(),
                                      self.ety1.get(),
                                      self.ety2.get(),
                                      self.ety3.get()]))
                    f.write('\n')
                self.fixed_model[self.cmb.get()]=[self.ety1.get(),self.ety2.get(),self.ety3.get()]
                
                name_list=self.fixed_cmb_value()
                self.cmb['value']=name_list
                self.cmb.current(len(name_list)-2)
                self.set_fixed_para()
            else:
                showwarning('Warning','存在卡池参数值为空！')

    def delete_fixed_model(self):
        if self.cmb.get() not in self.fixed_model.keys():
            showerror('Error','无已有模板！')
        elif self.cmb.get() in ['PCR','blhx']:
            showwarning('Warning','初始模板不可删除！')
        else:                                               #self.cmb.get() in fixed_model.keys()
            with open(self.file,'r',encoding='utf-8') as f:
                lines=f.readlines()
            with open(self.file,'w',encoding='utf-8') as f:
                for line in lines:
                    if self.cmb.get() not in line:
                        f.write(line)
            del self.fixed_model[self.cmb.get()]

            name_list=self.fixed_cmb_value()
            self.cmb['value']=name_list
            self.cmb.set('')
            self.set_fixed_para()

    def fixed_cmb_value(self):
        
        cache=[item for item in self.fixed_model.keys()]
        cache.append('自定义')
        name_list=tuple(cache)
        return name_list

    def createWidgets_collection(self):
        for widget in self.master.winfo_children():
            if (widget.winfo_class()!='Frame')and(widget.winfo_class()!='Menu'):
                widget.destroy()

        label_list=['收藏品总数','收藏品获得概率','兑换new所需token','重复收藏品转换token',
                    '总抽数','已有收藏品情况','重复收藏品情况/token数量']
        for i in range(4):
            self.lb=Label(self.master,text=label_list[i],font=self.label_font)
            self.lb.place(relx=0.2*i+0.05,rely=0.25,relwidth=0.2,relheight=0.05)

        self.ety1=Entry(self.master)
        self.ety2=Entry(self.master)
        self.ety3=Entry(self.master)
        self.ety4=Entry(self.master)
        self.ety1.place(relx=0.1,rely=0.325,relwidth=0.1,relheight=0.05)
        self.ety2.place(relx=0.3,rely=0.325,relwidth=0.1,relheight=0.05)
        self.ety3.place(relx=0.5,rely=0.325,relwidth=0.1,relheight=0.05)
        self.ety4.place(relx=0.7,rely=0.325,relwidth=0.1,relheight=0.05)

        for i in range(3):
            self.lb=Label(self.master,text=label_list[4+i],font=self.label_font)
            self.lb.place(relx=0.2*i+0.05,rely=0.45,relwidth=0.2,relheight=0.05)

        self.ety5=Entry(self.master)
        self.ety6=Entry(self.master)
        self.ety7=Entry(self.master)
        self.ety5.place(relx=0.1,rely=0.525,relwidth=0.1,relheight=0.05)
        self.ety6.place(relx=0.3,rely=0.525,relwidth=0.1,relheight=0.05)
        self.ety7.place(relx=0.5,rely=0.525,relwidth=0.1,relheight=0.05)

        for widget in self.winfo_children():
            if widget.winfo_class()=='Entry':
                widget.bind('FocusOut',self.check_collection)

        self.lb8=Label(self.master,text='',font='Times\sNew\sRoman -18')
        self.lb8.place(relx=0.25,rely=0.75,relwidth=0.5,relheight=0.1)

        self.btn1=Button(self.master,text='计算',font='Times\sNew\sRoman -20',command=lambda: threading.Theard(target=self.collection_output,args=()).start())
        self.btn1.place(relx=0.7,rely=0.5,relwidth=0.2,relheight=0.1)
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
            traceback.print_exc()
            showwarning('Warning','存在参数值为空或参数格式存在错误！')

if __name__=='__main__':
    pass
