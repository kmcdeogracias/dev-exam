def fibonacci(num):
    x, y = 0, 1
    for i in range(num):
        i += 1
        z = x + y
        x = y
        y = z

        if z % 3 == 0 and z % 5 == 0:
            z = "Maria Health"
        elif z % 3 == 0:
            z = "Maria"
        elif z % 5 == 0:
            z = "Health"

        print(z)

fibonacci(20)