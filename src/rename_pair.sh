#!/bin/bash

# 功能：奇数.mp3文件名改名为奇数&偶数.mp3
# 作者：hanjackcom
# 个人主页：https://hanjack.com

for ((n=1; n<=143; n+=2)); do
    src=$(printf "%03d.mp3" "$n")
    next=$((n + 1))
    dst=$(printf "%03d&%03d.mp3" "$n" "$next")

    if [ -f "$src" ]; then
        mv -v -- "$src" "$dst"
    else
        echo "跳过：$src 不存在"
    fi
done

echo "重命名完成"