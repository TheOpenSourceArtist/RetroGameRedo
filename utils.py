def distSquared(a: list[float], b: list[float]) -> float:
    return ((b[0] - a[0]) * (b[0] - a[0])) + ((b[1] - a[1]) * (b[1] - a[1]))

def dist(a: list[float], b: list[float]) -> float:
    return distSquared(a,b) ** 0.5