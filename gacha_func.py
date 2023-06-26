import random
import traceback
import time

from tkinter.messagebox import showerror, showwarning
from typing import Optional, Callable

def running_time(func: Callable):
    def wrapper(*args, **kwargs):
        print("Running time test\n---")
        st = time.time()
        res = func(*args, **kwargs)
        et = time.time()
        print(f"{func.__name__} Running time: {et-st} seconds\nWith args: {', '.join([str(_) for _ in args[1:]])}\nWith kwargs: {', '.join([(': '.join(key, str(kwargs[key]))) for key in kwargs])}\nThe result is {res}")
    return wrapper

def judge_exp(key:list, e:list, exc:Optional[int]=0) -> bool:
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
        
def details_report(details:dict):
    """
    输出对抽卡结果的反馈

    Parameters
    ---
    - details: key值包括由抽到up角色前抽数组成的列表`count`, 以及记录角色信息的`ups_record`, 以及歪的总数`others_rarest`
    """
    times = len(details['raw'])
    e = details['meta']['e']

    count = 0
    max_ups = None
    min_ups = None
    max_turns = None
    min_turns = None
    max_other_rarest = None
    up_insur = 0 if details['meta']['mg_type'] == "mg" else None

    for _ in range(times):
        cache = 0
        ups = [0 for _ in range(len(e))]
        other_rarest = 0                            # 歪计数器
        unfortune = 0                               # 大保底计数器
        for rarest_record in details['raw'][_]:
            if rarest_record[1] == -1:
                other_rarest += 1
                unfortune += 1
            else:
                ups[rarest_record[1]] += 1
                if details['meta']['mg_type'] == "mg" and unfortune == details['meta']['mg']:
                    up_insur += 1
                min_turns = min(rarest_record[0]-cache, min_turns if min_turns else rarest_record[0])
                max_turns = max(rarest_record[0]-cache, max_turns if max_turns else 0)
                cache = rarest_record[0]
        
        max_turns = max(details['meta']['n']-cache, max_turns if max_turns else 0)
        min_ups = min(sum(ups), min_ups if min_ups is not None else details['raw'][_][-1][0])
        max_ups = max(sum(ups), max_ups if max_ups else 0)
        max_other_rarest = max(other_rarest, max_other_rarest if max_other_rarest else 0)
        if e and judge_exp(ups, e):
            count += 1
        
    return {'summary': f'共进行{times}次模拟',
            'expect': f'共有{count}次模拟达到了 {",".join([str(_) for _ in e])} 的抽卡期望\n' if e else None,
            'ups': (f'在{times}次模拟中，' + f'最多抽到过{max_ups}个up角色，最少抽到了{min_ups}个角色' if max_ups else '' + f'最非的一次歪了{max_other_rarest}个角色' if max_other_rarest else '') if times>1 else (f'共抽到了{max_ups}个up角色' + (((f'，最非的一次' if times>1 else '，另外')+ f'歪了{max_other_rarest}个角色') if max_other_rarest else '')),
            'turns': f'在{times}次模拟中，最长没抽到过up角色的连续抽数为{max_turns}，最快抽出up角色的连续抽数为{min_turns}' if min_turns else None,
            'datas': {'max_ups': max_ups, 'min_ups': min_ups, 'max_turns': max_turns, 'min_turns': min_turns, 'max_other_rarest': max_other_rarest, 'smlt_success': count}}

def p_return(p:float, smlt_result:Optional[bool]= None) -> str:
    if smlt_result is None:             # 无模拟
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
    elif smlt_result:                   # 模拟出货
        if p<.05:
            return random.choice(["你怎么知道...",
                                  "抽数不是问题，能不能成为海豹才是问题"])
        elif p<.25:
            return random.choice(["不懂就问..."])
        elif p<.5:
            return random.choice(["什么吗我抽的还是挺准的"])
        elif p<.75:
            return random.choice(["概率没有抛弃我"])
        elif p<.95:
            return random.choice(["稳如老狗"])
        else:
            return random.choice(["这还能沉了不成"])
    else:                               # 模拟沉船
        if p<.05:
            return random.choice(["池子已经垫好了",
                                  "没有机会可以创造机会"])
        elif p<.25:
            return random.choice(["只要不停下来..."])
        elif p<.5:
            return random.choice(["人一定要有梦想"])
        elif p<.75:
            return random.choice(["日内瓦，退钱！"])
        elif p<.95:
            return random.choice(["该考虑扶老奶奶过马路了"])
        else:
            return random.choice(["反向欧皇也是欧皇（划掉"])
        