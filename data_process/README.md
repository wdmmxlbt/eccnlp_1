# Data Process Introduction for ECCNLP

## 版本号说明
1. 2.0 正则过滤原版本
2. 2.1 正则过滤现版本1，Actype1：业绩归因的回答，Actype123：前三类回答
3. 2.2 正则过滤现版本2，其他同2.1

## 数据集：第一第二期手工标注数据汇总-20221220.xlsx

__描述性统计__
| 是否为业绩归因| 数量 | 
|:------------:|:----:|
|    正类样本   | 3760 |
|    负类样本   | 21111|
|    总计       | 24871|

__归因不在回答文本__
| 原因归属在回答文本中| 数量 | 
|:------------:|:----:|
|    负类样本   | 134  |
|    正类样本   | 3626 |
|    总计       | 3760 |

## 数据预处理
1. 将非业绩归因回答进行正则过滤，去除部分标注为0的样本。
2. 对回答文本进行切分，对于原句的【是否为业绩归因回答】标注为1的子句，如果原因归属在子句中，则该子句标注为1，否则标注为0；对于原句【是否为业绩归因回答】标注为0的子句，保持标注为0。
3. 划分训练集、验证集和测试集。
4. 数据集采样方法（上/下）

__数据集划分:__
| 数据集 | 数据量 |
| :---: | :----: |
| 训练集 |        |
| 验证集 |       |
| 测试集 |       |