import argparse
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
    args = parser.parse_args()

    analyzer = LogAnalyzer(args.log_data, args.warning, args.error)
    analyzer.start()