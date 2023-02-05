#%%
import pandas as pd
import matplotlib.pyplot as plt

data = {'timestamp': [pd.Timestamp('2022-01-01 00:00:00'),
                      pd.Timestamp('2022-01-01 01:00:00'),
                      pd.Timestamp('2022-01-01 02:00:00'),
                      pd.Timestamp('2022-01-01 03:00:00'),
                      pd.Timestamp('2022-01-01 04:00:00'),
                      pd.Timestamp('2022-01-01 05:00:00'),
                      pd.Timestamp('2022-01-01 06:00:00')],
        'value': [2, 4, 6, 2, 7, 8, 10]}

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
grouped = df.groupby('value').size().reset_index(name='count')

# Sort the groups by count
grouped.sort_values('count', ascending=False, inplace=True)

# Assign a color to each group based on the number of groups
colors = plt.get_cmap('tab10', grouped.shape[0])
grouped['color'] = [colors(i) for i in range(grouped.shape[0])]

# Create a color dictionary from the grouped data
color_dict = dict(zip(grouped['value'], grouped['color']))


#%%



import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns

def plot_timestamps(df, start=None, end=None):
    df = df.sort_values('timestamp')
    grouped = df.groupby('value')
    colors = sns.color_palette("husl", len(grouped))
    grouped_colors = {key: value for (key, value) in zip(grouped.groups.keys(), colors)}
    df['color'] = df['value'].apply(lambda x: grouped_colors[x])
    df['x'] = df['timestamp'].apply(lambda x: mdates.date2num(x))
    x = df['x'].to_list()
    y = [0 for i in range(len(x))]
    widths = [x[i + 1] - x[i] for i in range(len(x) - 1)] + [1]
    fig, ax = plt.subplots()
    start = mdates.date2num(start)
    end = mdates.date2num(end)
    for i, color in enumerate(df['color']):
        if x[i] >= start and x[i] <= end:
            if x[i]+widths[i] > end:
                width = end - x[i]
                ax.bar(x[i], 20, width=width, color=color, align='edge', edgecolor='black')
            else:
                ax.bar(x[i], 20, width=widths[i], color=color, align='edge', edgecolor='black')
        elif x[i]+widths[i] >= start and x[i]+widths[i] <= end:
            width = x[i]+widths[i] - start
            ax.bar(start, 20, width=width, color=color, align='edge', edgecolor='black')
        elif x[i] < start and x[i]+widths[i] > end:
            ax.bar(start, 20, width=end-start, color=color, align='edge', edgecolor='black', hatch='/')
    ax.xaxis_date()
    date_format = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(date_format)
    # Rotate the x-axis labels
    fig.autofmt_xdate()

    # Adjust the subplot params to avoid overlapping labels
    plt.tight_layout()

    plt.show()

data = {'timestamp': ['2021-01-01 10:00:00', '2021-01-01 11:00:00', '2021-01-01 12:00:00', '2021-01-01 13:00:00', '2021-01-01 14:00:00', '2021-01-01 15:00:00', '2021-01-01 19:00:00'],
        'value': [3, 4, 5, 7, 8, 6, 5]}
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
plot_timestamps(df, pd.to_datetime('2021-01-01 10:30:00'), pd.to_datetime('2021-01-01 15:30:00'))
# %%