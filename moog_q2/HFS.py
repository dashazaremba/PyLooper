from data_processing_utils import sp_map
import csv
import pandas as pd
import numpy as np


def find_hfs_corrections(hfs_file_path, lines_csv_path, tolerance=0.03):
    hfs_corrections = []  
    
    # Load wavelengths from lines.csv into a set for efficient lookup
    wavelengths_set = set()
    with open(lines_csv_path, 'r') as lines_file:
        next(lines_file) 
        for line in lines_file:
            parts = line.strip().split(',')
            wavelength = float(parts[0])
            wavelengths_set.add(wavelength)
    
    # Iterate over lines in the HFS file
    with open(hfs_file_path, 'r') as hfs_file:
        next(hfs_file) 
        for line in hfs_file:
            if line.strip().startswith('-'):
                continue  # Skip lines starting with '-'
            parts = line.strip().split()
            if len(parts) < 2:
                continue 
            wavelength = float(parts[0])
            species = float("{:.1f}".format(float(parts[1])))
            for target_wavelength in wavelengths_set:
                if abs(wavelength - target_wavelength) <= tolerance:
                    hfs_corrections.append({'wavelength': target_wavelength, 'species': species})
                    element = [key for key, value in sp_map.items() if value == species]
                    if element:
                        element = element[0]
                    else:
                        element = "Unknown"
                    print(f"HFS corrections needed for {target_wavelength} (Species: {species} ({element}))")
                    break 
    
    if not hfs_corrections:
        print("No HFS corrections found.")
    
    return hfs_corrections

def apply_hfs_corrections(hfs_file_path, lines_csv_path, hfs_corrections, tolerance=0.03):
    # Create a temporary file to store the modified lines.csv content
    temp_csv_path = "temp_lines.csv"

    hfs_lines = set()
    with open(temp_csv_path, 'w', newline='') as temp_csv, open(lines_csv_path, 'r') as lines_csv:
        reader = csv.reader(lines_csv)
        writer = csv.writer(temp_csv)
        
        for row in reader:
            if reader.line_num == 1:
                writer.writerow(row) 
                continue
            
            wavelength = float(row[0])
            species = float(row[1])
            
            # Check if the current line needs HFS corrections and if it's not already modified
            if (wavelength, species) not in hfs_lines:
                for correction in hfs_corrections:
                    if abs(correction['wavelength'] - wavelength) <= tolerance and correction['species'] == species:
                        writer.writerow(row)
                        
                        # Look for corresponding HFS lines in the hfs_file_path
                        with open(hfs_file_path, 'r') as hfs_file:
                            for hfs_line in hfs_file:
                                if hfs_line.startswith('-'):
                                    parts = hfs_line.strip().split()
                                    hfs_wavelength = float(parts[0]) 
                                    hfs_species = float("{:.1f}".format(float(parts[1])))
                                    hfs_ep = float(parts[2])
                                    hfs_gf = float(parts[3])
                                    if abs(abs(hfs_wavelength) - wavelength) <= tolerance and hfs_species == species:
                                        writer.writerow([hfs_wavelength, hfs_species, hfs_ep, hfs_gf, 0])
                                        hfs_lines.add((hfs_wavelength, hfs_species))
                        break  # Break after applying corrections to avoid duplicate entries
                else:
                    # If no corrections applied, write the original row
                    writer.writerow(row)
            else:
                # If the line is already modified, skip it
                continue
                
    ## Replace the original lines.csv with the modified content
    import shutil
    shutil.move(temp_csv_path, lines_csv_path)
    #return hfs_lines