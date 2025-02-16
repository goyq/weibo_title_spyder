## 项目介绍
本spyder项目针对weibo相关话题的数据爬取以及数据可视化，本话题为[网恋](https://s.weibo.com/weibo?q=%E7%BD%91%E6%81%8B)和[婚恋意愿](https://s.weibo.com/weibo?q=%E5%A9%9A%E6%81%8B%E6%84%8F%E6%84%BF)，旨于观察分析对网恋的相关数据分析。<br />

本代码均个人独立完成.

## 项目流程
### 1.话题为“网恋”的爬取
先爬取数据，[weibo_wanlian.py](https://github.com/goyq/weibo_title_spyder/blob/main/weibo_wanlian.py)，存储到weibo_wanlian_myself.csv.<br />

进行统计分析，[weibo_wl_bi.py](https://github.com/goyq/weibo_title_spyder/blob/main/weibo_bi.py) ,针对数据利用相关Python库进行统计柱状图显示、情感分析、分词统计词频、大屏展示等.

### 2.话题为“婚恋意愿”的爬取
先爬取数据，[weibo_hunlianyiyuan.py](https://github.com/goyq/weibo_title_spyder/blob/main/weibo_hunlianyiyuan.py)，存储到weibo_wanlian_myself.csv.<br />

进行统计分析，[weibo_hunlianyiyuan_bi.py](https://github.com/goyq/weibo_title_spyder/blob/main/weibo_hunlianyiyuan_bi.py) ,针对数据利用相关Python库进行统计柱状图显示、情感分析、分词统计词频、大屏展示等.


## 备注
.json文件为空.<br />
test.py 为中途插叙使用的测试代码，无实用.<br />
使用的库和方法以及相关代码注释都在代码中.

### 使用手册

关于获取此模板

> $ git clone https://github.com/goyq/weibo_title_spyder.git


## License
Apache License 2.0
