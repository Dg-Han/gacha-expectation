import random

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
'''
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
    def __init__(self,p,p_up,thres,most,*args,**kwargs):
        '''
        p:最高稀有度出率
        p_up:up占最高稀有度比例
        thres:触发保底机制下限
        most:必出抽数
        '''
        step.p=p
        step.p_up=p_up
        step.thres=thres
        if most>1:
            step.most=most
        else:
            step.most=threshold+(1-p)*most

    def prob(self,n):
        if n<self.thres:
            return self.p
        else:
            return (1-self.p)*(n-self.thres)/(self.most-self.thres)+self.p

    def smlt(self,n,e,times):
        s=0
        up=dict()
        for i in range(times):                              #新狗哥入场
            insur=False                                     #非酋计数器（大保底是否可用）
            turn=0                                          #小保底计数器
            count=0                                         #up计数器
            for j in range(n):
                turn+=1
                cache=random.random()                       #抽卡！
                if cache<self.prob(turn):                   #抽中五星
                    if insur:                               #非酋的强运！（大保底）
                        count+=1
                        insur=False                         #大保底重置
                    elif cache<self.prob(turn)*self.p_up:   #直击up！
                        count+=1
                    else:                                   #大保底人（悲
                        insur=True                          #非酋复活甲（大保底激活）
                        s+=1                                #歪计数器+1
                    turn=0                                  #新轮回开始（保底计数器清零）
            up[count]=up.get(count,0)+1
        result=times
        for i in range(e):
            result-=up.get(i,0)
        return eval('%.4f'%(result/times))

    def output_list(self,up):
        for i in sorted(up.keys()):
            print(i,up[i])

class bound():
    def __init__(self,p,p_up,most,*args,**kwargs):
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

    def prob(self,n):
        if n<self.most:
            return 1-(1-self.p_up)**n
        else:
            return 0

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

if __name__=="__main__":
    print('欢迎使用原神抽卡模拟计算器(ver 1.1)！')
    ys=step(0.006,0.5,73,90)
    b1=True
    while b1:
        e=eval(input('请输入up目标命座（默认初始new，若非new则请输入目标命座-当前命座-1）:'))
        b2=True
        while b2:
            n=eval(input('请输入计划抽数:'))
            print('抽到up%d命的概率是 %.2f %%.'%(e,100*ys.smlt(n,e+1,100000)))
            cache=input('是否继续(y/n):')
            if cache=='n':
                b1=False
                b2=False
            if b1:
                cache=input('是否需要更改命座数(y/n):')
                if cache=='y':
                    b2=False

'''
p_ys=[]
ys=step(0.006,0.5,73,90)
for i in range(360):
    p.append(ys(i).smlt(n,2,100000))
    print('%3d %.5f'%(i,p[-1]))
print(p)

p_mrfz=[]
for i in range(1,401):
    p.append(lottery_mrfz(i,2))
    print('%3d %.5f'%(i,lottery_mrfz(i,2)))
print(p)
'''
