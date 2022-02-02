import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

from utils.data_processing import min_max_scaler, df_melter

def subplot_generator(df: pd.DataFrame, plot: str, y=None) -> None:
    """
    Prepare the main plot to be filled out with subplots.
    """
    df = min_max_scaler(df)

    fig, axes = plt.subplots(2, 5, figsize=(16, 12), sharey=True)
    fig.tight_layout(pad=3.0)
    axes = axes.flatten()

    plot_feature(df, plot, axes)
    
def plot_feature(df: pd.DataFrame, plot: str, axes, y=None) -> None:
    """
    Create the selected plot for each future in the DataFrame.
    """
    for i, feature in enumerate(df.columns):
        if plot == 'histogram':
            histoplot(df, feature, i, axes)
        elif plot == 'violinplot':
            violinplot(df, y, feature, i, axes)
        elif plot == 'swarmplot':
            swarmplot(df, y, feature, i, axes)
        elif plot == 'boxplot':
            boxplot(df, y, feature, i, axes)


def histoplot(df: pd.DataFrame, feature: str, i: int, axes) -> None:
    """
    Prepare the several histograms to enter the main plot.
    """

    bin_count = int(np.ceil(np.log2(len(df))) + 1)

    sns.histplot(ax=axes[i],
                data=df,
                x=feature,
                bins=bin_count,
                kde=True,
                line_kws={'lw': 3})

    plot_polishing(axes=axes, i=i, plot='histogram')

def violinplot(df: pd.DataFrame, y: pd.Series, feature: str, i: int, axes) -> None:
    """
    Prepare the several violinplots to enter the main plot.
    """

    df = df_melter(y, df)

    sns.violinplot(ax=axes[i],
                data=df[df['features'] == feature],
                x='features', 
                y='value', 
                hue='diagnosis',
                split=True)

    plot_polishing(axes=axes, i=i, plot='violinplot')

def swarmplot(df: pd.DataFrame, y: pd.Series, feature: str, i: int, axes) -> None:
    """
    Prepare the several swarmplots to enter the main plot.
    """
    
    df = df_melter(y, df)

    sns.swarmplot(ax=axes[i],
                data=df[df['features'] == feature],
                x='features', 
                y='value', 
                hue='diagnosis',
                size=3)
    
    plot_polishing(axes=axes, i=i, plot='swarmplot')

def boxplot(df: pd.DataFrame, y: pd.Series, feature: str, i: int, axes) -> None:
    """
    Prepare the several swarmplots to enter the main plot.
    """

    sns.boxplot(ax=axes[i],
                data=df,
                x=feature,
                orient='v',
                width=0.3,
                flierprops={'marker' : 'x',
                            'markeredgecolor' : 'red', 
                            'markersize' : 6})
    
    plot_polishing(axes=axes, i=i, plot='histogram')


def plot_polishing(axes, i: int, plot: str) -> None:
    """
    Eliminate the clutter from the plots. 
    """
    axes[i].spines['top'].set_visible(False)
    axes[i].spines['right'].set_visible(False)
    axes[i].spines['left'].set_visible(False)
    axes[i].get_yaxis().set_visible(False)

    if plot in {'boxplot', 'histogram'}:
        axes[i].set(ylabel='')
        axes[i].set_xticks([])
    else:
        axes[i].get_legend().remove()
        axes[i].set(xlabel='', ylabel='')