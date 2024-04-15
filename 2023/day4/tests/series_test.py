def exponential(n: int, a: int) -> int:
    if n < 1:
        return 0
    return a ** (n - 1)

def test() -> None:
    assert exponential(1, 2) == 1
    assert exponential(2, 2) == 2
    assert exponential(3, 2) == 4
    assert exponential(4, 2) == 8
    assert exponential(5, 2) == 16
    assert exponential(6, 2) == 32
