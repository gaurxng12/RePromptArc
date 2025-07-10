#!/bin/bash

# 🔧 Configuration
TIMEOUT_EXEC="$(which timeout)"
PYTHON_EXEC="$(which python)"
MPROF_EXEC="$(which mprof)"

# 📥 Input arguments
completion_file="$1"         # full path to .py file
completion_dat_file="$2"     # full path to .dat output file
max_execution_time="$3"      # in seconds

# 🧾 Show input info
echo "🔍 Python Script: $completion_file"
echo "📤 Data Output: $completion_dat_file"
echo "⏱️ Max Execution Time: ${max_execution_time}s"
echo "🐍 Python Exec: $PYTHON_EXEC"
echo "📈 mprof Exec: $MPROF_EXEC"

# 🚫 Check if input script exists
if [ ! -f "$completion_file" ]; then
    echo "❌ ERROR: Python script $completion_file does not exist!"
    exit 1
fi

# 🚫 Check if Python and mprof are available
if [ ! -f "$PYTHON_EXEC" ]; then
    echo "❌ ERROR: Python not found at $PYTHON_EXEC"
    exit 127
fi

if [ ! -f "$MPROF_EXEC" ]; then
    echo "❌ ERROR: mprof not found at $MPROF_EXEC"
    exit 127
fi

# 🧹 Clean previous dat file
rm -f "$completion_dat_file"

# 🚀 Start profiling
echo "⏳ Starting memory profiling..."
"$MPROF_EXEC" run --interval 0.0001 --output "$completion_dat_file" --include-children "$PYTHON_EXEC" "$completion_file" &

MPROF_PID=$!

# Wait for the allowed execution time
sleep "$max_execution_time"

# Kill the mprof process
kill $MPROF_PID 2>/dev/null
wait $MPROF_PID 2>/dev/null

# ✅ Confirm output
if [ ! -f "$completion_dat_file" ]; then
    echo "❌ ERROR: $completion_dat_file was not created!"
    exit 1
else
    echo "✅ SUCCESS: $completion_dat_file created!"
fi

echo "🏁 Profiling completed."
exit 0
