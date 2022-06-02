import traceback

from tkinter.messagebox import showerror, showwarning

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
        return "抽数不是问题，能不能成为海豹才是问题"
    elif p<.25:
        return "小抽怡情，强抽吃土"
    elif p<.5:
        return "出货的为什么不能是我呢"
    elif p<.75:
        return "概率过半了好诶"
    elif p<.95:
        return "已经能看到老婆（划掉）了"
    else:
        return "这还能沉了不成"
