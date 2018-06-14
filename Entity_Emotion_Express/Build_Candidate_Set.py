# coding=utf-8

import re


class data_line():

    def __init__(self, line):
        self.line = line
        if ' 难_a [^ ]{1,15}_v[ ]{0,1}' or ' 容易_a [^ ]{1,15}_v[ ]{0,1}' in line:
            self.pre_line()

    def pre_line(self):
        '''
        很_d 难_a 看到_v 日照_n 金山_nr 的_uj 美景_n 了_ul
        '''
        res = re.findall(' 容易_a [^ ]{1,15}_v[ ]{0,1}| 难_a [^ ]{1,15}_v[ ]{0,1}', self.line)
        for _ in res:
            tmp = _.replace('_a ', '')
            tmp = tmp.replace('v', 'a')
            self.line = self.line.replace(_, tmp)


class Data2NS_dict():
    noun_dict = {'n': '', 'ns': '', 'vn': '', 'nz': '', 's': '', 'nr': ''}
    sent_dict = {'a': ''}

    def __init__(self):
        self.ns_dict = {}

    def Read_ORI2POS(self, path):
        import jieba.posseg as pseg
        with open(path + '/data.ori', 'rb')as f,\
             open(path + '/data.ori.pos', 'wb')as fw:
            for line in f:
                words = pseg.cut(line.strip())
                for w in words:
                    fw.write(w.word.encode('utf8') + '_' + w.flag.encode('utf8') + ' ')
                fw.write('\n')

    def Read_POS2SEG(self, path):
        import re
        r = ' ._x| \._m| \.._m| \…_x| \..._m| 。_x| ！_x| !_x| \?_x| ？_x| ~_x| ,_x| ，_x| ；_x| ;_x| :_x| ：_x| \*_x| _x|  _x'
        k = '[^ ]{0,10}_x|\.{1,50}_m'
        with open(path + '/data.ori.pos', 'rb')as f,\
             open(path + '/data.ori.pos.seg', 'wb')as fw:
            for line in f:
                a = line.strip()
                b = re.split(r, a)
                # b = a.split(k)
                for one in b:
                    if one == '' or one == ' ' or one == '  ' or one == '   ':
                        break
                    else:
                        c = one.strip()
                        fw.write(c + '\n')

    def Read_SEG2NSD(self, path):
        with open(path + '/data.ori.pos.seg', 'rb')as f:
            for line in f:
                line = data_line(line).line
                N_list = []
                S_list = []
                word_list = []
                tag_list = []
                line_list = line.strip().split()
                N = len(line_list)
                for w_t in line_list:
                    if len(w_t.split('_')) != 2:
                        print(line)
                        word_list.append('Error')
                        tag_list.append('Error')
                    else:

                        w, t = w_t.split('_')
                        word_list.append(w)
                        tag_list.append(t)
                for i in range(N):
                    if tag_list[i] in self.noun_dict:
                        N_list.append(i)
                    elif tag_list[i] in self.sent_dict:
                        S_list.append(i)
                if N_list and S_list:
                    self.make_nsdict(word_list, N_list, S_list)

    def make_nsdict(self, word, N_list, S_list):
        for n in N_list:
            # if word[n] not in ns_dict:
            #     ns_dict[word[n]] = {}
            for s in S_list:
                if (1 < n - s < 6) or (1 < s - n < 6):
                    if word[n] not in self.ns_dict:
                        self.ns_dict[word[n]] = {}
                    if word[s] not in self.ns_dict[word[n]]:
                        self.ns_dict[word[n]][word[s]] = {}
                    if n > s:
                        patt = ' '.join(word[s + 1: n]) + '+'
                    else:
                        patt = ' '.join(word[n + 1: s]) + '-'
                    if patt not in self.ns_dict[word[n]][word[s]]:
                        self.ns_dict[word[n]][word[s]][patt] = 0.
                    self.ns_dict[word[n]][word[s]][patt] += 1.

    def NSD_write(self, ns_dict, path):
        path_ns = path + '/pair_ns'
        path_pt = path + '/pair_pt'
        with open(path_ns, 'wb')as f1,\
             open(path_pt, 'wb')as f2:
            for n in ns_dict:
                for s in ns_dict[n]:
                    f1.write(n + '\t' + s + '\n')
                    f2.write(n + '\t' + s + '\n')
                    # f3.write(n+'\t'+s+'\n')
                    for p in ns_dict[n][s]:
                        f2.write('#' + p + '#\t' + str(ns_dict[n][s][p]) + '\n')
                        # f3.write('#' + p +'#\t'+str(ns_dict[n][s][p][0])+'\n')
                        # for c in ns_dict[n][s][p][1:]:
                            # f3.write('###\t'+c+'\n')

    def noise_del(self):
        self.noise('是', self.ns_dict)
        self.noise('说', self.ns_dict)
        self.noise('时候', self.ns_dict)
        self.noise('人', self.ns_dict)
        self.noise('免费', self.ns_dict)
        self.noise('美', self.ns_dict)
        self.noise('会', self.ns_dict)

        # del self.ns_dict['是']
        # del self.ns_dict['说']
        # del self.ns_dict['时候']
        # del self.ns_dict['人']
        # del self.ns_dict['免费']
        # del self.ns_dict['美']
        # del self.ns_dict['会']

        for n in self.ns_dict:
            self.noise('最', self.ns_dict[n])
            self.noise('不', self.ns_dict[n])
            self.noise('很', self.ns_dict[n])
            for s in self.ns_dict[n]:
                self.noise('的-', self.ns_dict[n][s])
                self.noise('和-', self.ns_dict[n][s])
                self.noise('和+', self.ns_dict[n][s])
                self.noise('而+', self.ns_dict[n][s])
                self.noise('而-', self.ns_dict[n][s])
                self.noise('又+', self.ns_dict[n][s])
                self.noise('又-', self.ns_dict[n][s])
                self.noise('而且+', self.ns_dict[n][s])
                self.noise('而且-', self.ns_dict[n][s])

    def noise(self, str, dict):
        if str in dict:
            del dict[str]


def main():
    import argparse
    parser = argparse.ArgumentParser(description='build candidate set')
    parser.add_argument('--path', default='./CCF_data', help='file path')
    args = parser.parse_args()
    path = args.path.rstrip('/')
    # path = './test'
    NSD = Data2NS_dict()
    NSD.Read_ORI2POS(path)
    NSD.Read_POS2SEG(path)
    NSD.Read_SEG2NSD(path)
    NSD.noise_del()
    NSD.NSD_write(NSD.ns_dict, path)


if __name__ == '__main__':
    main()
