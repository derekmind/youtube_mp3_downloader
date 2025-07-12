import os
import subprocess
import sys
from pathlib import Path
import json
import time
import argparse
from typing import List, Optional, Dict, Any

class YouTubeMP3Downloader:
    def __init__(self, output_dir="downloads", check_deps=True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 检查必要的工具
        if check_deps:
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
    
    def search_and_get_url(self, query: str) -> Optional[Dict[str, Any]]:
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
    
    def download_audio(self, video_url: str, output_filename: str) -> bool:
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
    
    def download_song(self, song_name: str) -> bool:
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
    
    def sanitize_filename(self, filename: str) -> str:
        """清理文件名，移除不安全字符"""
        import re
        # 移除或替换不安全的字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip('. ')
        return filename[:100]  # 限制长度
    
    def batch_download(self, song_list: List[str], delay: int = 2) -> Dict[str, List[str]]:
        """批量下载歌曲
        
        Args:
            song_list: 歌曲名称列表
            delay: 下载间隔时间（秒）
            
        Returns:
            包含成功和失败歌曲列表的字典
        """
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
            if i < len(song_list) and delay > 0:
                print(f"等待{delay}秒...")
                time.sleep(delay)
        
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
        
        return {
            'successful': successful,
            'failed': failed
        }

def download_songs(songs: List[str], output_dir: str = "downloads", delay: int = 2) -> Dict[str, List[str]]:
    """便捷函数：下载歌曲列表
    
    Args:
        songs: 歌曲名称列表
        output_dir: 输出目录
        delay: 下载间隔时间（秒）
        
    Returns:
        包含成功和失败歌曲列表的字典
    """
    downloader = YouTubeMP3Downloader(output_dir=output_dir)
    return downloader.batch_download(songs, delay=delay)

def download_single_song(song_name: str, output_dir: str = "downloads") -> bool:
    """便捷函数：下载单首歌曲
    
    Args:
        song_name: 歌曲名称
        output_dir: 输出目录
        
    Returns:
        下载是否成功
    """
    downloader = YouTubeMP3Downloader(output_dir=output_dir)
    return downloader.download_song(song_name)

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="YouTube MP3 下载器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用示例:
  python youtube_mp3_downloader.py                    # 使用默认歌曲列表
  python youtube_mp3_downloader.py -s "歌曲名1" "歌曲名2"  # 下载指定歌曲
  python youtube_mp3_downloader.py -o my_music        # 指定输出目录
  python youtube_mp3_downloader.py -d 5               # 设置下载间隔为5秒
        """
    )
    
    parser.add_argument(
        "-s", "--songs",
        nargs="+",
        help="要下载的歌曲列表"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="downloads",
        help="输出目录 (默认: downloads)"
    )
    
    parser.add_argument(
        "-d", "--delay",
        type=int,
        default=2,
        help="下载间隔时间（秒） (默认: 2)"
    )
    
    parser.add_argument(
        "--no-check-deps",
        action="store_true",
        help="跳过依赖检查"
    )
    
    return parser.parse_args()

def main(songs: Optional[List[str]] = None):
    """主函数
    
    Args:
        songs: 可选的歌曲列表，如果不提供则使用默认列表或命令行参数
    """
    # 默认歌曲列表
    default_songs = [
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
    
    # 如果直接传入了歌曲列表，使用传入的列表
    if songs is not None:
        song_list = songs
        output_dir = "downloads"
        delay = 2
        check_deps = True
    else:
        # 解析命令行参数
        args = parse_arguments()
        song_list = args.songs if args.songs else default_songs
        output_dir = args.output
        delay = args.delay
        check_deps = not args.no_check_deps
    
    try:
        downloader = YouTubeMP3Downloader(
            output_dir=output_dir, 
            check_deps=check_deps
        )
        result = downloader.batch_download(song_list, delay=delay)
        return result
    except KeyboardInterrupt:
        print("\n用户中断下载")
        return None
    except Exception as e:
        print(f"程序出错: {e}")
        return None

if __name__ == "__main__":
    main()