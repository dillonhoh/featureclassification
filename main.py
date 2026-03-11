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

def nearest_neighbor(data, features):
    correct = 0
    samples = len(data)

    for n in range(samples):
        
        result = None
        best_dist = float("inf")
        

        for i in range(samples):
            if n == i: #cant compare against itself
                continue

            distance = 0

            # compute distance using all features
            for feature in features:
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

def forward_selection(data):
    remaining = set(range(1, len(data[0])))  # set of features
    current_set = []
    best_set = []
    best_acc = 0.0
    branchlevel_acc = 0.0
    current_acc = 0.0

    while remaining:
        best_feature = None # best feature to add at a certain branch level
        branchlevel_acc = current_acc
        for new_feature in sorted(remaining): # test all features
            test_features = current_set + [new_feature] # test current feature set + additional
            acc = nearest_neighbor(data, test_features)
            print(f"Using features {test_features} accuracy is {acc * 100:.3f}%")

            if acc > branchlevel_acc: # if test feature is better than our other features at this level
                branchlevel_acc = acc
                best_feature = new_feature
        if best_feature is None:    # early abandomment, if adding new features atlevel doesnt improve, break off.
            break
        current_set.append(best_feature) # add feature to this iteration
        remaining.remove(best_feature) # remove from set. we would not test it again
        current_acc = branchlevel_acc

        print(f"\nFeature set {current_set} was best, accuracy is {branchlevel_acc * 100:.3f}%\n")
        if current_acc > best_acc: #if new subset is better than global subset then replace
            best_acc = current_acc
            best_set = current_set.copy()

    return best_set, best_acc


def main():
    while True:
        choice = input("Select dataset: type '1' for small, '2' for large, '3' for sanitycheck1, '4' for sanitycheck2: ").strip()
        if choice == '1':
            data_file = 'CS170_Small_DataSet__31.txt'
        if choice == '2':
            data_file = 'CS170_Large_DataSet__7.txt'
        if choice == '3':
            data_file = 'SanityCheck_DataSet__1.txt'
        if choice == '4':
            data_file = 'SanityCheckDataSet__2.txt' 
        print("Please enter '1' or '2'.")
  
        data = load(data_file)
        choice = input("Select algorithm: type '1' for forward selection and '2' for backwards elimination").strip()
        if choice == '1':
            selected, sel_acc = forward_selection(data)
            break
        print("Please enter '1' or '2'.")
    
    print(f"Finished Search! The best feature subset is {selected}, which has an accuracy of {sel_acc:%}")



if __name__ == "__main__":
    main()