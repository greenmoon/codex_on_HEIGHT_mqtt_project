# A1528B eSRD Range Profile UART Recorder

Dashboard title:

`A1528B eSRD range profile V02 2026.06.25 15:08`

## Purpose

Read JSON-per-line range records from the Radar UART port through a PC USB-UART adaptor, show a real-time curve by `fn`, and save the parsed data to CSV.

## Browser Global URL Version

Open `index.html` from an HTTPS host such as GitHub Pages to read the radar UART directly in Chrome or Edge with the Web Serial API.

| Item | Behavior |
|---|---|
| UART access | The radar USB-UART adaptor must be connected to the same PC that opens the web page. |
| Browser | Chrome or Edge. Firefox/Safari do not support Web Serial. |
| URL requirement | HTTPS or localhost. A GitHub Pages URL is valid. |
| Save data | Use `Download CSV` and `Download Raw` in the page. Browsers cannot silently write to `./data`. |
| Plot colors | `r0` red, `r1` green, `r2` blue. |

## Run

```powershell
pip install -r requirements.txt
python gep_uart_recorder.py
```

## Defaults

| Item | Default |
|---|---|
| COM port | `COM5` |
| Baud rate | `921600` |
| Plot window | `300` frames |
| CSV filename | `data/jb_GEP_dataset_YYYYMMDD_HHMMSS.csv` |
| Raw log filename | `data/jb_GEP_dataset_YYYYMMDD_HHMMSS_raw.log` |

## Expected UART JSON Line

```json
{"fn": 123, "r0": 1.234, "r1": 1.567, "r2": 1.890}
```

Required:

| Field | Meaning |
|---|---|
| `fn` | Frame number |

Optional plotted fields:

| Field | Meaning |
|---|---|
| `r0` | Range channel 0 |
| `r1` | Range channel 1 |
| `r2` | Range channel 2 |

## Notes

- Use `Refresh` to update the COM port list.
- Baud rate is editable before pressing `Start`.
- The save filename is shown in green after recording starts.
- Click `Open ./data folder` to browse saved CSV and raw log files.
- CSV is flushed after each valid JSON record to reduce data loss.
- Bad JSON lines are counted and skipped, while raw text is still saved to the raw log.
## Native MQTT Bridge

For a normal MQTT TCP broker, use the local Windows Python bridge instead of browser MQTT/WebSocket.

Flow:

```text
Radar -> COM5 -> PC Python bridge -> derived height_cm -> native MQTT publish
```

Default publish format:

```text
topic: height_cm
payload: {"fn":123,"height_cm":182.3,"timetag":"2026.06.29 16:48:30.123"}
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run with defaults:

```powershell
python uart_to_mqtt_bridge.py --port COM5 --baud 921600 --mqtt-host 59.124.7.96 --mqtt-port 1883 --topic height_cm
```

Or edit `run_uart_to_mqtt_bridge.bat` and double-click it. When this bridge owns COM5, do not also click `Connect UART` in the browser page.

