"""Publication plotting conventions shared with the finite-strain Biot paper."""
import re
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from cycler import cycler

COLORS = list(plt.get_cmap('viridis')([0.0, 0.5, 1.0]))


def _move_panel_marker_to_bottom():
    """Render leading panel markers below, rather than in, plot titles."""
    if getattr(Axes, '_biot_panel_marker_bottom', False):
        return
    original_set_title = Axes.set_title

    def set_title(self, label, *args, **kwargs):
        match = re.match(r'^\(([a-z])\)\s*(.*)$', str(label))
        if match:
            self.text(.5, -.34, f'({match.group(1)})', transform=self.transAxes,
                      ha='center', va='top', clip_on=False,
                      fontsize=plt.rcParams['axes.titlesize'])
            label = match.group(2)
        return original_set_title(self, label, *args, **kwargs)

    Axes.set_title = set_title
    Axes._biot_panel_marker_bottom = True


def apply_style():
    _move_panel_marker_to_bottom()
    plt.rcParams.update({
        'font.family': 'serif', 'mathtext.fontset': 'cm',
        'font.size': 9, 'axes.labelsize': 9, 'axes.titlesize': 9,
        'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8,
        'axes.linewidth': .8, 'lines.linewidth': 1.6,
        'lines.markersize': 3.4, 'lines.markerfacecolor': 'white',
        'lines.markeredgewidth': .8, 'axes.prop_cycle': cycler(color=COLORS),
        'axes.spines.top': True, 'axes.spines.right': True,
        'pdf.fonttype': 42, 'savefig.bbox': 'tight',
        # PGF is compiled inside main.tex.  These settings make standalone
        # PGF previewing use the same LuaLaTeX/Latin Modern configuration.
        'pgf.texsystem': 'lualatex', 'pgf.rcfonts': False,
        'pgf.preamble': '\\RequirePackage{fix-cm}\n'
                       '\\usepackage{lmodern}\n'
                       '\\usepackage{unicode-math}\n'
                       '\\unimathsetup{mathbf=sym,bold-style=upright}\n'
                       '\\setmainfont{Latin Modern Roman}\n'
                       '\\setmathfont{Latin Modern Math}',
    })


def publication_size(fig):
    """Keep the companion's print width while retaining room for panel labels."""
    width, height = fig.get_size_inches()
    if width > 6.35:
        fig.set_size_inches(6.35, max(2.77, height * 6.35 / width))
