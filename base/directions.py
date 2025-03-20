def get_direction(x_1: int, y_1: int, x_2: int, y_2: int) -> tuple[float, float]:
    leng = length(x_1, x_2, y_1, y_2)
    return (x_2 - x_1) / leng, (y_2 - y_1) / leng


def length(x: int, x_2: int, y: int, y_2: int) -> float:
    e_x = x_2 - x
    e_y = y_2 - y
    leng = (e_x ** 2 + e_y ** 2) ** 0.5
    return leng
