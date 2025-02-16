from pyecharts.charts import Grid

import pandas as pd
from pyecharts.charts import Pie, Bar, EffectScatter,WordCloud,Page
from pyecharts.components import Table
from pyecharts import options as opts
from pyecharts.globals import *
from snownlp import SnowNLP
import matplotlib.pyplot as plt

from pyecharts import options as opts
from pyecharts.charts import WordCloud
from collections import Counter
import jieba
import re



# 读取 CSV 文件
df = pd.read_csv('weibo_myself.csv', usecols=['链接', '名称', '时间', '发表', '分享', '讨论', '点赞'])

# 设置分段
bins1 = [0, 10, 20, 30, 40, 50, 60, 70]
bins2 = [0, 10, 20, 30, 40, 50, 60, 70]
bins3 = [0, 100, 200, 300, 400, 500, 1000, 2000]

# 设置标签
labels1 = ['0-60', '60-120', '120-180', '240-300', '360-420', '420-480', '480-540']
labels2 = ['0-60', '60-120', '120-180', '240-300', '360-420', '420-480', '480-540']
labels3 = ['0-100', '100-200', '200-300', '300-400', '400-500', '500-1000', '1000-2000']


# 将非整数类型的值设为0，并进行离散化处理
shares_list = df['分享'].apply(lambda x: int(x) if str(x).isdigit() else 0)
talks_list = df['讨论'].apply(lambda x: int(x) if str(x).isdigit() else 0)
stars_list = df['点赞'].apply(lambda x: int(x) if str(x).isdigit() else 0)

# 对分享数进行离散化
shares_segments = pd.cut(shares_list, bins1, labels=labels1)
shares_counts = pd.Series(shares_segments).value_counts(sort=False).values.tolist()  # 统计各个分段的个数

# 对讨论数进行离散化
talks_segments = pd.cut(talks_list, bins2, labels=labels2)
talks_counts = pd.Series(talks_segments).value_counts(sort=False).values.tolist()  # 统计各个分段的个数

# 对点赞数进行离散化
stars_segments = pd.cut(stars_list, bins3, labels=labels3)
stars_counts = pd.Series(stars_segments).value_counts(sort=False).values.tolist()  # 统计各个分段的个数

# 打印结果
print("分享数离散化统计:", shares_counts)
print("讨论数离散化统计:", talks_counts)
print("点赞数离散化统计:", stars_counts)


def bar_chart(x_labels, y_counts, title) -> Bar:
    bar = Bar(
        init_opts=opts.InitOpts(theme=ThemeType.CHALK, width="450px", height="350px", chart_id='bar_chart'))  # 初始化条形图
    bar.add_xaxis(x_labels)  # 增加x轴数据
    bar.add_yaxis("数量", y_counts)  # 增加y轴数据
    bar.set_global_opts(
        legend_opts=opts.LegendOpts(pos_left='right'),
        title_opts=opts.TitleOpts(title=title, pos_left='center'),  # 标题
        toolbox_opts=opts.ToolboxOpts(is_show=False),  # 不显示工具箱
        xaxis_opts=opts.AxisOpts(name="数量", axislabel_opts=opts.LabelOpts(font_size=8)),  # x轴名称
        yaxis_opts=opts.AxisOpts(name="数量",
                                 axislabel_opts={"rotate": 0},
                                 splitline_opts=opts.SplitLineOpts(is_show=True,
                                                                   linestyle_opts=opts.LineStyleOpts(type_='solid'))
                                 ),  # y轴名称
    )
    # 标记最大值
    bar.set_series_opts(
        markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="最大值"), ],
                                          symbol_size=35)  # 标记符号大小
    )
    return bar

# 对评论数量进行柱形图生成
# 对评论数量进行柱形图生成
comment_bar = bar_chart(labels2, talks_counts, "评论数量区间分布-柱形图")
comment_bar.render("评论数分布-柱形图.html")
print('生成完毕:评论数分布-柱形图.html')

# 对点赞数量进行柱形图生成
star_bar = bar_chart(labels3, stars_counts, "点赞数量区间分布-柱形图")
star_bar.render("点赞数分布-柱形图.html")
print('生成完毕:点赞数分布-柱形图.html')

# 对分享数量进行柱形图生成
share_bar = bar_chart(labels1, shares_counts, "分享数量区间分布-柱形图")
share_bar.render("分享数分布-柱形图.html")
print('生成完毕:分享数分布-柱形图.html')



score_list = []  # 情感评分值
tag_list = []  # 打标分类结果
pos_count = 0  # 计数器-积极
mid_count = 0  # 计数器-中性
neg_count = 0  # 计数器-消极
count = 0
v_cmt_list=df['发表']#.tolist()
for comment in v_cmt_list:
	comment=str(comment)
	tag = ''
	sentiments_score = SnowNLP(comment).sentiments
	if sentiments_score < 0.4:  # 情感分小于0.4判定为消极
		tag = '消极'
		neg_count += 1
	elif 0.4 <= sentiments_score <= 0.6:  # 情感分在[0.4,0.6]直接判定为中性
		tag = '中性'
		mid_count += 1
	else:  # 情感分大于0.6判定为积极
		tag = '积极'
		pos_count += 1
	score_list.append(sentiments_score)  # 得分值
	tag_list.append(tag)  # 判定结果
df['情感得分'] = score_list
df['分析结果'] = tag_list
# df.to_excel('情感判定结果.xlsx', index=None)  # 把情感分析结果保存到excel文件

def emotion_pie() -> Pie:
    # 画饼图
    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.CHALK, width="450px", height="350px", chart_id='pie1'))
            .add(series_name="评价情感分布",  # 系列名称
                 data_pair=[['积极', pos_count],  # 添加数据
                            ['中性', mid_count],
                            ['消极', neg_count]],
                 rosetype="radius",  # 是否展示成南丁格尔图
                 radius=["30%", "55%"],  # 扇区圆心角展现数据的百分比，半径展现数据的大小
                 )  # 加入数据
            .set_global_opts(  # 全局设置项
            title_opts=opts.TitleOpts(title="短评情感分布-饼图", pos_left='center'),  # 标题
            legend_opts=opts.LegendOpts(pos_left='right', orient='vertical')  # 图例设置项,靠右,竖向排列
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")))  # 样式设置项
    return pie

pie = emotion_pie()
pie.render('情感分布_饼图.html')  # 生成html文件
print('生成完毕:情感分布_饼图.html')




# 示例数据
df['发表'].fillna('', inplace=True)

# 分词
def segment_text(text):
    words = jieba.lcut(text)
    # 使用正则表达式来过滤非中文字符
    words = [word for word in words if re.match('^[\u4e00-\u9fa5]+$', word)]
    return words

df['words'] = df['发表'].apply(segment_text)

# 2. 词频统计
words_list = [word for sublist in df['words'] for word in sublist]
word_freq = Counter(words_list)

# 按词频降序排序
sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

# 选择前120个词语及其出现次数
top_120_words = sorted_word_freq[:120]
x_data = [word for word, freq in top_120_words]
y_data = [freq for word, freq in top_120_words]

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
#
# 生成条形图
plt.figure(figsize=(12, 8))
plt.bar(x_data, y_data)
plt.xlabel('词语')
plt.ylabel('出现次数')
plt.title('微博发表内容词频统计（前120个词语）')
plt.xticks(rotation=90)  # 设置x轴标签旋转角度，以便显示所有词语
plt.tight_layout()  # 自动调整布局，防止重叠
plt.show()


# 3. 准备数据
data = [(word, freq) for word, freq in word_freq.items()]

# 4. 生成词云
def movie_name_wordcloud() -> WordCloud:
    wc = (
        WordCloud()
        .add(series_name="微博名称", data_pair=data, word_size_range=[15, 20], word_gap=5)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="微博名称分析-词云图", title_textstyle_opts=opts.TextStyleOpts(font_size=20)),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    )
    return wc

# 5. 生成HTML文件
movie_name_wordcloud().render("微博名称_词云图.html")

v_title='基于Python的电影数据分析大屏'
def hear_table()->Table:
    table = Table()
    table.add(headers=[v_title], rows=[], attributes={
        "align": "center",
        # "border": False,
        "padding": "2px",
        "style": "background:{}; width:1350px; height:50px; font-size:25px; color:#C0C0C0;".format('#293441')
    })
    return table
    # table.render('大标题.html')
    # print('生成完毕:大标题.html')

page = Page(layout=Page.DraggablePageLayout, page_title="基于Python的电影数据分析大屏")

# Add title to the page
page.add(hear_table())

# Create a grid for the charts
grid = (
    Grid(init_opts=opts.InitOpts(width="100%", height="800px", theme=ThemeType.LIGHT))
    .add(
        bar_chart(labels2, talks_counts, "评论数量区间分布-柱形图"),
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="60%", pos_top="10%", pos_bottom="60%"),
    )
    .add(
        bar_chart(labels3, stars_counts, "点赞数量区间分布-柱形图"),
        grid_opts=opts.GridOpts(pos_left="60%", pos_right="10%", pos_top="10%", pos_bottom="60%"),
    )
    .add(
        bar_chart(labels1, shares_counts, "分享数量区间分布-柱形图"),
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%", pos_top="50%", pos_bottom="10%"),
    )
)

# Add the grid to the page
page.add(grid)

# Add other visualizations to the page
page.add(emotion_pie())
page.add(movie_name_wordcloud())

# Render the page
page.render('大屏.html')


