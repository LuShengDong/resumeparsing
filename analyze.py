# -*- coding:utf-8 -*-
import cutter.bayes_cutter
import cutter.kmeans_cutter
from utils.parser import Parser
import codecs
import utils.cleaner
import json
import jieba
import jieba.analyse
from jieba import posseg as pseg
import re
import logging
import pynlpir
import os
import argparse

pynlpir.open()
jieba.setLogLevel(logging.INFO)
prodict_txt = os.path.join(os.path.abspath(os.path.dirname(__file__)), './pro_dict.txt')
jieba.load_userdict(prodict_txt)


class HeadParser(Parser):
    def parse_time(self, line):
        times = re.findall(r'[0-9]{4}[./年][0-9]{2}', line)
        if len(times) == 0:
            return
        temp_time = []
        for ii, t in enumerate(times):
            temp_time.append(re.sub('[.年]', '/', t))
        if len(temp_time) == 1:
            return {'from': temp_time[0]}
        if len(temp_time) == 2:
            return {'from': temp_time[0], 'to': temp_time[1]}
        if line.find('20') != -1:
            return line

    def parse_company(self, line):
        if line[-2:] == '公司':
            return line


class DescParser(Parser):
    def parse_skills(self, line):
        skills = []
        pairs = []
        match_list = ['prow', 'eng']
        w_tlist = pseg.cut(line)
        temp = []
        lasttag = 'prow'
        for word, tag in w_tlist:
            if tag in match_list:
                if lasttag in match_list:
                    temp.append((word, tag))
                else:
                    pairs.append(temp)
                    temp = [(word, tag)]
            lasttag = tag

        for line in pairs:
            des = ""
            for index, pair in enumerate(line):
                if pair[1] == 'prow' and (index == 0 or index == len(line)-1)\
                        and pynlpir.segment(pair[0])[0][1] != 'noun':
                    continue
                des += pair[0]
            if len(des) != 0:
                if des not in skills:
                    wash_text = jieba.analyse.extract_tags(des, withWeight=True)
                    if sum([pair[1] for pair in wash_text]) > 8.0:
                        skills.append(des)
        return skills


def parse_project(head_data, desc):
    project_info = {'skills': []}
    dp = DescParser()
    hp = HeadParser()
    if hp.parse_time(head_data[0]) is None:
        project_info['project_name'] = head_data[0]
        del head_data[0]
    elif len(head_data) > 1:
        project_info['project_name'] = head_data[1]
        del head_data[1]
    else:
        project_info['project_name'] = "未知"

    for data in head_data:
        for key, value in hp.parse(data):
            project_info[key] = value

    for data in desc:
        for key, value in dp.parse(data):
            if key == 'skills':
                project_info[key] += value
            else:
                project_info[key] = value
    project_info['skills'] = list(set(project_info['skills']))
    return project_info


def analyze(resume):
    title_cluster = [0, 2, 3]
    structure = cutter.bayes_cutter.cut(resume)
    project_key = ''

    for key in structure:
        if key.find('项目') != -1:
            project_key = key

    if project_key == '':
        return structure

    experience = structure[project_key]
    project_list = cutter.kmeans_cutter.cut(experience, title_cluster)
    project_infomation = []
    for head, desc in project_list:
        project_infomation.append(parse_project(head, desc))
    structure[project_key] = project_infomation
    return structure


def summary(structure):
    report = ""
    report += "姓名：{}\n".format(structure['Personal_Info'][0])
    for key in structure:
        if "项目" in key:
            project_info = structure[key]
            for project in project_info:
                report += "-" * 10 + "\n"
                report += "项目名称：{}\n".format(project['project_name'])
                if 'time' in project:
                    if 'to' in project['time']:
                        report += "时间：{} 至 {}\n".format(project['time']['from'], project['time']['to'])
                    else:
                        report += "时间：{}\n".format(project['time']['from'])
                if 'company' in project:
                    report += "所属公司：{}\n".format(project['company'])
                if len(project['skills']) > 0:
                    report += "专业技能：{}\n".format("、".join(project['skills']))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="简历分析器")
    parser.add_argument('-i', help="待分析简历文件，utf-8编码。默认作者本人的简历。",
                        default=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'samples/1.txt'))
    parser.add_argument('-o', help="输出文件，utf-8编码。默认output.json。",
                        default='output.json')
    args = parser.parse_args()
    file_name = args.i
    output_file = args.o
    resume = list(utils.cleaner.clean(file_name))
    result = analyze(resume)
    with codecs.open(output_file, 'wb', 'utf-8') as output:
        json_string = json.dumps(result, ensure_ascii=False, indent=4)
        output.write(json_string)
    print(summary(result))
