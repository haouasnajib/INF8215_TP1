class MyClass:
    miaou = 0

    def __init__(self):
        MyClass.miaou += 1


def main():
    obj = MyClass()
    obj2 = MyClass()
    # print(obj.miaou)

    A = []
    B = []
    A.append(obj)
    B.append(3)

    if obj in A and 3 in B:
        M = A[0]
        print(M.miaou)


if __name__ == '__main__':
    main()