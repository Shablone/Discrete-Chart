#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

def plot_timestamps(df, start=None, end=None):
    df = df.copy().sort_values('timestamp')
    grouped = df.groupby('value')

    colors = sns.color_palette("husl", len(grouped))
    grouped_colors = {key: value for (key, value) in zip(grouped.groups.keys(), colors)}
    df['color'] = df['value'].apply(lambda x: grouped_colors[x])

    
    df['xpos'] = df['timestamp'].apply(lambda x: mdates.date2num(x))
    xpos = df['xpos'].to_list()
    widths = [xpos[i + 1] - xpos[i] for i in range(len(xpos) - 1)] + [1]
    fig, ax = plt.subplots()

    if start is None: start = df.iloc[0].timestamp
    if end  is None: end = df.iloc[-1].timestamp
    start = mdates.date2num(start) 
    end = mdates.date2num(end)

    height = 10

    for i, color in enumerate(df['color']):
        if xpos[i] >= start and xpos[i] <= end:
            if xpos[i]+widths[i] > end:
                width = end - xpos[i]
                ax.bar(xpos[i], height, width=width, color=color, align='edge', edgecolor='black')
            else:
                ax.bar(xpos[i], height, width=widths[i], color=color, align='edge', edgecolor='black')
        elif xpos[i]+widths[i] >= start and xpos[i]+widths[i] <= end:
            width = xpos[i]+widths[i] - start
            ax.bar(start, height, width=width, color=color, align='edge', edgecolor='black')
        elif xpos[i] < start and xpos[i]+widths[i] > end:
            ax.bar(start, height, width=end-start, color=color, align='edge', edgecolor='black', hatch='/')
        else:
            continue

    ax.xaxis_date()
    date_format = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    plt.tight_layout()

    plt.show()

data = {'timestamp': ['2021-01-01 10:00:00', '2021-01-01 11:00:00', '2021-01-01 12:00:00', '2021-01-01 13:30:00', '2021-01-01 14:00:00', '2021-01-01 15:00:00', '2021-01-01 19:00:00'],
        'value': [3, 4, 3, 7, 8, 3, 5],
        'value2': [4, 4, 2, 4, 8, 5, 5]}
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
print(df)
plot_timestamps(df, pd.to_datetime('2021-01-01 10:30:00'), pd.to_datetime('2021-01-01 15:30:00'))
# %%