import math
import random
import time
import numpy
import itertools

from tkinter.messagebox import showwarning
from typing import Optional, Callable

from gacha_func import judge_exp

def running_time(func: Callable):
    def wrapper(*args, **kwargs):
        print("Running time test\n---")
        st = time.time()
        res = func(*args, **kwargs)
        et = time.time()
        print(f"{func.__name__} Running time: {et-st} seconds\nWith args: {', '.join([str(_) for _ in args[1:]])}\nWith kwargs: {', '.join([(': '.join(key, str(kwargs[key]))) for key in kwargs])}\nThe result is {res}")
    return wrapper

class step():
    def __init__(self, p:float, p_up: float|list[float], ups: Optional[int], thres:int, most:int, mg:int, mg_type:Optional[str]="default", *args, **kwargs):
        '''
        Parameters
        ---
        - p:最高稀有度出率
        - p_up:up占最高稀有度比例, 或up出率列表
        - ups:up角色数量, 如果p_up为出率列表则为None
        - thres:触发保底机制下限, 0为无概率递增机制(计划与fixed合并)
        - most:必出抽数/触发保底机制后每抽递增概率
        - mg:大保底歪几必出 (minimum guarantee)
           或 可以兑换up的抽数; 0为无大保底机制
        - mg_type: 大保底机制, `mg`为歪几必出, `exc`为固定抽数兑换, `None`为无大保底机制,
            无输入默认为`default`, 将根据p_up, ups, thres以及most自动测算
        
        Returns
        ---
        - Class step
        '''
        step.p=p
        if ups == None:
            try:
                self.p_up = [sum(p_up)[:_+1] for _ in range(len(p_up))]
            except:
                raise TypeError("Mismatch between p_up and ups: should be float-int or list-None pair")
        else:
            try:
                self.p_up = [(_+1)*p*p_up/ups for _ in range(ups)]
            except:
                raise TypeError("Mismatch between p_up and ups: should be float-int or list-None pair")
        step.ups=ups
        step.thres=thres
        step.most=most if step.thres else 0
        step.mg=mg

        if mg_type not in ['', 'mg', 'exc', 'None', 'default']:
            raise ValueError("mg_type must be null string, mg, exc or None")
        elif mg_type != 'default':
            self.mg_type = mg_type if mg_type else None
        elif not mg:
            self.mg_type = 'None'
        else:
            self.mg_type = 'mg' if mg*p<1 else 'exc'
        
        self.up=None
        self.up_result=dict()
        self.result = {}
        self.p_list = {}

        for key in kwargs:
            setattr(self,key,kwargs[key])

    def prob(self,n:int) -> float:
        '''
        Parameters
        ---
        n: times after getting last rarest item

        Return
        ---
        The proability of getting the rarest item
        '''
        if (self.thres==0) or (n<self.thres):
            return self.p
        elif self.most>1:
            return (1-self.p)*(n-self.thres)/(self.most-self.thres)+self.p
        else:
            return self.p+(n-self.thres)*self.most if self.p+(n-self.thres)*self.most<1 else 1

    #@running_time
    def smlt(self,n:int,e:list,t:int=0,detail:bool=False,times:int=100000) -> float:
        '''
        模拟抽卡

        Parameters
        ---
        - n: 总抽数
        - e: 期望抽卡结果（数组形式表示）
        - t: 未出最高稀有度角色抽数
        - times: 重复模拟次数, 默认为1e5
        '''
        
        if self.up==None:
            self.up=[[[0 for _ in range(len(e))],0,t,0] for _ in range(times)]
        '''
        up[0]: up结果
        up[1]: 总抽数
        up[2]: 该轮抽数
        up[3]: 保底结果
        '''

        if len(self.up)==0:
            return 1

        if tuple([tuple(e),n]) in self.up_result:
            return self.up_result[tuple([tuple(e),n])]

        while self.up[0][1]<n:
            j=0
            while j<len(self.up):
                pt=self.prob(self.up[j][2]+1)
                cache=random.random()
                if cache<pt:                                        #出最高稀有度
                    mg_b=True
                    for _ in range(len(self.p_up)):                 #判断是否是第(k+1)个up
                        if cache*self.p < pt*self.p_up[_]:
                            self.up[j][0][_]+=1
                            self.up[j][2], self.up[j][3]=0,0
                            mg_b=False
                            break
                    if self.mg_type=="mg" and mg_b:
                        if self.up[j][3]==self.mg:                  #非酋的强运！（大保底）
                            for _ in range(len(self.p_up)):
                                if cache*self.p_up[-1] < pt*self.p_up[_]:
                                    self.up[j][0][_]+=1
                                    self.up[j][2], self.up[j][3]=0,0
                                    break
                        else:
                            self.up[j][2]=0
                            self.up[j][3]+=1                        #非酋复活甲（大保底计数）
                    else:
                        self.up[j][2]=0
                    if judge_exp(self.up[j][0],e):
                        del self.up[j]
                    else:
                        self.up[j][1]+=1
                        j+=1
                else:                                               #未出最高稀有度
                    self.up[j][2]+=1
                    self.up[j][1]+=1
                    j+=1

            self.up_result[tuple([tuple(e),self.up[0][1]])]=1-len(self.up)/times
            
            if len(self.up)==0:
                break

        if self.mg_type=="exc" and self.up:
            j=0
            t=n//self.mg
            if t:
                while j<len(self.up):
                    if judge_exp(self.up[j][0],e,t):
                        del self.up[j]
                    else:
                        j+=1

        return eval('%.4f'%(1-len(self.up)/times))
        '''
        up=dict()
        
        for i in range(times):                                  #新狗哥入场
            insur=0                                             #非酋计数器（大保底计数器）
            turn=t                                              #小保底计数器
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

        return eval('%.4f'%(result/times))
        '''

    def clmp_n(self,e:list,target:float=0.95,lower=0,upper=None,fdis=None) -> int:
        '''
        返回达到预期e概率大于target概率的最小抽数n
        '''
        if upper==None:
            upper=sum(e)*int((self.most if self.most>1 else self.thres+round((1-self.p)/self.most))/self.p_up)
        if fdis==None:
            fdis=upper-lower
        n=int(lower+(upper-lower)*(target+0.5)/2)
        p1=self.calc(n,e)
        p2=self.calc(n+1,e)
        #print(lower,upper,n,p1,p2)
        if p1<=target<p2:
            return n+1
        elif p2<target:
            return self.clmp_n(e,target,n,upper,fdis)
        else:
            return self.clmp_n(e,target,lower,n,fdis)

    #@running_time
    def calc_numpy(self, n:int, e:int, t:int=0):
        """
        仅限单up
        """
        upper = (self.most if self.most>1 else self.thres+round((1-self.p)/self.most)) if self.most else n
        insur = self.mg if self.mg else n

        if e in self.result.keys():
            if n<len(self.p_list[e]):
                return sum(self.p_list[e][:n+1])
            else:
                start = len(self.p_list[e])
                cache = self.result[e]
                self.result[e] = numpy.zeros((n+1, e+1, insur+1, upper+1))
                self.result[e][*[slice(_) for _ in cache.shape]] = cache
                self.p_list[e].extend([0 for _ in range(n+1-start)])
        else:
            self.result[e] = numpy.zeros((n+1, e+1, insur+1, upper+1))
            self.result[e][0,0,0,t] = 1
            self.p_list[e] = [0 for _ in range(n+1)]
            start = 1

        self.p1 = numpy.asarray([self.prob(_) for _ in range(1, upper+1)]).reshape(upper,1)
        self.p0 = numpy.asarray([1-self.prob(_) for _ in range(1, upper+1)])
        
        for i in range(start, n+1):
            for j in range(e):
                for k in range(insur+1):
                    rarest_p = numpy.dot(numpy.asarray([self.result[e][i-1,j,k,_] for _ in range(upper)]).reshape(1,upper), self.p1)
                    
                    self.result[e][i,j+1,0,0] += self.p_up[-1] * rarest_p / self.p
                    if k<insur:
                        self.result[e][i,j,k+1,0] += (1 - self.p_up[-1] / self.p) * rarest_p
                    else:
                        self.result[e][i,j+1,0,0] += (1 - self.p_up[-1] / self.p) * rarest_p
                    
                    self.result[e][i,j,k,1:] += self.p0 * self.result[e][i-1,j,k,:-1]
            self.p_list[e][i] = sum([self.result[e][i,e,_,0] for _ in range(2)])
        
        return sum(self.p_list[e])
    
    #@running_time
    def calc_numpy_ups(self, n:int, e:list, wish:Optional[int]= None, t:int= 0):
        """
        多up版本
        """
        upper = (self.most if self.most>1 else self.thres+round((1-self.p)/self.most)) if self.most else n
        insur = self.mg if self.mg else n

        if tuple(e) in self.result.keys():
            if n<len(self.p_list[tuple(e)]):
                return sum(self.p_list[tuple(e)][:n+1])
            else:
                start = len(self.p_list[tuple(e)])
                cache = self.result[tuple(e)]
                self.result[tuple(e)] = numpy.zeros((n+1, *[_+1 for _ in e], insur+1, upper+1))
                self.result[tuple(e)][*[slice(_) for _ in cache.shape]] = cache
                self.p_list[tuple(e)].extend([0 for _ in range(n+1-start)])
        else:
            self.result[tuple(e)] = numpy.zeros((n+1, *[_+1 for _ in e], insur+1, upper+1))
            self.result[tuple(e)][0,*[0 for _ in range(len(e))],0,t] = 1
            self.p_list[tuple(e)] = [0 for _ in range(n+1)]
            start = 1

        self.p1 = numpy.asarray([self.prob(_) for _ in range(1, upper+1)]).reshape(upper,1)
        self.p0 = numpy.asarray([1-self.prob(_) for _ in range(1, upper+1)])

        for i in range(start, n+1):
            for j in itertools.product(*[range(_+1) for _ in e]):
                if not judge_exp(j,e):
                    for k in range(insur+1):
                        rarest_p = numpy.dot(numpy.asarray([self.result[tuple(e)][i-1,*j,k,_] for _ in range(upper)]).reshape(1,upper), self.p1)
                        
                        for n in range(len(e)):
                            self.result[tuple(e)][i,*[((j[_]+1) if ((_==n) and (j[_]<e[_])) else j[_]) for _ in range(len(e))],0,0] += (self.p_up[n] - (self.p_up[n-1] if n else 0)) * rarest_p / self.p
                        if k<insur:
                            self.result[tuple(e)][i,*j,k+1,0] += (1 - self.p_up[-1] / self.p) * rarest_p
                        else:
                            if wish:
                                self.result[tuple(e)][i,*[((j[_]+1) if ((wish==_+1) and (j[_]<e[_])) else j[_]) for _ in range(len(e))],0,0] += (1 - self.p_up[-1] / self.p) * rarest_p
                            else:
                                for n in range(len(e)):
                                    self.result[tuple(e)][i,*[(j[_]+1) if ((_==n) and (j[_]<e[_])) else j[_] for _ in range(len(e))],0,0] += (1 - self.p_up[-1] / self.p) * rarest_p / len(e)

                        self.result[tuple(e)][i,*j,k,1:] += self.p0 * self.result[tuple(e)][i-1,*j,k,:-1]
            
            self.p_list[tuple(e)][i] = sum([self.result[tuple(e)][i,*e,_,0] for _ in range(insur+1)])
        
        return sum(self.p_list[tuple(e)])
    
    #@running_time
    def calc(self,n:int,e:list,t:int=0,rel_exp:int=6) -> float:
        '''
        rel_exp: 小于最大概率分支的10*(-exp)的分支将不再计算
        '''
        if self.up==None and (not self.up_result.keys()):
            self.up=[[tuple([0 for i in range(len(e))]),0,t,0,1]]
        '''
        up[0]: up结果
        up[1]: 总抽数
        up[2]: 该轮抽数
        up[3]: 保底结果
        up[4]: 概率
        '''

        if (self.mg_type=="mg" and (n>=(self.mg+1)*(self.most if self.most>1 else self.thres+round((1-self.p)/self.most))*sum(e)))\
           or (self.mg_type=="exc" and n>=self.mg*sum(e)):
            return 1
        elif tuple([tuple(e),n]) in self.up_result:     #已有计算结果
            return self.up_result[tuple([tuple(e),n])]
        elif not self.up:                               #所有剩余分支均为小概率事件或不可能事件
            return self.up_result.get(tuple([tuple(e),n]),1)
        else:
            cache_dict=dict()
            result=0
            max_p=0                                     #判断rel_exp的小概率事件
            
            i=0
            result=self.up_result.get(tuple([tuple(e),self.up[0][1]]),0)
            
            while self.up[i][1]<=n-1:
                #未抽中最高稀有度
                cache_dict[tuple([self.up[i][0],self.up[i][1]+1,self.up[i][2]+1,self.up[i][3]])]=cache_dict.get(tuple([self.up[i][0],self.up[i][1]+1,self.up[i][2]+1,self.up[i][3]]),0)+self.up[i][4]*(1-self.prob(self.up[i][2]+1))
                #大保底
                if self.mg_type=="mg" and (self.up[i][3]==self.mg): 
                    for j in range(len(e)):
                        cache=[]
                        #判断大保底角色
                        for k in range(len(e)):
                            if j==k:
                                cache.append(self.up[i][0][k]+1)
                            else:
                                cache.append(self.up[i][0][k])
                        #判断是否达到期望
                        if judge_exp(cache,e):                                                                                                                                          
                            cache_p=self.up[i][4]*self.prob(self.up[i][2]+1)*(self.p_up[j] if not j else self.p_up[j]-self.p_up[j-1])/self.p_up[-1]
                            if cache_p>max_p:
                                max_p=cache_p
                            result+=cache_p
                        else:
                            #记录未达到期望记录分支
                            cache_dict[tuple([tuple(cache),self.up[i][1]+1,0,0])]=cache_dict.get(tuple([tuple(cache),self.up[i][1]+1,0,0]),0)+self.up[i][4]*self.prob(self.up[i][2]+1)*(self.p_up[j] if not j else self.p_up[j]-self.p_up[j-1])/self.p_up[-1]
                else:
                    #歪
                    cache_dict[tuple([self.up[i][0],self.up[i][1]+1,0,self.up[i][3]+1])]=cache_dict.get(tuple([self.up[i][0],self.up[i][1]+1,0,self.up[i][3]+1]),0)+self.up[i][4]*self.prob(self.up[i][2]+1)*(1-self.p_up[-1]/self.p)
                    #非大保底
                    for j in range(len(e)):
                        cache=[]
                        #判断up角色
                        for k in range(len(e)):
                            if j==k:
                                cache.append(self.up[i][0][k]+1)
                            else:
                                cache.append(self.up[i][0][k])
                        if judge_exp(cache,e):
                            cache_p=self.up[i][4]*self.prob(self.up[i][2]+1)*(self.p_up[j] if not j else self.p_up[j]-self.p_up[j-1])/self.p
                            if cache_p>max_p:
                                max_p=cache_p
                            result+=cache_p
                        else:
                            cache_dict[tuple([tuple(cache),self.up[i][1]+1,0,0])]=cache_dict.get(tuple([tuple(cache),self.up[i][1]+1,0,0]),0)+self.up[i][4]*self.prob(self.up[i][2]+1)*(self.p_up[j] if not j else self.p_up[j]-self.p_up[j-1])/self.p
                
                if (i+1==len(self.up)):
                    next_up=[]
                    for key in cache_dict.keys():
                        #print(key,cache_dict[key])
                        if rel_exp:
                            if cache_dict[key]>max_p*10**(-rel_exp):
                                cache=list(key)
                                cache.append(cache_dict[key])
                                next_up.append(cache)
                        else:
                            if cache_dict[key]:
                                cache=list(key)
                                cache.append(cache_dict[key])
                                next_up.append(cache)
                    self.up_result[tuple([tuple(e),self.up[i][1]+1])]=result
                    self.up=next_up
                    i=-1
                    cache_dict=dict()

                i+=1

                if not self.up:
                    break

        if self.up and self.mg_type=="exc":
            t=n//self.mg
            if t:
                for case in self.up:
                    if judge_exp(case[0],e,t):
                        result-=case[4]
                
        return eval('%.4f'%result)

    def output_list(self):
        for i in sorted(self.up.keys()):
            print(i,self.up[i])

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

    #@running_time
    def smlt(self,n,res=None,rp=None,times=100000):
        '''
        n: 抽数
        res: 已有收藏品
        rp: 已有重复收藏品
        '''
        
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
        
        return eval('%.4f'%(result/times))

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

if __name__=='__main__':    
    pass
