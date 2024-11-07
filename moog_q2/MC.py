from data_processing_utils import * 
import numpy as np
import q2 

def run_MC(star_id, initial_params, num_iterations, teff_err, logg_err, feh_err, vt_err):
    results = []
    start_time = time.time() 
    
    for _ in range(num_iterations):
        teff = np.random.normal(initial_params['teff'], teff_err) 
        logg = np.random.normal(initial_params['logg'], logg_err) 
        feh = np.random.normal(initial_params['feh'], feh_err) 
        vt = np.random.normal(initial_params['vt'], vt_err)   
        
        stars_data = [{'id': star_id, 'teff': teff, 'logg': logg, 'feh': feh, 'vt': vt}]
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
        
        results.append({'teff': teff, 'logg': logg, 'feh': feh, 'vt': vt,
                        'fe1_abundance': fe1_abundance, 'fe2_abundance': fe2_abundance})
    
    end_time = time.time() 
    elapsed_time = end_time - start_time
    print(f"Elapsed time for {num_iterations} iterations: {format_time(elapsed_time)}")
    
    return results