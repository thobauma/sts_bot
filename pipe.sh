#!/bin/bash

# Pipe CommunicationMod IO to FIFOs provided by the host

INPUT=$1
OUTPUT=$2

# # Check if the named pipe exists
# if [[ ! -p "$INPUT" ]]; then
#     # echo "Creating FIFO: $INPUT"
#     mkfifo "$INPUT"
# else
#     rm "$INPUT"
#     mkfifo "$INPUT"
# fi

# # Check if the named pipe exists
# if [[ ! -p "$OUTPUT" ]]; then
#     # echo "Creating FIFO: $OUTPUT"
#     mkfifo -m 666 "$OUTPUT"
# else
#     rm "$OUTPUT"
#     # echo "FIFO already exists: $OUTPUT"
#     mkfifo -m 666 "$OUTPUT"
# fi

function cleanup() {
    kill $BG_PID
}

trap cleanup EXIT

cat $INPUT &
BG_PID=$!

# Sleep to allow time for the background process to start
sleep 0.2

cat > $OUTPUT