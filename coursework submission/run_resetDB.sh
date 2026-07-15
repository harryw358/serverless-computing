#!/bin/zsh

python DeleteDB.py
python CreateDB.py
python EnableSQLTracking.py

echo "--- Database has been reset to initial state ---"