import numpy
from matplotlib import pyplot
from matplotlib.pyplot import subplots
from matplotlib.ticker import AutoMinorLocator
from .hcl import HCL


class PLOT:
    def __init__(
        self, n = 1, size = 3, output = 'plot.pdf',
        dot_size = 0.1, dot_alpha = 0.9, label_size = 8, line_width = 0.5
    ):
        self.output = output
        self.dot_size = dot_size
        self.dot_alpha = dot_alpha
        self.label_size = label_size
        self.line_width = line_width
        self.figure, self.axes = subplots(nrows = 1, ncols = n, figsize = (size * n, size), squeeze = False)
        self.plots = 0
        return None

    def plot(self, x, y, l):
        hcl = HCL()
        unique_labels = numpy.unique(l)
        for label, color in zip(unique_labels, hcl.main(unique_labels.size)):
            mask = l == label
            x_ = x[mask]
            y_ = y[mask]
            self.axes[0, self.plots].scatter(
                x_, y_, s = self.dot_size, alpha = self.dot_alpha, label = label, color = color, marker = ','
            )
            self.axes[0, self.plots].text(
                numpy.mean(x_), numpy.mean(y_), label.astype(numpy.str_),
                verticalalignment = 'center', horizontalalignment = 'center', color = '#555555', fontsize = 4
            )
        self.axes[0, self.plots].tick_params(labelsize = self.label_size)
        self.axes[0, self.plots].xaxis.set_minor_locator(AutoMinorLocator(2))
        self.axes[0, self.plots].yaxis.set_minor_locator(AutoMinorLocator(2))
        self.axes[0, self.plots].grid(True, which = 'both', linestyle = '--', linewidth = self.line_width)
        self.plots += 1
        return self

    def save(self):
        self.figure.savefig(self.output, format = 'pdf', dpi = 300, bbox_inches = 'tight')
        pyplot.close(self.figure)
        return None
