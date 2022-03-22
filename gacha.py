import random

'''
def gacha(n,mode,times=100000):
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

def ct(text,Default=True):
    cache=input(text+'(Y/N):')
    if (cache=='Y') or (cache=='y') or (not cache and Default):
        return True
    elif (cache=='N') or (cache=='n') or (not cache and not Default):
        return False
    else:
        ct(text,Default)
    

def ys_OI(n=None,e=None):
    ys=step(0.006,0.5,1,73,90,1)
    if e is None:
        e=check_input('请输入up目标命座（默认初始new，若非new则请输入目标命座-当前命座-1）:','N')
    if n is None:
        n=check_input('请输入计划抽数:','N')
    print('抽到up%d命的概率是 %.2f %%.'%(e,100*ys.smlt(n,[e+1])))
    cache=ct('是否继续')
    if cache:
        cache=ct('是否需要更改命座数')
        if cache:
            ys_OI()
        else:
            ys_OI(None,e)

def mrfz_OI(ups=None,n=None,e=None):
    if ups is None:
        ups=check_input("请输入池子中up角色数量:",'N')
    if e is None:
        e=[]
        for i in range(ups):
            e.append(check_input("请输入期望抽到第%d个目标的数量:"%(i+1),'N'))
    if n is None:
        n=input('请输入计划抽数:','N')
    if ups==1:
        mrfz1=step(0.02,0.5,1,50,99,0)
        print('抽到up%d潜的概率是 %.2f %%.'%(e[0],100*mrfz1.smlt(n,e)))
    if ups==2:
        mrfz2=step(0.02,0.7,2,50,99,0)
        print('达到目标结果的概率是 %.2f %%.'%(100*mrfz2.smlt(n,e)))
    cache=ct('是否继续')
    if cache:
        cache=ct('是否需要更换卡池')
        if cache:
            mrfz_OI()
        else:
            cache=ct('是否需要更改期望结果')
            if cache:
                mrfz_OI(ups)
            else:
                mrfz_OI(ups,None,e)

def diy_step_OI(p=None,p_up=None,ups=None,thres=None,most=None,mg=None,n=None,e=None):
    if p is None:
        p=check_input("请输入稀有度最高角色的出率:",'p')
    if p_up is None:
        p_up=check_input("请输入up角色出率占稀有度最高角色的比例:",'p')
    if ups is None:
        ups=check_input("请输入up角色个数:",'N')
    if thres is None:
        thres=check_input("请输入触发概率递增的阈限抽数:",'N')
    if most is None:
        most=check_input("请输入必出最高稀有度的上限抽数/触发递增概率后每抽增加的概率:")
    if mg is None:
        mg=check_input("请输入歪几必出（如无大保底机制请输入0）:",'N')
    diy=step(p,p_up,ups,thres,most,mg)
    if e is None:
        e=[]
        for i in range(ups):
            e.append(eval(input("请输入期望抽到第%d个目标的数量:"%(i+1))))
    if n is None:
        n=eval(input('请输入计划抽数:'))
    print('达到目标结果的概率是 %.2f %%.'%(100*diy.smlt(n,e)))
    cache=ct('是否继续')
    if cache:
        cache=ct('是否需要更换卡池')
        if cache:
            diy_step_OI()
        else:
            cache=ct('是否需要更改期望抽卡结果')
            if cache:
                diy_step_OI(p,p_up,ups,thres,most,mg)
            else:
                diy_step_OI(p,p_up,ups,thres,most,mg,None,e)

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
    print('欢迎使用抽卡模拟计算器(ver 1.3)！')
    mode=input('请输入想选择的卡池(1:原神, 2:明日方舟, 3:自定义可变概率卡池):')
    if mode=='1':
        ys_OI()
    elif mode=='2':
        mrfz_OI()
    elif mode=='3':
        diy_step_OI()

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
