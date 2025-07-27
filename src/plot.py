# =============================================================================
# Description: This script reads a single-read or multi-read FAST5 file from
#              Oxford Nanopore sequencing, extracts the raw electrical
#              current signal ("squiggle") from the first available read,
#              and generates a plot of the signal over time.
# =============================================================================

import h5py
import matplotlib.pyplot as plt


def plot_first_squiggle(fast5_filepath):
    """
    Reads a .fast5 file and plots the raw signal of the first read found.

    Args:
        fast5_filepath (str): The full path to the .fast5 file.
    """
    try:
        # Open the FAST5 file in read-only mode
        with h5py.File(fast5_filepath, "r") as f5:
            print(f"Successfully opened: {fast5_filepath}")

            # --- Find the first read in the file ---
            # The structure can vary slightly, but reads are typically under the 'Raw/Reads' group.
            # We will programmatically find the first read entry.
            reads_group = f5.get("Raw/Reads")
            if reads_group is None:
                print("Error: Could not find the 'Raw/Reads' group in the file.")
                print("This might not be a valid raw signal FAST5 file.")
                return

            if not list(reads_group.keys()):
                print("Error: No reads found in the 'Raw/Reads' group.")
                return

            # Get the name of the first read (e.g., 'Read_123')
            first_read_name = list(reads_group.keys())[0]
            print(f"Found first read: {first_read_name}")

            # --- Extract the raw signal ---
            # The signal data is stored in the 'Signal' dataset for that read.
            signal_dataset = reads_group[first_read_name]["Signal"]
            raw_signal = signal_dataset[:]  # Load the entire dataset into memory

            print(f"Extracted raw signal with {len(raw_signal)} data points.")

            # --- Plot the raw signal ---
            plt.style.use("seaborn-v0_8-whitegrid")
            plt.figure(figsize=(20, 5))  # Use a wide figure to see the signal details

            # Plot a subset of the signal for clarity, as the full signal can be very long
            plot_points = 5000
            if len(raw_signal) > plot_points:
                print(f"Plotting the first {plot_points} points for clarity.")
                signal_to_plot = raw_signal[:plot_points]
            else:
                signal_to_plot = raw_signal

            plt.plot(signal_to_plot)

            # --- Add plot details ---
            plt.title(
                f"Raw Nanopore Signal (Squiggle)\nFile: {fast5_filepath.split('/')[-1]} | Read: {first_read_name}",
                fontsize=16,
            )
            plt.xlabel("Time (Samples)", fontsize=12)
            plt.ylabel("Raw Current Signal (pA)", fontsize=12)
            plt.tight_layout()  # Adjust layout to make sure everything fits

            # --- Show the plot ---
            print("Displaying plot...")
            plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{fast5_filepath}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please ensure the file is a valid, uncorrupted .fast5 file.")



if __name__ == "__main__":
    
    file_path = "data/SRR7517493"  # Replace with your actual file path

    plot_first_squiggle(file_path)
