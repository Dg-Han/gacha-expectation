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
            step.most=thres+(1-p)*most

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
                                if (k+(1-k)*pt)<=cache*self.ups/self.p_up<(k+1-k*pt):
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

if __name__=="__main__":
    print('欢迎使用原神抽卡模拟计算器(ver 1.2)！')
    ys=step(0.006,0.5,1,73,90,1)
    mrfz1=step(0.02,0.5,1,50,99,0)
    mrfz2=step(0.02,0.7,2,50,99,0)
    b1=True
    while b1:
        e=eval(input('请输入up目标命座（默认初始new，若非new则请输入目标命座-当前命座-1）:'))
        b2=True
        while b2:
            n=eval(input('请输入计划抽数:'))
            print('抽到up%d命的概率是 %.2f %%.'%(e,100*ys.smlt(n,[e+1])))
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
ys=step(0.006,0.5,73,90,True)
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
