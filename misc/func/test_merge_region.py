def merge_regions(arr, region_size):
    result = []
    for i in range(0, len(arr), region_size):
        row = []
        for j in range(0, len(arr[0]), region_size):
            region_values = []
            for x in range(region_size):
                for y in range(region_size):
                    if i + x < len(arr) and j + y < len(arr[0]):
                        region_values.append(arr[i + x][j + y])
            region_mean = any(region_values)
            row.append(region_mean)
        result.append(row)
    return result
