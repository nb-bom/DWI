"""Dry Windy Index functions"""

import xarray as xr
import pandas as pd
import numpy as np

#function to calculate dewpoint depression
#inputs: datasets of temperature and relative humidity
#outputs: a dataset of dewpoint depression
def calc_dpd(ds_temp, ds_rh):
    dpd = ds_temp - 243.5 * (np.log(ds_rh/100) + 17.67*ds_temp/(243.5 + ds_temp))/(17.67 - (np.log(ds_rh/100) + 17.67*ds_temp/(243.5 + ds_temp)))

    dpd.attrs = {
        'long_name': 'afternoon dewpoint depression computed from tasmax and hursmin',
        'standard_name': 'dpd',
        'units': 'degC',
        'program' : 'Australian Climate Service (ACS)',
        'summary' : f'Fire weather metric: dewpoint depression for Global Warming Level {chosen_gwl} C',
        'naming_authority' : "Bureau of Meteorology",
        'publisher_type' : "group",
        'publisher_type' : "group" ,
        'publisher_institution' : "Bureau of Meteorology",
        'publisher_name' : "Bureau of Meteorology",
        'publisher_url' : "http://www.bom.gov.au",
        'creator_type' : "institution" ,
        'creator_institution' : "Bureau of Meteorology" ,
        'contact' : "Naomi Benger (naomi.benger@bom.gov.au)" ,
        'institute_id' : "BOM" ,
        'institution' : "Bureau of Meteorology",
        'acknowledgement' : "Development of data supported with funding from the Australian Climate Service.",
    }
    ds_dpd = xr.Dataset({'dpd' : dpd})
    ds_rh.close()
    ds_temp.close()
    
    return ds_dpd

def calc_dwi(ds_temp, ds_rh, ds_wind_sp, A, B, C, D):
    dwi = (calc_dpd(ds_temp, ds_rh)['dpd'] + A)/B * (ds_wind_sp + C)/D

    dwi.attrs = {
    'long_name': 'afternoon dry-windy index computed from tasmax, hursmin, maximum wind speed, and the tuned constants',
    'standard_name': 'dwi',
    'units': 'km h-1',
    'program' : 'Australian Climate Service (ACS)',
    'summary' : f'Fire weather metric: Dry-windy index for Global Warming Level {chosen_gwl} C',
    'naming_authority' : "Bureau of Meteorology",
    'publisher_type' : "group",
    'publisher_type' : "group" ,
    'publisher_institution' : "Bureau of Meteorology",
    'publisher_name' : "Bureau of Meteorology",
    'publisher_url' : "http://www.bom.gov.au",
    'creator_type' : "institution" ,
    'creator_institution' : "Bureau of Meteorology" ,
    'contact' : "Naomi Benger (naomi.benger@bom.gov.au)" ,
    'institute_id' : "BOM" ,
    'institution' : "Bureau of Meteorology",
    'acknowledgement' : "Development of data supported with funding from the Australian Climate Service.",
    }
    ds_dwi = xr.Dataset({'dwi' : dwi})
    ds_rh.close()
    ds_temp.close()
    ds_wind_sp.close()
    return ds_dwi

#conversion factor to FFDI from Kevin
#Psudo FFDI: (50/3)*(DF/10) matching FFDI for a particular event provided by Musa, 30 Sept 2023
#also computed for mean T humidity for Melb airport for Feb for total obs history at that time
#this removes the wind speed bias - FFDI undersensitive to wind and over sensitive to temp, 
#they often compensate. But not great on cool windy days
def calc_p_ffdi(ds_dwi):
    p_ffdi = 50/3*ds_dwi

    p_ffdi.attrs = {
    'long_name': 'Psudo FFDI computed from tasmax, hursmin, maximum wind speed, and the tuned constants',
    'standard_name': 'p_ffdi',
    #'units': 'km h-1',
    'program' : 'Australian Climate Service (ACS)',
    'summary' : f'Fire weather metric: p_ffdi for Global Warming Level {chosen_gwl} C',
    'naming_authority' : "Bureau of Meteorology",
    'publisher_type' : "group",
    'publisher_type' : "group" ,
    'publisher_institution' : "Bureau of Meteorology",
    'publisher_name' : "Bureau of Meteorology",
    'publisher_url' : "http://www.bom.gov.au",
    'creator_type' : "institution" ,
    'creator_institution' : "Bureau of Meteorology" ,
    'contact' : "Naomi Benger (naomi.benger@bom.gov.au)" ,
    'institute_id' : "BOM" ,
    'institution' : "Bureau of Meteorology",
    'acknowledgement' : "Development of data supported with funding from the Australian Climate Service.",
    }
    ds_p_ffdi = xr.Dataset({'p_ffdi' : p_ffdi})
    ds_dwi.close()
    return ds_p_ffdi

#conversion factor to FFDI from Kevin
#Faux FFDI: (T + 12)(DF/10)/2 

def calc_faux_ffdi(ds_dwi, ds_temp):
    faux_ffdi = (ds_temp + 12)*ds_dwi/2

    faux_ffdi.attrs = {
    'long_name': 'Faux FFDI computed from tasmax, hursmin, maximum wind speed, and the tuned constants',
    'standard_name': 'faux_ffdi',
    #'units': 'km h-1',
    'program' : 'Australian Climate Service (ACS)',
    'summary' : f'Fire weather metric: faux_ffdi for Global Warming Level {chosen_gwl} C',
    'naming_authority' : "Bureau of Meteorology",
    'publisher_type' : "group",
    'publisher_type' : "group" ,
    'publisher_institution' : "Bureau of Meteorology",
    'publisher_name' : "Bureau of Meteorology",
    'publisher_url' : "http://www.bom.gov.au",
    'creator_type' : "institution" ,
    'creator_institution' : "Bureau of Meteorology" ,
    'contact' : "Naomi Benger (naomi.benger@bom.gov.au)" ,
    'institute_id' : "BOM" ,
    'institution' : "Bureau of Meteorology",
    'acknowledgement' : "Development of data supported with funding from the Australian Climate Service.",
    }
    ds_faux_ffdi = xr.Dataset({'faux_ffdi' : faux_ffdi})
    ds_temp.close()
    ds_dwi.close()
    return ds_faux_ffdi

if __name__ == "__main__":
    main()