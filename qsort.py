import random

qs0, qs1, qs2 = 0, 0, 0
def qsort(array, low: int, high: int):
    global qs0, qs1
    if low >= high or low < 0:
        return
    pivot = array[high][0]
    i = low
    for j in range(low, high):
        if array[j][0] <= pivot:
            array[i], array[j] = array[j], array[i]
            if array[i][0] == array[j][0]:
                qs0 += 1
            else:
                qs1 += 1
            i += 1
    array[i], array[high] = array[high], array[i]
    if array[i][0] == array[high][0]:
        qs0 += 1
    else:
        qs1 += 1
    print(array)
    qsort(array, low, i - 1)
    qsort(array, i + 1, high)

def qsort2(array, low: int, high: int):
    global qs2
    if low >= high or low < 0:
        return
    pivot = array[(low + high) // 2][0]
    i = low
    j = high
    while True:
        while array[i][0] < pivot:
            i += 1
        while array[j][0] > pivot:
            j -= 1
        if i >= j:
            break
        array[i], array[j] = array[j], array[i]
        qs2 += 1
        i += 1
        j -= 1
    print(array)
    qsort2(array, low, j)
    qsort2(array, j + 1, high)

array = [(random.randint(5, 10), n) for n in range(6)]
a2 = [*array]
print(array)
qsort(array, 0, len(array) - 1)
print(array, qs0, qs1)
qsort2(a2, 0, len(a2) - 1)
print(a2, qs2)