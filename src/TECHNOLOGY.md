# TECHNOLOGY

### 拼接文件

```code=shell
printf "file '%s'\n" *.mp3 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c:a libmp3lame -b:a 128k ../y1.mp3
```

### 去除片头片尾

```code=shell
python3 remove_bell_intro.py
```