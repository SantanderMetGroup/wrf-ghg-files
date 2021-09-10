# plot_CAMtr_files.py
#
# Copyright (C) 2021 Santander Meteorology Group (http://meteo.unican.es)
#
# This work is licensed under a Creative Commons Attribution 4.0 International
# License (CC BY 4.0 - http://creativecommons.org/licenses/by/4.0)
#
# Author: Jesus Fernandez
# Date: 2021-08-24
# Description:
#   Plot GHG concentration pathways formatted as WRF CAMtr vmr files
#
import glob
import matplotlib.pyplot as plt
import pandas as pd
import re

def read_CAMtr(fname):
  return(pd.read_fwf(
    fname,
    comment = '#', header = None,
    names = ['year'] + variables,
    widths = [4,9,11,11,11,11]
  ).set_index('year'))

def get_tag(fname):
  return(re.sub(r'.*CAMtr_volume_mixing_ratio\.', '', fname))

variables = ['CO2', 'N2O', 'CH4', 'CFC11', 'CFC12']

camtr_files = sorted(glob.glob('CAMtr_volume_mixing_ratio.*'))
camtr_files.append('https://raw.githubusercontent.com/wrf-model/WRF/v4.2.2/run/CAMtr_volume_mixing_ratio.RCP4.5')
camtr_files.append('https://raw.githubusercontent.com/wrf-model/WRF/v4.2.2/run/CAMtr_volume_mixing_ratio.RCP8.5')

tags = [get_tag(x) for x in camtr_files]

fulltable = pd.concat(
  [read_CAMtr(x) for x in camtr_files],
  axis = 1, join = 'outer',
  keys = tags
)

fig, axs = plt.subplots(2, 3, sharex='all')
plt.rc('legend',fontsize='small')
for ivar,var in enumerate(variables):
  ax = axs.flatten()[ivar]
  fulltable.iloc[:, fulltable.columns.get_level_values(1) == var].loc[1950:2100].plot(ax=ax, style = ['-' if x.startswith('SSP') else '--' for x in tags])
  ax.axvline(x=2014.5, color='grey', ls=':')
fig.tight_layout()
plt.show()

