
def load(file):
    data = []
    with open(file, 'r', encoding='utf-8') as dataset:
        for line in dataset:
            line = line.strip()
            if line == "":
                continue
            row = [float(x) for x in line.split()]
            data.append(row)
    return data


def main():
    data_file = 'CS170_Large_DataSet__7.txt'
    data = load(data_file)

    for r in data[:100000000000]:
        print(r)


if __name__ == "__main__":
    main()