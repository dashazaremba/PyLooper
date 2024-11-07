import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import q2 
from NLTE import apply_nlte
from data_processing_utils import * 

def solve_for_logg(star_id, Teff, new_logg, feh, vt, lower_ew_threshold, upper_ew_threshold, ep_threshold, delavg_threshold, moog_dir, save_output):
    start_time = time.time()

    stars_data = [{'id': star_id, 'teff': Teff, 'logg': new_logg, 'feh': feh, 'vt': vt}]

    write_stars_csv(stars_data)

    data = q2.Data('stars.csv', 'lines.csv')
    star = q2.Star(star_id)
    star.get_data_from(data)
    star.get_model_atmosphere('marcs')

    md = q2.moog.Driver()
    md.create_file()
    q2.moog.create_model_in(star)
    q2.moog.create_lines_in(star)

    q2.moog.abfind(star, 26.0, 'fe1')
    q2.moog.abfind(star, 26.1, 'fe2')
    q2.specpars.iron_stats(star)
    fe1_abundance = star.iron_stats['afe1']
    fe2_abundance = star.iron_stats['afe2']
    
    moog_out_path = f'{moog_dir}/MOOG_OUTPUT_{star_id}_{Teff}_{new_logg}_{feh}_{vt}'
    os.makedirs(moog_out_path, exist_ok=True)

    id_feI = 26.0
    id_feII = 26.1

    combined_output_file = f'moog_out_fe.csv'

    with open(f'{moog_out_path}/{combined_output_file}', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        header_feI = ['id'] + list(star.fe1.keys())
        writer.writerow(header_feI)
        for i in range(len(star.fe1['ww'])):
            row = [id_feI] + [star.fe1[key][i] for key in star.fe1.keys()]
            writer.writerow(row)

        for i in range(len(star.fe2['ww'])):
            row = [id_feII] + [star.fe2[key][i] for key in star.fe2.keys()]
            writer.writerow(row)

    moog_df = pd.read_csv(f'{moog_out_path}/{combined_output_file}')

    filtered_moog_df = filter_moog_output(moog_df, lower_ew_threshold, upper_ew_threshold, ep_threshold)
    filtered_moog_df.to_csv(f'{moog_out_path}/moog_out_fe_filtered.csv', index=False)
    
    moog_out_file = f'{moog_out_path}/moog_out_fe_filtered.csv'
    output_file = f'{moog_out_path}/moog_out_fe_filtered.csv'

    filtered_moog_df = remove_outliers(delavg_threshold, moog_out_file, output_file)
    filtered_moog_df.to_csv(output_file, index=False) 
    
    filtered_moog_df = pd.read_csv(f'{moog_out_path}/moog_out_fe_filtered.csv', delim_whitespace=False, engine='python')

    star_info = [Teff, new_logg, feh, vt]
    mpia_results = apply_nlte(filtered_moog_df, database='mpia', star_info=star_info, model_atmos='marcs')

    df_delta = pd.DataFrame(mpia_results)
    df_delta.columns = ['elem', 'line', 'delta']

    df_delta['line'] = df_delta['line'].astype(moog_df['ww'].dtype)
    df_merged = pd.merge(filtered_moog_df, df_delta, left_on='ww', right_on='line', how='left')

    df_merged.drop(columns=['line', 'elem', 'difab'], inplace=True)

    df_merged.to_csv(f'{moog_out_path}/MOOG_OUT_Fe_NLTE_final.csv', index=False)

    df_merged['delta'] = df_merged['delta'].astype(float)
    df_merged['delta'].fillna(0.0, inplace=True)
    df_merged['delta'].replace(999.0, 0.0, inplace=True)

    df_feI = df_merged[df_merged['id'] == 26.01]
    df_feII = df_merged[df_merged['id'] == 26.02]

    fig, axes = plt.subplots(3, 1, figsize=(8, 12))

    for ax, x_data, y_data, x_label in zip(axes, [df_feI['ep'], df_feI['rew'], df_feI['ww']],
                                            [df_feI['ab'], df_feI['ab'], df_feI['ab']], ['ep', 'rew', 'ww']):
        plot_with_linear_fit(ax, x_data, y_data, marker='x', color='blue', label='FeI LTE')
        plot_with_linear_fit(ax, x_data, y_data + df_feI['delta'], marker='x', color='orange', label='FeI NLTE')
        ax.scatter(df_feII[x_label], df_feII['ab'], marker='o', color='blue', edgecolor='k', label='FeII LTE',
                   alpha=0.5)
        ax.scatter(df_feII[x_label], df_feII['ab'] + df_feII['delta'], marker='o', color='orange', edgecolor='k',
                   label='FeII NLTE', alpha=0.5)
        mean_feI = np.mean(df_feI['ab'] + df_feI['delta'])
        mean_feII = np.mean(df_feII['ab'] + df_feII['delta'])
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel('A(Fe)', fontsize=12)
        ax.legend(fontsize=10)

    axes[-1].axhline(mean_feI, linestyle='--', color='k', label='mean FeI NLTE')
    axes[-1].axhline(mean_feII, linestyle='--', color='grey', label='mean FeII NLTE')
    axes[-1].fill_between(x=[min(df_feI[x_label]), max(df_feI[x_label])], y1=mean_feI, y2=mean_feII,
                          color='lightcoral', alpha=0.3)
    axes[-1].legend(fontsize=10)

    fig.suptitle(f'{star_id} {Teff} {new_logg} {feh} {vt}', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'{moog_out_path}/combined_nlte_diagnostic_plots')
    plt.show()

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if not save_output:
        for filename in os.listdir(moog_out_path):
            file_path = os.path.join(moog_out_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
        os.rmdir(moog_out_path)

    print(f"mean A(FeI)_LTE: {np.mean(df_feI['ab']):.2f}")
    print(f"mean A(FeI)_NLTE: {np.mean(df_feI['ab'] + df_feI['delta']):.2f}")
    print(f"mean A(FeII)_LTE: {np.mean(df_feII['ab']):.2f}")
    print(f"mean A(FeII)_NLTE: {np.mean(df_feII['ab'] + df_feII['delta']):.2f}")
    print('--------------------------')
    print(f"Elapsed time for running this cell: {format_time(elapsed_time)}")
    
    delta_fe_nlte_new_logg = abs(np.mean(df_feI['ab'] + df_feI['delta']) - np.mean(df_feII['ab'] + df_feII['delta']))
    
    return delta_fe_nlte_new_logg

