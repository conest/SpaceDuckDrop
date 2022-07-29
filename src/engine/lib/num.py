import numbers


def clip(n: numbers, bottom: numbers, top: numbers) -> numbers:
    return max(min(n, top), bottom)


def nmark(n: numbers) -> int:
    if n < 0:
        return -1
    elif n > 0:
        return 1
    else:
        return 0


def approach(n: float, t: float, step: float) -> float:
    '''Return a number n that is trying to approach(become) t, in step'''
    if n > t:
        if n - step > t:
            return n - step
        else:
            return t
    else:
        if n + step < t:
            return n + step
        else:
            return t
