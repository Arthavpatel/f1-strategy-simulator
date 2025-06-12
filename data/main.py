import fastf1 as f1
import os
import pprint 
import pandas as pd

cache = '/Users/arthavpatel/Desktop/VERSTAPPEN_THIRD_PIT_STOP/f1_cache'
os.makedirs(cache, exist_ok=True)
f1.Cache.enable_cache(cache)

# ------------------------------------------ Loading sessions -----------------------------------
grandprix_name = 'Spanish Grand Prix'
grandprix_year = 2025
session_name = ['FP1' , 'FP2', 'FP3', 'Q']
laps_data = {}
for session_np in session_name:
    try:
        session = f1.get_session(grandprix_year, grandprix_name, session_np)
        session.load()
        laps_data[session_np] = session.laps
    except Exception as e:
        print(f"{session_np} failed to load: {e}")


# ------------------------------------------ Team names -----------------------------------
driver_team_map =  {
    'NOR': 'McLaren', 'PIA': 'McLaren',
    'LEC': 'Ferrari', 'HAM': 'Ferrari',
    'RUS': 'Mercedes', 'ANT': 'Mercedes',
    'VER': 'Red Bull Racing', 'TSU': 'Red Bull Racing',
    'ALB': 'Williams', 'SAI': 'Williams',
    'LAW': 'Racing Bulls', 'HAJ': 'Racing Bulls',
    'OCO': 'Haas', 'BEA': 'Haas',
    'HUL': 'Kick Sauber', 'BOR': 'Kick Sauber',
    'ALO': 'Aston Martin', 'STR': 'Aston Martin',
    'GAS': 'Alpine', 'COL': 'Alpine'
}
FP1_laps = laps_data.get('FP1')
if FP1_laps is None:
    print("❌ FP1 data unavailable")

FP1_features_laps = []
for index, lap in FP1_laps.iterlaps():
    driver = lap['Driver']
    team = driver_team_map.get(driver, 'Unknown')
    
    FP1_features_laps.append({
        'Driver': driver,
        'Team': team,
        'LapNumber': lap['LapNumber'],
        'StintNumber': lap['Stint'],
        'Compound': lap['Compound'],
        'LapTime': lap['LapTime'],
        'LapTimeSeconds': lap['LapTime'].total_seconds() if pd.notnull(lap['LapTime']) else None,
        'TrackStatus': lap['TrackStatus'],
        'IsAccurate': lap['IsAccurate'],
        'PitInLap': lap.get('PitInLap', None),
        'Sector1Time': lap['Sector1Time'],
        'Sector2Time': lap['Sector2Time'],
        'Sector3Time': lap['Sector3Time']
    })
df_fp1 = pd.DataFrame(FP1_features_laps)
df_fp1.to_csv('FP1_data.csv', index=False)
