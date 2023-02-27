#!/usr/bin/python3

# This program takes a list of values as input followed by a value
# and if some consecutive values in the list equal to the other
# value provided then return TRUE.

def find_sequence(my_list, my_sum):
    for i0 in range(len(my_list)):
        total = 0
        for i1 in range(i0, len(my_list)):
            total += my_list[i1]
            if total == my_sum:
                print('Sequence found: ', end='')
                print(my_list[i0:i1+1], sep=',')
                return True
            if total > my_sum:
                continue
    print('No sequence found in', my_list, 'that sums to', my_sum)
    return False


myList = [1, 2, 3, 4, 2, 6, 7, 8, 9]
mySum = 12
print(find_sequence(myList, mySum))

while mySum != 0:
    mySum = int(input('Enter the target sum (0 to terminate): '))
    if mySum != 0:
        myList = list(map(int, input('Enter a list of values in the form: [1,2,3,4]: ').split(',')))
        find_sequence(myList, mySum)