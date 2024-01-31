import matplotlib.pyplot as plt
import numpy as np


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
        return np.array(matrix_data)
    except FileNotFoundError:
        print(f"File \"{file_name}\" not found")


def fit_plot(x, y, fit_degree, x_name, y_name, data_name):  # polts a fits data, returns fit parameters
    global save_state
    fig, ax = plt.subplots()

    x_data = np.linspace(x[0], x[-1], 100)
    fit_par = np.polyfit(x, y, fit_degree)
    fit_data = np.poly1d(fit_par)

    ax.plot(x_data, fit_data(x_data), "r-", label=f"Polyfit {fit_degree}. deg")
    ax.plot(x, y, "bx", label="Data")

    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    plt.legend()
    plt.tight_layout()
    if save_state:
        plt.savefig(f"{data_name}.pdf")
        print(f"\nFile saved as \"{data_name}.pdf\"")
    else:
        plt.show()
    return fit_par


if __name__ == "__main__":
    save_state = False  # True -> only saves figure, False -> only displays figures

    # PLACEHOLDER
    data = data_read("test.txt", 0, "\t")
    fit_parameters = fit_plot(data[:, 0], data[:, 1], 2, "x axis", "y axis", "graph")
