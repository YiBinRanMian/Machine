num=[int(n) for n in input("get the array: ").split()]
import copy
def getTheMax(array):
  if(len(array)==1):
    return array,array[0]
  array_pop_end=copy.deepcopy(array)
  array_pop_end.pop()
  array_pop_beg=copy.deepcopy(array)
  array_pop_beg.pop(0)
  result_array_beg,value_beg=getTheMax(array_pop_beg)
  result_array_end,value_end=getTheMax(array_pop_end)
  if sum(array)>value_beg:
   if sum(array)>value_end:
     return array,value_beg+array[0]
  if value_beg>value_end:
    return result_array_beg,value_beg
  if value_end>=value_beg:
    return result_array_end,value_end
print(getTheMax(num))
