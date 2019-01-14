#!/bin/bash

LOG=$1
DATE_BEGIN=$(grep 'Date is now' "$LOG" | awk -F': ' '{print $2}')
DATE_PREPROCESSED=$(grep -i shuffle "$LOG" | tail -1 | awk -F': ' '{print $1}')
TRAIN_TIME=$(grep 'Training took' "$LOG" | awk '{print $4}')

TIMESTAMP_BEGIN=$(date -d "$DATE_BEGIN" +%s)
TIMESTAMP_PREPROCESSED=$(date -d "$DATE_PREPROCESSED" +%s)

PREPROCESS_TIME=$(echo $TIMESTAMP_PREPROCESSED - $TIMESTAMP_BEGIN | bc -l)
WORK_TIME=$(echo $TRAIN_TIME - $PREPROCESS_TIME | bc -l)

LC_ALL=C printf "%.2f %.2f %.2f\n" $TRAIN_TIME $PREPROCESS_TIME $WORK_TIME
