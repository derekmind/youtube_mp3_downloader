# YouTube MP3 Downloader

一个简单易用的YouTube音频下载工具，可以搜索并下载YouTube视频的音频部分为MP3格式。

## 功能特性

- 🎵 **智能搜索**: 通过歌曲名称自动搜索YouTube视频
- 📥 **高质量下载**: 支持192K高质量MP3音频提取
- 📦 **批量下载**: 支持批量下载多首歌曲
- 🛡️ **安全文件名**: 自动处理特殊字符，确保文件名安全
- ⏱️ **智能延迟**: 自动添加请求间隔，避免被限制
- 📊 **下载统计**: 显示详细的下载成功/失败统计

## 系统要求

- Python 3.6+
- yt-dlp
- ffmpeg

## 安装依赖

### 1. 安装 yt-dlp
```bash
pip install yt-dlp

brew install ffmpeg
```

## 使用方法
### 基本使用
1. 克隆或下载项目文件
2. 运行程序：
```bash
python youtube_mp3_downloader.py
```
### 自定义歌曲列表
编辑 youtube_mp3_downloader.py 文件中的 songs 列表：
```python
songs = [
    "歌曲1 - 歌手1",
    "歌曲2 - 歌手2",
    # 添加更多歌曲...
]
```
### 批量下载
运行程序后，根据提示输入歌曲数量和列表序号，即可批量下载指定歌曲。

### 项目结构
```plaintext
youtube_mp3_downloader/
├── youtube_mp3_downloader.py  # 主程序文件
├── downloads/                 # 默认下载目录
│   ├── 极乐净土.mp3
│   ├── 恋爱循环.mp3
│   └── ...
└── README.md                 # 项目说明文档
```

## 配置选项
- 输出目录 : 默认为 downloads/ ，可在初始化时自定义
- 音频质量 : 默认为 192K，可在代码中修改
- 请求延迟 : 默认2秒间隔，可在 batch_download 方法中调整

## 注意事项
1. 版权声明 : 请确保下载的内容符合当地法律法规和版权要求
2. 网络连接 : 需要稳定的网络连接访问YouTube
3. 文件命名 : 程序会自动处理特殊字符，确保文件名兼容性
bluceqiu

复制

删除

帮我生成一个readme

Trae

我需要先查看项目的代码文件来了解这个YouTube MP3下载器的功能和特性，然后生成一个合适的README文档。

youtube_mp3_downloader.py

我已经分析了你的YouTube MP3下载器项目，现在为你生成一个完整的README文档：

```
# YouTube MP3 Downloader

一个简单易用的YouTube音频下载工具，可以搜索并下载YouTube视频的音频部分为MP3格式。

## 功能特性

- 🎵 **智能搜索**: 通过歌曲名称自动搜索YouTube视频
- 📥 **高质量下载**: 支持192K高质量MP3音频提取
- 📦 **批量下载**: 支持批量下载多首歌曲
- 🛡️ **安全文件名**: 自动处理特殊字符，确保文件名安全
- ⏱️ **智能延迟**: 自动添加请求间隔，避免被限制
- 📊 **下载统计**: 显示详细的下载成功/失败统计

## 系统要求

- Python 3.6+
- yt-dlp
- ffmpeg

## 安装依赖

### 1. 安装 yt-dlp
```bash
pip install yt-dlp
```
### 2. 安装 ffmpeg
macOS (使用 Homebrew):

```
brew install ffmpeg
```
Windows:

- 访问 FFmpeg官网 下载
- 或使用 chocolatey: choco install ffmpeg
Linux (Ubuntu/Debian):

```
sudo apt update
sudo apt install ffmpeg
```
## 使用方法
### 基本使用
1. 克隆或下载项目文件
2. 运行程序：
```
python youtube_mp3_downloader.py
```
### 自定义歌曲列表
编辑 youtube_mp3_downloader.py 文件中的 songs 列表：

```
songs = [
    "你想下载的歌曲名称1",
    "你想下载的歌曲名称2",
    "你想下载的歌曲名称3",
    # 添加更多歌曲...
]
```
### 编程接口使用
```
from youtube_mp3_downloader import YouTubeMP3Downloader

# 创建下载器实例
downloader = YouTubeMP3Downloader(output_dir="my_music")

# 下载单首歌曲
downloader.download_song("歌曲名称")

# 批量下载
song_list = ["歌曲1", "歌曲2", "歌曲3"]
downloader.batch_download(song_list)
```
## 项目结构
```
youtube_mp3_downloader/
├── youtube_mp3_downloader.py  # 主程序文件
├── downloads/                 # 默认下载目录
│   ├── 极乐净土.mp3
│   ├── 恋爱循环.mp3
│   └── ...
└── README.md                 # 项目说明文档
```
## 使用示例
### 示例1：简单批量下载
python youtube_mp3_downloader.py -s "极乐净土" "恋爱循环" "心做L"

### 示例2：在Python项目中使用
from youtube_mp3_downloader import download_songs

playlist = [
    "曾经我也想过一了百了",
    "骑在银龙的背上",
    "留在我身边"
]

result = download_songs(playlist, output_dir="./music", delay=3)
print(f"下载完成！成功: {len(result['successful'])}首，失败: {len(result['failed'])}首")

## 主要类和方法
### YouTubeMP3Downloader 类
- __init__(output_dir="downloads") : 初始化下载器
- download_song(song_name) : 下载单首歌曲
- batch_download(song_list) : 批量下载歌曲列表
- search_and_get_url(query) : 搜索YouTube视频
- download_audio(video_url, output_filename) : 下载并转换音频
## 配置选项
- 输出目录 : 默认为 downloads/ ，可在初始化时自定义
- 音频质量 : 默认为 192K，可在代码中修改
- 请求延迟 : 默认2秒间隔，可在 batch_download 方法中调整
## 注意事项
1. 版权声明 : 请确保下载的内容符合当地法律法规和版权要求
2. 网络连接 : 需要稳定的网络连接访问YouTube
3. 文件命名 : 程序会自动处理特殊字符，确保文件名兼容性
4. 下载限制 : 建议适度使用，避免频繁请求被限制
## 故障排除
### 常见问题
Q: 提示 "需要安装 yt-dlp" A: 运行 pip install yt-dlp 安装依赖

Q: 提示 "需要安装 ffmpeg" A: 根据你的操作系统安装 ffmpeg（见上方安装说明）

Q: 下载失败或找不到视频 A: 检查网络连接，尝试更具体的搜索关键词

Q: 文件名包含特殊字符 A: 程序会自动清理文件名，移除不安全字符

## 许可证
本项目仅供学习和个人使用。请遵守相关法律法规和平台服务条款。

## 贡献
欢迎提交 Issue 和 Pull Request 来改进这个项目！

免责声明 : 本工具仅用于个人学习和研究目的。用户需自行承担使用责任，确保遵守相关法律法规和版权要求。