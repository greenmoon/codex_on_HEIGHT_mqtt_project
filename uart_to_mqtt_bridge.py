"""Read radar UART from COM5, derive height_cm, and publish native MQTT TCP.

Payload example on topic height_cm:
{"fn":123,"height_cm":182.3,"timetag":"2026.06.29 16:48:30.123"}
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from typing import Any

import serial
import paho.mqtt.client as mqtt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Radar UART to native MQTT height publisher")
    parser.add_argument("--port", default="COM5", help="Radar UART COM port, default COM5")
    parser.add_argument("--baud", type=int, default=921600, help="UART baud rate, default 921600")
    parser.add_argument("--mqtt-host", default="59.124.7.96", help="Native MQTT broker host/IP")
    parser.add_argument("--mqtt-port", type=int, default=1883, help="Native MQTT TCP port")
    parser.add_argument("--topic", default="height_cm", help="MQTT topic for JSON payload")
    parser.add_argument("--sensor-height-m", type=float, default=2.4, help="Height formula base in meters")
    parser.add_argument("--cali-cm", type=float, default=0.0, help="Calibration offset in centimeters")
    parser.add_argument("--min-valid-cm", type=float, default=60.0, help="Minimum valid height in cm")
    parser.add_argument("--max-valid-cm", type=float, default=210.0, help="Maximum valid height in cm")
    parser.add_argument("--publish-period-ms", type=int, default=200, help="Minimum publish interval")
    parser.add_argument("--username", default="", help="Optional MQTT username")
    parser.add_argument("--password", default="", help="Optional MQTT password")
    return parser.parse_args()


def timetag() -> str:
    return datetime.now().strftime("%Y.%m.%d %H:%M:%S.%f")[:-3]


def number_or_none(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if number == number else None


def derive_height_cm(record: dict[str, Any], sensor_height_m: float, cali_cm: float) -> float | None:
    r0 = number_or_none(record.get("r0"))
    if r0 is None:
        return None
    return (sensor_height_m - r0) * 100.0 + cali_cm


def connect_mqtt(args: argparse.Namespace) -> mqtt.Client:
    callback_api = getattr(mqtt, "CallbackAPIVersion", None)
    if callback_api is not None:
        client = mqtt.Client(callback_api.VERSION2)
    else:
        client = mqtt.Client()
    if args.username:
        client.username_pw_set(args.username, args.password)
    client.connect(args.mqtt_host, args.mqtt_port, keepalive=60)
    client.loop_start()
    return client


def main() -> int:
    args = parse_args()
    min_publish_gap_s = max(0.0, args.publish_period_ms / 1000.0)
    last_publish_s = 0.0

    print(f"Opening UART {args.port} @ {args.baud}")
    print(f"Publishing native MQTT TCP {args.mqtt_host}:{args.mqtt_port}, topic {args.topic}")

    try:
        mqtt_client = connect_mqtt(args)
    except Exception as err:
        print(f"MQTT connect failed: {err}", file=sys.stderr)
        return 2

    try:
        with serial.Serial(args.port, args.baud, timeout=1) as uart:
            while True:
                raw = uart.readline()
                if not raw:
                    continue
                line = raw.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                height_cm = derive_height_cm(record, args.sensor_height_m, args.cali_cm)
                if height_cm is None or height_cm <= args.min_valid_cm or height_cm >= args.max_valid_cm:
                    continue

                now_s = time.monotonic()
                if now_s - last_publish_s < min_publish_gap_s:
                    continue
                last_publish_s = now_s

                fn = record.get("fn")
                payload = {
                    "fn": int(fn) if isinstance(fn, (int, float)) else fn,
                    "height_cm": round(height_cm, 1),
                    "timetag": timetag(),
                }
                payload_text = json.dumps(payload, separators=(",", ":"))
                mqtt_client.publish(args.topic, payload_text, qos=0, retain=False)
                print(f"{args.topic} {payload_text}")
    except KeyboardInterrupt:
        print("Stopping.")
    except Exception as err:
        print(f"Bridge failed: {err}", file=sys.stderr)
        return 1
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
