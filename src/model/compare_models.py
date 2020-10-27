# %%
from sklearn.linear_model import Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from train_test_model import train_test_model
import numpy as np
import pandas as pd
from joblib import dump
from sklearn.preprocessing import StandardScaler

df = pd.read_csv(r'..\..\data\final\final.csv')
num_cols = df.select_dtypes(np.number).drop(columns=['geoid', 'avg']).columns

# %% Ridge Regression
%%time
param_distributions = {'model__alpha': np.logspace(-5, 5, 500)}
model, prediction = train_test_model(df, Ridge, 'avg', num_cols, param_distributions)
dump(model, r'..\..\models\ridge.joblib')
dump(prediction, r'..\..\results\ridge.joblib')

# %% Lasso Regression 
%%time
param_distributions = {'model__alpha': np.logspace(-5, 5, 500)}
model, prediction = train_test_model(df, Lasso, 'avg', num_cols, param_distributions)
dump(model, r'..\..\models\lasso.joblib')
dump(prediction, r'..\..\results\lasso.joblib')

# %% KNN
%%time
param_distributions = {'model__n_neighbors': np.linspace(1, 100, 500, dtype=int)}
model, prediction = train_test_model(df, KNeighborsRegressor, 'avg', num_cols, param_distributions)
dump(model, r'..\..\models\knn.joblib')
dump(prediction, r'..\..\results\knn.joblib')

# %% Random Forest
%%time
param_distributions = {
    'model__n_estimators': [50, 75, 100],
    'model__max_features': ["auto", 3, 5, 7],
    'model__max_depth'   : [None, 3, 5, 10]
}
model, prediction = train_test_model(df, RandomForestRegressor, 'avg', num_cols, param_distributions)
dump(model, r'..\..\models\random_forest.joblib')
dump(prediction, r'..\..\results\random_forest.joblib')
# %%
coefs = pd.DataFrame(
    model.named_steps['model'].regressor_.coef_,
    columns=['Coefficients'], index=num_cols
)