import random

def prob(n,p,mode,most=0,least=0):
    if mode=='1' or 'step' or 'ys' or 'mrfz':
        if mode=='ys':
            return prob_ys(n)
        if mode=='mrfz':
            return prob_mrfz(n)
        else:
            if n<=least:
                return p
            else:
                return (1-p)*(n-least)/(most-least)+p
    if mode=='2' or 'bound':
        if n<most:
            return p
        else:
            return 1
    if mode=='3' or 'unlimit':
        return p
'''
def gacha(n,mode,times=100000):
    if mode=='1' or 'step' or 'ys' or 'mrfz':
        if mode=='ys':
            p=0.006
            least=73
            most=90
            target=0.5
        if mode=='mrfz':
            p=0.02
            least=50
            most=99
            target=0.35
        else:
            p=eval(input("请输入未触发保底机制时每抽出货的概率:"))
            least=eval(input("请输入触发保底机制的抽数:"))
            most=eval(input("请输入100%抽中的抽数:"))
    if mode=='2' or 'bound':
        p=eval(input('请输入每抽出货的概率:'))
        most=eval('请输入保底抽数:')
    if mode=='3' or 'unlimit':
        p=eval(input('请输入每抽出货的概率:'))
        
    if mode=='4' or 'collection':
        p=1/eval(print('请输入套装收藏品件数:'))
        r=eval(input("请输入重复收藏品兑换新收藏品的比例:"))
        
    for i in range(times):
        insur=0
        c=0
        count=0
        for j in range(n):
            insur+=1
            cache=random.random()

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
'''
def lottery_ys(n,e=2,times=100000):
    s=0                                             
    up=dict()
    for i in range(times):                          #下一个狗哥入场
        insur=0                                     #小保底计数器
        c=0                                         #大保底计数器清零
        count=0                                     #抽到up个数
        for j in range(n):
            insur+=1                                #保底计数器
            cache=random.random()                   #抽卡！
            if cache<prob_ys(insur):                #抽中五星
                if not c:                           #非大保底
                    if cache<prob_ys(insur)/2:      #直击up
                        count+=1                    #up+1
                    else:
                        c+=1                        #触发大保底
                        s+=1                        #歪计数器+1
                else:
                    count+=1                        #大保底人
                    c=0                             #大保底清除
                insur=0                             #保底计数器清零
        up[count]=up.get(count,0)+1
    result=times
    for i in range(e):
        result-=up.get(i,0)
    return eval('%.4f'%(result/times))
    #print('%.4f'%(s/times))
    #for i in sorted(up.keys()):
    #    print(i,up[i])

def lottery_mrfz(n,up=1,times=100000):
    s=0
    if up==1:
        result=dict()
        for i in range(times):
            insur=0
            count=0
            for j in range(n):
                insur+=1
                cache=random.random()
                if cache<prob_mrfz(insur):
                    if cache<prob_mrfz(insur)/2:
                        count+=1
                    else:
                        s+=1
                    insur=0
            result[count]=result.get(count,0)+1
        for i in sorted(result.keys()):
            print(i,result[i])
    if up==2:
        time=0
        for i in range(times):
            insur=0
            up1=0
            up2=0
            for j in range(n):
                insur+=1
                cache=random.random()
                if cache<prob_mrfz(insur):
                    if cache<prob_mrfz(insur)*0.7:
                        if cache<prob_mrfz(insur)*0.35:
                            up1+=1
                        else:
                            up2+=1
                    else:
                        s+=1
                    insur=0
                if j<300:
                    if up1 and up2:
                        time+=1
                        break
                else:
                    if up1 or up2:
                        time+=1
                        break
        #print('%.4f'%(time/times))
        return time/times

def beta():
    mode=input('请输入希望模拟抽卡的游戏首字母或抽卡类型:')
    lottery(mode)

if __name__=="__main__":
    print('欢迎使用原神抽卡模拟计算器(ver 1.0)！')
    b1=True
    while b1:
        e=eval(input('请输入up目标命座（默认初始new，若非new则请输入目标命座-当前命座-1）:'))
        b2=True
        while b2:
            n=eval(input('请输入计划抽数:'))
            print('抽到up%d命的概率是 %.2f %%.'%(e,100*lottery_ys(n,e+1)))
            cache=input('是否继续(y/n):')
            if cache=='n':
                b1=False
                b2=False
            if b1:
                cache=input('是否需要更改命座数(y/n):')
                if cache=='y':
                    b2=False

'''
p=[]
for i in range(360):
    p.append(lottery_ys(i))
    print('%3d %.5f'%(i,lottery_ys(i)))
print(p)

p=[]
for i in range(1,401):
    p.append(lottery_mrfz(i,2))
    print('%3d %.5f'%(i,lottery_mrfz(i,2)))
print(p)
'''
