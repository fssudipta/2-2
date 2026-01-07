import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

INF = 8

def plot(
        signal, 
        title=None, 
        y_range=(-1, 3), 
        figsize = (8, 3),
        x_label='n (Time Index)',
        y_label='x[n]',
        saveTo=None
    ):
    plt.figure(figsize=figsize)
    plt.xticks(np.arange(-INF, INF + 1, 1))
    
    y_range = (y_range[0], max(np.max(signal), y_range[1]) + 1)
    # set y range of 
    plt.ylim(*y_range)
    plt.stem(np.arange(-INF, INF + 1, 1), signal)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    if saveTo is not None:
        plt.savefig(saveTo)
    # plt.show()

def init_signal():
    return np.zeros(2 * INF + 1)


def time_scale_signal(x: np.ndarray, k: int) -> np.ndarray:
    y = np.zeros_like(x)
    center = INF

    n = np.arange(-INF, INF + 1)
    valid = (n % k == 0)

    src = n[valid] // k
    in_range = (src >= -INF) & (src <= INF)

    y[center + n[valid][in_range]] = x[center + src[in_range]]
    return y


def time_scale_signal_interpolate(x: np.ndarray, k: int) -> np.ndarray:
    y = np.zeros_like(x)
    center = INF

    n = np.arange(-INF, INF + 1)
    src = n / k

    low = np.floor(src).astype(int)
    high = np.ceil(src).astype(int)

    valid = (low >= -INF) & (high <= INF)

    y[center + n[valid]] = (
        x[center + low[valid]] + x[center + high[valid]]
    ) / 2

    return y


def main():
    img_root = '.'
    signal = init_signal()
    signal[INF] = 1
    signal[INF+1] = .5
    signal[INF-1] = 2
    signal[INF + 2] = 1
    signal[INF - 2] = .5

    plot(signal, title='Original Signal(x[n])', saveTo=f'{img_root}/x[n].png')
    plot(time_scale_signal(signal, 3), title='x[n/3]', saveTo=f'{img_root}/x[n divided by 3].png')
    plot(time_scale_signal(signal, 1), title='x[n/1]', saveTo=f'{img_root}/x[n divided by 1].png')
    plot(time_scale_signal_interpolate(signal, 3), title='x[n/3] with interpolation', saveTo=f'{img_root}/x[n divided by 3]_with_interpolation.png')
    plot(time_scale_signal_interpolate(signal, 1), title='x[n/1] with interpolation', saveTo=f'{img_root}/x[n divided by 1]_with_interpolation.png')

main()