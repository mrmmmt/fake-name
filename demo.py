import random
import sqlite3


def random_weight(weight_data):
    '''
    实现加权随机抽样
    weight_data 为一个字典
    key = 样本
    value = 权重
    '''
    total = sum(weight_data.values())  # 权重求和
    ra = random.uniform(0, total)  # 在 0 与权重和之前获取一个随机数 
    curr_sum = 0
    for k in weight_data.keys():
        curr_sum += weight_data[k]
        if ra <= curr_sum:
            return k
    return None


with sqlite3.connect('./fake.db') as conn:
    cursor = conn.cursor()
    sql = 'SELECT lastname, weight FROM lastnames'
    cursor.execute(sql)
    last_name_dict = dict()
    result = cursor.fetchall().copy()
    for i in range(len(result)):
        last_name_dict[result[i][0]] = result[i][1]
    sql = 'SELECT firstname FROM firstnames'
    cursor.execute(sql)
    first_name_lst = [x[0] for x in cursor.fetchall()]
    cursor.close()

name_lst = []

i = 0
while i < 10000:
    last_name = random_weight(last_name_dict)
    first_name = random.choice(first_name_lst)
    name = last_name + first_name
    if name not in name_lst:
        i += 1
        name_lst.append(name)
        print(i, name)
        
        
# df = pd.DataFrame({'名字': name_lst})
# df['序号'] = list(range(1, df.shape[0] + 1))
# df.to_excel('模拟名字.xlsx', index=None)