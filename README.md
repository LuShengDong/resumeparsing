# 简易中文简历分析器
作者：Shengdong Lu

github repository：https://github.com/LuShengDong/resumeparsing.git

## 使用方法
1. 安装 python 3.5
2. 在项目根目录（resumeparsing）下运行 ``pip3 install -r requirment.txt`` 安装所需模块。
3. 运行 ``pynlpir update ``激活模块
3. 运行``python analyze.py [-i inputFile] [-o outputFile]``
4. 程序将分析指定简历。在控制台打印项目经历简报，并将结构化简历输出到指定的输出文件。输出文件默认为当前目录下的output.json

## 项目原理
### 1. 格式化
将简历中所有内容分割为行。分割标准：tab符号或连续两个以上的空格。
### 2. 节段分割
使用朴素贝叶斯分类器识别某行是否为节段标题，以节段标题为分割点，将节段标题之间的内容识别为前一个节段的内容。
### 3. 项目标题识别
选出标题带有“项目”二字的阶段内容，作为简历项目经验部分。
使用用无监督学习（K-means）在项目经验中训练，将项目标题所属类别构建为标题类列表。
判断每一行是否属于项目标题类对项目标题进行识别。
### 4. 项目信息提取
继承分析器类（Parser）, 编写解析规则，从项目头数据和描述数据中提取关键信息。
analyze模块实现了项目时间，所属公司，技能列表的提取，也可以根据需要拓展提取规则。

## 项目结构
1. cutter: 简历分割器：贝叶斯分割器以及kMeans分割器所在模块
2. samples：示例简历，有去除了格式的txt格式简历（本人简历）
3. spiders：网络爬虫，用于构建训练数据，拓展分词词典。
4. utils：工具集， 包括格式化，分析器原型，词典提取器（其中词典提取器代码来自https://blog.csdn.net/zhangzhenhu/article/details/7014271 ， 作者：zhangzhenhu）
5. pro_dict.txt: 构造的专业词汇词典，用于识别简历中专业词汇。

