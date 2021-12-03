import io
import pandas as pd
from glob import glob


files = glob('*PREC.csv')
print (files)
birdseye_max = 0.0
with io.open('MaxHistoricRainflows.txt', 'w') as f:
    for file in files:
        try:
            df = pd.read_csv(file)
            max = df.HIGH_PREC.max()
            date = str(int(df[df['HIGH_PREC'] == max]['MO'])) + '/' + str(int(df[df['HIGH_PREC'] == max]['DY'])) + '/' + str(int(df[df['HIGH_PREC'] == max]['YR_PREC']))
            lat = file.split('PREC')[0].split('_')[0]
            lat = lat[:-2] + '.' + lat[-2:]
            lon = file.split('PREC')[0].split('_')[1]
            lon = lon[:-2] + '.' + lon[-2:]
            sitename = file.split('PREC')[0].split('_')[2]
            f.write(f'{sitename}: \n')
            f.write(f'\t Coordinates: {lat}, {lon}\n')
            f.write(f'\t Max 1 Day Precipitation: {max} in. on {date}\n')
            f.write(f'\t Max Potential 5 Day Prec: {max * 5} in.\n\n')
            if 'Birdseye' in file:
                birdseye_max = max
        except Exception as e:
            print(file, '\n', e)
    f.close()

close_max_date = {}
for file in files:
    df = pd.read_csv(file)
    sitename = file.split('PREC')[0].split('_')[2]
    sorted_df = df.sort_values('HIGH_PREC', ascending=True)
    for index, row in sorted_df.iterrows():
        if row['HIGH_PREC'] >= birdseye_max:
            close_max = row['HIGH_PREC']
            date = str(int(row['MO'])) + '/' + str(int(row['DY'])) + '/' + str(int(row['YR_PREC']))
            break
    close_max_date[f'{sitename}'] = {'date': date, 'Closest Max': close_max}

with io.open('MaxHistoricRainflows.txt', 'a+') as f:
    for key in close_max_date.keys():
        close_max = close_max_date[key]['Closest Max']
        date = close_max_date[key]['date']
        f.write(f'{key} Closest Daily Max to Birdseye: \n')
        f.write(f'\t{close_max} in. on {date}\n\n')
    f.close()
print(close_max_date)
