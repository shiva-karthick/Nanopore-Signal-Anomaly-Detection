#     Reads a .pod5 file and plots the raw signal of the first read found.

import pod5
import matplotlib.pyplot as plt
import os


def plot_first_pod5_squiggle(pod5_filepath) -> None:
    try:
        with pod5.Reader(pod5_filepath) as reader:
            print(f"Successfully opened: {pod5_filepath}")

            # The Reader object allows us to iterate through all reads in the file.
            # We only need the first one for my purpose.
            first_read_record = next(reader.reads(), None)

            if first_read_record is None:
                print("Error: No reads found in this POD5 file.")
                return

            # Extract the raw signal
            # The read record object has a 'signal' attribute which is a numpy array
            raw_signal = first_read_record.signal

            if raw_signal is None:
                print(
                    f"Error: Could not retrieve signal for read ID: {first_read_record.read_id}"
                )
                return

            print(f"Extracted signal from read: {first_read_record.read_id}")
            print(f"Signal contains {len(raw_signal)} data points.")

            # Plot the raw signal
            plt.style.use("seaborn-v0_8-whitegrid")
            plt.figure(figsize=(20, 5))  # Use a wide figure for better detail

            # For clarity, we'll plot a subset of the signal. Full signals are huge nd seemed to be messy.
            plot_points: int = len(
                raw_signal
            )  # Change the number of points to plot as needed
            if len(raw_signal) >= plot_points:
                print(f"Plotting the first {plot_points} points for clarity.")
                signal_to_plot = raw_signal[:plot_points]
            else:
                signal_to_plot = raw_signal

            plt.plot(signal_to_plot)

            # Add plot details
            plt.title(
                f"Raw Nanopore Signal (Squiggle) from POD5\nFile: {os.path.basename(pod5_filepath)} | Read ID: {first_read_record.read_id}",
                fontsize=16,
            )
            plt.xlabel("Time (Samples)", fontsize=12)
            plt.ylabel("Raw Current Signal (pA)", fontsize=12)
            plt.tight_layout()

            # Save and Show the plot
            print("Displaying plot...")
            plt.savefig("raw_signal_plot.png", dpi=300, bbox_inches="tight")
            plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{pod5_filepath}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please ensure this is a valid, uncorrupted .pod5 file.")


if __name__ == "__main__":
    """
    The raw signal with all the data points is very messy and hard to read.
    For clarity, we will plot only the first 1000 points.
    """
    plot_first_pod5_squiggle(
        "data/raw/PAU85136/pod5/PAU85136_fail_279c9095_68316534_10.pod5"
    )
