import numpy as np
import pandas as pd
import re
import mechanicalsoup
from urllib.request import urlopen


##### INSPECT

app_url = 'http://www.inspect-stars.com/cp/application.py/'
elem_list = ['Li', 'O', 'Na', 'Mg', 'Ti', 'Fe', 'Sr']

def check_near(line, lines_dict):
    # TOLERANCE, change if you wish.
    dw = 0.03
    
    keys = lines_dict.keys()
    values = list(lines_dict.values())
    
    if line in keys:
        return lines_dict[line]
    else:
        float_keys = [float(i) for i in keys]
        delta_float_keys = np.abs(np.array(float_keys) - float(line))
        min_ind = delta_float_keys.argmin()
        
        if delta_float_keys[min_ind] <= dw:
            return values[min_ind]
        else:
            return None
        
        
# Helper function to check that input parameters are within bounds
def find_bounds_html(html, elem, n):
    pattern = 'class=""></td><td>.*?</td></tr>'

    lst = []
    
    for m in re.finditer(pattern, html):
        trunc = html[m.start():m.end()]
        trunc = trunc.strip('class=""></td></tr>[]').split(',')
        i = [float(j) for j in trunc]
        lst.append(i)
        
    return(lst)


def inspect_cor(elem, e, t, g, f, v, line, EW = False):
    """
    DESCRIPTION -------------------------------------------------------------
        Given input parameters, return the NLTE correction performed by INSPECT.
    
    PARAMETERS --------------------------------------------------------------
        elem (str) - a chemical element that is in the format of the contents of
            elem_list, defined in the second code-block.
        e (float) - if EW == True: the equivalent width of element at line
                    if EW == False: the abundance of element at line
        t (float) - the effective temperature of your star
        g (float) - the surface gravity of your star
        f (float) - the metallicity [Fe/H] of your star
        v (float) - the micro-turbulent velocity of your star
        line (float) - the line at which you want the NLTE correction to be performed
        
    RETURNS ----------------------------------------------------------------
        list(float) - the returned NLTE correction at element X in the format:
            [elem,
            line,
            EW (mA), 
            A(X) LTE, 
            A(X) NLTE, 
            Delta, 
            [X/Fe] NLTE] (Unless X == Fe, then it's [Fe/H])
            
            If the correction is not able to be performed, each value is replaced
            with '999'
    """
    # If the calculation can not be performed for any reason, this will be
    #  returned
    issue_response = [elem, line, 999, 999, 999, 999, 999]
    issue_txt = ':' + str(elem) + ' @ ' + str(line) + ' '
    
    input_nums = [e, t, g, f, v]
    input_names = ['Abundance A(X)', 'Temp', 'Log(g)', 'Metallicity', 'Microturbulence']
    if EW == True:
        input_names[0] = 'EW'
    
    # Checking if the inputted element is able to be processed
    if elem in elem_list:
        elem_url = app_url + 'nonlte_from_lte?element_name=' + elem
        if EW == True:
            elem_url = app_url + 'A_from_e?element_name=' + elem
    else:
        print('Sorry, element not in element list' + issue_txt)
        return issue_response
    
    # Because Ti & Fe don't take the metallicity input, this is necessary
    n = 5
    if elem in ['Ti', 'Fe']:
        input_nums.pop(3)
        input_names.pop(3)
        n = 4
    
    # Creating a list with all of the wavelengths available for this element
    lines_dict = {}
    
    html = urlopen(elem_url).read().decode("utf-8")
    pattern = "<option.*?>.*?</option.*?>"
    for match in re.finditer(pattern, html):
        trunc = html[match.start():match.end()]
        trunc = trunc.strip('<option value"></=').replace('"', '').split(">")
        if len(trunc) > 1:
            lines_dict[trunc[1]] = int(trunc[0])
    
    # Checking all of the bounds for the input-able parameters
    bounds = find_bounds_html(html, elem, n)
    for ind, input_num in enumerate(input_nums):
        bound = bounds[ind]
        if not (input_num >= bound[0]) & (input_num <= bound[1]):
            print('Sorry, cannot perform calculation' + issue_txt)
            print(input_names[ind], 'must be within', bound)
            return issue_response
    
    line_index = check_near(line, lines_dict)
    if line_index == None:
        print('Sorry, input wavelength not in list' + issue_txt)
        return issue_response

    # Actually submitting the inputs to the NLTE correction
    # Note, for Ti & Fe adding the metallicity doesn't affect the product, so no
    #  need to actually go and remove it from the submission
    
    url_extension = '&A_lte={}&t={}&g={}&f={}&x={}&wi={}'.format(e, t, g, f, v, line_index)
    if EW == True:
        url_extension = '&e={}&t={}&g={}&f={}&x={}&wi={}'.format(e, t, g, f, v, line_index)
    
    submit_url = elem_url + url_extension
    
    submit_html = urlopen(submit_url).read().decode("utf-8")
    
    if 'Calculation failed' in submit_html:
        print('No data for this equivalent width' + issue_txt)
        return issue_response
    
    results = submit_html.split('pre')[1].split('\n')[3].split('\t')
    
    # For results that can't be computed, replace nan w/ 999 just for easier handling
    #  and turn all strings into floats at the same time
    for count, i in enumerate(results):
        if i == 'nan':
            results[count] = 999
        else: 
            results[count] = eval(i)

    results.insert(0, elem)
    results.insert(1, line)
    
    return results

##### MPIA

#           ['O', 'Mg', 'Si', 'CaI', 'CaII', 'TiI', 'TiII', 'Cr', 'Mn', 'FeI', 'FeII', 'Co']
elem_list = [8.01, 12.01, 14.01, 20.01, 20.02, 22.01, 22.02, 24.01, 25.01, 26.01, 26.02, 27.01]

def mpia_cor(elem, lines, t, g, feh, vt, model_atmos='mafags-os'):
    """
    DESCRIPTION --------------------------------------------------------
        Given input parameters, return the NLTE correction performed by MPIA
        
    PARAMETERS ---------------------------------------------------------
        elem (float) - a chemical element in the form of the contents of elem_list,
            defined in the previous code-block
        lines (list(float)) - a list of the lines at which you want the NLTE correction
            to be performed for this element
        t (float) - the effective temperature of your star
        g (float) - the surface gravity of your star
        feh (float) - the metallicity [Fe/H] of your star
        vt (float) - the micro-turbulent velocity of your star
        model_atmos (string) - atmosphere model choice {options: mafags-os, marcs, rsg}
            check mpia website for details on the stellar parameter range for each
            grid
        
    RETURNS -------------------------------------------------------------
        np.array() - a 2D numpy array with 3 elements per row, such that each row
            has the element id, line at which the correction was performed, and
            the resulting correction delta
            [elem, line, delta]
            
            If the correction was not able to be performed, delta is replaced with the
            value '999'
    """
    # If the element isn't in the element list, return 999 for delta
    if elem not in elem_list:
        print('Element not available: ' + str(elem))
        delta = np.full(len(lines), 999.0)
        return np.transpose(np.array([np.full(len(lines), elem), lines, delta]))

    # If the element is either O, Mn, or Co, the NLTE correction must be done at
    #  a separate webpage
    if elem in [8.01, 25.01, 27.01]:
        weblink = 'https://nlte.mpia.de/gui-siuAC_secEnew.php'
        if model_atmos != 'mafags-os':
            print(f'{model_atmos} is not available for {elem}, using mafags-os instead')
        model_atmos = 'mafags-os'
    else:
        weblink = "https://nlte.mpia.de/gui-siuAC_secE.php"
    
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(weblink)
    
    form = browser.select_form()
    
    if model_atmos == 'marcs':
        for name, param, upper_lim, lower_lim in zip(['Teff', 'Logg', '[Fe/H]'],
                                                     [t, g, feh], 
                                                     [7750, 3.5, 1.0], 
                                                     [2500, -0.5, -5.0]):
            if (param < lower_lim) or (param > upper_lim):
                print(f'{name} = {param} is not within the {model_atmos} grid [{lower_lim}, {upper_lim}]')
                print(f'Using mafags-os atmosphere grid instead')
                model_atmos = 'mafags-os'
                break
    elif model_atmos == 'rsg-marcs':
        for name, param, upper_lim, lower_lim in zip(['Teff', 'Logg', '[Fe/H]'],
                                                     [t, g, feh], 
                                                     [4400, 1.0, 1.0], 
                                                     [3400, -0.99, -1.5]):
            if (param < lower_lim) or (param > upper_lim):
                print(f'{name} = {param} is not within the {model_atmos} grid [{lower_lim}, {upper_lim}]')
                print(f'Using mafags-os atmosphere grid instead')
                model_atmos = 'mafags-os'
                break
                
    if model_atmos == 'marcs' and elem in [20.01, 20.02]:
        print("marcs is not available for Ca, using mafags-os instead")
       #use_mafags = input("Would you like to use MAFAGS instead? (yes/no): ").strip().lower()
        model_atmos = 'mafags-os'


                
    form["model"] = model_atmos
    
    param_txt = "{} {} {} {} {}".format('my_star', t, g, feh, vt)
    form.set_textarea({"user_input":param_txt})
    
    line_txt = ""
    
    for line in lines:
        append = "{} {}\n".format(line, elem)
        line_txt += append
        
    form.set_textarea({"lines_input":line_txt})
        
    browser.submit_selected()
        
    result_txt = browser.page.get_text().split('lines(A)')[-1].split('Download')[0].split('my_star')
    
    lines = result_txt[0].split()
    delta = result_txt[1].split()
        
    for i, d in enumerate(delta):
        if float(d) == 30.0:
            delta[i] = 999.0
            print('Line not in linelist (or too weak) at: ' + str(elem) + ' ' + str(lines[i]))
        elif float(d) == 20.0:
            delta[i] = 999.0
            print('NLTE not converged at: ' + str(elem) + ' ' + str(lines[i]))
        elif float(d) == 10.0:
            delta[i] = 999.0
            print('Error in lineformation' + str(elem) + ' ' + str(lines[i]))
    # This is a fail-safe, feel free to comment out the below condition if you do not want it
        elif float(d) == 0.0:
            delta[i] = 999.0
            print('No NLTE departures for this line' + str(elem) + ' ' + str(lines[i]))


    return np.transpose(np.array([np.full(len(lines), elem), lines, delta]))



def apply_nlte(moog_df, database, star_info, model_atmos='marcs', EW=False):
    if database == 'inspect':
        elem_dict = {26: 'Fe', 3: 'Li', 8: 'O', 11: 'Na', 12: 'Mg', 22: 'Ti', 38: 'Sr'}
        
        # Check if 'ab_hfscor' column exists in moog_df
        if 'ab_hfscor' in moog_df.columns:
            # Create a copy of moog_df with relevant columns
            df = moog_df[['id', 'ab', 'ab_hfscor', 'ww']].copy()
            df.columns = ['elem', 'A(X)', 'hfs', 'line']
            
            # Round 'elem' column and replace with element names using elem_dict
            df['elem'] = df['elem'].round().replace(elem_dict)
            
            # Apply condition to use 'ab_hfscor' where available
            df['A(X)'] = df.apply(lambda row: row['ab_hfscor'] if not pd.isna(row['ab_hfscor']) else row['ab'], axis=1)
            
            return df
        else:
            # 'ab_hfscor' column does not exist, proceed with standard 'ab' column
            df = moog_df[['id', 'ab', 'ww']].copy()
            df.columns = ['elem', 'A(X)', 'line']
            df['elem'] = df['elem'].round().replace(elem_dict)
            
            return df

        data = []
        for i, row in df.iterrows():
            if EW == True:
                params_i = inspect_cor(row['elem'], row['EW'], *star_info, row['line'], EW = True)
                data.append(params_i)
                
            else:
                params_i = inspect_cor(row['elem'], row['A(X)'], *star_info, row['line'])
                data.append(params_i)

        #results = pd.DataFrame(data, columns=['Elem', 'Line', 'EW [mA]', 'A(Elem) LTE', 'A(Elem) NLTE', 'Delta:[Elem/Fe]'])
        results = pd.DataFrame(data)
        #results['Elem'] = 'X' if elem != 'Fe' else 'H'
        return results
    
    elif database == 'mpia':
        elem_dict = {26.0: 26.01, 26.1: 26.02, 8.0: 8.01, 12.0: 12.01, 14.0: 14.01, 20.0: 20.01, 20.1: 20.02, 22.0: 22.01, 22.1: 22.02, 24.0: 24.01, 25.0: 25.01,  27.0: 27.01}  
        
        moog_df['id'] = moog_df['id'].replace(elem_dict)
        moog_df = moog_df.sort_values('id')
        grouped = moog_df.groupby('id')
        results = []

        for elem, group in grouped:
            linelist = group['ww'].to_numpy()
            results.append(mpia_cor(elem, linelist, *star_info, model_atmos=model_atmos))

        results = pd.DataFrame(np.concatenate(results))
        results.columns = ['elem', 'line', 'nlte_delta']
        
        return results

    else:
        raise ValueError("Invalid database. Please choose either 'inspect' or 'mpia'.")


