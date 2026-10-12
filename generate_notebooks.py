import json
import os

def create_notebook(filename, cells):
    nb = {
        "cells": cells,
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(filename, "w") as f:
        json.dump(nb, f, indent=2)

def markdown_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": [source]}

def code_cell(source):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [source]}

def create_notebooks():
    os.makedirs("notebooks", exist_ok=True)
    
    # 01
    cells_1 = [
        markdown_cell("# 01. Data Exploration"),
        markdown_cell("This notebook loads the dataset, checks its dimensions, and performs basic exploratory data analysis (EDA)."),
        code_cell("import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport sys\nsys.path.append('..')\nfrom src.data.loader import load_data\n\ntrain_df, test_df, rul_df = load_data()\ntrain_df.head()"),
        code_cell("print(f'Train shape: {train_df.shape}')\nprint(f'Test shape: {test_df.shape}')"),
        code_cell("train_df.describe()"),
        markdown_cell("## Sensor Trends\nLet's visualize the trends of sensors for a specific engine."),
        code_cell("engine_1 = train_df[train_df['unit_id'] == 1]\nplt.figure(figsize=(10,4))\nplt.plot(engine_1['cycle'], engine_1['sensor_2'])\nplt.title('Sensor 2 vs Cycle (Unit 1)')\nplt.xlabel('Cycle')\nplt.ylabel('Sensor 2 Value')\nplt.show()")
    ]
    create_notebook("notebooks/01_data_exploration.ipynb", cells_1)
    
    # 02
    cells_2 = [
        markdown_cell("# 02. Feature Engineering"),
        markdown_cell("This notebook generates the Remaining Useful Life (RUL) labels and implements feature engineering (rolling stats)."),
        code_cell("import pandas as pd\nimport sys\nsys.path.append('..')\nfrom src.data.preprocessing import generate_train_rul\nfrom src.features.engineering import add_rolling_features"),
        code_cell("# Load data and generate RUL\n# train_df = ...\n# train_df = generate_train_rul(train_df)\n# train_df.head()")
    ]
    create_notebook("notebooks/02_feature_engineering.ipynb", cells_2)

    # 03
    cells_3 = [
        markdown_cell("# 03. Machine Learning Models"),
        code_cell("import sys\nsys.path.append('..')\nfrom src.models.baseline import train_baseline\nfrom src.models.random_forest import train_random_forest\nfrom src.models.xgboost_model import train_xgboost")
    ]
    create_notebook("notebooks/03_ml_models.ipynb", cells_3)

    # 04
    cells_4 = [
        markdown_cell("# 04. LSTM Model"),
        code_cell("import sys\nsys.path.append('..')\nfrom src.features.engineering import generate_sequences\nfrom src.models.lstm import train_lstm_model")
    ]
    create_notebook("notebooks/04_lstm_model.ipynb", cells_4)

    # 05
    cells_5 = [
        markdown_cell("# 05. Model Comparison"),
        code_cell("import json\nimport pandas as pd\nimport sys\nsys.path.append('..')\nfrom src.evaluation.plots import plot_model_comparison")
    ]
    create_notebook("notebooks/05_model_comparison.ipynb", cells_5)

if __name__ == "__main__":
    create_notebooks()
