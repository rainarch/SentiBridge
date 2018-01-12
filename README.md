# SentiBridge

《SentiBridge: 中文实体情感知识库》/ SentiBridge: A Knowledge Base for Entity-Sentiment Representation 

本词典包含：实体/属性—情感词。例如：“长城  宏伟”、“性价比  高”、“价格  高”。主要目的是刻画人们是怎么描述某个实体的，例如大家通常用 宏伟 来形容长城。

目前词典包含三个领域语料的抽取结果：新闻、旅游、餐饮，共计30万对。

## 文件说明
每个文件夹中包含两种文件
1. 前缀pair_sort代表排序得到的结果:

  * pair_sort_[m,n]，指的是从m%到n%的排序部分

  * 数据形式是：实体/属性  情感词  收敛分数

2. 前缀pair_mine代表提炼得到的结果:
  * 数据形式是：实体/属性  情感词  相似度分数1  相似度分数2

  * pair_mine后面的数字是提炼算法得到的结果中，保证正确率取的分数值。即文本中所有分数1和2，都必须高于该值并保留的结果

## 领域说明

1. 新闻领域(Gigaword新闻语料)：
  * pair_sort_[0,1]，正确率统计92%，数量11.9w个
  * pair_mine_0.25，正确率统计90%，数量1.7w个

2. 旅游领域(旅游用户评论)：
  * pair_sort_[0,1]，正确率统计98%
  * pair_sort_[1,2]，正确率统计94%
  * pair_sort_[2,3]，正确率统计90%
  * 以上总计8w个
  * pair_mine_0.2，正确率统计90%，数量5624个

3. 餐饮领域（餐饮用户评论）：
  * pair_sort_[0,1]，正确率统计92%，数量9.3w个
  * pair_mine_0.2，正确率统计90%，数量5.2w个


## 代码
整理中


## 声明和参考文献
1. SentiBridge数据仅供学术研究使用，商用请联系我们获取授权。
2. 文章
  * 卢奇, 陈文亮. 大规模中文实体情感知识的自动获取, 中文信息学报, 已录用2018-1
  * LU Qi, CHEN Wenliang, Automatically Building a Large Scale Dictionary of Chinese Entity Sentiment Expressions, Journal of Chinese Information Processing, Accepted for publication (2018-1).

