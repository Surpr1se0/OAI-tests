import re
import os
import pandas as pd

trace_file = os.path.join("traces", "replay_1.txt")

# Regular expressions
frame_slot_pattern = re.compile(r'frame (\d+), slot (\d+)', re.IGNORECASE)
timestamp_pattern = re.compile(r'^(\d{2}:\d{2}:\d{2}\.\d+):')
event_pattern = re.compile(r'(TX_FUNC|RX_FUNC|Calling scheduler|cannot schedule DCI0)', re.IGNORECASE)

# List to store events
events = []

with open(trace_file, 'r') as file:
    for line in file:
        # Capture timestamp
        ts_match = timestamp_pattern.search(line)
        if not ts_match:
            continue
        timestamp = ts_match.group(1)

        # Capture main event
        event_match = event_pattern.search(line)
        if event_match:
            event = event_match.group(1)
        else:
            event = None

        # Store event
        events.append({
            'timestamp': timestamp,
            'event': event,
            'line': line.strip()
        })

# Converte to dataframe
df = pd.DataFrame(events)

# convert timestamps to microseconds
df['timestamp_us'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S.%f')
df['delta_us'] = df['timestamp_us'].diff().dt.total_seconds() * 1e6

# Filter important events
df_filtered = df.dropna(subset=['event'])

# Store as CSV
df_filtered.to_csv(os.path.join("traces", "parsed_tracer_events.csv") , index=False)
