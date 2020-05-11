import time


def main():
    a = time.time()
    print(int(a))
    print(time.localtime(a))
    return 0

if __name__ == "__main__":
    main()