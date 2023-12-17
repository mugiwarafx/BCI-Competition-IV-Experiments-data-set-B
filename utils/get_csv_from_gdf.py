import mne
import pandas as pd

file_path = 'BCICIV_2b_gdf/B0101T.gdf'
raw = mne.io.read_raw_gdf(file_path, preload=True)

data = raw.get_data()
df = pd.DataFrame(data.transpose(), columns=raw.ch_names)

df['time'] = raw.times
df.set_index('time', inplace=True)

annotations = raw.annotations
annotations_df = pd.DataFrame({
    'onset': annotations.onset,
    'duration': annotations.duration,
    'description': annotations.description
})

unique_events = annotations_df['description'].unique()
print("Esdeveniments únics:", unique_events)

"""
Event type Description
276 0x0114 Idling EEG (eyes open)
277 0x0115 Idling EEG (eyes closed)
768 0x0300 Start of a trial
769 0x0301 Cue onset left (class 1)
770 0x0302 Cue onset right (class 2)
781 0x030D BCI feedback (continuous)
783 0x030F Cue unknown
1023 0x03FF Rejected trial
1077 0x0435 Horizontal eye movement
1078 0x0436 Vertical eye movement
1079 0x0437 Eye rotation
1081 0x0439 Eye blinks
32766 0x7FFE Start of a new run
"""

df['event'] = 'None'
for _, row in annotations_df.iterrows():
    start_sample = int(row['onset'] * raw.info['sfreq'])
    end_sample = start_sample + int(row['duration'] * raw.info['sfreq'])
    df.iloc[start_sample:end_sample, df.columns.get_loc('event')] = row['description']

event_counts = df['event'].value_counts()
print("Recompte de mostres per esdeveniment:", event_counts)

df.to_csv('eeg_data_with_events.csv')
