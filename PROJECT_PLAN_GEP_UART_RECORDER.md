# GEP UART Dataset Recorder Project Plan

## Goal

Build a PC tool for recording GEP radar UART data through a USB-UART adaptor, displaying the data in real time, and saving the received records into CSV files.

The tool should follow the curve display method and JSON record format used by `codex_on_gep_project_check_dataset_windowsBased`.

## Core Requirements

| Item | Requirement |
|---|---|
| Input source | Radar UART port connected to PC through USB-UART adaptor |
| Baud rate | 921600 |
| Input format | One JSON record per line |
| Frame key | `fn` means frame number |
| Frame period | About 50 ms per frame |
| Real-time display | Show live curve using the same style/method as `codex_on_gep_project_check_dataset_windowsBased` |
| Save format | CSV file |
| Output filename | `jb_GEP_dataset_YYYYMMDD_HHMMSS.csv` |

## Expected Data Flow

```text
Radar UART port
  -> USB-UART adaptor
  -> PC COM port
  -> serial reader
  -> line buffer
  -> JSON parser
  -> real-time curve state
  -> curve display
  -> CSV writer
  -> optional raw UART log
```

## UART Reading Design

Use Python `pyserial` for UART communication.

Recommended settings:

| Setting | Value |
|---|---|
| Baud rate | `921600` |
| Data bits | `8` |
| Parity | `None` |
| Stop bits | `1` |
| Timeout | Small timeout, for example `0.05` or `0.1` seconds |

The COM port should be configurable from the UI or command line. Do not hard-code one physical COM port unless testing.

## JSON Record Format

The input should use the same JSON-per-line format as the checker project.

Example expected record:

```json
{"fn": 123, "r0": 1.234, "r1": 1.567, "r2": 1.890}
```

Minimum required field:

| Field | Meaning |
|---|---|
| `fn` | Frame number |

Common optional fields:

| Field | Meaning |
|---|---|
| `r0` | Range channel 0 |
| `r1` | Range channel 1 |
| `r2` | Range channel 2 |

The parser should tolerate optional fields and should not crash when one JSON line is incomplete or malformed.

## Real-Time Curve Display

The display should reuse the curve concept from `codex_on_gep_project_check_dataset_windowsBased`.

Recommended display items:

| UI Item | Purpose |
|---|---|
| COM port selector | Choose USB-UART adaptor port |
| Baud display/input | Default `921600` |
| Start button | Open UART and start recording |
| Stop button | Stop reading and close files safely |
| Frame count | Number of valid JSON records parsed |
| Latest `fn` | Current frame number |
| JSON error count | Number of bad JSON lines |
| Output filename | Current CSV path |
| Live curve | Plot `r0`, optional `r1`, optional `r2` |

The plotting loop should not block UART reading. Use a reader thread, queue, or async design.

## CSV Saving Design

Save parsed JSON records into a CSV file while recording.

Recommended filename:

```text
jb_GEP_dataset_YYYYMMDD_HHMMSS.csv
```

Example:

```text
jb_GEP_dataset_20260625_142530.csv
```

Recommended CSV columns:

| Column | Meaning |
|---|---|
| `pc_time_iso` | PC timestamp when line was received |
| `pc_time_ms` | PC timestamp in milliseconds |
| `fn` | Frame number from JSON |
| `r0` | Range channel 0 if present |
| `r1` | Range channel 1 if present |
| `r2` | Range channel 2 if present |
| `raw_json` | Original JSON line for traceability |

CSV should be flushed periodically or after each row to reduce data loss if the program crashes.

## Raw Log Recommendation

Also save the raw UART text into a `.log` file during recording.

Recommended filename:

```text
jb_GEP_dataset_YYYYMMDD_HHMMSS_raw.log
```

Reason:

If the CSV parser has a bug or the JSON schema changes, the raw log can be used to rebuild the CSV later.

## Error Handling

| Case | Recommended Behavior |
|---|---|
| COM port cannot open | Show error and do not start recording |
| Bad JSON line | Save to raw log, increment error count, continue |
| Missing `fn` | Mark as invalid or save with blank `fn`, continue |
| UART disconnect | Stop recording safely and show status |
| CSV write failure | Stop recording and show output error |

## Suggested Implementation Structure

```text
codex_on_HEIGHT_mqtt_project/
  AGENTS.md
  PROJECT_PLAN_GEP_UART_RECORDER.md
  gep_uart_recorder.py
  requirements.txt
  data/
    jb_GEP_dataset_YYYYMMDD_HHMMSS.csv
    jb_GEP_dataset_YYYYMMDD_HHMMSS_raw.log
```

## Recommended Python Modules

| Module | Purpose |
|---|---|
| `serial` / `pyserial` | UART reading |
| `json` | JSON parsing |
| `csv` | CSV writing |
| `threading` or `asyncio` | Non-blocking UART reader |
| `queue` | Pass records from reader to UI/plotter |
| `pathlib` | Cross-platform file paths |
| `datetime` | File naming and timestamps |

## Test Method

1. Start with a fake UART source or replay a saved `.log` file.
2. Confirm JSON lines are parsed correctly.
3. Confirm CSV file is created with expected filename.
4. Confirm every valid frame produces one CSV row.
5. Confirm bad JSON lines do not crash the program.
6. Connect real Radar UART through USB-UART adaptor.
7. Confirm live curve updates about every 50 ms per frame.
8. Stop recording and confirm CSV and raw log are closed safely.

## Future Enhancements

| Enhancement | Benefit |
|---|---|
| Auto-detect COM ports | Easier setup |
| Replay mode from raw `.log` | Debug without hardware |
| Record session summary | Easier validation |
| Drop-frame detection by `fn` gap | Detect UART/data loss |
| Config file | Remember COM port and display settings |
| Same browser-style viewer export | Share recorded dataset easily |
