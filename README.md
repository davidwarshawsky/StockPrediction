  # Stock Prediction Project

This project aims to develop a model capable of predicting stock prices using historical data and various technical indicators.

## Data

The project utilizes historical stock price data from various sources, including:

- **Yahoo Finance:** Provides historical stock prices, dividends, and splits.
- **Financial Modeling Prep:** Offers fundamental data like financial statements, key ratios, and company news.

The data is preprocessed to extract relevant features and handle missing values.

## Models

The project implements different machine learning models for stock prediction, including:

- **Long Short-Term Memory (LSTM):** A type of recurrent neural network suitable for time series data.
- **Transformer:** An attention-based neural network architecture known for its effectiveness in natural language processing and time series forecasting.

## Training

The training process involves:

- **Data Splitting:** Dividing the data into training, validation, and testing sets.
- **Model Selection:** Choosing the appropriate model based on the data characteristics and prediction requirements.
- **Hyperparameter Tuning:** Optimizing the model's parameters to achieve the best performance.
- **Model Training:** Training the chosen model on the training data.

## Evaluation

The trained models are evaluated using various metrics, including:

- **Mean Absolute Error (MAE):** Measures the average absolute difference between predicted and actual prices.
- **Root Mean Squared Error (RMSE):** Measures the square root of the average squared difference between predicted and actual prices.
- **R-squared:** Indicates the proportion of variance in the dependent variable (stock price) that is explained by the independent variables (features).
