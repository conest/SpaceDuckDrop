import itertools

def main():
    for i, j in itertools.product(range(5), range(5)):
        print(i, j)
    
if __name__ == "__main__":
    main()
