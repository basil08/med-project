import pickle


def read(f):
    b = open(f, 'rb')

    data = pickle.load(b)

    try:
        while True:
            data = pickle.load(b)
            print(data)
    except EOFError:
        print('Reading complete')
    finally:
        b.close()

read('Robin_Guthrie.dat')
