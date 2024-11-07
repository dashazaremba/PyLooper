import csv
import glob
import os
import shutil
import pandas as pd
import time
import numpy as np

# dictionary of species

sp_map = {
          'LiI' :   3.0,
          'BeI' :   4.0,
          'BeII':   4.1,
          'BI'  :   5.0,
          'CI'  :   6.0,
          'CH'  : 106.0,
          'NI'  :   7.0,
          'OI'  :   8.0,
          'FI'  :   9.0,
          'NaI' :  11.0,
          'MgI' :  12.0,
          'MgII':  12.1,
          'AlI' :  13.0,
          'SiI' :  14.0,
          'PI'  :  15.0,
          'SI'  :  16.0,
          'KI'  :  19.0,
          'CaI' :  20.0,
          'ScI' :  21.0,
          'ScII':  21.1,
          'TiI' :  22.0,
          'TiII':  22.1,
          'VI'  :  23.0,
          'CrI' :  24.0,
          'CrII':  24.1,
          'MnI' :  25.0,
          'FeI' :  26.0,
          'FeII':  26.1,
          'CoI' :  27.0,
          'NiI' :  28.0,
          'CuI' :  29.0,
          'ZnI' :  30.0,
          'RbI' :  37.0,
          'SrI' :  38.0,
          'SrII':  38.1,
          'YII' :  39.1,
          'ZrII':  40.1,
          'BaII':  56.1,
          'LaII':  57.1,
          'CeII':  58.1,
          'NdII':  60.1,
          'SmII':  62.1,
          'EuII':  63.1,
          'DyII':  66.1
          }

# Solar abundances and errs from Asplund 2009 - may need to add more based on the lines you are interested in     

AX_sol = { 
    'LiI' : [1.05, 0.10],
    'CI' : [8.50, 0.06], 'NI' : [7.86, 0.12], 'OI' : [8.76, 0.07],
    'NaI' : [6.24, 0.04], 'MgI' : [7.60, 0.04], 
    'AlI' : [6.45, 0.03],
    'SiI' : [7.51, 0.03], 'SI' : [7.12, 0.03],
    'KI' : [5.03, 0.09], 'SmII' : [0.96, 0.04],
    'CaI' : [6.34, 0.04],'CaII' : [6.34, 0.04],
    'ScI' : [3.15, 0.04], 'ScII' : [3.15, 0.04],
    'TiI' : [4.95, 0.05], 'TiII' : [4.95, 0.05],
    'VI' : [3.93, 0.08], 'VII' : [3.93, 0.08], 
    'CrI' : [5.64, 0.04], 'CrII' : [5.64, 0.04], 
    'MnI' : [5.43, 0.04], 'MnII' : [5.43, 0.04],
    'FeI' : [7.50, 0.04],'FeII' : [7.50, 0.04],
    'CoI' : [4.99, 0.07],'CoII' : [4.99, 0.07],
    'NiI' : [6.22, 0.04], 'NiII' : [6.22, 0.04], 
    'CuI' : [4.19, 0.04], 'CuII' : [4.19, 0.04], 
    'ZnI' : [4.56, 0.05], 'CeII': [1.58, 0.04],
    'SrII' : [2.87, 0.07], 'YII' : [2.21, 0.07], 
    'ZrI' : [2.58, 0.04], 'ZrII' : [2.58, 0.04],
    'BaII' : [2.18, 0.09], 'LaII' : [1.10, 0.04], 
    'NdII': [1.42, 0.04], 'EuII' : [0.52, 0.04], 'PbI' : [1.75, 0.10]}


def format_time(elapsed_time):
    if elapsed_time < 60:
        return f"{elapsed_time:.2f} seconds"
    else:
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60
        return f"{minutes} minutes {seconds:.2f} seconds"


### INPUT FOR q2:

def write_stars_csv(stars_data, filename='stars.csv'):
    fieldnames = ['id', 'teff', 'logg', 'feh', 'vt']
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for star in stars_data:
            writer.writerow(star)
            
def write_lines_csv(lines_file, star_id, filename='lines.csv'):
    fieldnames = ['wavelength', 'species', 'ep', 'gf'] + [star_id]
    
    lines_data = []
    with open(lines_file, 'r') as f:
        next(f)
        for line in f:
            parts = line.strip().split()
            wavelength = float(parts[0])
            species = parts[1]
            ep = float(parts[2])
            gf = float(parts[3])
            ew = float(parts[4])
            
            line_dict = {'wavelength': wavelength, 'species': species, 'ep': ep, 'gf': gf}
            line_dict[star_id] = ew
            lines_data.append(line_dict)
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in lines_data:
            writer.writerow(line)

# def write_lines_csv(lines_file, star_id, filename='lines.csv'):
#     fieldnames = ['wavelength', 'species', 'ep', 'gf'] + [star['id'] for star in stars_data]
    
#     lines_data = []
#     with open(lines_file, 'r') as f:
#         next(f)
#         for line in f:
#             parts = line.strip().split()
#             wavelength = float(parts[0])
#             species = parts[1]
#             ep = float(parts[2])
#             gf = float(parts[3])
#             ew = float(parts[4])
            
#             line_dict = {'wavelength': wavelength, 'species': species, 'ep': ep, 'gf': gf}
#             for star in stars_data:
#                 line_dict[star['id']] = ew
#             lines_data.append(line_dict)
    
#     with open(filename, 'w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for line in lines_data:
#             writer.writerow(line)
            
### Append other lines to Fe:

def append_lines_to_csv(lines_file, star_id, existing_csv='lines.csv'):
    fieldnames = ['wavelength', 'species', 'ep', 'gf', star_id]  # Put star_id inside a list
    
    lines_data = []
    with open(lines_file, 'r') as f:
        next(f)
        for line in f:
            parts = line.strip().split()
            wavelength = float(parts[0])
            species = float(parts[1])
            ep = float(parts[2])
            gf = float(parts[3])
            ew = float(parts[4])
            
            # Check if ew is not equal to -99.9 before appending
            if ew != -99.9:
                line_dict = {'wavelength': wavelength, 'species': species, 'ep': ep, 'gf': gf}
                line_dict[star_id] = ew
                lines_data.append(line_dict)
    
    existing_lines = set()
    with open(existing_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existing_lines.add((float(row['wavelength']), float(row['species']), float(row['ep']), float(row['gf']), float(row[star_id])))
    
    new_lines_data = []
    for line in lines_data:
        if (line['wavelength'], line['species'], line['ep'], line['gf'], line[star_id]) not in existing_lines:
            new_lines_data.append(line)
            existing_lines.add((line['wavelength'], line['species'], line['ep'], line['gf'], line[star_id]))
    
    with open(existing_csv, 'a', newline='') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for line in new_lines_data:
            writer.writerow(line)


### Remove outliers in abundances from moog output file
                          

def remove_outliers(delta_avg_threshold, moog_out_file, output_file):
    moog_df = pd.read_csv(moog_out_file)
    ab_avg = moog_df['ab'].mean()
    moog_df = moog_df[abs(moog_df['ab'] - ab_avg) <= delta_avg_threshold]
    moog_df.to_csv(output_file, index=False)
    
    print(f'After removing outliers, there are {len(moog_df)} lines remaining.')
    
    return moog_df


### Filter moog output based on strength of lines (ew) and ep             

def filter_moog_output(moog_df, lower_ew_threshold=None, upper_ew_threshold=None, ep_threshold=None):
    moog_df['ew'] = pd.to_numeric(moog_df['ew'], errors='coerce')
    moog_df['ep'] = pd.to_numeric(moog_df['ep'], errors='coerce')
    moog_df['ww'] = pd.to_numeric(moog_df['ww'], errors='coerce')

    if lower_ew_threshold is not None:
        moog_df = moog_df[moog_df['ew'] >= lower_ew_threshold]  # Remove weak lines if lower_threshold is provided
    
    if upper_ew_threshold is not None:
        moog_df = moog_df[moog_df['ew'] <= upper_ew_threshold]  # Remove strong lines if upper_threshold is provided
    
    if ep_threshold is not None:
        moog_df = moog_df[moog_df['ep'] >= ep_threshold]  # Remove lines with certain excitation potential if ep_threshold is provided
    
    return moog_df


### Plots for moog output anaysis:

def linfit(x, y):
    """Linear fit that returns intercept, slope, slope error, and scatter of 'ab' data points w respect to linear fit."""
    n = len(x)
    dp = n * np.sum(x**2) - (np.sum(x)**2)
    a = (np.sum(x**2) * np.sum(y) - np.sum(x) * np.sum(x*y)) / dp
    b = (n * np.sum(x*y) - np.sum(x) * np.sum(y)) / dp
    residuals = y - a - b * x
    sigma = np.sqrt(np.sum(residuals**2) / (n - 2))
    err_a = np.sqrt((sigma**2 / dp) * np.sum(x**2))
    err_b = np.sqrt((sigma**2 / dp) * n)
    return a, b, err_b, sigma

def plot_with_linear_fit(ax, x, y, marker, color, label):
    ax.scatter(x, y, marker=marker, color=color, label=label, alpha=0.5)
    a, b, err_b, sigma = linfit(x, y)
    ax.plot(x, b*x + a, color=color)
    text_x = np.mean(x)
    text_y = np.max(y)
    va = 'top' if 0.1 < text_y < 0.9 else 'bottom'
    ax.text(text_x, text_y, f'Slope: {b:.2f} ± {err_b:.2f}, $\sigma$ = {sigma:.2f}', color=color, fontsize=10, verticalalignment=va, bbox=dict(facecolor='white', edgecolor=color, boxstyle='round,pad=0.5'))
    
### Save solution for the star

def write_solution_csv(star_id, data):
    filename = f"{star_id}_solution.csv"
    fieldnames = ['id', 'teff', 'logg', 'feh_model', 'vt', 'feh', 'err_feh', 'feh1', 'err_feh1', 'nfe1', 'feh2', 'err_feh2', 'nfe2', 'slope_ep', 'err_slope_ep', 'slope_rew', 'err_slope_rew', 'err_teff', 'err_logg', 'err_feh_', 'err_vt']
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            
### Get out what species are available in 'lines.csv' file

def get_available_species(star_id, lines_csv):
    elements = set() 

    with open(lines_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if float(row[star_id]) == -99.9:
                continue  # Ignore lines with star_id == -99.9
            
            species = float(row['species'])
            for element, code in sp_map.items():
                if species == code:
                    elements.add(element)
    
    elements_list = sorted(elements)
    return elements_list