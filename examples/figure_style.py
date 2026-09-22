"""Publication plotting conventions shared with the finite-strain Biot paper."""
import matplotlib.pyplot as plt
from cycler import cycler

COLORS = list(plt.get_cmap('viridis')([0.0, 0.5, 1.0]))


def apply_style():
    plt.rcParams.update({
        'font.family': 'serif', 'mathtext.fontset': 'cm',
        'font.size': 9, 'axes.labelsize': 9, 'axes.titlesize': 9,
        'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8,
        'axes.linewidth': .8, 'lines.linewidth': 1.6,
        'lines.markersize': 3.4, 'lines.markerfacecolor': 'white',
        'lines.markeredgewidth': .8, 'axes.prop_cycle': cycler(color=COLORS),
        'axes.spines.top': True, 'axes.spines.right': True,
        'pdf.fonttype': 42, 'savefig.bbox': 'tight',
    })


def publication_size(fig):
    """Keep the companion's print width while retaining room for panel labels."""
    width, height = fig.get_size_inches()
    if width > 6.35:
        fig.set_size_inches(6.35, max(2.77, height * 6.35 / width))
