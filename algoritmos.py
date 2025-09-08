def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def cycle_sort(arr):
    n = len(arr)
    
    for cycle_start in range(0, n-1):
        item = arr[cycle_start]
        
        pos = cycle_start
        for i in range(cycle_start+1, n):
            if arr[i] < item:
                pos += 1
        
        if pos == cycle_start:
            continue
        
        while pos < n and item == arr[pos]:
            pos += 1
        
        if pos < n:
            arr[pos], item = item, arr[pos]
        else:
            continue
        
        while pos != cycle_start:
            pos = cycle_start
            
            for i in range(cycle_start+1, n):
                if arr[i] < item:
                    pos += 1
            
            while pos < n and item == arr[pos]:
                pos += 1
            
            if pos < n and item != arr[pos]:
                arr[pos], item = item, arr[pos]
            else:
                break