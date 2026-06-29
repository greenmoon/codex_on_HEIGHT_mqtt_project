@echo off
cd /d "%~dp0"
REM Edit MQTT_HOST to your native MQTT broker IP if needed.
set "MQTT_HOST=59.124.7.96"
set "MQTT_PORT=1883"
set "MQTT_TOPIC=height_cm"
python uart_to_mqtt_bridge.py --port COM5 --baud 921600 --mqtt-host "%MQTT_HOST%" --mqtt-port %MQTT_PORT% --topic "%MQTT_TOPIC%"
pause
