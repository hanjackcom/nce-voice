#!/bin/bash

# 功能：批量重命名mp3，取文件名前3字符
# 作者：hanjackcom
# 个人主页：https://hanjack.com

find . -maxdepth 1 -type f -iname "*.mp3" -print0 | while IFS= read -r -d '' file; do
    filename="${file##*/}"
    head3="${filename:0:3}"
    mv -v -- "$file" "./${head3}.mp3"
done
echo "重命名完成"