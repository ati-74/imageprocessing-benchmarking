"""
This script plots single-cell measurements exported from
ProcessCellProfilerdata.ProcessData() 

Instructions:
1. Optional: adjust plotting parameters for min/max of x-axis
2. Optional: adjust filtering range for growth rate
3. Run the script and select the .csv file to process
4. Save figures manually
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import lognorm
from tkinter import Tk
from tkinter.filedialog import askopenfilename

plt.rcParams.update({'font.size': 12})

def plot_radius_pdf(data, fig, distribution='norm', xmin=0, xmax=1.0):
    """
    Plots a histogram of the cell radii as probability density function
    
    @param data     Analyzed data from CelProfiler as dataframe
    @param fig      pyplot figure
    @param xmin     Start plotting the distribution at xmin
    @param xmax     Stop plotting the distribution at xmax
    """
    
    radius = data.groupby(['id'])['radius'].mean()
    plt.hist(radius, bins = 100, density = True, facecolor = 'b', alpha = 1)
    fit_dist(radius, xmin, xmax, distribution)
        
    # labels
    plt.xlabel('Radius (um)')
    plt.ylabel('Density')
    plt.xlim(xmin, xmax)
    
def plot_division_length_pdf(data, fig, distribution='norm', xmin=0, xmax=10):
    """
    Plots a histogram of division length as probability density function.
    Currently, the function assumes that 'length' is the total length of the cell;
    CellModeller takes the length as L_total - 2*r
    
    @param data     Analyzed data from CelProfiler as dataframe
    @param fig      pyplot figure
    @param xmin     Start plotting the distribution at xmin
    @param xmax     Stop plotting the distribution at xmax
    """
    
    data_divideFlag = data[data['divideFlag'] == True]
    division_length = data_divideFlag['length'] - 2*data_divideFlag['radius']
       
    # plot historgram
    plt.hist(division_length, bins = 100, density = True, facecolor = 'b', alpha = 1)
    fit_dist(division_length, xmin, xmax, distribution)
    
    # labels
    plt.xlabel('Division length (um)')
    plt.ylabel('Density')
    

def plot_growth_rate_pdf(data, fig, filter_min, filter_max, distribution='norm'):
    """
    Plots a histogram of growth rate as probability density function
    
    @param  data        analyzed data from CelProfiler as dataframe
    @param  fig         pyplot figure
    @param  filter_min  minimum growth rate required to be included in analysis
    @param  filter_max  maxiimum growth rate required to be included in analysis
    """

    # Filter between min and max values
    growth_rate_filter = (
        data.
        groupby("id", dropna=True).
        filter(lambda x: x['growthRate'].mean() >= filter_min and x['growthRate'].mean() <= filter_max)
    )
    growth_rate = growth_rate_filter.groupby(['id'])['growthRate'].mean()

    # plot historgram
    xmin = filter_min; xmax = filter_max
    plt.hist(growth_rate, bins = 100, density = True, facecolor = 'b', alpha = 1)
    fit_dist(growth_rate, xmin, xmax, distribution)

    # labels
    plt.xlabel('Growth Rate (1/h)')
    plt.ylabel('Density')
    plt.xlim(xmin, xmax)
      
def fit_dist(data, xmin, xmax, distribution):
    """
    Fits a normal distribution to data and plots
    
    @param data Experiental data
    @param xmin Start plotting the distribution at xmin
    @param xmax Stop plotting the distribution at xmax
    @param distribution The type of distribution to fit
    """
    samples = len(data)
    if distribution == 'norm':
        mu, std = norm.fit(data)
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        title = "Fit results: mean = %.2f,  std = %.2f,  n = %d" % (mu, std, samples)
    elif distribution == 'lognorm':
        shape, loc, scale = lognorm.fit(data) # shape = std, scale = exp(mean)
        x = np.linspace(xmin, xmax, 100)
        p = lognorm.pdf(x, shape, loc, scale)
        title = "Fit results: mean = %.2f,  std = %.2f, loc = %.2f,  n = %d" % (scale, shape, loc, samples)
    plt.plot(x, p, 'k', linewidth=2)
    
    plt.title(title)
    
if __name__ == "__main__":
    # Read in data
    print('Select the analysis csv file')
    csv_file = askopenfilename()
    print(csv_file)
    data = pd.read_csv(csv_file)
    data.dropna()
    
    # Plot growth rates
    growth_filter_min = 0.25
    growth_filter_max = 2.1 #doubling time of 0.33 h (20 min) [growth_rate = ln(2)/doubling_time]
    growth_fig = plt.figure(1)
    plot_growth_rate_pdf(data, growth_fig, growth_filter_min, growth_filter_max, distribution='lognorm')
        
    # Plot radii
    radius_fig = plt.figure(2)
    plot_radius_pdf(data, radius_fig, distribution='lognorm')
    
    # Plot division length
    division_length_fig = plt.figure(3)
    plot_division_length_pdf(data, division_length_fig, distribution='lognorm')
    
    plt.show()