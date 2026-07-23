"""
GIF处理脚本 - 提取第一帧作为PNG预览图
"""
import os
from PIL import Image

def extract_first_frame(input_path, output_path):
    """
    提取GIF第一帧作为PNG图片
    
    Args:
        input_path: 输入GIF路径
        output_path: 输出PNG路径
    """
    print(f"正在读取GIF: {input_path}")
    
    # 打开GIF文件
    gif = Image.open(input_path)
    
    # 获取第一帧
    first_frame = gif.convert('RGB')
    
    # 调整大小以减小文件
    max_dimension = 1200
    width, height = first_frame.size
    if width > max_dimension or height > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int(height * max_dimension / width)
        else:
            new_height = max_dimension
            new_width = int(width * max_dimension / height)
        first_frame = first_frame.resize((new_width, new_height), Image.LANCZOS)
    
    # 保存为PNG
    first_frame.save(output_path, format='PNG', optimize=True, quality=90)
    
    file_size = os.path.getsize(output_path)
    print(f"\n✅ 处理成功!")
    print(f"输出文件: {output_path}")
    print(f"文件大小: {file_size/1024/1024:.2f}MB")
    print(f"图片尺寸: {new_width}x{new_height}")

if __name__ == "__main__":
    input_gif = r"d:\Trae CN\program\daily_market_tracking\0715邮件推送.gif"
    output_png = r"d:\Trae CN\program\daily_market_tracking\assets\email_preview.png"
    
    # 创建输出目录
    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    
    extract_first_frame(input_gif, output_png)