import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from scipy.optimize import curve_fit
import numpy as np
import locale


def data_read(file_name, line_skip, split_char):  # read file
    matrix_data = []
    try:
        with open(file_name, "r") as f:
            for _ in range(line_skip):  # skip header
                next(f)
            for line in f.readlines():
                temp = []
                values = line.strip().split(split_char)
                for item in values:  # load all columns
                    temp.append(np.float64(item))
                matrix_data.append(temp)
        print(f"Loaded file \"{file_name}\"")
        f.close()
        return np.array(matrix_data)
    except FileNotFoundError:
        print(f"File \"{file_name}\" not found")


def polyfit_plot(x, y, fit_degree, x_name, y_name, data_title, data_name):  # plots a fits data, returns fit parameters
    global save_state
    fig, ax = plt.subplots()

    x_data = np.linspace(x[0], x[-1], 100)
    fit_par = np.polyfit(x, y, fit_degree)
    fit_data = np.poly1d(fit_par)

    ax.plot(x_data, fit_data(x_data), "r-", label=f"Polyfit {fit_degree}. deg")
    ax.plot(x, y, "bx", label="Data")

    print(f"PolyFit par: {fit_par}")  # print fit par

    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    ax.yaxis.set_major_formatter(tkr.StrMethodFormatter('{x:#.2n}'))  # apply ticker - decimal comma
    ax.xaxis.set_major_formatter(tkr.StrMethodFormatter('{x:#.2n}'))

    plt.legend()
    plt.title(data_title)
    plt.tight_layout()
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')  # set locale for decimal comma
    if save_state:
        plt.savefig(f"{data_name}.pdf")
        print(f"\nFile saved as \"{data_name}.pdf\"")
    else:
        plt.show()
    return fit_par


def fit_eq(x, a, b, c):
    return a * np.exp(b * x) + c


def eq_fit_plot(x, y, fit_input, x_name, y_name, data_title, data_name):  # plots a fits data, returns fit parameters
    global save_state
    fig, ax = plt.subplots()

    x_data = np.linspace(x[0], x[-1], 100)
    popt, pcov = curve_fit(fit_eq, x, y, p0=fit_input)

    ax.plot(x_data, fit_eq(x_data, *popt), "r-", label=r"Fit: $y={:.4f}\cdot e^{{{:.4f}\cdot x}}+{:.4f}$".format(*popt))
    ax.plot(x, y, "bx", label="Data")

    print("Fit par: a = {}, b = {}, c = {}".format(*popt))  # print fit par and uncertainties
    print("\t Fit unc.: a = +- {}, b = +- {}, c = +- {}".format(*np.sqrt(np.diag(pcov))))

    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    ax.yaxis.set_major_formatter(tkr.StrMethodFormatter('{x:#.2n}'))  # apply ticker - decimal comma
    ax.xaxis.set_major_formatter(tkr.StrMethodFormatter('{x:#.2n}'))

    plt.legend()
    plt.title(data_title)
    plt.tight_layout()
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')  # set locale for decimal comma
    if save_state:
        plt.savefig(f"{data_name}.pdf")
        print(f"\nFile saved as \"{data_name}.pdf\"")
    else:
        plt.show()
    return popt


if __name__ == "__main__":
    save_state = False  # True -> only saves figure, False -> only displays figures

    # PLACEHOLDER
    data = data_read("test.txt", 0, "\t")
    fit_parameters_1 = polyfit_plot(data[:, 0], data[:, 1], 2, "x axis", "y axis", "1", "graph_1")
    fit_parameters_2 = eq_fit_plot(data[:, 0], data[:, 1], [1, -1, 0], "x axis", "y axis", "2", "graph_2")
