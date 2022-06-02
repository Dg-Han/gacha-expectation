# gacha-expectation

本程序旨在为抽卡玩家对抽卡预期和预计资源提供信息<br>

## version 1.1

### ver 1.1.1

Update:
* 增加了分析卡池曲线中自定义期望的部分
* 补充了对多up池概率曲线的分析以及计算页面的达成期望结果概率所需抽数的输出
* 对代码进行了一定的拆分
* 对step类中smlt函数进行了重构，现在smlt与calc共用up以及up_result储存
> 注意！在IDE内对于同一卡池同时使用smlt和calc，在切换类型时需要重新定义卡池以清除缓存，或者输入
> ```
> step.up=None
> step.up_result=dict()
> ```
> 手动清除缓存避免数据类型冲突可能导致的错误

### ver 1.1.0

Update: 
* 增加了对于单up池概率曲线的分析，默认输出up期望为1,2,3时的概率曲线
* 补充了初始抽数的参数输入
* 对输入合法性判断的结构逻辑进行了改写<br>

## version 1.0

### ver 1.0.2
<details>
<summary>Little Updates</summary>
  
* 增加了对于不同达成目标期望的文案
* 一定的UI更改
* 完善补充了固定概率卡池模型保存/删除模板功能
  </details>

### ver 1.0.1
Update: 对达成期望结果概率所需抽数的运算进行了优化，避免了重复运算，加快计算速度<br>

### ver 1.0.0
Update:
* 增加了对于单up卡池抽卡期望对应达成概率的所需抽数计算功能<br>

可通过概率递增的UI直接输入，也可在主体程序结束运行后在IDE内输入<br>
```
step(p,p_up,ups,thres,most,mg).interplt(e,target=0.95,lower=0,upper=None)
```
>e为抽卡期望结果（数组形式）<br>
>target为达成概率<br>
>lower, upper为抽数上下界，upper=None时会自动进行初始化<br>

结果返回最小的达成期望概率为95%的抽数<br>

* 发布第一个正式可运行文件版本<br>

## ver 0.x
### version 0.1.7.0
Update: 增加了对于收藏品抽卡的支持以及相应的UI构建<br>
可通过菜单栏切换至收藏品类型进行全收藏概率计算，也可在主体程序结束运行后在IDE内输入<br>
```
collection(num,p,cost,value).smlt(n,res,rp)
```
>num为收藏品件数<br>
>p为收藏品获得概率，以列表的形式分不同稀有度等级输入
>>E.g. [16,0.95]代表对于某稀有度等级中有18件收藏品，获得该稀有度等级收藏品的总概率为0.95.<br>
>>或者[2,0.04,0.01]代表对于某稀有度等级中有2件收藏品，它们的获取概率分别为0.04, 0.01.<br>
>
>cost为兑换new收藏品时所需token数，以列表形式输入，长度与稀有度等级相同<br>
>value为获得重复收藏品时获得token数，以列表形式输入，长度与稀有度等级相同<br>
>n为总抽数<br>
>res为已有收藏品情况，以列表形式输入，长度与稀有度等级相同<br>
>rp为重复收藏品情况，可直接输入token数，也可以列表形式输入，长度与稀有度等级相同<br>

<details>
<summary>代码示例</summary>

E.g. 对于代码
```
collection(18,[[16,0.95],[2,0.04,0.01]],[4,20],[1,5]).smlt(30,[0,0],0)<br>
```
其模拟收藏品抽卡情况为:<br>
收藏品共有18件，分为两个稀有度等级，N为16件，获得概率相等，N等级收藏品获得概率95%；R为2件，获得概率分别为4%和1%。<br>
如果希望兑换未获得的N级收藏品需要4个代币，兑换未获得的R级收藏品需要20个代币。<br>
如果重复获得N级收藏品可以获得1个代币，重复获得R级收藏品可以获得5个代币。<br>
计划在这个卡池投入30抽，且尚未获得任何收藏品和重复收藏品。<br>
</details>

结果返回达成全收藏的概率（保留四位小数）<br> 

### version 0.1.6
Update: 增加了递推算法计算期望的功能。目前仅对单up池开放，多up池因耗时较长暂未使用<br>
如需使用递推算法计算期望，可在主体程序结束运行后（即关闭窗体）在IDE内定义卡池参数后输入<br>
以明日方舟双up池为例: 
```
mrfz=step(0.02,0.7,2,50,99,0)
mrfz.calc(n,e,rel_exp=6)
```
>n为总抽数<br>
>e为抽卡期望，以数组形式输入，例: [2]; [1,1]<br>
>rel_exp为剪枝精度，概率低于最大概率分支的10^(-rel_exp)的概率分支将不再计算。如输入0则无剪枝<br>
>>警告! 对于多up池请谨慎输入参数exp的值，否则会由于极端小概率分支导致时间复杂度原地爆炸

### version 0.1.5
Update: 增加菜单栏和切换卡池类型（现支持递增概率模型和固定概率模型）<br>

### version 0.1.4
Update: 构建UI界面，增加自定义抽卡模型导入导出功能<br>
发布第一版可运行文件exe<br>

使用说明：当up角色数多于1个时，期望抽卡各角色数量用逗号分隔（不需空格）<br>

### version 0.1.3
<details>
<summary>已废弃的文本交互接口Update</summary>
Update: 构建了新的IO接口，现在运行程序可选择一种类型卡池进行抽卡预期测算<br>
对于部分输入增加了合法性判断，在输入不合法数据时会提示合法输入格式<br>
</details>

### version 0.1.2
Update: 增加了程序的兼容性，现可对类似于明日方舟双up池等多up池的抽卡模型进行支持（暂不支持周年庆中副up，即某干员为其他干员几倍出率）<br>
现在在主体程序结束运行后（即是否继续后选择n）可以在IDE内输入
```
step(p,p_up,ups,thres,most,mg).smlt(n,e,times=100000)
```
>p为最高稀有度角色出率<br>
>p_up为up角色占最高稀有度角色出率的比例<br>
>ups为up角色数量<br>
>thres为触发保底机制的抽数下限<br>
>most为必出抽数<br>
>>也可输入触发保底机制后每次递增的概率<br>
>
>mg为大保底歪几必出（如无大保底机制输入0）<br>
>n为总抽数<br>
>e为期望抽卡结果（数组形式）<br>
>>E.g. 单up池中期望抽出三个up角色：e=[3]<br>
>>     双up池中期望抽全两个up角色：e=[1,1]<br>
>
>times为模拟次数（默认为1e6）<br>

结果返回达到期望结果的概率<br>

### version 0.1.1
Update: 更改了程序结构，在原有内容的基础上增加了对界限触发可变概率保底和固定概率有保底的抽卡模型的支持<br>
现在在主体程序结束运行后（即是否继续后选择n后）可以在IDE内输入
```
bound(p,p_up,most).prob(n)
```
>p为最高稀有度角色出率<br>
>p_up为up角色出率<br>
>most为硬保底抽数<br>
>n为总抽数<br>

结果返回达到目标up数的频率（保留四位小数）<br>

### version 0.1.0
`gacha.py`程序主体运行为原神抽卡计算器，通过大样本频率趋近于概率的方式进行相应概率计算<br>
