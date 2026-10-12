# Academic Project Explanation & Viva Preparation

## 1. Problem Statement
In the aviation and mechanical engineering industries, unexpected engine failures can lead to disastrous consequences and massive financial losses. The traditional approach to maintenance involves replacing parts based on fixed time intervals (preventive maintenance), which often results in replacing perfectly healthy components, wasting resources.

## 2. Why Predictive Maintenance?
Predictive Maintenance (PdM) leverages data from sensors to monitor the real-time health of equipment. By predicting when a machine will fail, maintenance can be scheduled "just in time." This maximizes the useful life of components while preventing unexpected catastrophic failures.

## 3. What is Remaining Useful Life (RUL)?
RUL is the estimated number of operational cycles (or hours, flights, etc.) an engine has left before it degrades beyond a safe operational threshold and fails.

## 4. Dataset Overview (C-MAPSS)
The project utilizes the NASA C-MAPSS (Commercial Modular Aero-Propulsion System Simulation) dataset. It provides simulated data of turbofan engines degrading over time.
- It contains **21 sensor readings** (e.g., temperature, pressure, fan speed) and **3 operational settings**.
- The data is structured as time-series sequences representing the life of each engine from a healthy state to failure.

## 5. Data Preprocessing & Leakage Prevention
Preprocessing involves cleaning the data, handling missing values, and scaling features.
- **Scaling:** Sensor readings have vastly different ranges. We use `StandardScaler` to normalize them.
- **Data Leakage Prevention:** Scalers must ONLY be fitted on the training dataset. If we fit them on the entire dataset (train + test), information from the test set "leaks" into the training process, leading to falsely high accuracy.

## 6. Feature Engineering
Instead of just using raw sensor data, we generate features that capture the *trend* of degradation:
- **Rolling Means and Standard Deviations:** To smooth out sensor noise and capture the rate of degradation over time.
- **Sequence Generation:** Grouping data into sliding windows (e.g., 30 cycles) to feed into the LSTM model.

## 7. Machine Learning Models
We implemented multiple models to establish a comprehensive comparison:
- **Linear Regression:** Used as a simple baseline. It assumes a linear relationship between sensors and RUL, which is rarely true in complex mechanical systems.
- **Random Forest:** An ensemble of decision trees. It captures non-linear relationships well but doesn't inherently understand time-series sequences.
- **Gradient Boosting (XGBoost/HistGradientBoosting):** Builds trees sequentially to correct the errors of previous trees, generally providing higher accuracy for tabular data.

## 8. Deep Learning: Why LSTM?
Long Short-Term Memory (LSTM) networks are a specialized type of Recurrent Neural Network (RNN).
- Mechanical degradation is a **sequential process**. The health of an engine at cycle $t$ depends heavily on its state at cycle $t-1$.
- Standard ML models treat every row independently. LSTMs maintain an internal "memory" state, allowing them to learn patterns over time from sequences of sensor data.

## 9. Evaluation Metrics
In regression tasks, accuracy is not a valid metric because we are predicting a continuous number.
- **MAE (Mean Absolute Error):** The average absolute difference between the predicted RUL and the actual RUL. If MAE is 10, our predictions are off by 10 cycles on average.
- **RMSE (Root Mean Squared Error):** Similar to MAE but squares the errors before averaging. This heavily penalizes large errors, which is crucial in predictive maintenance (a large error could mean a fatal crash).

---

## 🟢 Potential Viva Questions & Answers

**Q1: What is predictive maintenance?**
**A:** It is a technique that uses data analysis and machine learning to monitor equipment condition and predict when maintenance should be performed, optimizing component lifespan and preventing sudden failures.

**Q2: What is RUL?**
**A:** Remaining Useful Life. It is the number of cycles or time units left before a machine component fails.

**Q3: Why did you choose the NASA C-MAPSS dataset?**
**A:** It is a highly respected, standardized benchmark dataset in the Prognostics and Health Management (PHM) community, widely used for evaluating predictive maintenance algorithms.

**Q4: Why can't we just use Accuracy to evaluate this model?**
**A:** Because this is a regression problem, not a classification problem. We are predicting a continuous number (cycles), not categorizing data into classes (like "cat" or "dog").

**Q5: What is overfitting and how did you prevent it?**
**A:** Overfitting happens when a model memorizes the training data but fails to generalize to new data. I prevented it by using Techniques like Dropout in the LSTM, Early Stopping (halting training when validation loss stops improving), and cross-validation for ML models.

**Q6: How did you prevent data leakage?**
**A:** By ensuring that the scaler (`StandardScaler`) was fitted exclusively on the training data. The testing data was only transformed. Also, by splitting sequences correctly so future data doesn't influence past predictions.

**Q7: What does LSTM solve compared to ordinary regression?**
**A:** Ordinary regression treats each data point independently. LSTM is designed for time-series data; it remembers past sequential information, which is critical since mechanical wear is a progressive, time-dependent process.

**Q8: What is the purpose of Dropout in your LSTM?**
**A:** Dropout randomly ignores a fraction of neurons during training. This prevents the network from relying too heavily on any specific neuron, reducing overfitting and making the model more robust.

**Q9: What are the limitations of this specific project?**
**A:** The FD001 dataset assumes only one operating condition and one fault mode. Real engines operate under varying altitudes, temperatures, and speeds (as seen in FD002-FD004 datasets), which requires more complex modeling. Furthermore, it is simulated data, not physical real-world data.
