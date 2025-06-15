import csv
from datetime import datetime

class LogParser:
    @staticmethod
    def parse(file_path):
        jobs = {}
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for idx, row in enumerate(reader, 1):
                try:
                    time_str, desc, status, pid = row
                    timestamp = datetime.strptime(time_str.strip(), "%H:%M:%S")
                    status = status.strip()
                    pid = pid.strip()

                    if pid not in jobs:
                        jobs[pid] = {}
                    jobs[pid][status] = timestamp
                except Exception as e:
                    print(f"Skipping malformed line {idx}: {row} | Reason: {e}")
        return jobs