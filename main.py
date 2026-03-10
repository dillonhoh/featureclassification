import math

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

def nearest_neighbor(data):
    correct = 0
    samples = len(data)
    features_size = len(data[0]) - 1

    for n in range(samples):
        
        result = None
        best_dist = float("inf")
        

        for i in range(samples):
            if n == i: #cant compare against itself
                continue

            distance = 0

            # compute distance using all features
            for feature in range(1, features_size + 1):
                difference = data[n][feature] - data[i][feature] #x1 - y1
                distance += difference * difference #square

            distance = math.sqrt(distance) #square root

            if distance < best_dist:
                best_dist = distance
                result = data[i][0]

        if result == data[n][0]:
            correct += 1

    accuracy = correct / samples
    return accuracy

def main():
    while True:
        choice = input("Select dataset: type '1' for small or '2' for large: ").strip()
        if choice == '1':
            data_file = 'CS170_Small_DataSet__31.txt'
            break
        if choice == '2':
            data_file = 'CS170_Large_DataSet__7.txt'
            break
        print("Please enter '1' or '2'.")
  
    data = load(data_file)

    print(f"Nearest-neighbor accuracy: {nearest_neighbor(data):.3%}")


if __name__ == "__main__":
    main()