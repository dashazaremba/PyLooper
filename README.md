## PyLooper

The PY_LOOPER notebooks 

## THE_LOOPER_Part1:
### (Iron lines and stellar parameters)
* Measures EWs for given FeI and FeII lines using pyEW package (v.1.0.0.) developed by Monika Adamow (https://github.com/madamow/pyEW) .
* Generates plots displaying Gaussian, Multigaussian, and Voigt fits for individual lines.
* Measures iron abundances with MOOG using q2 Python package [(Ramirez et al. 2014, A&A, 572, A48)](https://github.com/astroChasqui/q2/tree/master)
* Creates diagnostic plots A(Fe) vs $\chi$, A(Fe) vs log(EW/$\lambda$), and A(Fe) vs $\lambda$ for stellar parameters checking/adjustement
* 
* Applies NLTE corrections by quering Inspect and/or MPIA database(s) based on scripts developed by Anya Dovgal (https://github.com/anyadovgal/NLTE-correction.git)
* Provides test for optimizing logg value based on ionization equilibrium between A(FeI)_NLTE and A(FeII)
* Runs MC simulation for Fe abundances within 1 sigma of stellar parameters

## THE_LOOPER_Part2:
### (Other lines and corrections)
* Measures EWs for lines of other elements using pyEW package.
* Generates plots displaying Gaussian and optionally Multigaussian, and Voigt fits for individual lines.
* Measures elemental abundances with MOOG using q2 Python package, using stellar parameters and iron abundances derived in Part I.
* Applies HFS corrections
* Applies NLTE corrections
* Propagates uncertainties from stellar parameters and metallicity 
* Plots derived abundances [X/Fe] vs [Fe/H] compared to MW halo
