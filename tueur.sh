#!/bin/bash

# Find the process ID (PID) using the port
PID=$(lsof -ti :16001)

if [ -z "$PID" ]; then
  echo "No process found using port 16001."
else
  # Kill the process
  echo "Killing process with ID: $PID"
  kill -9 $PID
fi
