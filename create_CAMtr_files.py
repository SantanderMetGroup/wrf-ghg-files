# create_CAMtr_files.py
#
# Copyright (C) 2021 Santander Meteorology Group (http://meteo.unican.es)
#
# This work is licensed under a Creative Commons Attribution 4.0 International
# License (CC BY 4.0 - http://creativecommons.org/licenses/by/4.0)
#
# Author: Jesus Fernandez
# Date: 2021-08-22
# Description:
#   Retrieve CMIP6 GHG concentration pathways from
#   https://greenhousegases.science.unimelb.edu.au and format them to be used
#   by WRF (using the -DCLWRFGHG macro at compile time).

import numpy as np
import pandas as pd

version = dict(hist = '1.2.0', scen = '1.2.1')
period = dict(hist = '0000-2014', scen = '2015-2500')
column = 'data_mean_global'
dirbase = 'https://greenhousegases.science.unimelb.edu.au/data'
dirname = dict(
  hist = f'historical/CMIP6GHGConcentrationHistorical_{version["hist"].replace(".","_")}',
  scen = f'future/CMIP6GHGConcentrationProjections_{version["scen"].replace(".","_")}'
)
varname = dict(
  CO2 = 'mole-fraction-of-carbon-dioxide-in-air',
  N2O = 'mole-fraction-of-nitrous-oxide-in-air',
  CH4 = 'mole-fraction-of-methane-in-air',
  CFC11 = 'mole-fraction-of-cfc11-in-air',
  CFC12 = 'mole-fraction-of-cfc12-in-air',
)
sspname = dict(
  SSP119 = 'ScenarioMIP_UoM-IMAGE-ssp119',
  SSP126 = 'ScenarioMIP_UoM-IMAGE-ssp126',
  SSP245 = 'ScenarioMIP_UoM-MESSAGE-GLOBIOM-ssp245',
  SSP370 = 'ScenarioMIP_UoM-AIM-ssp370',
  SSP585 = 'ScenarioMIP_UoM-REMIND-MAGPIE-ssp585',
)

def get_column(url, col):
  return(pd.read_csv(url).set_index('year')[col])

for ssp in sspname:
  print(ssp)
  sspdf = pd.DataFrame()
  for var in varname:
    print(var)
    data = []
    for chunk in ('hist', 'scen'):
      expname = sspname[ssp] if chunk=='scen' else 'CMIP_UoM-CMIP'
      url = f'{dirbase}/{dirname[chunk]}/{varname[var]}_input4MIPs_GHGConcentrations_{expname}-{version[chunk].replace(".","-")}_gr1-GMNHSH_{period[chunk]}.csv'
      # print(url)
      data.append(get_column(url, column))
    sspdf[var] = pd.concat(data)
  # Write to file
  ofile = open(f'CAMtr_volume_mixing_ratio.{ssp}', 'w')
  ofile.write(f'''## year[1] | co2 (ppmv) [2] | n2o (ppbv)[3] | ch4 (ppbv)[4] | cfc11 (ppbv)[5] | cfc12 (pppbv)[6] 
## Non values are given by  -9999.999 values {ssp}
''')
  fmt = '%.0f %8.3f %10.3f %10.3f %10.3f %10.3f'
  np.savetxt(ofile, sspdf[1765:2500].reset_index().values, fmt)
  ofile.close()
