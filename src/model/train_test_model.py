from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV, RepeatedKFold 
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
import pandas as pd

def train_test_model(df, model, target, num_cols, param_distributions):
    # Trains model fitting hyperparameters with a randomized search and returns
    # best estimator
    numeric_transformer = Pipeline(
    steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
            ('scaler', StandardScaler())
        ]
    )

    preprocessor = ColumnTransformer(
                    [('numeric', numeric_transformer, num_cols)],
                    remainder='drop')

    # Split train and test set
    X_train, X_test, y_train, y_test = train_test_split(
                                            df.drop(target, axis = 'columns'),
                                            df[target],
                                            train_size   = 0.8,
                                            random_state = 1234,
                                            shuffle      = True)

    #Train
    pipe = Pipeline([('preprocessing', preprocessor),
                ('model', model())])

    grid = RandomizedSearchCV(
            estimator=pipe,
            param_distributions=param_distributions,
            n_iter=20,
            scoring='neg_root_mean_squared_error',
            cv=RepeatedKFold(n_splits = 5, n_repeats = 3), 
            refit= True, 
            n_jobs=-1,
            verbose=0,
            random_state=123,
            return_train_score=True
        )

    grid.fit(X = X_train, y = y_train)

    final_model = grid.best_estimator_

    #Test and compute errors
    prediction = final_model.predict(X = X_test)
    rmse_final = mean_squared_error(
            y_true  = y_test,
            y_pred  = prediction,
            squared = False
          )
    mae_final = mean_absolute_error(
        y_true  = y_test,
        y_pred  = prediction,
    )
    r2_final = r2_score(
        y_true  = y_test,
        y_pred  = prediction
    )
    print(f'rmse: {rmse_final}')
    print(f'mae_score: {mae_final}')
    print(f'r2_score: {r2_final}')

    return final_model, pd.DataFrame({'target' : y_test, 'prediction' : prediction})