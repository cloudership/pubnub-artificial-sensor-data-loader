# PubNub Artificial Sensor Data Loader

## Summary

Loads the artificial sensor data from PubNub into S3-compatible buckets.

Creates JSON files containing about 10 seconds worth of data.

Once started, runs continuously until terminated.

## Instructions

Set up a venv or however you want to play it (you're a Python developer, figure it out).

Copy .env.example to .env and customize, then run:

```shell
python src/cloudership/pubnub_sensors/runner.py
```
