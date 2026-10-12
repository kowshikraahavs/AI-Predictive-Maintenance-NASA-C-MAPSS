import numpy as np
import pandas as pd
import os

def generate_cmapss_dummy():
    np.random.seed(42)
    os.makedirs("data/raw", exist_ok=True)
    
    # Generate 5 engines
    train_data = []
    test_data = []
    rul_data = []
    
    for unit_id in range(1, 6):
        # random max cycle between 150 and 200
        max_cycle = np.random.randint(150, 200)
        
        # training data (full run to failure)
        for cycle in range(1, max_cycle + 1):
            row = [unit_id, cycle]
            settings = np.random.randn(3).tolist()
            sensors = np.random.randn(21).tolist()
            train_data.append(row + settings + sensors)
            
        # testing data (runs up to some random cycle before failure)
        test_max_cycle = np.random.randint(50, max_cycle - 20)
        for cycle in range(1, test_max_cycle + 1):
            row = [unit_id, cycle]
            settings = np.random.randn(3).tolist()
            sensors = np.random.randn(21).tolist()
            test_data.append(row + settings + sensors)
            
        # True RUL for the last cycle of testing data
        true_rul = max_cycle - test_max_cycle
        rul_data.append([true_rul])
        
    train_df = pd.DataFrame(train_data)
    test_df = pd.DataFrame(test_data)
    rul_df = pd.DataFrame(rul_data)
    
    train_df.to_csv("data/raw/train_FD001.txt", sep=" ", index=False, header=False)
    test_df.to_csv("data/raw/test_FD001.txt", sep=" ", index=False, header=False)
    rul_df.to_csv("data/raw/RUL_FD001.txt", sep=" ", index=False, header=False)
    
    print("Dummy CMAPSS data generated successfully.")

if __name__ == "__main__":
    generate_cmapss_dummy()
