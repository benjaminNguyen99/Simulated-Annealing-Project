import random
import math
import copy
import csv
#---------------------------------------------------------------
List =[]
filename = "Progress.csv"
field = ["State", "Temperature", "Attempt", "Weight", "Utility"]
fi = open("Final Result.txt", "w")
progress_list = []


with open("Program2Input.txt", "r") as file:
    List = [line.split() for line in file]
utility_list=[]
weight_list=[]
for each in List:
    utility_list.append(float(each[0]))
    weight_list.append(float(each[1]))

#print(weight_list)
#print(utility_list)

def createlist(n):
    return_list = []
    tog = []
    for i in range (0, n):
        return_list.append(0)
    x = 0
    while x <20:
        randompoint = random.randrange(0, len(return_list))
        if not(randompoint in tog):
            return_list[randompoint] = 1
            tog.append(randompoint)
            x += 1
    return return_list

def main():
    cur_state = createlist(len(utility_list))
    T = 100
    change=0
    attempt =0
    count=0
    #--------------------------------

    while True:
        attempt+= 1
        cur_score, cur_utility, cur_weight = modify(cur_state, weight_list, utility_list)
        new_state = change_c(cur_state)
        new_score, new_utility, new_weight = modify(new_state, weight_list, utility_list)
        delta_u =new_score - cur_score
        if delta_u >= 0:
            cur_score = new_score
            change += 1
            cur_state = copy.deepcopy(new_state)
            cur_weight = copy.deepcopy(new_weight)
            cur_utility = copy.deepcopy(new_utility)
            count += 1
            print("[State:", count, "Temperature:", T, "Attempt:", attempt, "]----Weight:", cur_weight,
                  " Utility:", cur_utility, "[", cur_state[0], ",", cur_state[1], ",",cur_state[2], ",",cur_state[3], ",",cur_state[4], ",...,",
                    cur_state[395], ",", cur_state[396], ",",cur_state[397], ",",cur_state[398], ",",cur_state[399], "]")
            progress_list.append((count, T, attempt, cur_weight, cur_utility))
        elif (math.e **(delta_u/T)) > random.uniform(0, 1) :
            cur_score = new_score
            change += 1
            cur_state = copy.deepcopy(new_state)
            cur_weight = copy.deepcopy(new_weight)
            cur_utility = copy.deepcopy(new_utility)
            count += 1
            print("[State:", count, "Temperature:", T, "Attempt:", attempt, "]----Weight:", cur_weight,
                  " Utility:", cur_utility, "[", cur_state[0], ",", cur_state[1], ",",cur_state[2], ",",cur_state[3], ",",cur_state[4], ",...,",
                    cur_state[395], ",", cur_state[396], ",",cur_state[397], ",",cur_state[398], ",",cur_state[399], "]")
            progress_list.append((count, T, attempt, cur_weight, cur_utility))

        if attempt > 40000 and change == 0:
            packages = []
            total_item_packed = 0
            for x in range(0, len(cur_state)):
                if cur_state[x] == 1 :
                    total_item_packed+=1
                    packages.append((utility_list[x], weight_list[x]))
            print("------------------------------------------------------NO CHANGE ACCEPTED------------------------------------------------------")
            print("------------------------------------------------------ FINISH ANNEALING ------------------------------------------------------")
            print("|----------------------------|", "|--------------------------------|")
            print("|Number of items packed:", total_item_packed, "|", "|Highest Temperature: 100        |")
            print("|----------------------------|", "|--------------------------------|")
            print("|Total Utility:", cur_utility, "       |", "|Lowest Temperature:", round(T, 3), "      |")
            print("|----------------------------|", "|--------------------------------|")
            print("|Total Weight:", cur_weight,"        |", "|Alpha: 0.95 (Geometric Cooling) |")
            print("|----------------------------|", "|--------------------------------|")
            print("Have a nice camping trip!!!")
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(field)
                csvwriter.writerows(progress_list)
            fi.write("Number of items packed: "+ str(total_item_packed) + "\n")
            fi.write("Total Utility: "+ str(cur_utility) + "\n")
            fi.write("Total Weight: " + str(cur_weight) + "\n")
            stt = 1
            while stt < len(packages)+1:
                fi.write ("Item "+ str(stt) + " - " + " Utility: "+ str(packages[stt-1][0]) + " Weight: "+ str(packages[stt-1][1]) + "\n")
                stt+=1
            break

        if attempt > 40000 or change > 4000:

            T = (T * 0.95)
            print("Temperature:", T)
            attempt = 0
            change = 0

def change_c(l):
    re_list = copy.deepcopy(l)
    randompoint = random.randrange(0, len(l))
    if re_list[randompoint] == 0:
        re_list[randompoint] = 1
    else:
        re_list[randompoint] = 0
    return re_list

def modify(list, wlist, ulist):
    total_u = 0
    total_w = 0
    for x in range(0, len(list)):
        if list[x] == 1:
            total_u += ulist[x]
            total_w += wlist[x]

    if total_w > 500:
        real_total_u = total_u - ((total_w - 500) * 20)
    else:
        real_total_u = total_u
    return real_total_u, total_u ,  total_w

if __name__ == "__main__":
    main()
