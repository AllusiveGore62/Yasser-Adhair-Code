def merge_sort(arr):
    n = len(arr)
    curr_size = 1
    while curr_size < n:
        left = 0
        while left < n - 1:
            mid = min(left + curr_size - 1, n - 1)
            right = min(left + 2 * curr_size - 1, n - 1)
            merge(arr, left, mid, right)
            left += 2 * curr_size
        curr_size *= 2
    return arr

def merge(arr, left, mid, right):
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1

    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1

    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1


arr = [12, 11, 13, 5, 6, 7]
print("Original array:", arr)
sorted_arr = merge_sort(arr)
print("Sorted array:", sorted_arr)
