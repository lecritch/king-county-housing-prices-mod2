# imports:
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')

from statsmodels.formula.api import ols
import statsmodels.api as sm
import scipy.stats as stats


def check_for_assumptions(modelname):
#     rsquared = modelname.rsquared
#     params = modelname.params
#     print(f'Rsquared of Model: {rsquared}')
#     print('----------')
#     print('Beta values of Model:')
#     print(params)
#     rainbow_statistic, rainbow_p_value = linear_rainbow(model1)
#     print("Rainbow statistic:", rainbow_statistic)
#     print("Rainbow p-value:", rainbow_p_value)
    fig, ax = plt.subplots(1,2, figsize=(12,6))
    residuals = modelname.resid
    fig = sm.graphics.qqplot(residuals, dist=stats.norm, line='45', fit=True, ax=ax[0])
    ax[0].set_title('QQ-Plot of Residuals')
    ax[1].scatter(modelname.predict(), modelname.resid)
    sns.set(font_scale = 1)
    ax[1].set_title('Homoscadasicity Assumption')
    plt.xlabel('Model Predictions')
    plt.ylabel('Model Residuals')
    ax[1].plot(modelname.predict(), [0 for i in range(len(df))], color = 'red')
    fig.tight_layout()
    return plt.show()


def z_score(feature, df):
    """
    feaure is a string of the feature you want the z-score of
    df is the dataframe where the feature can be found
    """
    z_name = 'z_' + feature
    df[z_name] = (df[feature] - df[feature].mean()) / df[feature].std()
    
    return df


def model(lst_of_features, df, target_var):
    """
    lst_of_features is a list of strings of the features to use from the df
    df is the data frame to subset the features from 
    target_var is a string of the target variable
    """

    # Create a dataframe with only the target and the chosen corellation feature
    df_model = df[lst_of_features]

    # build the R-style formula.
    target = target_var
    copy_lst_features = lst_of_features.copy()
    copy_lst_features.remove(target)
    x_vals = copy_lst_features
    x_formula = '+'.join(x_vals)
    formula = target + '~' + x_formula

    # Fit the model on the dataframe composed of the two features
    model = ols(formula=formula, data=df_model).fit()
    
    print(model.summary())
    # view r^2 and model summary:
    
    # check assumptions
#     normality_assumption(model)
#     homo_assumption(model, df)
    
    return model


def normality_assumption(model):
    # plot normality assumption
    fig, ax = plt.subplots(figsize = (15, 10))
    figure = sm.graphics.qqplot(model.resid, dist=stats.norm, line='45', fit=True, ax = ax);
    ax.set_title('QQ-Plot of Residuals', fontsize = 25)
    return plt.show()


def homo_assumption(model, df):
    # plot homoscadasicity assumption
    fig, ax = plt.subplots(figsize = (15, 10))
    plt.scatter(model.predict(), model.resid)
    sns.set(font_scale = 1)
    fig.suptitle('Scatter Plot of Model Predictions vs. Residuals', fontsize = 25)
    # ax.set_title('Homoscadasicity Assumption Not Met', fontsize = 20) - change this to an iff statement maybe...
    plt.xlabel('Model Predictions', fontsize = 18)
    plt.ylabel('Model Residuals', fontsize = 18)
    ax.tick_params(labelsize=10)
    plt.plot(model.predict(), [0 for i in range(len(df))], color = 'red')
    return plt.show()

def heatmap_multi(x_features, df):
    """
    Creates a heatmap of all the x feautres in a model to show multicollinearity.
    x_features (lst):  A list of strings of the column header names of the x features in the model
    df:  the dataframe where the features belong
    returns the plotted heatmap
    """
    df_x_feats = df.loc[:, x_features]

    x_corrs = df_x_feats.corr()

    mask = np.triu(np.ones_like(x_corrs, dtype=np.bool))
    f, ax = plt.subplots(figsize = (18, 16))
    sns.heatmap(x_corrs, mask = mask, cmap="YlGnBu", vmax = 0.3, 
            center = 0, square = True, linewidths = 0.5, 
            cbar_kws = {'shrink': 0.5})
    ax.tick_params(axis='both', which='major', labelsize=20, labelrotation = 45)
    ax.set_title('Heat Map of Feature Multicollinearity', fontsize = 30)
    
    return plt.show()