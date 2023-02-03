# # 123...n,123...n 全排列，先上车后下车
# # 首尾不存在两个连续的相同的数
import copy

def  all_arrangement(to_be_arranged, start, end, all_list):
    if start == end:
        a = copy.deepcopy(to_be_arranged)
        if(a in all_list):
            pass
        else:
            all_list.append(a)
    else:
        for i in range(start, end+1):
            # 将第i个元素与首位元素交换
            to_be_arranged[start], to_be_arranged[i] = to_be_arranged[i], to_be_arranged[start]
            # 子序列进行全排列
            all_arrangement(to_be_arranged, start + 1, end, all_list)
            # 将i个元素放回原位置，准备下一个元素的交换
            to_be_arranged[start], to_be_arranged[i] = to_be_arranged[i], to_be_arranged[start]


def printList(list_to_print):
    n = 0
    for i in range(0, len(list_to_print)):
        # 删除末尾连续两个或者开头连续两个相同的
        print(list_to_print[i])
        n += 1
    print(n)

def genAllList():
    origin_list = [1,1,2,2,3,3]
    all_list = []
    new_list = []

    all_arrangement(origin_list, 0, len(origin_list) - 1, all_list)

    for i in range(0,len(all_list)):
        # 删除末尾连续两个或者开头连续两个相同的
        if(all_list[i][0] == all_list[i][1] or all_list[i][-1] == all_list[i][-2]):
            continue
        new_list.append(all_list[i])

    return new_list
    # return [[1,2,3,1,2,3]]

def main():
    printList(genAllList())


if __name__ == '__main__':
    main()
