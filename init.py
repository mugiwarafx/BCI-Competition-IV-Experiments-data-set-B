import mne

# Carregar les dades
file_path = 'BCICIV_2b_gdf/B0101T.gdf'
raw = mne.io.read_raw_gdf(file_path, preload=True)

# Informació bàsica sobre les dades
print(raw.info)

# Preprocessament: Filtratge
raw.filter(l_freq=1., h_freq=40.)

# Trobar els esdeveniments
events, _ = mne.events_from_annotations(raw)

# Crear epochs
epochs = mne.Epochs(raw, events, tmin=-1., tmax=4., preload=True, event_repeated='merge')

# Visualitzar algunes dades
epochs.plot()
