import pandas as pd
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from collections import Counter
import jieba
import re

df = pd.read_csv('weibo_wanlian_myself.csv', usecols=['链接', '名称', '时间', '发表', '分享', '讨论', '点赞'])


# 示例数据
df['发表'].fillna('', inplace=True)
# 1. 分词并删除非中文词语
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

# 选择前120个词语及其出现次数   '''可以改
top_120_words = sorted_word_freq[:120]
x_data = [word for word, freq in top_120_words]
y_data = [freq for word, freq in top_120_words]

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

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