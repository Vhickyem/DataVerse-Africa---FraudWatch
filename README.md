# FraudWatch Africa

## Problem Statement  
The availability and rise of mobile money platforms and services has significantly improved financial inclusion in Africa. However, it has also gained the attraction of fraudsters, who exploit factors such as anonymity of transactions and weak security measures. And as a result, incidents of identity theft, SIM swaps and unauthorized transactions, have also been on the rise.

## Objective
Implement and Build a model using suitable anomaly detection algorithm, that accurately detects and flags a fraudulent transaction. Also deploy model for integration into existing services and for real-time monitoring of transactions.

## Data Source  
Due to an inavailability of data for the company in consideration, the dataset used for this project was simulated. It consists of 10,000 transactions that spans across different user details and behaviours such as *Transaction ID*, *User ID*, *Transaction Type*, *Amount*, *Location*, *Network Provider*, *Device Type*, *User Type*, *Time of the day*, *Foreign Transaction flags*, *SIM swap flags*, *Multiple accounts flags* and *datetime*.

## Data Preprocessing  
* Missing values and duplicates were checked for
* Data was cleaned and inconsistencies, especially in the *transaction_type* column were removed
* *time of the day* column had no value and so was gotten from the *datetime* column
* Invalid transactions below 1KSH were eliminated to ensure data integrity and high-value *amount* were capped at the 99th percentile to mitigate skew without losing too much data
* To enhance fraud detection, features like *night_transaction*, *transaction_frequency*, *avg_amount_per_user* and *fraud_risk_score*, were engineered based on domain knowledge that these features would amplify signals from suspicious transactions and so improve the model's sensitivity
* Scaling was applied to balance feature magnitudes. Due to the presence of outliers, the Robust Scaler which wasn't as sensitive to outliers was used.

## Data Analysis and Visualizations  
Data was analysed using Python libraries such as *Pandas*, *Matplotlib* and *Seaborn*

## Modelling
The Isolation Forest Algorithm was employed

## Challenges  
* Data Imbalances such as >5% foreign numbers, and this was addresses by application of weighting technique, to remove model balance
* Probably due to simulation, data distribution was shown to be uniform, and we were unable to notice a clean pattern. To solve that, log scales and interaction analyses were used.
