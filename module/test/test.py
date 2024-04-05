import numpy as np

arr1 = np.asarray([[1,2,3,4,5], []])
# arr2 = np.asarray([3,2,7,9,1])

print(arr1.ndim)
arr = np.concatenate(arr1, axis=0)
print(set(arr))
# print(set(np.concatenate((arr1, arr2), axis=0)))

