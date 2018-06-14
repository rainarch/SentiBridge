# coding=utf8

path = './CCF_data/data.ori.pos'

with open(path, 'rb')as f, open(path + '.w2v', 'wb')as fw:
    for line in f:
        line_list = line.rstrip('\n').split()
        line_cws = []
        for _ in line_list:
            tmp = _.split('_')
            if len(tmp) == 2:
                line_cws.append(tmp[0])
        fw.write(' '.join(line_cws) + '\n')
        
