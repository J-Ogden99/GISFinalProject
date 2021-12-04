import io
import os
import pandas as pd
from glob import glob

def extract_maxes_to_txt(
        search_path: str,
        primary_site_name: str,
        output_txt_path: str,
        prec_val_col: str,
        month_col: str,
        day_col: str,
        year_col: str):
    files = glob(os.path.join(search_path,'*PREC.csv'))

    """
    Args:
        search_path: path to directory to search for .csv files
            -must be formatted as following: 'lat_lon_sitenamePREC.csv'
            -latitude and longitude in path name must be to two decimal places
            
        primary_site_name: the primary site in your area of study. The text file
            will contain the closest maxes to the primary site max for each
            surrounding site
        
        output_txt_path: path for your desired output. Must end with .txt suffix
        
        prec_val_col: column name of the precipitation values in the .csvs. Must be
            consistent
    """

    search_max = 0.0
    with io.open(output_txt_path, 'w') as f:
        for file in files:
            try:
                df = pd.read_csv(file)
                file = os.path.split(file)[-1]
                max = df[prec_val_col].max()
                date = str(int(df[df[prec_val_col] == max][month_col])) + '/' + str(int(df[df[prec_val_col] == max][day_col])) + '/' + str(int(df[df[prec_val_col] == max][year_col]))
                lat = file.split('PREC')[0].split('_')[0]
                lat = lat[:-2] + '.' + lat[-2:]
                lon = file.split('PREC')[0].split('_')[1]
                lon = lon[:-2] + '.' + lon[-2:]
                sitename = file.split('PREC')[0].split('_')[2]
                f.write(f'{sitename}: \n')
                f.write(f'\t Coordinates: {lat}, {lon}\n')
                f.write(f'\t Max 1 Day Precipitation: {max} in. on {date}\n')
                f.write(f'\t Max Potential 5 Day Prec: {max * 5} in.\n\n')
                if primary_site_name in file:
                    search_max = max
            except Exception as e:
                print(file, '\n', e)
        f.close()

    close_max_date = {}
    for file in files:
        df = pd.read_csv(file)
        sitename = file.split('PREC')[0].split('_')[2]
        sorted_df = df.sort_values(prec_val_col, ascending=True)
        for index, row in sorted_df.iterrows():
            if row[prec_val_col] >= search_max:
                close_max = row[prec_val_col]
                date = str(int(row[month_col])) + '/' + str(int(row[day_col])) + '/' + str(int(row[year_col]))
                break
        close_max_date[f'{sitename}'] = {'date': date, 'Closest Max': close_max}

    with io.open(output_txt_path, 'a+') as f:
        for key in close_max_date.keys():
            close_max = close_max_date[key]['Closest Max']
            date = close_max_date[key]['date']
            f.write(f'{key} Closest Daily Max to {primary_site_name}: \n')
            f.write(f'\t{close_max} in. on {date}\n\n')
        f.close()



search_path = r'C:\Users\polar\PycharmProjects\GISFinalProject'
primary_site_name = 'Birdseye'
output_txt_path = 'MaxHistoricRainflows.txt'
prec_val_col = 'HIGH_PREC'
month_col = 'MO'
day_col = 'DY'
year_col = 'YR_PREC'

extract_maxes_to_txt(search_path, primary_site_name, output_txt_path, prec_val_col, month_col, day_col, year_col)
print(year_col)