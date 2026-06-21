#!/bin/bash

# 功能：设置MP3文件的metadata数据
# 作者：hanjackcom
# 个人主页：https://hanjack.com

# sudo apt install id3v2
# sudo apt install python3-mutagen

find . -maxdepth 1 -type f -iname "*.mp3" -print0 | while IFS= read -r -d '' f; do
    base="$(basename $f)"
    echo $base

    if [ -e "../$base" ]; then
        TRCK="$(mid3v2 --list ../$base | grep TRCK | sed 's/TRCK=//g')"
        TIT2="$(mid3v2 --list ../$base | grep TIT2 | sed 's/TIT2=//g')"
        echo "TRCK: $TRCK, TIT2: $TIT2"

        mid3v2 --TIT2 "$TIT2" --TPE1 "hanjack.com" --TPE2 "hanjack.com" --TALB "新概念英语第一册美音" --TRCK "$TRCK" "$f"
    else
        echo "[ERROR] File ../$base not found, skipping."
        continue
    fi
    
done

# mid3v2 --TIT2 "新概念英语第一册单文件美音" --TPE1 "hanjack.com" --TPE2 "hanjack.com" --TALB "新概念英语第一册美音" --TRCK "999" "m1-fixed.mp3"

# find . -maxdepth 1 -type f -iname "*.mp3" | while read line; do mid3v2 --TPE1 "hanjack.com" --TPE2 "hanjack.com" "$line"; done
