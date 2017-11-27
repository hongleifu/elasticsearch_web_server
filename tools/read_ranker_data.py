#  encoding=utf8
#  读取 pageranker、alexa


def read():
    f = open("ranker_data.txt", "r")
    rows_data=[]
    lines = f.readlines()
    for line in lines:
        line=line.strip()
        rows_data.append(line.split('\t'))
    f.close()
    print 'ranker_data read over len:',len(rows_data)
    pr_dict = {}
    alexa_dict = {}
    if rows_data:
        for i in range(1, len(rows_data)):
            row = rows_data[i]
            pr_dict[row[0]] = int(row[1])
            alexa_dict[row[0]] = int(row[2])
    else:
        print 'ranker_data is null !'
    return pr_dict, alexa_dict

