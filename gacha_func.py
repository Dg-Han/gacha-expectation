import random
import traceback

from tkinter.messagebox import showerror, showwarning

def judge_exp(key,e,exc=0):
    c=[e[_]-key[_] if e[_]>key[_] else 0 for _ in range(len(e))]
    if sum(c)<=exc:
        return True
    else:
        return False

def input2nlist(text:str) -> list:
    cache=text.split(',')
    list=[]
    for i in cache:
        try:
            list.append(eval(i))
        except:
            traceback.print_exc()
            showerror('Error','数据格式错误！请输入以英文逗号分隔的数字')
            return None
    return list

def check_input(text:str,require:str='',r:bool=False):                   #酒馆防爆机制（输入合法性检查）
    '''
    require参数设置: 'N':自然数, 'p':0-1, 'P':0-1/0-100%, 'f':任意数字
    r: 是否返回值
    '''
    if require:
        if require=='N':
            try:
                if (eval(text)==int(eval(text))) and (eval(text)>=0):
                    if r:
                        return eval(text)
                    else:
                        return True
                else:
                    if r:
                        print('请输入自然数！')
                        return check_input(text,require)
                    else:
                        showwarning('Warning','请输入自然数')
                        return False
            except:
                if r:
                    print('数据格式错误！请输入自然数')
                    return check_input(text,require)
                else:
                    showerror('Error','数据类型错误！请输入自然数')
                    raise TypeError
        if require=='p':
            try:
                if 0<=eval(text)<=1:
                    if r:
                        return eval(text)
                    else:
                        return True
                else:
                    if r:
                        print('请输入0-1之间的数！')
                        return check_input(text,require)
                    else:
                        showwarning('Warning','请输入0-1之间的数！')
                        return False
            except:
                if r:
                    print('数据格式错误！请输入0-1之间的数')
                    return check_input(text,require)
                else:
                    showerror('Error','数据类型错误！请输入0-1之间的数')
                    raise TypeError
        if require=='f':
            try:
                if r:
                    return eval(text)
                else:
                    eval(text)
                    return True
            except:
                showerror('Error','数据类型错误！请输入数字')
                raise TypeError
    else:
        if r:
            try:
                return eval(text)
            except:
                return text
        else:
            return True

def p_return(p:float) -> str:
    if p<.05:
        return random.choice(["抽数不是问题，能不能成为海豹才是问题",
                              "没有机会可以创造机会"])
    elif p<.25:
        return random.choice(["小抽怡情，强抽吃土",
                              "概率范围是0到1，但结果只有0或1"])
    elif p<.5:
        return random.choice(["出货的为什么不能是我呢",
                              "人一定要有梦想"])
    elif p<.75:
        return random.choice(["概率过半了好诶",
                              "你觉得我有机会吗"])
    elif p<.95:
        return random.choice(["已经能看到老婆（划掉）了",
                              "有经验的抽卡者要勇于下判断"])
    else:
        return random.choice(["这还能沉了不成",
                              "不需要的抽卡资源可以给有需要的人"])
