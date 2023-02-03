import copy
import question1
import numpy as np
import csv
import math
import question2_angle
import question3


# 全局变量，计算总共进行了多少次的枚举
counting = 0
# 全局变量，记录总路径
routines = []

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
	return L*1000


'''
作用：读取文件
参数：三个列表，分别存放1-3的csv文件信息
'''
def fileReading(road_info, dis_info, case_info):
	with open(
			r"D:/studyyyyyyyyyyyyyyyyyyyyyyyy/5 2023winter/mcm/MCM2023 Training Contest - Problem B Support Materials/R1-link.csv",
			'r') as f:
		# 使用csv.reader将文件读取进来，并转为list形式，方便后续处理
		road_info = list(csv.reader(f))
		# csv文件第一行标题，第一列id，可以分情况去掉
		road_info = np.array(road_info[1:])[:, :].astype(float)
		# [:, :]列表套列表，前面是切第一层列表，后面切第二层列表

	with open(
			r"D:/studyyyyyyyyyyyyyyyyyyyyyyyy/5 2023winter/mcm/MCM2023 Training Contest - Problem B Support Materials/R2-distance.csv",
			'r') as f:
		dis_info = list(csv.reader(f))
		dis_info = np.array(dis_info[:])[:, :].astype(float)

	with open(
			r"D:/studyyyyyyyyyyyyyyyyyyyyyyyy/5 2023winter/mcm/MCM2023 Training Contest - Problem B Support Materials/R3-case.csv",
			'r') as f:
		case_info = list(csv.reader(f))
		case_info = np.array(case_info[2:])[:, :].astype(float)
	return road_info, dis_info, case_info


'''
作用：查找函数。根据路的编号，查询路的两个端点编号
参数：
index：路的编号
chart：读取文件1得到的道路信息列表
'''
def finder(index, chart):
	m = []
	for i in range(len(chart)):
		if(chart[i][0] == float(index)):
			m = chart[i]
			break
	return m

def newFinder(index, chart):
	for i in range(len(chart)):
		if(chart[i][0] == float(index)):
			m = [chart[i][1],chart[i][4]]
			return m


'''
作用：提供一个点的编号（路口的编号），返回经纬度
'''
def dotLocator(index,road_info):
	for i in range(len(road_info)):
		if road_info[i][1] == index:
			return road_info[i][2], road_info[i][3]
		elif road_info[i][4] == index:
			return road_info[i][5], road_info[i][6]


'''
作用：递归调用函数。
参数：
road_index_and_two_dots：路的编号and两个端点的编号
prefer_info：走的序列[0,1,2,3,4,5,6]
dis_info：最短距离，原始表格
start：递归的下标
distance_list：所有可能的距离
current_dis：递归到这一步走的长度
last_node_number：上一步走的节点。初始为-1
'''
# def findMinWay(road_index_and_two_dots, prefer_info, dis_info, start, distance_list, current_dis, last_node_number, current_routine):
# 	# prefer_info 里面是[0,1,2,3,4,5,6]的序列
# 	if start == 7:
# 		distance_list.append(current_dis)
# 		global counting
# 		counting += 1
# 		global routines
# 		a = copy.deepcopy(current_routine)
# 		routines.append(a)
# 		print(counting, "distance:", current_dis)
# 		return
#
# 	# 当前路
# 	now_road_index = prefer_info[start]
# 	now_road_info = road_index_and_two_dots[now_road_index]
# 	now_road_node0 = now_road_info[1]
# 	now_road_node1 = now_road_info[2]

	#### 选择这条路的0号端点
	# if last_node_number != -1:
	# 	# 加上距离：node0和上一个节点
	# 	current_dis += dis_info[int(now_road_node0)][int(last_node_number)]
	#
	# current_routine.append("1-6序号：" + str(now_road_index) + "，路编号：" + str(now_road_info[0]) + "，路口：0")
	# findMinWay(road_index_and_two_dots, prefer_info, dis_info, start + 1,distance_list,current_dis, now_road_node1,current_routine)
	# # 把0号端点吐出来：减去node0和上一个节点的距离
	# if last_node_number != -1:
	# 	current_dis -= dis_info[int(now_road_node0)][int(last_node_number)]
	# # 去除上一步routine
	# current_routine.pop()
	#
	#
	# #### 选择这条路的1号端点
	# if last_node_number != -1:
	# 	current_dis += dis_info[int(now_road_node1)][int(last_node_number)]
	#
	# current_routine.append("1-6序号："+str(now_road_index)+"，路编号："+str(now_road_info[0])+"，路口：1")
	# findMinWay(road_index_and_two_dots, prefer_info, dis_info, start + 1, distance_list, current_dis, now_road_node0,current_routine)
	# # 把1号端点吐出来
	# if last_node_number != -1:
	# 	current_dis -= dis_info[int(now_road_node1)][int(last_node_number)]
	# # 去除上一步routine
	# current_routine.pop()


	# return distance_list

# '''
# 作用：求最短距离。
# 参数：
# road_index_and_two_dots：路的编号and两个端点的编号
# prefer_info：走的序列[0,1,2,3,4,5,6]
# dis_info：最短距离，原始表格
# '''
# def findTheMinimalWay(road_index_and_two_dots, prefer_info, dis_info, case_info,road_info):
# 	current_distance = 0
# 	# TODO for debug
# 	# print("start road counting:",prefer_info,current_distance)
#
#
# 	# 上一条马路
# 	last_road_info = []
#
# 	# 汽车开始的位置
# 	car_position = [case_info[18],case_info[19]]
# 	# 最后乘客下车的位置
# 	last_destination = [case_info[(prefer_info[-1]-1)*3-3], case_info[(prefer_info[-1]-1)*3+1-3]]
#
# 	now_road_info = []
#
# 	i = 0
# 	# 注意到可能存在同路人的情况
# 	while i < 7:
# 		if i == 0:
# 			# 刚开始的时候，出租车顺着马路到路口的距离
# 			last_road_info = road_index_and_two_dots[prefer_info[i]]
# 			# last_road_node0 = last_road_info[1]
# 			last_road_node1 = last_road_info[2]
# 			tu = dotLocator(last_road_node1,road_info)
#
# 			current_distance += distanceCalculator(car_position[0],car_position[1],tu[0],tu[1])
#
# 			print(i, "车准备接第一个人：", distanceCalculator(car_position[0],car_position[1],tu[0],tu[1]),current_distance)
#
# 		elif i != 6:
# 			now_road_info = road_index_and_two_dots[prefer_info[i]]
#
# 			current_distance += dis_info[int(last_road_info[2])][int(now_road_info[1])]	# 从上一条路的尾巴走到这条路的头
# 			print(i, "车从上一个尾巴到头", dis_info[int(last_road_info[2])][int(now_road_info[1])],current_distance)
# 			current_distance += dis_info[int(now_road_info[1])][int(now_road_info[2])]	# 从这条路的头走到这条路的尾巴
# 			print(i, "车从这条路头到尾巴", dis_info[int(now_road_info[1])][int(now_road_info[2])],current_distance)
# 			last_road_info = now_road_info
#
# 		elif i == 6:
# 			#  （1）上一个节点到这一个起点；
# 			#  （2）加上出租车到终点的长度：路的起点->人的位置
#
# 			now_road_info = road_index_and_two_dots[prefer_info[i]]
# 			last_start_dot = now_road_info[1]
#
# 			tu2 = dotLocator(last_start_dot,road_info)
#
# 			current_distance += dis_info[int(last_road_info[2])][int(now_road_info[1])]
# 			print(i,"车从上一个尾巴到头",dis_info[int(last_road_info[2])][int(now_road_info[1])],current_distance)
# 			current_distance += distanceCalculator(last_destination[0],last_destination[1],tu2[0],tu2[1])
# 			print(i, "车到终点", distanceCalculator(last_destination[0],last_destination[1],tu2[0],tu2[1]),current_distance)
# 		i += 1
#
#
# 	a = copy.deepcopy(current_distance)
# 	return [a]

'''
返回路的长度
'''
def roadLength(index,road_info):
	for i in range(len(road_info)):
		if road_info[i][0] == index:
			return road_info[i][7]


'''
作用：求最短距离。
参数：
road_index_and_two_dots：路的编号and两个端点的编号
prefer_info：走的序列[0,1,2,3,4,5,6]
dis_info：最短距离，原始表格
'''
def findTheMinimalWay(road_index_and_two_dots, prefer_info, dis_info, case_info,road_info):
	current_distance = 0

	# 考虑到可能存在同路人的情况，同时还可能存在多个人（超过2人存在同一条路上），
	# 我们不是在执行指令的时候处理，而是在执行指令之前处理数据

	raw_visiting_order = []	# 按顺序存放要拜访的点：格式：[经度，维度，马路号]
	cooked_visiting_order = []

	raw_visiting_order.append([case_info[18],case_info[19],case_info[20]])
	for i in range(1,7):
		index = prefer_info[i]
		# 1->0,1,2	2->6,7,8	3->12,13,14
		# 4->3,4,5	5->9,10,11	6->15,16,17
		if 1<=index<=3:
			raw_visiting_order.append([case_info[index*6-6],case_info[index*6-6+1],case_info[index*6-6+2]])
		else:
			raw_visiting_order.append([case_info[index*6-21],case_info[index*6-21+1],case_info[index*6-21+2]])

	# last_road_number = raw_visiting_order[0][2]	# 汽车的初始马路号
	# now_road_number = 0
	shadow = []
	for i in range(0,7):
		# 只要依次记录马路号就可以了，开头结尾的点直接去raw里面找就可以
		if raw_visiting_order[i][2] not in shadow:
			shadow.append(raw_visiting_order[i][2])

	for i in range(len(shadow)):
		cooked_visiting_order.append([shadow[i]]+newFinder(shadow[i],road_info))

	last_road_info = []
	car_position = [case_info[18],case_info[19]]
	# 4->3,4	5->9,10	  6->15,16
	last_destination = [case_info[(prefer_info[-1]) * 6 - 21], case_info[(prefer_info[-1]) * 6 + 1 - 21]]
	# 开始计算路程
	for i in range(len(cooked_visiting_order)):
		if i == 0:
			# 刚开始的时候，出租车顺着马路到路口的距离
			last_road_info = cooked_visiting_order[i]
			last_road_node1 = last_road_info[2]

			tu = dotLocator(last_road_node1,road_info)

			current_distance += distanceCalculator(car_position[0],car_position[1],tu[0],tu[1])

			# print(i, distanceCalculator(car_position[0],car_position[1],tu[0],tu[1]),"刚开始的时候，出租车顺着马路到路口的距离")


		elif i == len(cooked_visiting_order)-1:
			# 接最后一个人：
			# （1）上一个尾巴到这个头
			# （2）出租车从这个头到终点
			now_road_info = cooked_visiting_order[i]
			last_start_dot = now_road_info[1]

			tu2 = dotLocator(last_start_dot,road_info)

			current_distance += dis_info[int(last_road_info[2])][int(now_road_info[1])]
			current_distance += distanceCalculator(last_destination[0],last_destination[1],tu2[0],tu2[1])

			# print(i, "last tail->this head", dis_info[int(last_road_info[2])][int(now_road_info[1])])
			# print(i, "this head->desti", distanceCalculator(last_destination[0],last_destination[1],tu2[0],tu2[1]))
		else:
			# 普通情况
			now_road_info = cooked_visiting_order[i]

			# 车从上一个尾巴到头
			current_distance += dis_info[int(last_road_info[2])][int(now_road_info[1])]

			# print(i, "tail->head", dis_info[int(last_road_info[2])][int(now_road_info[1])])
			# 车从这条路的头到尾巴
			current_distance += roadLength(now_road_info[0],road_info)

			# print(i, "this head->tail", roadLength(now_road_info[0],road_info))
			last_road_info = now_road_info

	return [current_distance]

'''
作用：对于确定的一辆车三个人，遍历60种不同的上下车顺序，找出最短的路径长度。
参数：
road_info：读取自文件1，原始道路信息list
dist_info：读取自文件2，点之间最短距离list
case_info：读取自文件3的第一列，一辆车三个人的位置信息list
prefer_info：60种可能的排列list
'''
def traverseAllArrangement(road_info, dis_info, case_info, prefer_info):
	# the max float
	min_dis = float('inf')
	current_distance_list = []

	####### 处理一辆车三个人的位置信息。
	# 读取道路的序号
	road_index = [-1]	# 列表。表中信息为七条道路的序号。格式：[路的序号,...]
	road_index_and_two_dots = [[]]	# 列表。表中信息为七条道路的序号和两个顶点的序号。格式：[[路的序号，顶点1，顶点2],...]
	for i in range(7):
		road_index.append(case_info[3*i+2])

	for i in range(1,8):
		road_num = road_index[i]
		road_num_info = finder(road_num, road_info)
		a = [road_num, road_num_info[1], road_num_info[4]]
		road_index_and_two_dots.append(a)

	# 把汽车的信息放在数组index为0的位置
	# road_index_and_two_dots[0], road_index_and_two_dots[7] = road_index_and_two_dots[7], road_index_and_two_dots[0]
	# 交换位置：135->123,246->456
	exchange = [road_index_and_two_dots[7],road_index_and_two_dots[1],road_index_and_two_dots[3],road_index_and_two_dots[5],road_index_and_two_dots[2],road_index_and_two_dots[4],road_index_and_two_dots[6],[]]
	road_index_and_two_dots = exchange

	###### 开始枚举
	# 遍历所有可能的顺序
	for i in range(0, len(prefer_info)):
		# 对每种对应的序列（如[1,4,2,3,5,6]）进行计算
		# 调用计算函数。第二个参数在序列中加入[0]，标识车辆信息
		# current_distance_list += findMinWay(road_index_and_two_dots, [0]+prefer_info[i], dis_info, 0, [], 0, -1, [])
		current_distance_list += findTheMinimalWay(road_index_and_two_dots,[0]+prefer_info[i],dis_info,case_info,road_info)

	# # # TODO for debug(important) question2未优化显示 easonchan
	for i in range(len(current_distance_list)):
		print(prefer_info[i])

	for i in range(len(current_distance_list)):
		print(current_distance_list[i])

	# 找到最小的
	# min_dis = min(current_distance_list)
	min_index = -1
	# print(len(current_distance_list))

	for i in range(len(current_distance_list)):
		if current_distance_list[i] < min_dis:
			min_index = i
			min_dis = current_distance_list[i]

	# need for question2未优化 easonchan
	print("shortest:", prefer_info[min_index])

	return min_dis

def traverseAllArrangement2(road_info, dis_info, case_info, prefer_info):
	# the max float
	min_dis = float('inf')
	current_distance_list = []

	####### 处理一辆车三个人的位置信息。
	# 读取道路的序号
	road_index = [-1]	# 列表。表中信息为七条道路的序号。格式：[路的序号,...]
	road_index_and_two_dots = [[]]	# 列表。表中信息为七条道路的序号和两个顶点的序号。格式：[[路的序号，顶点1，顶点2],...]
	for i in range(7):
		road_index.append(case_info[3*i+2])

	for i in range(1,8):
		road_num = road_index[i]
		road_num_info = finder(road_num, road_info)
		a = [road_num, road_num_info[1], road_num_info[4]]
		road_index_and_two_dots.append(a)

	# 把汽车的信息放在数组index为0的位置
	# road_index_and_two_dots[0], road_index_and_two_dots[7] = road_index_and_two_dots[7], road_index_and_two_dots[0]
	# 交换位置：135->123,246->456
	exchange = [road_index_and_two_dots[7],road_index_and_two_dots[1],road_index_and_two_dots[3],road_index_and_two_dots[5],road_index_and_two_dots[2],road_index_and_two_dots[4],road_index_and_two_dots[6],[]]
	road_index_and_two_dots = exchange

	###### 开始枚举
	# 遍历所有可能的顺序
	for i in range(0, len(prefer_info)):
		# 对每种对应的序列（如[1,4,2,3,5,6]）进行计算
		# 调用计算函数。第二个参数在序列中加入[0]，标识车辆信息
		# current_distance_list += findMinWay(road_index_and_two_dots, [0]+prefer_info[i], dis_info, 0, [], 0, -1, [])
		current_distance_list += findTheMinimalWay(road_index_and_two_dots,[0]+prefer_info[i],dis_info,case_info,road_info)

	# # # TODO for debug(important) question2未优化显示 easonchan
	# for i in range(len(current_distance_list)):
	# 	print(prefer_info[i])
	#
	# for i in range(len(current_distance_list)):
	# 	print(current_distance_list[i])

	# 找到最小的
	# min_dis = min(current_distance_list)
	min_index = -1
	# print(len(current_distance_list))

	for i in range(len(current_distance_list)):
		if current_distance_list[i] < min_dis:
			min_index = i
			min_dis = current_distance_list[i]

	# need for question2未优化 easonchan
	# print("shortest:", prefer_info[min_index])

	return min_dis,prefer_info[min_index]


'''
作用：验证假设路是直的
'''
def testDistanceCalculation(road_info):
	calcu_length = 0
	actual_length = 0
	for i in range(1000):
		actual_length += road_info[i][7]
		calcu_length += distanceCalculator(road_info[i][2],road_info[i][3],road_info[i][5],road_info[i][6])

	a = (actual_length-calcu_length)/actual_length
	return abs(a)
	# 误差：0.0008772146987417321


def solvingQuestion2Origin(road_information,min_distance,cases,preference_index):
	# 对于某辆车和某三个人，遍历所有可能
	# 这里传入的形参cases是10个例子，但是事实上我们只测了第一个
	# preference_index = [[1, 3, 2, 5, 6, 4]]
	answer = traverseAllArrangement(road_information, min_distance, cases[0], preference_index)

	print("the shortest distance:", answer)


def solvingQustion3Origin(road_info, min_distance_chart, cases, prefer_index):
	current_case = cases[1]
	# 执行人的移动，生成更多的case可能
	new_case_list = question3.peopleMover(current_case,road_info)

	prefer_index =  [[1,3,2,5,4,6]]
	# 告诉乘客应该在什么位置等候上车
	passenger_position = []

	min_dis = float('inf')
	# 遍历所有的case in new_case_list，从中筛选出最小值
	for i in range(len(new_case_list)):
		# 注意做类型转换，不然传参会出现错误
		array1 = np.array(new_case_list[i])
		answer = traverseAllArrangement(road_info,min_distance_chart,array1,prefer_index)
		print("本次最短：",answer)
		if answer < min_dis:
			min_dis = answer
			passenger_position = array1.tolist()

	print("最短距离：",min_dis)

	# 输出经度纬度即可
	# array[0][1],array[6][7],array[12][13]
	print("第1名乘客的出发位置：","经度：",passenger_position[0],"纬度：",passenger_position[1])
	print("第2名乘客的出发位置：","经度：", passenger_position[6], "纬度：", passenger_position[7])
	print("第3名乘客的出发位置：", "经度：", passenger_position[12], "纬度：", passenger_position[13])


def solvingQustion2_improved(road_information,min_distance,cases,preference_index):
	man = cases[1]
	for i in range(1):
		print("-----------",i,"--------------")
		man = cases[0]
		# 优化直接处理prefer_info
		################## (important)优化：角度
		preference_index = question2_angle.listFilter(preference_index, man.tolist())
		# 进一步优化：贪心算法
		greedy_choice = question2_angle.greedyFilter(man.tolist())

		# for debug
		print("greedy:", greedy_choice)
		for i in range(len(preference_index)):
			print(preference_index[i])
		print("20!!!!!!!!!!!!!!!!")

		if not greedy_choice in preference_index:
			preference_index.append(greedy_choice)

		######### 进一步优化：折线长度优化
		preference_index = question2_angle.secondFilter(preference_index, man.tolist())

		# 对于某辆车和某三个人，遍历所有可能
		# 这里传入的形参cases是10个例子，但是事实上我们只测了第一个
		print("----------------")
		answer = traverseAllArrangement(road_information, min_distance, man, preference_index)

		print("the shortest distance:", answer)



def solvingQuestion4(road_info, min_distance, cases, preference_index):
	# 十个例子的处理
	# 先扩张（人的移动），再剪枝
	cases = [cases[9]]
	for i in range(len(cases)):
		if i == 2:
			continue
		print("case:",i+1)
		current_case = cases[i]
		# 先扩张，生成更多case
		raw_new_case_list = question3.peopleMover(current_case,road_info)
		# 注意格式转换
		new_case_list = np.array(raw_new_case_list)

		min_dis = float('inf')
		index_to_choose = []
		# 对于new_case_list，遍历，求最小值
		passenger_position = []
		for i in range(len(new_case_list)):
			# 再对prefer_list进行剪枝
			preference_index = question2_angle.listFilter(preference_index, new_case_list[i].tolist())
			greedy_choice = question2_angle.greedyFilter(new_case_list[i].tolist())

			if not greedy_choice in preference_index:
				preference_index.append(greedy_choice)

			# 折线长度优化
			preference_index = question2_angle.secondFilter(preference_index, new_case_list[i].tolist())

			answer,index_list = traverseAllArrangement2(road_info,min_distance,new_case_list[i],preference_index)
			if answer < min_dis:
				min_dis = answer
				index_to_choose = index_list
				passenger_position = new_case_list[i]

		print("顺序：",index_to_choose,"最短距离：",min_dis)
		print(passenger_position[0],passenger_position[1],passenger_position[6],passenger_position[7],passenger_position[12],passenger_position[13])



def main():
	# 分别存放三个文件的信息
	road_information = []
	min_distance = []
	cases = []

	road_information, min_distance, cases = fileReading(road_information, min_distance, cases)

	# # 验证假设路是直的
	# print(testDistanceCalculation(road_information))


	# 接送乘客顺序的列表，调用question1生成
	preference_index = question1.genAllList()

	# for debug
	for i in range(0, len(preference_index)):
		# 将prefer_info中存放的序列为[1,2,3,1,2,3]这种，数字1第一次出现标识1号人上车，第二次出现标识1号人下车
		# 现在我们将其修改为[1,2,3,4,5,6]，数字1标识1号人上车，数字4标识1号人下车
		flag = [0,0,0,0]
		for j in range(0, len(preference_index[i])):
			if flag[preference_index[i][j]] == 0:
				flag[preference_index[i][j]] += 1
			else:
				preference_index[i][j] += 3

	# # 问题2（未优化），问题2的优化在上面的代码中，搜索important关键字
	# solvingQuestion2Origin(road_information,min_distance,cases,preference_index)

	# # 问题2（优化）
	# solvingQustion2_improved(road_information,min_distance,cases,preference_index)

	# 问题3
	solvingQustion3Origin(road_information,min_distance,cases,preference_index)

	# # 问题4
	# solvingQuestion4(road_information,min_distance,cases,preference_index)


if __name__ == '__main__':
    main()