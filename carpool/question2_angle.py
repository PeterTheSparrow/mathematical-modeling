import math

'''
将地理经纬度转换成笛卡尔坐标系
:param lat: 纬度
:param lng: 经度
:param r: 地球半径
:return: 返回笛卡尔坐标系
'''
def getDescartes(lng, lat, r=6400):
    theta = (math.pi * lat) / 180
    phy = (math.pi * lng) / 180
    x = r * math.cos(theta) * math.cos(phy)
    y = r * math.cos(theta) * math.sin(phy)
    z = r * math.sin(theta)
    return [x,y,z]


'''
:param l1: 经纬度（列表）
:param l2: 顶点经纬度
:param l3: 经纬度
:return: 返回角度值。
'''
def getAngle(l1, l2, l3):
    p1 = getDescartes(l1[0], l1[1])
    p2 = getDescartes(l2[0], l2[1])
    p3 = getDescartes(l3[0], l3[1])

    _P1P2 = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)
    _P2P3 = math.sqrt((p3[0] - p2[0]) ** 2 + (p3[1] - p2[1]) ** 2 + (p3[2] - p2[2]) ** 2)
    P = (p1[0] - p2[0]) * (p3[0] - p2[0]) + (p1[1] - p2[1]) * (p3[1] - p2[1]) + (p1[2] - p2[2]) * (p3[2] - p2[2])

    angle = (math.acos(P / (_P1P2 * _P2P3)) / math.pi) * 180

    # angle = abs(angle)
    return angle


'''
作用：通过经度纬度计算两点距离
'''
def distanceCalculator(jingduA, weiduA, jingduB, weiduB):
	R = 6371.393
	Pi = math.pi

	a = (math.sin(math.radians(weiduA / 2 - weiduB / 2))) ** 2
	b = math.cos(weiduA * Pi / 180) * math.cos(weiduB * Pi / 180) * (
		math.sin((jingduA / 2 - jingduB / 2) * Pi / 180)) ** 2

	L = 2 * R * math.asin((a + b) ** 0.5)

	# 单位是米
	return L * 1000


'''
获得一个list：[0,1,2,3,4,5,6]
判断的是每个人和汽车的位置
para: list_to_judge 传入的接人顺序
para: case_info 每个人的位置信息

对角度计算特征值，返回特征值
'''
def angleJudgement(list_to_judge,case_info):
    list_to_judge = [0] + list_to_judge
    points = []
    distances_para = []
    edges = []
    angles = []

    # mod3==0,mod3==1的位置分别放的是经度和维度
    for i in range(0,7):
        j = list_to_judge[i]
        points.append([case_info[3*j],case_info[3*j+1]])

    for i in range(0,5):
        angles.append(getAngle(points[i],points[i+1],points[i+2]))

    # 计算边的长度
    for i in range(0,6):
        edges.append(distanceCalculator(points[i][0],points[i][1],points[i+1][0],points[i+1][1]))

    for i in range(0,5):
        distances_para.append(edges[i+1])

    # return angles
    # 计算特征值
    flag = 0

    eason = 90
    for i in range(len(distances_para)):
        if angles[i] < eason:
            # flag += (1000/distances_para[i]) *math.sin(angles[i])*(1/math.sin(eason))
            x =  (1000 / distances_para[i]) / math.cos(angles[i])
            if x > 1:
                flag += 1
            else:
                flag += x
        else:
            flag += 1

    return flag;

'''
角度筛选函数：
获得60个原始序列，进行筛选
选出最好的20个
'''
def listFilter(origin_prefer_list, case_info):
    # case_info 信息格式处理
    new_case_info = []
    car_info = case_info[18:21:]
    new_case_info += car_info
    new_case_info += case_info[0:18]

    # # for debug
    # for i in range(len(origin_prefer_list)):
    #     angleJudgement(origin_prefer_list[i],new_case_info)

    new_prefer_list = []

    flag_list = []

    # 筛选出20个
    for i in range(len(origin_prefer_list)):
        flag_list.append(angleJudgement(origin_prefer_list[i],new_case_info))


    combined = [list(i) for i in zip(flag_list,origin_prefer_list)]
    combined.sort(key=lambda ele: ele[0], reverse=False)


    for i in range(len(combined)):
        new_prefer_list.append(combined[i][1])
        # if i < 20:
        #     print(combined[i])

    new_prefer_list = new_prefer_list[0:20]

    return new_prefer_list

    # for i in range(len(origin_prefer_list)):
    #     a = angleJudgement(origin_prefer_list[i],new_case_info)
    #     print(i, a)
    #
    # return origin_prefer_list

'''
贪心算法
输出格式：[1,2,3,4,6,5]，没有初始的0！
使用贪心算法，选出符合条件的路径：
【算法描述】
【起点】：汽车的位置
使用一个候选list，开始其中存放的是三个人的起点
每当一个人被接走，我们就将其对应的终点放到候选list中
当候选list为空，结束程序
每次从候选list中取出来一个数，我们就将其加入ideal_travel_list中
'''
def greedyFilter(case_info):
    # case_info 信息格式处理
    new_case_info = []
    car_info = case_info[18:21:]
    new_case_info += car_info
    new_case_info += case_info[0:18]
    case_info = new_case_info

    ideal_travel_list = []
    candidate_list = [1,2,3]

    current_position = [case_info[0],case_info[1],0]   # 经度纬度，初始为汽车的位置
    next_position = []  # 经度纬度，编号

    while len(candidate_list)>0:
        min_length = float('inf')
        for i in range(len(candidate_list)):
            index = candidate_list[i]
            if 1<=index<=3: # 1->3,2->9,3->15
                jindu = case_info[(index-1)*6+3]
                weidu = case_info[(index-1)*6+3+1]
            else:   # 4->6,5->12,6->18
                jindu = case_info[(index-3)*6]
                weidu = case_info[(index-3)*6+1]
            dis = distanceCalculator(jindu,weidu,current_position[0],current_position[1])
            if min_length > dis:
                min_length = dis
                next_position = [jindu,weidu,index]

        # 如果离开候选人位置的是123，则加入456
        if 1<= next_position[2] <=3:
            candidate_list.append((next_position[2]+3))
        candidate_list.remove(next_position[2])
        current_position = next_position
        ideal_travel_list.append(next_position[2])


    return ideal_travel_list


'''
折线长度计算函数
参数：
（1）list_to_calculate,[0,1,2,3,5,4,6]
（2）case_info 每个人的位置信息
'''
def lengthCalculator(list_to_judge, case_info):
    length = 0
    points = []
    list_to_judge  = [0] + list_to_judge

    car = case_info[0:3]
    case_info = case_info[3:]
    case_info = case_info + car

    # mod3 == 0,1分别存放的是经度和纬度
    for i in range(0,7):
        j = list_to_judge[i]
        if j == 0:
            points.append([case_info[18],case_info[19]])
        elif 1<=j<=3:   # 1->0,2->6,3->12
            points.append([case_info[6*j-6],case_info[6*j-5]])
        else:   # 4->3,5->9
            points.append([case_info[6 * j - 21], case_info[6 * j - 20]])

    # 计算边的长度
    for i in range(6):
        length += distanceCalculator(points[i][0],points[i][1],points[i+1][0],points[i+1][1])
    return length


'''
筛选都是在case_info确定的情况下，筛选raw_prefer_list
作用：折线距离筛选，将prefer_list根据折线总长度，进一步筛选出10个
参数：
（1）待筛选的raw_prefer_list
（2）case_info
返回值：
（1）筛选后的cooked_prefer_list
'''
def secondFilter(raw_prefer_list, case_info):
    cooked_prefer_list = []
    flag_list = []  # 装我们计算出的折线距离（特征值），用于排序

    # case_info 信息格式处理
    new_case_info = []
    car_info = case_info[18:21:]
    new_case_info += car_info
    new_case_info += case_info[0:18]

    # 筛选出10个
    for i in range(len(raw_prefer_list)):
        flag_list.append(lengthCalculator(raw_prefer_list[i],new_case_info))

    combined = [list(i) for i in zip(flag_list,raw_prefer_list)]
    combined.sort(key=lambda ele:ele[0],reverse=False)

    for i in range(len(combined)):
        cooked_prefer_list.append(combined[i][1])
        # # for debug
        # if i < 10:
        #     print(combined[i])

    cooked_prefer_list = cooked_prefer_list[0:10]
    return cooked_prefer_list


def main():
    pass


if __name__ == '__main__':
    main()