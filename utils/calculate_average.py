def calculate_average(old_average: float, count: int, new_value: int) -> float:
    """This function is used to calculate the average data
    based on the old average and count

    Params:
    old_average(float): The Old average value
    count(int): The current count data
    new_value(int): The new value that you want to add in.

    Return:
    float: The new average value
    int: The new count
    """
    old_sum_value = old_average * count
    count += 1
    new_sum_value = old_sum_value + new_value
    new_average = new_sum_value / count

    return round(new_average, 2), count
