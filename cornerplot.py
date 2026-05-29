import pandas as pd
import numpy as np
import corner
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os
#File - Adjust these file part according to the star you are studying with.
EXCEL_FILE  = 'Your_file_name.xlsx'
SHEET_68    = 'err68'
SHEET_90    = 'err90'
SHEET_99    = 'err99'
params = [
    'i', 'T2', 'POT1', 'POT2',
    'q_MASS_RATIO',
    'L1', 'L2', 'L3'
]
labels = [
    r'$i\ (^\circ)$', r'$T_2$',
    r'$\Omega_1$', r'$\Omega_2$', r'$q$',
    r'$L_1$', r'$L_2$', r'$L_3$'
]

# MCMC out.dsp best fit values /// Adjust these parameters according to the star you are studying with. 
outDSP = {
    'i':            59.98584,
    'T2':            0.69846,
    'POT1':          6.94548,
    'POT2':          6.94548,
    'q_MASS_RATIO':  3.64145,
    'L1':            2.49188,
    'L2':            6.10543,
    'L3':            0.24657,
}
best_fit = np.array([outDSP[p] for p in params])

# Color and contour adjustments
LAYERS = [
    {'sheet': SHEET_99, 'color': '#E07B54', 'label': 'err99 (99%)'},
    {'sheet': SHEET_90, 'color': '#5B8DB8', 'label': 'err90 (90%)'},
    {'sheet': SHEET_68, 'color': '#2D6A4F', 'label': 'err68 (68%)'},
]
# Cleaning function /// Adjust these parameters according to the star you are studying with.
def load_and_clean(sheet):
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)
    df = df[params].dropna().copy()
    df = df[
        (df['i'] < 70) &
        (df['T2'] < 1.0) &
        (df['POT1'] < 10.0) &
        (df['POT2'] < 10.0) &
        (df['q_MASS_RATIO'] < 6.0) &
        (df['L3'] < 1.0) &
        (df['L2'] < 7.0) &
        (df['L1'] < 4.0)
    ]
    for col in params:
        med = df[col].median()
        mad = np.median(np.abs(df[col] - med)) # mad = Median Absolute Deviation
        if mad == 0:
            continue
        sigma = 1.4826 * mad
        df = df[np.abs(df[col] - med) < 5.0 * sigma] # You can change sigma value. 
    print(f"  {sheet}: {len(df)} example")
    return df[params].values

if not os.path.exists(EXCEL_FILE):
    raise FileNotFoundError(f"ERROR: '{EXCEL_FILE}' could not be found! Please place the Excel file in the same folder as the code.")
print("Data Loading...")
datasets = []
for layer in LAYERS:
    data = load_and_clean(layer['sheet'])
    datasets.append(data)
# Corner plot 
fig = None
for idx, (layer, data) in enumerate(zip(LAYERS, datasets)):
    lw = [0.8, 1.2, 1.8][idx]
    kwargs = dict(
        labels=labels if idx == 2 else ['' ] * len(params),
        bins=30,
        smooth=1.5,
        color=layer['color'],
        show_titles=False,
        fill_contours=True,
        plot_contours=True,
        plot_density=False,
        plot_datapoints=False,
        levels=[0.68, 0.95],
        contour_kwargs={
            'linewidths': lw,
            'colors': [layer['color'], layer['color']],
        },
        hist_kwargs={
            'density': True,
            'histtype': 'step',
            'linewidth': lw,
            'color': layer['color'],
            'alpha': 0.9,
        },
        label_kwargs={'fontsize': 26},
    )
    if fig is None:
        fig = corner.corner(data, **kwargs)
    else:
        corner.corner(data, fig=fig, **kwargs)

# Median and out.dsp lines
n = len(params)
axes = np.array(fig.get_axes()).reshape(n, n)

data_90_tmp = datasets[1]
medians = np.array([np.percentile(data_90_tmp[:, i], 50) for i in range(len(params))])

for i in range(n):
    # Median lines
    axes[i, i].axvline(medians[i], color='red',
                       linewidth=1.5, linestyle='--', zorder=10)
    # out.dsp lines
    axes[i, i].axvline(best_fit[i], color='black',
                       linewidth=2, linestyle=':', zorder=10)
    for j in range(i):
        axes[i, j].axvline(medians[j], color='red',
                           linewidth=1.5, linestyle='--', alpha=0.7, zorder=10)
        axes[i, j].axhline(medians[i], color='red',
                           linewidth=1.5, linestyle='--', alpha=0.7, zorder=10)
        axes[i, j].axvline(best_fit[j], color='black',
                           linewidth=1.5, linestyle=':', alpha=0.7, zorder=10)
        axes[i, j].axhline(best_fit[i], color='black',
                           linewidth=1.5, linestyle=':', alpha=0.7, zorder=10)

# Titles: median + asymmetric error 
# median = Q50, +error = Q84-Q50, -error = Q50-Q16 (err68 - datasets[2] - 16,50,84)
# median = Q50, +error = Q95-Q50, -error = Q50-Q05 (err90 - datasets[1] - 5,50,95)
# median = Q50, +error = Q99.5-Q50, -error = Q50-Q0.5 (err99 - datasets[0] - 0.5, 50, 99.5)
data_90 = datasets[1]   # err90 
decimal_places = {
    'i': 3, 'T2': 4, 'POT1': 4, 'POT2': 4,
    'q_MASS_RATIO': 4,
    'L1': 4, 'L2': 4, 'L3': 4,
}
for i, col in enumerate(params):
    values = data_90[:, i]
    q05    = np.percentile(values, 5)
    q50    = np.percentile(values, 50)  
    q95    = np.percentile(values, 95)
    err_lo = q50 - q05                   
    err_hi = q95 - q50                  
    d      = decimal_places.get(col, 4)
    #best_fit (black) is written in the title, errors come from the median.
    fmt    = f".{d}f"
    title  = (f"{best_fit[i]:{fmt}}"  + r"$^{+" + f"{err_hi:{fmt}}" + r"}_{-" + f"{err_lo:{fmt}}" + r"}$") # if you don't want to use out.dsp values change the f"{best_fit[i]:{fmt}}" to f"{q50:{fmt}}"  
    axes[i, i].set_title(title, fontsize=16, pad=6)
legend_elements = [
    Line2D([0], [0], color=layer['color'], linewidth=2, label=layer['label'])
    for layer in LAYERS ] + [
    Line2D([0], [0], color='red', linewidth=1.5,
           linestyle='--', label='err90 median'),
    Line2D([0], [0], color='black', linewidth=1.5,
           linestyle=':', label='out.dsp best fit'),
]
fig.legend(
    handles=legend_elements,
    loc='upper right',
    bbox_to_anchor=(0.98, 0.98),
    fontsize=26,
    framealpha=0.9
)
fig.set_size_inches(30, 30)
for ax in fig.get_axes():
    ax.tick_params(axis='both', labelsize=16)
#plt.suptitle('Monte Carlo Posterior Distributions',fontsize=16, y=1.02)
plt.subplots_adjust(left=0.15, bottom=0.15)
plt.savefig('corner.png', dpi=300,bbox_inches='tight', facecolor='white')
print("Saved: corner.png")
plt.savefig('corner.eps', format='eps',bbox_inches='tight')
print("Saved: corner.eps")