#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
def plot_timestamps(df, start=None, end=None):
    df = df.copy().sort_values('timestamp')
    cols = [col for col in df.columns if col not in ['timestamp', 'color']]
    fig, axs = plt.subplots(len(cols), 1, sharex=True)

    if start is None: start = df.iloc[0].timestamp
    if end  is None: end = df.iloc[-1].timestamp
    start = mdates.date2num(start) 
    end = mdates.date2num(end)
    
    for index_col, col in enumerate(cols):
        grouped = df.groupby(col)
        colors = sns.color_palette("husl", len(grouped))
        grouped_colors = {key: value for (key, value) in zip(grouped.groups.keys(), colors)}
        df['color'] = df[col].apply(lambda x: grouped_colors[x])

        df['xpos'] = df['timestamp'].apply(lambda x: mdates.date2num(x))
        xpos = df['xpos'].to_list()
        widths = [xpos[i + 1] - xpos[i] for i in range(len(xpos) - 1)] + [1]



        height = 10
        for i, color in enumerate(df['color']):
            print(f"{i}, {xpos[i]}, {widths[i]}")
            if xpos[i] >= start and xpos[i] <= end:
                if xpos[i]+widths[i] > end:
                    width = end - xpos[i]
                    axs[index_col].bar(xpos[i], height, width=width, color=color, align='edge', edgecolor='black')
                else:
                    axs[index_col].bar(xpos[i], height, width=widths[i], color=color, align='edge', edgecolor='black')
            elif xpos[i]+widths[i] >= start and xpos[i]+widths[i] <= end:
                width = xpos[i]+widths[i] - start
                axs[index_col].bar(start, height, width=width, color=color, align='edge', edgecolor='black')
            elif xpos[i] < start and xpos[i]+widths[i] > end:
                axs[index_col].bar(start, height, width=end-start, color=color, align='edge', edgecolor='black')
            else:
                continue
            print(width)
        
        axs[index_col].set_ylabel('')
        axs[index_col].set_yticklabels([])

    axs[1].xaxis_date()
    axs[0].xaxis_date()
    date_format = mdates.DateFormatter('%H:%M:%S')
    axs[1].xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.subplots_adjust(hspace=0, wspace=0  )
    plt.show()

data = {'timestamp': ['2021-01-01 10:00:00', '2021-01-01 11:00:00', '2021-01-01 12:00:00', '2021-01-01 13:30:00', '2021-01-01 14:00:00', '2021-01-01 15:00:00', '2021-01-01 19:00:00'],
        'value': [3, 4, 3, 7, 8, 3, 5],
        'value2': [4, 4, 5, 4, 4, 4, 4],
        'value3': [1, 4, 5, 3, 7, 4, 4]}
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
plot_timestamps(df, pd.to_datetime('2021-01-01 10:30:00'), pd.to_datetime('2021-01-01 15:30:00'))
# %%