#!/bin/bash

svn_root=$1
file_path=$2
line_number=$3

# 检查目录是否是SVN根目录
if ! [ -d "$svn_root/.svn" ]; then
    echo "目录不是SVN根目录"
    exit 1
fi

# 检查文件是否存在
if ! [ -f "$file_path" ]; then
    echo "文件不存在或不是当前SVN目录中的文件"
    exit 1
fi

# 检查行数是否是数字
if ! [[ $line_number =~ ^[0-9]+$ ]]; then
    echo "行数不是数字"
    exit 1
fi

# 获取文件总行数
total_lines=$(wc -l < "$file_path")

# 检查行数是否大于文件总行数
if [ "$line_number" -gt "$total_lines" ]; then
    echo "行数大于文件的行数"
    exit 1
fi

# 获取指定行的提交记录
blame_output=$(svn blame "$file_path")

# 获取指定行的提交记录、修改内容、修改时间和提交人
line_info=$(echo "$blame_output" | sed -n "${line_number}p")

# 提取修订版本号和提交人
revision=$(echo "$line_info" | awk '{ print $1 }')
author=$(echo "$line_info" | awk '{ print $2 }')

# 获取修订版本的提交记录
log_output=$(svn log -v -r "$revision" "$svn_root")

# 提取修改内容和修改时间
modifications=$(echo "$log_output" | awk '/^-/{flag=1; next} flag{print}')

# 显示结果
echo "提交记录信息:"
echo "修订版本号: $revision"
echo "提交人: $author"
echo "修改内容和修改时间:"
echo "$modifications"