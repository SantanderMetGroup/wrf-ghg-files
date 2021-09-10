WRF Greenhouse Gases (GHG) concentration files
==============================================

These are scripts to retrieve and create CMIP6 Shared Socioeconomic Pathways (SSP) GHG concentration
files for use in the Weather Research & Forecasting ([WRF](https://www2.mmm.ucar.edu/wrf/users)) modelling system.
New `CAMtr_volume_mixing_ratio.SSP*` files were generated following the SSPs used in CMIP6 scenarioMIP simulations. This
files allow for a consistent GHG concentration in the driving CMIP6 GCM fields and a nested WRF climate simulation.

[Input4MIPs](https://esgf-node.llnl.gov/projects/input4mips) provides forcing data sets for CMIP6 through the Earth System Grid Federation (ESGF). For GHG forcing, the data is also made available through a University of Melbourne server (https://greenhousegases.science.unimelb.edu.au), which provides access to easily parseable CSV files. We made use of **global average files** from this source, using versions v1.2.0 (historical) and v1.2.1 (scenario). Note that hemispheric and 30-degree-resolution files are also available.

This is a comparison (see [plot_CAMtr_files.py](./plot_CAMtr_files.py)) of the new SSP files created and the some of the existing concentration pathways (RCPs) files, as retrieved from WRF v4.2.2:
![SSP vs RCP concentrations](CAMtr_files.png)
