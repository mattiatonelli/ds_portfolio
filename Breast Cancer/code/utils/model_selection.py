import pandas as pd
import numpy as np

from skopt import BayesSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import recall_score


def nested_cv(X: pd.DataFrame, y: pd.Series, cv_outer: StratifiedKFold, opt_search: BayesSearchCV, validation_result: bool) -> None:
    """
    Run the nested cross validation.
    """
    outer_results, inner_results = outer_loop(X=X, y=y, cv_outer=cv_outer, opt_search=opt_search, validation_result=validation_result)

    # print the CV overall results
    print(f'Recall | Validation Mean: {round(np.mean(inner_results), 3)}, Validation Std: {round(np.std(inner_results), 3)}')
    print(f'Recall | Test Mean: {round(np.mean(outer_results), 3)}, Test Std: {round(np.std(outer_results), 3)}')
    

def outer_loop(X: pd.DataFrame, y: pd.Series, cv_outer: StratifiedKFold, opt_search: BayesSearchCV, validation_result: bool) -> list:
    """
    Perform the outer loop split and per each fold, its inner loop.
    """
    outer_results, inner_results = [], []
    
    for i, (train_index, test_index) in enumerate(cv_outer.split(X, y), start=1):
        X_train, X_test = X.loc[train_index], X.loc[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        # start the Bayes search
        _ = opt_search.fit(X_train, y_train)

        # save the best model
        best_model = opt_search.best_estimator_

        # predict on the test set
        y_pred = best_model.predict(X_test)

        # calculate the recall on test set
        recall = recall_score(y_test, y_pred)
        
        # append the recall results
        outer_results.append(recall)
        inner_results.append(opt_search.best_score_)
        
        print_validation_results(i=i, opt_search=opt_search, recall=recall, validation_result=validation_result)
    
    return outer_results, inner_results


def print_validation_results(i: int, opt_search: BayesSearchCV, recall: float, validation_result: bool) -> None:
    """
    Print the validation results per each fold.
    """
    if validation_result:
        print(f'Fold {i}')
        print(f'Recall | Validation: {round(opt_search.best_score_, 3)}\tTest: {round(recall, 3)}')
        print('\n')
        print(f'Best Hyperparameter Combination:\n{opt_search.best_params_}')
        print('\n')