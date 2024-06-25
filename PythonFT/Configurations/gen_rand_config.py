import csv
import random
import os 


def gen_rand_boolean_val_for_trials(): 
    # generate random boolean value
    random_values = [random.randint(0, 1) for _ in range(100)]
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_name = 'random_booleans.csv'
    FilePath = os.path.join(dir_path, file_name)
    # Write the random boolean values to the CSV file
    with open(FilePath, mode='w', newline='') as file:
        writer = csv.writer(file)
        for value in random_values:
            writer.writerow([value])

    print(f'{FilePath} has been written with 100 random boolean values.')

def gen_rand_triger_positions():
    random_values = [random.uniform(0.5, 0.8) for _ in range(100)]
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_name = 'random_triggers.csv'
    FilePath = os.path.join(dir_path, file_name)

    # Write the random values to the CSV file
    with open(FilePath, mode='w', newline='') as file:
        writer = csv.writer(file)
        for value in random_values:
            writer.writerow([value])

    print(f'{FilePath} has been written with 100 random values.')

def gen_target_position():
    random_values = [random.randint(0, 2) for _ in range(100)]
    random_values = [0.25 if x == 0 else 0.5 if x == 1 else 0.75 if x ==2 else x for x in random_values]
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_name = 'random_target_pos.csv'
    FilePath = os.path.join(dir_path, file_name)

    # Write the random values to the CSV file
    with open(FilePath, mode='w', newline='') as file:
        writer = csv.writer(file)
        for value in random_values:
            writer.writerow([value])

    print(f'{FilePath} has been written with 100 random values.')


#gen_rand_triger_positions()
#gen_target_position()
gen_rand_boolean_val_for_trials()
