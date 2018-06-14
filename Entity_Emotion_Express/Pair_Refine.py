# coding=utf8
from __future__ import division


def f(path, sim):
    with open(path, 'rb')as fp, open(path + '_' + str(sim), 'wb')as fw:
        for line in fp:
            p_l = line.strip().split('\t')
            if float(p_l[2]) < sim:
                break
            else:
                fw.write(line)


def di(f):
    dc = {}
    for line in f:
        n, s, score, c = line.strip().split('\t')
        dc[n + '\t' + s] = float(score)
    return dc


def main():
    import argparse
    parser = argparse.ArgumentParser(description='build candidate set')
    parser.add_argument('--n_path', default='./CCF_data/pair_mine_n_result', help='file path')
    parser.add_argument('--s_path', default='./CCF_data/pair_mine_s_result', help='file path')
    parser.add_argument('--sim', type=float, default=0.3, help='file path')

    parser.add_argument('--result_path', default='./CCF_data/pair_mine_result', help='file path')
    args = parser.parse_args()
    f(args.n_path, args.sim)
    f(args.s_path, args.sim)
    with open(args.n_path + '_' + str(args.sim), 'rb')as fn,\
         open(args.s_path + '_' + str(args.sim), 'rb')as fs,\
         open(args.result_path, 'wb')as fw:
        d1 = di(fn)
        d2 = di(fs)
        for pair in d1:
            if pair in d2:
                fw.write(pair + '\t' + str(d1[pair]) + '\t' + str(d2[pair]) + '\n')


if __name__ == '__main__':
    main()

