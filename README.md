# 📟 Log Analyzer

A lightweight Python tool to monitor job execution time from log files and flag long-running jobs using configurable thresholds. It provides both console and file output with dual logging and is tested via GitHub Actions CI.

---

## 📌 Features

* ✅ Parses log files with entries like: `HH:MM:SS,description,START/END,PID`
* 🕒 Calculates job durations using START/END pairs
* ⚠️ Warns if a job takes longer than the warning threshold
* ❌ Logs an error if a job exceeds the error threshold
* 🧪 Includes comprehensive unit tests
* 📂 Outputs logs to both console and file
* 🚰 Supports GitHub Actions for CI

---

## 📁 Directory Structure

```
log_analyzer/
├── main.py                       # Entry point for CLI
├── utils/
│   └── log_parser.py             # Contains the LogParser class
├── tests/
│   └── test_log_parser.py        # Unit tests using pytest
└── .github/
    └── workflows/
        └── test.yml              # GitHub Actions workflow for CI
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

* Python 3.8+
* Install testing dependencies:

```bash
pip install requirements.txt
```

---

### ▶️ Run the Analyzer

```bash
python main.py --log_data logs.log
```

### Optional arguments:

| Argument        | Description                                 | Default     |
| --------------- | ------------------------------------------- | ----------- |
| `--warning`     | Warning threshold in minutes                | `5`         |
| `--error`       | Error threshold in minutes                  | `10`        |
| `--output_path` | Directory to save `filtered_log.log` output | `./output/` |

#### Example:

```bash
python main.py --log_data logs.log --warning 3 --error 7 --output_path ./results/
```

---

## 📍 Log Format

Each row in the CSV-like log should follow this structure:

```
HH:MM:SS,Description,START|END,PID
```

### Example:

```
11:35:23,scheduled task 032,START,37980
11:35:56,scheduled task 032,END,37980
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

Unit tests cover the following scenarios:

| Scenario            | Covered |
| ------------------- | ------- |
| Valid parsing       | ✅       |
| Malformed time      | ✅       |
| Missing END/START   | ✅       |
| Duplicate START/END | ✅       |
| Empty lines         | ✅       |
| Extra columns       | ✅       |
| Wrong time format   | ✅       |

---

## 🔄 GitHub Actions

CI is configured to:

* ✅ Run on every push to `main`, `develop`, or feature branches
* ✅ Trigger **only when Python files** change
* ✅ Upload the test summary to the GitHub Actions **Summary tab**

Workflow location:

```
.github/workflows/test.yml
```

---

## 📂 Output Example

Logs are saved to both terminal and:

```
./output/filtered_log.log
```

Sample log entry:

```
WARNING: WARNING | PID: 81258 | Duration: 0:06:45 | Start: 11:36:58 | End: 11:43:43
```

---

## 📄 License

MIT License

---

## 🙌 Contributions

Contributions are welcome! Fork the repo and submit a pull request 🚀
