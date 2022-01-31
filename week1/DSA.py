def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1)+fib(n-2)


def noOfWays(n, m):
    if n <= 1:
        return n
    w = 0
    i = 1
    while i <= m and i <= n:
        w = w + noOfWays(n-i, m)
        i = i + 1
    return w


n = int(input("Enter the number of stairs: "))
no = fib(n + 1)

print(f"The number of ways 1/2 max stairs at a time are: {no}")


m = int(input("Enter max no. of ways one can take the stairs: "))
print("[Generalized form] Number of ways=", noOfWays(n+1, m))