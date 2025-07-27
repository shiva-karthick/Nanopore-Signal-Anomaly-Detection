from _decimal import ROUND_UP
import pod5
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, savgol_filter
import os


def apply_butterworth_filter(signal, cutoff=0.01, order=4):
    """
    Applies a low-pass Butterworth filter to the signal.
    The cutoff frequency of 0.01 and the order of 4 in the apply_butterworth_filter function are chosen to achieve a balance between noise reduction and signal preservation.

    - Cutoff Frequency (0.01): This value represents the normalized cutoff frequency, where 1 corresponds to the Nyquist frequency (half the sampling rate). A cutoff of 0.01 means that frequencies above 1% of the Nyquist frequency will be attenuated. This low value is typically chosen to remove high-frequency noise while preserving the lower-frequency signal components that are likely to contain the relevant information in nanopore signals. Nanopore signals often have a significant amount of high-frequency noise, so a low cutoff helps to smooth the signal.

    - Order (4): The order of the Butterworth filter determines the steepness of the filter's attenuation curve. A higher order results in a sharper cutoff, meaning that frequencies above the cutoff are more rapidly attenuated. An order of 4 provides a reasonable trade-off between effective noise reduction and avoiding excessive phase distortion or ringing artifacts in the filtered signal.

    Play with these parameters to see how they affect the filtered signal.
    """
    # Get the filter coefficients
    b, a = butter(order, cutoff, btype="low", analog=False)
    # Apply the filter forwards and backwards to remove phase shift
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal


def calculate_sliding_std(signal, window_size=100):
    """
    Calculates the standard deviation over a sliding window.

    Args:
        signal (np.array): The input signal.
        window_size (int): The size of the sliding window.

    Returns:
        np.array: The calculated local standard deviation.
    """
    # Use pandas for an efficient rolling window calculation
    import pandas as pd

    return pd.Series(signal).rolling(window=window_size, center=True).std().to_numpy()


def process_and_plot_signal(pod5_filepath) -> None:
    try:
        with pod5.Reader(pod5_filepath) as reader:
            print(f"Successfully opened: {pod5_filepath}")
            first_read = next(reader.reads(), None)
            if first_read is None:
                print("Error: No reads found in this POD5 file.")
                return

            raw_signal = first_read.signal
            if raw_signal is None:
                print(
                    f"Error: Could not retrieve signal for read ID: {first_read.read_id}"
                )
                return

            # For clarity, we'll process and plot a subset of the signal.
            plot_points = round(len(raw_signal) / 4)
            signal_subset = raw_signal[:plot_points]
            print(
                f"Processing first {len(signal_subset)} points of read: {first_read.read_id}"
            )

            # Apply Filters
            print("Applying Butterworth filter...")
            butter_filtered = apply_butterworth_filter(signal_subset)

            print("Applying Savitzky-Golay filter...")
            # Window length must be odd and less than signal length
            savgol_window = min(
                51,
                len(signal_subset) - 1
                if len(signal_subset) % 2 == 0
                else len(signal_subset) - 2,
            )
            savgol_filtered = savgol_filter(
                signal_subset, savgol_window, 3
            )  # window, polyorder

            print("Calculating sliding window standard deviation...")
            sliding_std = calculate_sliding_std(signal_subset, window_size=50)

            # Generate all the Plots
            fig, axs = plt.subplots(4, 1, figsize=(20, 15), sharex=True)
            fig.suptitle(
                f"Signal Processing Analysis\nFile: {os.path.basename(pod5_filepath)} | Read ID: {first_read.read_id}",
                fontsize=20,
            )

            # 1. Raw Signal
            axs[0].plot(signal_subset, color="gray", label="Raw Signal")
            axs[0].set_title("1. Original Raw Signal (The Chaos)", fontsize=14)
            axs[0].set_ylabel("Raw Current (pA)")
            axs[0].legend(loc="upper right")
            axs[0].grid(True)

            # 2. Butterworth Filtered Signal
            axs[1].plot(butter_filtered, color="blue", label="Butterworth Filtered")
            axs[1].set_title(
                "2. After Butterworth Low-Pass Filter (General Smoothing)", fontsize=14
            )
            axs[1].set_ylabel("Filtered Current (pA)") # in picoAmperes
            axs[1].legend(loc="upper right")
            axs[1].grid(True)

            # 3. Savitzky-Golay Filtered Signal
            axs[2].plot(savgol_filtered, color="green", label="Savitzky-Golay Filtered")
            axs[2].set_title(
                "3. After Savitzky-Golay Filter (Shape-Preserving Smoothing)",
                fontsize=14,
            )
            axs[2].set_ylabel("Filtered Current (pA)")
            axs[2].legend(loc="upper right")
            axs[2].grid(True)

            # 4. Sliding Window Standard Deviation
            axs[3].plot(sliding_std, color="red", label="Local Std. Dev.")
            axs[3].set_title(
                "4. New Feature: Local Signal Volatility (Finding Order)", fontsize=14
            )
            axs[3].set_xlabel("Time (Samples)", fontsize=12)
            axs[3].set_ylabel("Standard Deviation")
            axs[3].legend(loc="upper right")
            axs[3].grid(True)

            plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust for subtitle
            print("Displaying plot...")
            plt.savefig("processed_signal_plot.png", dpi=300, bbox_inches="tight")
            plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{pod5_filepath}' was not found.")
    except ImportError:
        print(
            "Error: pandas library not found. Please install it with 'pip install pandas'"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    process_and_plot_signal(
        "data/raw/PAU85136/pod5/PAU85136_fail_279c9095_68316534_10.pod5"
    )
