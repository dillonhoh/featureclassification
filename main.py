import math
import time
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


def zero_features(data): # accuracy calculated for zero features
    classList = [row[0] for row in data]
    acc = max(classList.count(1.0), classList.count(2.0)) / len(classList)
    return acc

def forward_selection(data):
    remaining = set(range(1, len(data[0])))  # set of features
    current_set = []
    best_set = []
    best_acc = 0.0
    branchlevel_acc = 0.0
    current_acc = 0.0

    while remaining:
        best_feature = None # best feature to add at a certain branch level
        branchlevel_acc = -float("inf")
        for new_feature in sorted(remaining): # test all features
            test_features = current_set + [new_feature] # test current feature set + additional
            acc = nearest_neighbor(data, test_features)
            print(f"Using features {test_features} accuracy is {acc * 100:.3f}%")

            if acc > branchlevel_acc: # if test feature is better than our other features at this level
                branchlevel_acc = acc
                best_feature = new_feature
        # if best_feature is None:    # early abandomment, if adding new features atlevel doesnt improve, break off.
        #     break
        current_set.append(best_feature) # add feature to this iteration
        remaining.remove(best_feature) # remove from set. we would not test it again
        current_acc = branchlevel_acc

        print(f"\nFeature set {current_set} was best, accuracy is {branchlevel_acc * 100:.3f}%")
        if current_acc > best_acc: #if new subset is better than global subset then replace
            best_acc = current_acc
            best_set = current_set.copy()

    return best_set, best_acc


def backward_elimination(data):
    current_set = list(range(1, len(data[0])))  # list of all featuers
    best_set = current_set.copy()
    best_acc = nearest_neighbor(data, current_set) # test accuracy with all features

    current_acc = best_acc
    while len(current_set) > 1:     # stop when one feature left
        best_remove = None
        branchlevel_acc = -float("inf")

        for feature in sorted(current_set):
            test_features = [x for x in current_set if x != feature] # removing features that are only in the current subset.
                                                                # dont remove a feature that isnt even in the current
            acc = nearest_neighbor(data, test_features)
            print(f"Using features {test_features} accuracy is {acc * 100:.3f}%")

            if acc > branchlevel_acc:
                branchlevel_acc = acc
                best_remove = feature
        # if best_remove is None: # early abandon if no removal improves accuracy
        #     break

        current_set.remove(best_remove) # actual removal
        current_acc = branchlevel_acc

        print(f"\nFeature set {current_set} was best after removal, accuracy is {current_acc * 100:.3f}%")

        if current_acc > best_acc: # update best
            best_acc = current_acc
            best_set = current_set.copy()

    return best_set, best_acc

def main():
    while True:
        print("Welcome to my Feature Selection Classifier Algorithm \n")

        choice = input("Select dataset: type '1' for small, '2' for large, '3' for sanitycheck1, '4' for sanitycheck2: ").strip()
        if choice == '1':
            data_file = 'CS170_Small_DataSet__31.txt'
        if choice == '2':
            data_file = 'CS170_Large_DataSet__7.txt'
        if choice == '3':
            data_file = 'SanityCheck_DataSet__1.txt'
        if choice == '4':
            data_file = 'SanityCheckDataSet__2.txt'
  
        data = load(data_file)

        # Print a dynamic trace reflecting the loaded data
        features = len(data[0]) - 1
        instances = len(data)
        allfeatures = list(range(1, len(data[0])))
        allacc = nearest_neighbor(data, allfeatures)

        
        print("Type the number of the algorithm you want to run. \n")
        print("\t 1) Forward Selection")
        print("\t 2) Backward Elimination \n")

        choice = input("Select: ").strip()

        print(f"This dataset has {features} features, with {instances} instances.")
        print(f"Running nearest neighbor with all {features} features, using \"leaving-one-out\"")
        print(f"evaluation, I get an accuracy of {allacc * 100:.1f}%")
        print("Beginning search.\n")

        if choice == '1':
            print(f"Using features [] accuracy is {zero_features(data) * 100:.3f}% \n")
            start_time = time.perf_counter()
            selected, sel_acc = forward_selection(data)
            end_time = time.perf_counter()
            print(f"Finished Search! The best feature subset is {selected}, which has an accuracy of {sel_acc:%}")
            print(f"Elapsed time: {end_time - start_time:.3f} seconds")
            break
        if choice == '2':
            print(f"All feature subset has an accuracy of {allacc:%}")
            start_time = time.perf_counter()
            selected, sel_acc = backward_elimination(data)
            end_time = time.perf_counter()
            print(f"Finished Search! The best feature subset is {selected}, which has an accuracy of {sel_acc:%}")
            print(f"Elapsed time: {end_time - start_time:.3f} seconds")
            break
        print("Please enter '1' or '2'.")
    
    # print(f"Finished Search! The best feature subset is {selected}, which has an accuracy of {sel_acc:%}")
    # print(f"Elapsed time: {end_time - start_time:.3f} seconds")



if __name__ == "__main__":
    main()