import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import sys
import tkinter as tk
from tkinter import filedialog

class NotebookLMWatermarkRemover:
    """NotebookLM PDF幻灯片水印移除工具（图形化选文件+支持中文路径）"""
    def __init__(self):
        # 核心参数
        self.inpaint_radius = 1.0
        self.kernel = np.ones((1, 1), np.uint8)
        
        # 鼠标操作状态
        self.drawing = False
        self.x1, self.y1 = -1, -1
        self.x2, self.y2 = -1, -1
        self.img_original = None
        self.img_display = None
        self.window_main = "NotebookLM水印移除工具"
        self.window_result = "去水印结果"
        self.input_path = ""

    def _cv_imread(self, path):
        """解决OpenCV读取中文路径问题"""
        try:
            img_pil = Image.open(path).convert('RGB')
            img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            return img_cv
        except Exception as e:
            print(f"❌ 读取图片失败：{e}")
            return None

    def _cv_imwrite(self, path, img):
        """解决OpenCV保存中文路径问题"""
        try:
            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            img_pil.save(path)
            return True
        except Exception as e:
            print(f"❌ 保存图片失败：{e}")
            return False

    def _get_output_path(self):
        """自动生成原路径输出"""
        if not self.input_path:
            return "output_no_watermark.png"
        
        dir_name = os.path.dirname(self.input_path)
        file_name = os.path.basename(self.input_path)
        name, ext = os.path.splitext(file_name)
        output_file = f"{name}_no_watermark{ext}"
        output_path = os.path.join(dir_name, output_file)
        return output_path

    def _mouse_callback(self, event, x, y, flags, param):
        """鼠标拖动框选水印"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.x1, self.y1 = x, y
            self.img_display = self.img_original.copy()
        
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            img_temp = self.img_display.copy()
            cv2.rectangle(img_temp, (self.x1, self.y1), (x, y), (0, 255, 0), 2)
            cv2.imshow(self.window_main, img_temp)
        
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.x2, self.y2 = x, y
            cv2.rectangle(self.img_display, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 0), 2)
            cv2.imshow(self.window_main, self.img_display)
            print(f"\n✅ 框选完成，坐标：")
            print(f"   左上角：({self.x1}, {self.y1})  右下角：({self.x2}, {self.y2})")

    def _remove_watermark_core(self):
        """核心去水印逻辑"""
        if self.img_original is None:
            print("❌ 错误：未加载图片！")
            return None
        
        mask = np.zeros(self.img_original.shape[:2], np.uint8)
        if self.x1 == -1 or self.y1 == -1:
            return mask
        
        x1 = min(self.x1, self.x2)
        y1 = min(self.y1, self.y2)
        x2 = max(self.x1, self.x2)
        y2 = max(self.y1, self.y2)
        
        mask[y1:y2, x1:x2] = 255
        mask = cv2.erode(mask, self.kernel, iterations=1)
        
        result = cv2.inpaint(self.img_original, mask, self.inpaint_radius, cv2.INPAINT_TELEA)
        mask_3ch = cv2.merge([mask, mask, mask]) / 255.0
        result = (self.img_original * (1 - mask_3ch) + result * mask_3ch).astype(np.uint8)
        
        return result

    def _select_image_file(self):
        """图形化选择图片文件（无需命令行输入）"""
        # 创建隐藏的Tk窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        root.attributes('-topmost', True)  # 对话框置顶
        
        # 打开文件选择对话框（支持中文路径）
        file_path = filedialog.askopenfilename(
            title="选择需要去水印的图片",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("所有文件", "*.*")
            ]
        )
        
        root.destroy()  # 销毁Tk窗口
        return file_path

    def run(self):
        """主运行函数（图形化选文件）"""
        # 1. 图形化选择图片
        print("📌 请在弹出的对话框中选择需要去水印的图片...")
        self.input_path = self._select_image_file()
        
        if not self.input_path:
            print("❌ 未选择任何图片，程序退出！")
            return
        
        self.input_path = os.path.normpath(self.input_path)
        print(f"✅ 已选择图片：{self.input_path}")
        
        # 2. 加载图片（支持中文路径）
        self.img_original = self._cv_imread(self.input_path)
        if self.img_original is None:
            print("❌ 无法读取所选图片，请检查文件格式！")
            return
        
        self.img_display = self.img_original.copy()
        print(f"   图片尺寸：{self.img_original.shape[1]} × {self.img_original.shape[0]}")
        print(f"   输出路径：{self._get_output_path()}")
        
        # 3. 创建窗口+绑定鼠标事件
        cv2.namedWindow(self.window_main, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_main, 800, 600)
        cv2.setMouseCallback(self.window_main, self._mouse_callback)
        
        # 4. 操作提示
        print("\n=== 📌 操作指南 ===")
        print("1. 按住鼠标左键 → 拖动框选水印区域 → 松开完成框选")
        print("2. 按 'r' 键：重置框选（重新选择水印）")
        print("3. 按 's' 键：移除水印并保存结果（原路径输出）")
        print("4. 按 'q' 键：退出程序")
        print("=== 📌 NotebookLM幻灯片预设坐标 ===")
        print("   1280×720分辨率：左上角(1100,680) → 右下角(1270,715)")
        print("   1920×1080分辨率：左上角(1650,1020) → 右下角(1900,1070)")

        # 5. 主循环
        while True:
            cv2.imshow(self.window_main, self.img_display)
            key = cv2.waitKey(1) & 0xFF
            
            # 重置框选
            if key == ord('r'):
                self.img_display = self.img_original.copy()
                self.x1, self.y1 = -1, -1
                self.x2, self.y2 = -1, -1
                print("\n🔄 已重置框选，请重新选择水印区域")
            
            # 移除水印+保存
            elif key == ord('s'):
                result = self._remove_watermark_core()
                if result is not None:
                    output_path = self._get_output_path()
                    if self._cv_imwrite(output_path, result):
                        cv2.namedWindow(self.window_result, cv2.WINDOW_NORMAL)
                        cv2.resizeWindow(self.window_result, 800, 600)
                        cv2.imshow(self.window_result, result)
                        print(f"\n✅ 去水印完成！")
                        print(f"   结果已保存到：{os.path.abspath(output_path)}")
                    else:
                        print(f"\n❌ 保存失败：{output_path}")
            
            # 退出程序
            elif key == ord('q'):
                print("\n👋 程序已退出")
                break

        # 清理窗口
        cv2.destroyAllWindows()

# ===================== 运行入口 =====================
if __name__ == "__main__":
    # 无需任何配置，直接运行即可
    remover = NotebookLMWatermarkRemover()
    remover.run()