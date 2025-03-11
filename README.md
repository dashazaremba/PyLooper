# PyLooper
<br/>
<a href="https://arxiv.org/abs/2503.05927">
    <img src="https://img.shields.io/badge/read-paper-blue"/></a>
    
The PY_LOOPER notebooks provide a semi-automatic routine for high-resolution spectral analysis using the equivalent width (EW) method. The process begins with measuring the metallicity ([Fe/H]) from iron lines, followed by the assessment and adjustment of spectral parameters ($T_{\text{eff}}, \log g, v_{\text{mic}}, [\text{M/H}]$) incorporating both LTE and NLTE analyses. The routine then proceeds to measure other spectral lines, applying all necessary corrections (NLTE, HFS) and propagating errors from metallicity and derived stellar parameters on the way. The final step includes plotting [X/Fe] vs. [Fe/H], comparing the derived abundances against those of MW halo stars to place the results in the broader context of the Milky Way.

### THE_LOOPER_Part1:
### (Iron lines and stellar parameters)
* Measures EWs for given FeI and FeII lines using a modified version of `pyEW` package originally developed by [Monika Adamow](https://github.com/madamow/pyEW).
* Generates plots displaying Gaussian, Multigaussian, and Voigt fits for individual lines.
* Measures iron abundances with MOOG using `q2` Python package [(Ramirez et al. 2014, A&A, 572, A48)](https://github.com/astroChasqui/q2/tree/master).
* Creates diagnostic plots A(Fe) vs $\chi$, A(Fe) vs log(EW/$\lambda$), and A(Fe) vs $\lambda$ for for assessing and adjusting stellar parameters.
* Calculates total uncertainties on iron abundances by propagating errors from stellar parameters.
* Applies NLTE corrections by quering Inspect and/or MPIA database(s) based on scripts developed by [Anya Dovgal](https://github.com/anyadovgal/NLTE-correction.git).
* Optimizes logg by testing ionization equilibrium between A(FeI)_NLTE and A(FeII).
* Runs MC simulation for Fe abundances within 1 sigma of stellar parameters.

### THE_LOOPER_Part2:
### (Other lines)
* Measures EWs for lines of other elements using `pyEW` package.
* Generates plots displaying Gaussian and optionally Multigaussian, and Voigt fits for individual lines.
* Measures elemental abundances with MOOG using `q2` Python package, using stellar parameters and metallicity derived in **Part 1**.
* Applies HFS corrections.
* Applies NLTE corrections.
* Propagates uncertainties from stellar parameters and metallicity. 
* Plots derived abundances [X/Fe] vs [Fe/H] compared to MW halo from SAGA database and Li et al. 2022 measurements.

## Installation
---------------
### Install `pyEW`
Navigate to the `pyEW_modified` directory:

```bash
cd PY_LOOPER/pyEW_modified
```
Install the package:
```
python setup.py install
```
 adding `--user` in the end installs the package locally for your user account (meaning it won’t require administrative (root) privileges).

### Install `q2`
The `q2` can only be installed via pip:

```bash
pip install q2
```
add PATH to your bashrc (.bash_profile for Mac OS) with `PY_LOOPER/moog_q2/q2/__init__.py`

```python
import q2
```

By importing `q2`, the latest version of <a href="http://www.as.utexas.edu/~chris/moog.html">MOOG</a> (2019) will begin to install. While importing for the first time, you need to declare the kind of machine you are using, i.g., 'rh64' for 64-bit linux (Linux Mint, Ubuntu, etc), 'rh' for 32-bit linux system and 'maclap' for Mac Os. Note that the `q2` package requires Python 3.7 or later. 

## Input files
---------------
To get started with `THE_LOOPER_Part1`, place the following two files in the `pyEW_modified/PYEW_INPUT` directory:
* A file containing the Fe lines to be measured (e.g., `Fe_linemake.linelist`)
* Your continuum normalized and RV corrected spectrum (e.g., `HD222925_normrv.xy`)

For `THE_LOOPER_Part2`, you will also need a linelist for other elements (e.g., `other_elems.linelist`)
