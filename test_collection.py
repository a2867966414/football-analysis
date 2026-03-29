
import sys
import io

# 重定向输入
sys.stdin = io.StringIO('y\n')

# 导入并运行收集脚本
exec(open('collect_historical_data.py').read())
