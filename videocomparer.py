import cv2 as cv
import numpy as np
import argparse

class VideoComparer:
    def __init__(self, video1_path, video2_path):
        """初始化视频对比器"""
        self.cap1 = cv.VideoCapture(video1_path)
        self.cap2 = cv.VideoCapture(video2_path)
        
        # 获取视频信息
        self.total_frames = min(int(self.cap1.get(cv.CAP_PROP_FRAME_COUNT)),
                              int(self.cap2.get(cv.CAP_PROP_FRAME_COUNT)))
        self.fps1 = self.cap1.get(cv.CAP_PROP_FPS)
        self.fps2 = self.cap2.get(cv.CAP_PROP_FPS)
        
        # 设置窗口
        self.window_name = "Video Comparison"
        cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)
        
        # 创建进度条
        cv.createTrackbar('Frame', self.window_name, 0, self.total_frames-1, self.on_trackbar)
        
        # 播放状态
        self.current_frame = 0
        self.is_playing = True
        self.step = 1  # 1为正向播放，-1为反向播放
        
        # 调整窗口大小
        self.window_width = 2560
        self.window_height = 720
        cv.resizeWindow(self.window_name, self.window_width, self.window_height)

    def on_trackbar(self, value):
        """进度条回调函数"""
        self.current_frame = value
        self.cap1.set(cv.CAP_PROP_POS_FRAMES, value)
        self.cap2.set(cv.CAP_PROP_POS_FRAMES, value)

    def read_and_resize(self, cap):
        """读取并调整图像大小"""
        ret, frame = cap.read()
        if ret:
            # 计算缩放比例
            scale = min(self.window_width/2 / frame.shape[1], 
                       self.window_height / frame.shape[0])
            width = int(frame.shape[1] * scale)
            height = int(frame.shape[0] * scale)
            frame = cv.resize(frame, (width, height))
        return ret, frame

    def run(self):
        """运行视频对比器"""
        print("\n控制说明:")
        print("Space: 暂停/继续")
        print("←/→: 前一帧/后一帧")
        print("A/D: 反向播放/正向播放")
        print("数字键1-9: 跳转到视频的相应位置(10%-90%)")
        print("Q: 退出\n")
        
        while True:
            if self.current_frame >= self.total_frames or self.current_frame < 0:
                self.current_frame = 0
                self.cap1.set(cv.CAP_PROP_POS_FRAMES, 0)
                self.cap2.set(cv.CAP_PROP_POS_FRAMES, 0)

            # 读取两个视频的当前帧
            ret1, frame1 = self.read_and_resize(self.cap1)
            ret2, frame2 = self.read_and_resize(self.cap2)

            if ret1 and ret2:
                # 添加帧信息
                frame_info = f"Frame: {self.current_frame}/{self.total_frames}"
                for frame in [frame1, frame2]:
                    cv.putText(frame, frame_info, (10, 30), 
                             cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                # 合并两个画面
                combined = np.hstack((frame1, frame2))
                cv.imshow(self.window_name, combined)
                
                # 更新进度条
                cv.setTrackbarPos('Frame', self.window_name, self.current_frame)
            else:
                break

            # 处理按键事件
            key = cv.waitKey(0 if not self.is_playing else 30) & 0xFF
            
            if key == ord('q'):  # 退出
                break
            elif key == ord(' '):  # 暂停/继续
                self.is_playing = not self.is_playing
            elif key == ord('a'):  # 反向播放
                self.step = -1
                self.is_playing = True
            elif key == ord('d'):  # 正向播放
                self.step = 1
                self.is_playing = True
            elif key == 81:  # 左方向键，上一帧
                self.current_frame = max(0, self.current_frame - 1)
                self.cap1.set(cv.CAP_PROP_POS_FRAMES, self.current_frame)
                self.cap2.set(cv.CAP_PROP_POS_FRAMES, self.current_frame)
            elif key == 83:  # 右方向键，下一帧
                self.current_frame = min(self.total_frames - 1, self.current_frame + 1)
                self.cap1.set(cv.CAP_PROP_POS_FRAMES, self.current_frame)
                self.cap2.set(cv.CAP_PROP_POS_FRAMES, self.current_frame)
            elif ord('1') <= key <= ord('9'):  # 跳转到指定位置
                pos = (key - ord('0')) * 0.1
                target_frame = int(self.total_frames * pos)
                self.current_frame = target_frame
                self.cap1.set(cv.CAP_PROP_POS_FRAMES, target_frame)
                self.cap2.set(cv.CAP_PROP_POS_FRAMES, target_frame)
            
            # 如果正在播放，更新帧
            if self.is_playing:
                self.current_frame += self.step

        # 清理资源
        self.cap1.release()
        self.cap2.release()
        cv.destroyAllWindows()

def parse_args():
    parser = argparse.ArgumentParser(description="视频对比播放工具")
    parser.add_argument("--video1", "-v1", type=str, required=True,
                      help="第一个视频文件路径")
    parser.add_argument("--video2", "-v2", type=str, required=True,
                      help="第二个视频文件路径")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    comparer = VideoComparer(args.video1, args.video2)
    comparer.run()