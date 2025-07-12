import os
import subprocess
import sys
from pathlib import Path
import json
import time

class YouTubeMP3Downloader:
    def __init__(self, output_dir="downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 检查必要的工具
        self.check_dependencies()
    
    def check_dependencies(self):
        """检查必要的依赖工具"""
        try:
            # 检查 yt-dlp
            subprocess.run(["yt-dlp", "--version"], 
                         capture_output=True, check=True)
            print("✓ yt-dlp 已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ 需要安装 yt-dlp")
            print("安装命令: pip install yt-dlp")
            sys.exit(1)
        
        try:
            # 检查 ffmpeg
            subprocess.run(["ffmpeg", "-version"], 
                         capture_output=True, check=True)
            print("✓ ffmpeg 已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ 需要安装 ffmpeg")
            print("macOS安装命令: brew install ffmpeg")
            print("或访问: https://ffmpeg.org/download.html")
            sys.exit(1)
    
    def search_and_get_url(self, query):
        """搜索并获取YouTube视频URL"""
        try:
            # 使用 yt-dlp 搜索
            cmd = [
                "yt-dlp",
                "--dump-json",
                "--playlist-end", "1",  # 只获取第一个结果
                f"ytsearch:{query}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                video_info = json.loads(result.stdout.strip().split('\n')[0])
                return {
                    'url': video_info['webpage_url'],
                    'title': video_info['title'],
                    'duration': video_info.get('duration', 0)
                }
            return None
            
        except Exception as e:
            print(f"搜索失败: {e}")
            return None
    
    def download_audio(self, video_url, output_filename):
        """下载视频并提取音频为MP3"""
        try:
            output_path = self.output_dir / f"{output_filename}.%(ext)s"
            
            cmd = [
                "yt-dlp",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "192K",  # 高质量音频
                "--output", str(output_path),
                "--no-playlist",
                video_url
            ]
            
            print(f"正在下载: {video_url}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ 下载完成: {output_filename}.mp3")
                return True
            else:
                print(f"❌ 下载失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"下载过程出错: {e}")
            return False
    
    def download_song(self, song_name):
        """搜索并下载单首歌曲"""
        print(f"\n正在搜索: {song_name}")
        
        # 搜索视频
        video_info = self.search_and_get_url(song_name)
        if not video_info:
            print(f"❌ 未找到: {song_name}")
            return False
        
        print(f"找到视频: {video_info['title']}")
        if video_info['duration']:
            duration_min = video_info['duration'] // 60
            duration_sec = video_info['duration'] % 60
            print(f"时长: {duration_min}:{duration_sec:02d}")
        
        # 清理文件名
        safe_filename = self.sanitize_filename(song_name)
        
        # 下载音频
        success = self.download_audio(video_info['url'], safe_filename)
        return success
    
    def sanitize_filename(self, filename):
        """清理文件名，移除不安全字符"""
        import re
        # 移除或替换不安全的字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip('. ')
        return filename[:100]  # 限制长度
    
    def batch_download(self, song_list):
        """批量下载歌曲"""
        successful = []
        failed = []
        
        print(f"开始批量下载 {len(song_list)} 首歌曲...")
        print(f"输出目录: {self.output_dir.absolute()}")
        
        for i, song in enumerate(song_list, 1):
            print(f"\n[{i}/{len(song_list)}] {song}")
            print("-" * 50)
            
            if self.download_song(song):
                successful.append(song)
            else:
                failed.append(song)
            
            # 添加延迟避免请求过于频繁
            if i < len(song_list):
                print("等待2秒...")
                time.sleep(2)
        
        # 输出结果统计
        print(f"\n{'='*50}")
        print(f"下载完成!")
        print(f"成功: {len(successful)} 首")
        print(f"失败: {len(failed)} 首")
        
        if successful:
            print(f"\n✓ 成功下载的歌曲:")
            for song in successful:
                print(f"  - {song}")
        
        if failed:
            print(f"\n❌ 失败的歌曲:")
            for song in failed:
                print(f"  - {song}")
        
        print(f"\n文件保存在: {self.output_dir.absolute()}")

def main():
    # 要下载的歌曲列表
    songs = [
        "极乐净土",
        "恋爱循环", 
        "心做L",
        "my all",
        "祈愿~致那个时候的你~",
        "青鸟",
        "绊",
        "曾经我也想过一了百了",
        "骑在银龙的背上",
        "留在我身边",
        "secret base"
    ]
    
    try:
        downloader = YouTubeMP3Downloader()
        downloader.batch_download(songs)
    except KeyboardInterrupt:
        print("\n用户中断下载")
    except Exception as e:
        print(f"程序出错: {e}")

if __name__ == "__main__":
    main()