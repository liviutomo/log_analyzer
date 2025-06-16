import csv
from datetime import datetime

class LogParser:
    @staticmethod
    def parse(file_path):
        jobs = {}

        # Open the log file in read mode
        with open(file_path, 'r') as f:
            reader = csv.reader(f)

            # Loop through each line with line number (starting at 1)
            for idx, row in enumerate(reader, 1):
                try:
                    # Unpack the row into expected fields
                    time_str, desc, status, pid = row
                    # Convert time string to datetime object for comparison
                    timestamp = datetime.strptime(time_str.strip(), "%H:%M:%S")
                    # Clean up strings
                    status = status.strip()
                    pid = pid.strip()
                    # Initialize a job entry for this PID if not already present
                    if pid not in jobs:
                        jobs[pid] = {}
                    # Store the timestamp under the status key (START or END)
                    jobs[pid][status] = timestamp
                except Exception as e:
                    # Catch and report any malformed rows without stopping execution
                    print(f"Skipping malformed line {idx}: {row} | Reason: {e}")
        return jobs