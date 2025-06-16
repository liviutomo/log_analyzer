import argparse
import os
import pathlib

from utils.log_parser import LogParser
import logging

class LogAnalyzer():
    def __init__(self, log_data, warning_threshold=5, error_threshold=10):
            self.log_data = log_data
            self.warning_threshold = warning_threshold
            self.error_threshold = error_threshold
            self.jobs = {}

    def parse_log_file(self):
        self.jobs = LogParser.parse(self.log_data)

    def analyze(self):
        print("\n Job Duration Report:\n")
        for pid, events in self.jobs.items():
            if "START" in events and "END" in events:
                duration = events["END"] - events["START"]
                minutes = duration.total_seconds() / 60

                if minutes > self.error_threshold:
                    level = logging.ERROR
                    status = "ERROR"
                elif minutes > self.warning_threshold:
                    level = logging.WARNING
                    status = "WARNING"
                else:
                    level = logging.INFO
                    status = "OK"
                logging.log(level, f"{status} |"
                                f" PID: {pid} |"
                                f" Duration: {str(duration)} |"
                                f" Start: {events['START'].time()} |"
                                f" End: {events['END'].time()}")
            else:
                logging.warning(f"Incomplete data for PID {pid} - missing START or END")

    def start(self):
        self.parse_log_file()
        self.analyze()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Log Analyzer",
        description="A simple log monitoring application that reads the file, "
                    "measures how long each job takes from start to finish and "
                    "generates warnings or errors if the processing time exceeds "
                    "certain thresholds."
    )
    parser.add_argument("--log_data", help="Log file that will be analyzed", required=True)
    parser.add_argument("--warning", help="Warning threshold in minutes", type=int, default=5)
    parser.add_argument("--error", help="Error threshold in minutes", type=int, default=10)
    parser.add_argument("--output_path", help="Output path where the filter logs are saved",
                        default=os.path.join(os.getcwd(), "output"))
    args = parser.parse_args()

    # Ensure output directory exists
    output_path = pathlib.Path(args.output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    # File logging path
    log_file_path = output_path / "filtered_log.log"

    # Clear any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Setup dual logging: file + console
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(str(log_file_path), mode="w"),
            logging.StreamHandler()
        ]
    )

    analyzer = LogAnalyzer(args.log_data, args.warning, args.error)
    analyzer.start()