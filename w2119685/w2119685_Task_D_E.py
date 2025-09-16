import w2119685_Task_A_B_C
import csv    # Import the CSv module to read CSV flie
import tkinter as tk
from collections import defaultdict

# Task D: Histogram Display
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.root.title("Histogram of Vehicle Frequency per Hour")
        self.canvas = None  # Will hold the canvas for drawing
        self.canvas_width = 1000
        self.canvas_height = 600
        self.bar_width = 15

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="mint cream")
        self.canvas.pack()

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        junction1 = self.traffic_data["Elm Avenue/Rabbit Road"]
        junction2 = self.traffic_data["Hanley Highway/Westway"]
        max_traffic = max(max(junction1), max(junction2))

        # Draw axes
        self.draw_axes(max_traffic)

        # Draw bars with labels
        for hour in range(24):
            # Junction 1 bar
            x1 = 75 + hour * 35 - self.bar_width
            y1 = 550 - (junction1[hour] / max_traffic) * 500
            x2 = 75 + hour * 35
            self.canvas.create_rectangle(x1, y1, x2, 550, fill="gold", outline="black")
            self.canvas.create_text((x1 + x2) // 2, y1 - 10, text=str(junction1[hour]), font=("Arial", 8), fill="black")

            # Junction 2 bar
            x1 = 75 + hour * 35
            y1 = 550 - (junction2[hour] / max_traffic) * 500
            x2 = 75 + hour * 35 + self.bar_width
            self.canvas.create_rectangle(x1, y1, x2, 550, fill="purple", outline="black")
            self.canvas.create_text((x1 + x2) // 2, y1 - 10, text=str(junction2[hour]), font=("Arial", 8), fill="black")

    def draw_axes(self, max_traffic):
        """
        Draws the X and Y axes for the histogram.
        """
        # Draw X-axis
        self.canvas.create_line(50, 550, 950, 550, width=2)
        self.canvas.create_text(500, 580, text="Hours 00:00 to 24:00", font=("Arial", 12), fill="black")
        for i in range(24):
            x = 75 + i * 35
            self.canvas.create_text(x, 560, text=str(i), font=("Arial", 10), fill="black")

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        # Title
        self.canvas.create_text(
            self.canvas_width // 2, 20,
            text=f"Histogram of Vehicle Frequency per Hour ({self.date})",
            font=("Arial", 16, "bold"),
            fill="black"
        )
        # Legend
        self.canvas.create_rectangle(100, 40, 120, 60, fill="gold", outline="black")
        self.canvas.create_text(130, 50, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10))
        self.canvas.create_rectangle(100, 70, 120, 90, fill="purple", outline="black")
        self.canvas.create_text(130, 80, text="Hanley Highway/Westway", anchor="w", font=("Arial", 10))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.add_legend()
        self.draw_histogram()
        self.root.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        data = defaultdict(lambda: [0] * 24)
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                junction = row["JunctionName"]
                time_of_day = row["timeOfDay"]
                hour = int(time_of_day.split(":")[0])
                data[junction][hour] += 1
        return data

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        self.clear_previous_data()
        
        while True:
            vailddate = w2119685_Task_A_B_C.validate_date_input()
            file_path =f"traffic_data{vailddate}.csv"    # Construct file path using validated data input
            file_date =f"{vailddate[:2]}/{vailddate[2:4]}/{vailddate[4:]}"
            outcomes= w2119685_Task_A_B_C.process_csv_data(file_path)          # Process CSV data 
            if outcomes:
                w2119685_Task_A_B_C.display_outcomes(outcomes)      # Display outcomes to console
                w2119685_Task_A_B_C.save_results_to_file(outcomes, txt_file="results.txt")    # Save results

            try:
                self.clear_previous_data()
                self.current_data = self.load_csv_file(file_path)
                print(f"\n{'*' * 25}")
                print(f"You should Exit from histogram before continue with the program")
                print(f"{'*' * 25}\n")
                app = HistogramApp(self.current_data, file_date)
                app.run()
                
            except Exception as e:
                print(f"Error processing file: {e}")

            self.process_files()
            break

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        if w2119685_Task_A_B_C.validate_continue_input() == "N":
            print(f"End of run")
        else:
            self.handle_user_interaction()


# Main
if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.handle_user_interaction()