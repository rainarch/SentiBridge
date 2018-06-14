# coding=utf8


class read_pair():
    '''F:\Corpus_Set\giga\newF\patt_1_result'''
    def __init__(self, path):
        ns_dict = {}
        with open(path + r'/pair_pt', 'rb')as f:
            n = ''
            s = ''
            for line in f:
                if '#' not in line:
                    n, s = line.strip().split('\t')
                    if n not in ns_dict:
                        ns_dict[n] = {}
                        ns_dict[n][s] = {}
                    elif s not in ns_dict[n]:
                        ns_dict[n][s] = {}
                else:
                    patt, count = line.strip().split('\t')
                    patt = patt.strip('#')
                    ns_dict[n][s][patt] = []
                    ns_dict[n][s][patt].append(count)
        self.ns_dict = ns_dict


class PPC():
    '''
    Pair-Patt-Count structure
    '''
    def __init__(self, ns_dict):
        self.get_map(ns_dict)

    def mkdir_record_path(self, path):
        import os
        self.path = path
        path = path.strip()
        isExists = os.path.exists(path + 'Iterative_record')

        if not isExists:
            os.makedirs(path + 'Iterative_record')
            os.makedirs(path + 'Iterative_record/pair_sort_ns')
            os.makedirs(path + 'Iterative_record/pair_sort_pt')
            os.makedirs(path + 'Iterative_record/patt_sort')
            print path + ' 创建成功'
            return True
        else:
            print path + ' 目录已存在'
            return False

    def get_map(self, ns_dict):
        '''
        get map: [pair-patt], [patt-pair], [pair](score), [patt](score)

        :param ns_dict: Entity.str { Emotion.str { Pattern.str { Count.int (It's a three-level hash structure)
        :return:
        '''
        pair_list = []
        patt_dict = {}
        patt_pair_map = {}
        pair_patt_map = {}
        for n in ns_dict:
            for s in ns_dict[n]:
                n_s = n + '\t' + s
                pair_list.append(n_s)
                pair_patt_map[n_s] = {}
                for patt in ns_dict[n][s]:
                    if patt not in patt_dict:
                        patt_dict[patt] = 1.0
                    pair_patt_map[n_s][patt] = float(ns_dict[n][s][patt][0])
                    if patt in patt_pair_map:
                        patt_pair_map[patt][n_s] = float(ns_dict[n][s][patt][0])
                    else:
                        patt_pair_map[patt] = {}
                        patt_pair_map[patt][n_s] = float(ns_dict[n][s][patt][0])
        self.patt_pair_map = patt_pair_map
        self.pair_patt_map = pair_patt_map
        self.pair_list = pair_list
        self.pair_len = len(pair_list)
        self.patt_len = len(patt_dict)
        self.ns_dict = ns_dict
        self.pair_score = dict([(word, 1.) for i, word in enumerate(pair_list)])
        self.patt_score = patt_dict

    def norm(self, score_dict, score_len):
        sum_score = 0.
        for s in score_dict:
            sum_score += score_dict[s]
        for s in score_dict:
            score_dict[s] = score_dict[s] / sum_score * score_len
        return score_dict

    def patt_pair(self):
        for pair in self.pair_patt_map:
            value = 0.
            for patt in self.pair_patt_map[pair]:
                value += self.pair_patt_map[pair][patt] * self.patt_score[patt]
            self.pair_score[pair] = value

    def pair_patt(self):
        for patt in self.patt_pair_map:
            value = 0.
            for pair in self.patt_pair_map[patt]:
                value += self.patt_pair_map[patt][pair] * self.pair_score[pair]
            self.patt_score[patt] = value

    def patt_correct(self):
        self.patt_score['的-'] = 0.0

    def Iterative(self):
        '''
        A complete iteration
        [pair] = [patt-pair] * [patt]
        [patt] = [pair-patt] * [pair]
        :return:
        '''
        # self.patt_correct()

        self.patt_pair()
        self.pair_score = self.norm(self.pair_score, self.pair_len)
        self.pair_patt()
        self.patt_score = self.norm(self.patt_score, self.patt_len)

    def record(self, i):
        '''
        record your result of i-th iterative into path
        :param i: number of iterative
        :return:
        '''
        with open(self.path + r'Iterative_record/pair_sort_ns/' + str(i), 'wb')as f_ns__, \
             open(self.path + r'Iterative_record/pair_sort_pt/' + str(i), 'wb')as f_nspt, \
             open(self.path + r'Iterative_record/patt_sort/'    + str(i), 'wb')as f_patt:

            pair_score = sorted(self.pair_score.iteritems(), key=lambda d: d[1], reverse=True)
            patt_score = sorted(self.patt_score.iteritems(), key=lambda d: d[1], reverse=True)

            for prs in pair_score:
                f_ns__.write(prs[0] + '\t' + str(prs[1]) + '\n')
                f_nspt.write(prs[0] + '\t' + str(prs[1]) + '\n')
                for patt in self.pair_patt_map[prs[0]]:
                    f_nspt.write('#' + patt + '#\t' + str(self.pair_patt_map[prs[0]][patt]) + '\n')
            for pts in patt_score:
                f_patt.write(pts[0] + '\t' + str(pts[1]) + '\n')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='build candidate set')
    parser.add_argument('--path', default='./CCF_data', help='file path')
    args = parser.parse_args()
    # path = './test/'
    if args.path[-1] != '/':
        path = args.path + '/'
    else:
        path = args.path
    p = read_pair(path)
    k = PPC(p.ns_dict)
    k.mkdir_record_path(path)
    for i in range(100):
        k.Iterative()
        k.record(i)

if __name__ == '__main__':
    main()
