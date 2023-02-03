import copy

import question1
import question2_angle
import help
# import question2
'''
moving man
人是可以移动的。
人的出发位置为圆心，半径为200米以内的路口，人移动到路口，就增加了很多新的选项，重新寻找最短的算法。【原本的定义】

沿着路网，人行走距离小于200米能到达的路口【这个是不是更合理】——同时我们注意到，人是可以验证马路两个方向走的。

func1：给出一个人的出发位置，找半径200米内的路口

修改算法：
prefer_info是不变的，假设还是[0,1,2,3,4,5,6]
但是1，2，3对应的道路的序号是可选择的——循环一层层套。
'''

'''
作用：查找函数。根据路的编号，查询路的两个端点编号
参数：
index：路的编号
chart：读取文件1得到的道路信息列表
返回值：
（1）[1][4]是start和end
'''
def finder(index, chart):
	m = []
	for i in range(len(chart)):
		if(chart[i][0] == float(index)):
			m = chart[i]
			break
	return m

'''
参数：
（1）人出发位置的经纬度0，1, 人出发位置的路的编号2
（2）路网信息
返回值：
（1）路口编号，如果返回-1则表示没有符合条件的路口
'''
def findCrossing(human_position, road_info):
    max_walking_dis = 200
    intended_crossing = -1

    current_road = finder(human_position[2],road_info)
    # current_road[1],current_road[4]分别计算

    # current_road[1]
    distance1 = question2_angle.distanceCalculator(human_position[0],human_position[1],current_road[2],current_road[3])
    # current_road[4]
    distance2 = question2_angle.distanceCalculator(human_position[0],human_position[1],current_road[5],current_road[6])

    if distance1 < distance2 and distance1 <= max_walking_dis:
        intended_crossing = current_road[1]
        return intended_crossing
    elif distance2 < distance1 and distance2 <= max_walking_dis:
        intended_crossing = current_road[4]
        return intended_crossing

    # 返回-1代表没有符合条件的路口
    return intended_crossing

'''
作用：给出一个路口，查询这个路口接通的道路
参数：
（1）路口编号
'''
def findRoad():
    pass

'''
作用：提供一个点的编号（路口的编号），返回经纬度
'''
def dotLocator(index,road_info):
	for i in range(len(road_info)):
		if road_info[i][1] == index:
			return road_info[i][2], road_info[i][3]
		elif road_info[i][4] == index:
			return road_info[i][5], road_info[i][6]

# '''
# 参数：
# （1）prefer_info:[0,1,2,3,4,5,6]
# （2）case_info
# （3）路网信息
# 返回值：
# （1）new_case_info_list：[[形式和原先的case_info一样],[],[],[],[],[]...]
# '''
# def advancedAlgo(prefer_info, case_info, road_info):
#     crossing_dict = help.dictionMaking()
#
#     new_case_info_list = []
#     raw_case_info = []  # 按顺序存放每个点对应的路口
#     cooked_case_info = []   # 按顺序存放
#     # 遍历prefer_info中的每一个点，对应去case_info中找到路
#     # 根据路调用findCrossing查路口
#     # 根据返回值修改case_info
#
#     # 优化只需要优化出发点
#     for i in range(len(prefer_info)):
#         n = prefer_info[i]
#         if 1<=n<=3:
#             # i=1->array[2],i=2->array[8],i=3->array[14]
#             road_index = case_info[(n - 1) * 6 + 2]
#             jingdu = case_info[(n - 1) * 6 + 2 - 2]
#             weidu = case_info[(n - 1) * 6 + 2 - 1]
#             human_position = [jingdu, weidu, road_index]
#             crossing = findCrossing(human_position, road_info)
#
#             raw_case_info.append(crossing)
#         else:
#             crossing = -1
#             raw_case_info.append(crossing)
#
#     # 处理new_case_info_raw，形成符合规范的case_info_list
#     # 给一个路口，查询路口的经度和纬度，链接的道路
#     for i in range(len(raw_case_info)):
#         if raw_case_info[i] == -1:
#             # 仅保留原先旅客所在道路
#             #
#             roads_connected = [int(case_info[prefer_info[i]*3+2])]
#         else:   # 在字典中查询路口链接的道路
#             roads_connected = crossing_dict[raw_case_info[i]]
#
#         cooked_case_info.append(roads_connected)
#
#     # 把汽车初始位置的信息放到最后
#     car_pos = cooked_case_info[0:1]
#     del cooked_case_info[0:1]
#     cooked_case_info+=car_pos
#
#     # 然后生成新的new_case_info_list
#     # 算法：从列表中依次抽取一个元素，组成新的列表
#     shadow_case_info_list = case_info.tolist()
#     for i in range(0,7):
#         pass

'''
参数：
（1）case_info
（2）路网信息
返回值：
（1）new_case_info_list：[[形式和原先的case_info一样],[],[],[],[],[]...]
'''
def peopleMover(case_info, road_info):
    crossing_dict = help.dictionMaking()

    new_case_info_list = []
    raw_case_info = []  # 按顺序存放每个点对应的路口
    cooked_case_info = []   # 按顺序存放
    # 遍历prefer_info中的每一个点，对应去case_info中找到路
    # 根据路调用findCrossing查路口
    # 根据返回值修改case_info

    # 优化只需要优化出发点
    for n in range(0,7):
        if n % 2 == 0 and n != 6:
            # i=0->array[2],i=2->array[8],i=4->array[14]
            road_index = case_info[n*3 + 2]
            jingdu = case_info[n*3 + 2 - 2]
            weidu = case_info[n*3 + 2 - 1]
            human_position = [jingdu, weidu, road_index]
            crossing = findCrossing(human_position, road_info)

            raw_case_info.append(crossing)
        else:
            crossing = -1
            raw_case_info.append(crossing)

    # 处理new_case_info_raw，形成符合规范的case_info_list
    # 给一个路口，查询路口的经度和纬度，链接的道路
    for i in range(len(raw_case_info)):
        if raw_case_info[i] == -1:
            # 仅保留原先旅客所在道路
            roads_connected = [int(case_info[i*3+2])]   # ??????
            raw_case_info[i] = int(case_info[i*3+2])
        else:   # 在字典中查询路口链接的道路
            roads_connected = crossing_dict[raw_case_info[i]]

        cooked_case_info.append(roads_connected)

    # 然后生成新的new_case_info_list
    # 算法：从列表中依次抽取一个元素，组成新的列表

    # 要修改的只有array[2],array[8],array[14]

    # 需要修改的经纬度查询
    shadow0 = case_info.tolist()
    dot1 = dotLocator(raw_case_info[0],road_info)
    dot2 = dotLocator(raw_case_info[2],road_info)
    dot3 = dotLocator(raw_case_info[4],road_info)
    shadow0[0],shadow0[1],shadow0[6],shadow0[7],shadow0[12],shadow0[13] = dot1[0],dot1[1],dot2[0],dot2[1],dot3[0],dot3[1]

    for i2 in range(len(cooked_case_info[0])):
        shadow_case_info_list = shadow0
        shadow_case_info_list[2] = cooked_case_info[0][i2]
        for i8 in range(len(cooked_case_info[2])):
            shadow_case_info_list[8] = cooked_case_info[2][i8]
            for i14 in range(len(cooked_case_info[4])):
                shadow_case_info_list[14] = cooked_case_info[4][i14]
                # use deep copy
                a = copy.deepcopy(shadow_case_info_list)
                new_case_info_list.append(a)

    return new_case_info_list


def main():
    # # for debug
    # # 分别存放三个文件的信息
    # road_information = []
    # min_distance = []
    # cases = []
    #
    # road_information, min_distance, cases = question2.fileReading(road_information, min_distance, cases)
    #
    # # # 接送乘客顺序的列表，调用question1生成
    # # preference_index = question1.genAllList()
    #
    # peopleMover(cases[0],road_information)
    pass

if __name__ == '__main__':
    main()


