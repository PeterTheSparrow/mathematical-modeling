# 重新绘制路网，得到csv文件
# 每个路口链接的路
import numpy as np
import csv
'''
作用：读取文件
参数：读取文件csv1
'''
def fileReading():
	with open(
			r"D:/studyyyyyyyyyyyyyyyyyyyyyyyy/5 2023winter/mcm/MCM2023 Training Contest - Problem B Support Materials/R1-link.csv",
			'r') as f:
		# 使用csv.reader将文件读取进来，并转为list形式，方便后续处理
		road_info = list(csv.reader(f))
		# csv文件第一行标题，第一列id，可以分情况去掉
		road_info = np.array(road_info[1:])[:, :].astype(float)
		# [:, :]列表套列表，前面是切第一层列表，后面切第二层列表

	return road_info

'''
处理数据。
查看每个路口链接的路。
map：crossing_dict = {"crossing_index":[]}，总共1901个路口
'''
def dictionMaking():
	road_info = fileReading()
	crossing_dict = {0:[]}
	# initialize the dictionary
	for i in range(1, 1902):
		crossing_dict.update({i: []})

	for i in range(len(road_info)):
		crossing_dict[road_info[i][1]].append(int(road_info[i][0]))
		crossing_dict[road_info[i][4]].append(int(road_info[i][0]))

	return crossing_dict


def main():
    road_info = fileReading()
    dictionMaking(road_info)


if __name__ == '__main__':
    main()