import tkinter as tk
from tkinter import filedialog, messagebox
import os

class UpdateProgramGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("更新程序生成器")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # 设置软件默认信息（部分可修改）
        self.default_software_name = "软件名称"
        self.copyright_info = "© 2023 xiaochenstudio. 保留所有权利"
        self.official_website = "https://xiaochenstudio.github.io"
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.root, text="更新程序生成器", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=20)
        
        # 可编辑选项
        options_frame = tk.Frame(self.root)
        options_frame.pack(fill="x", padx=50, pady=10)
        
        # 软件名称
        tk.Label(options_frame, text="软件名称:", font=("微软雅黑", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.software_name_var = tk.StringVar(value=self.default_software_name)
        tk.Entry(options_frame, textvariable=self.software_name_var, font=("微软雅黑", 10), width=25).grid(row=0, column=1, sticky="w", pady=5)
        
        # 版本号
        tk.Label(options_frame, text="版本号:", font=("微软雅黑", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.version_var = tk.StringVar(value="1.0.0")
        tk.Entry(options_frame, textvariable=self.version_var, font=("微软雅黑", 10), width=20).grid(row=1, column=1, sticky="w", pady=5)
        
        # 更新地址
        tk.Label(options_frame, text="更新地址:", font=("微软雅黑", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.update_url_var = tk.StringVar(value="https://xiaochenstudio.github.io/app/update/test.html")
        tk.Entry(options_frame, textvariable=self.update_url_var, font=("微软雅黑", 10), width=35).grid(row=2, column=1, sticky="w", pady=5)
        
        # 分隔线
        tk.Frame(self.root, height=2, bg="#cccccc").pack(fill="x", padx=50, pady=15)
        
        # 固定信息（不可编辑）
        fixed_info_frame = tk.Frame(self.root)
        fixed_info_frame.pack(fill="x", padx=50, pady=10)
        
        tk.Label(fixed_info_frame, text="版权信息:", font=("微软雅黑", 10)).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(fixed_info_frame, text=self.copyright_info, font=("微软雅黑", 10, "bold")).grid(row=0, column=1, sticky="w", pady=5)
        
        tk.Label(fixed_info_frame, text="官网链接:", font=("微软雅黑", 10)).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(fixed_info_frame, text=self.official_website, font=("微软雅黑", 10, "bold")).grid(row=1, column=1, sticky="w", pady=5)
        
        # 生成按钮
        generate_btn = tk.Button(self.root, text="生成更新程序", command=self.generate_program,
                                bg="#409eff", fg="white", font=("微软雅黑", 12, "bold"),
                                width=15, height=1)
        generate_btn.pack(pady=30)
        
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        status_label = tk.Label(self.root, textvariable=self.status_var, fg="#666666", font=("微软雅黑", 9))
        status_label.pack(side="bottom", pady=10)
    
    def generate_program(self):
        # 获取用户输入
        software_name = self.software_name_var.get().strip()
        version = self.version_var.get().strip()
        update_url = self.update_url_var.get().strip()
        
        # 验证输入
        if not software_name:
            messagebox.showerror("错误", "请输入软件名称")
            return
            
        if not version:
            messagebox.showerror("错误", "请输入版本号")
            return
            
        if not update_url:
            messagebox.showerror("错误", "请输入更新地址")
            return
            
        # 打开文件对话框选择保存位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")],
            title="保存更新程序"
        )
        
        if not file_path:
            return
            
        try:
            # 生成更新程序代码
            program_code = self._generate_code(software_name, version, update_url)
            
            # 写入文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(program_code)
                
            self.status_var.set(f"成功生成: {os.path.basename(file_path)}")
            messagebox.showinfo("成功", f"更新程序已成功生成到:\n{file_path}")
            
        except Exception as e:
            error_msg = f"生成失败: {str(e)}"
            self.status_var.set(error_msg)
            messagebox.showerror("错误", error_msg)
    
    def _generate_code(self, software_name, version, update_url):
        # 使用原始字符串(r'')处理正则表达式，避免转义问题
        regex_patterns = {
            'version': r'date:\s*([\d.]+)',
            'content': r'p:\s*([\s\S]*?)upload:',
            'download': r'upload:\s*([^\s]+)'
        }
        
        # 生成的代码模板
        code = f"""
import tkinter as tk
from tkinter import messagebox
import requests
import re
import webbrowser

# 当前版本
CURRENT_VERSION = "{version}"
# 获取更新信息的页面 URL
UPDATE_INFO_URL = "{update_url}"


class AppUpdater:
    def __init__(self, current_version, update_url):
        self.current_version = current_version
        self.update_url = update_url
        self.latest_version = None
        self.update_content = None
        self.download_url = None

    def check_updates(self):
        try:
            response = requests.get(self.update_url)
            if response.status_code == 200:
                html_text = response.text
                # 提取版本号
                version_match = re.search(r'{regex_patterns["version"]}', html_text)
                # 提取更新内容
                content_match = re.search(r'{regex_patterns["content"]}', html_text, re.IGNORECASE)
                # 提取下载链接
                url_match = re.search(r'{regex_patterns["download"]}', html_text, re.IGNORECASE)

                if version_match and content_match and url_match:
                    self.latest_version = version_match.group(1).strip()
                    self.update_content = content_match.group(1).strip()
                    self.download_url = url_match.group(1).strip()
                    # 比较版本号判断是否有更新
                    return self._is_new_version()
            return False
        except Exception as e:
            print(f"检查更新时出错: {{e}}")
            return False

    def _is_new_version(self):
        current_parts = list(map(int, self.current_version.split('.')))
        latest_parts = list(map(int, self.latest_version.split('.')))
        for c, l in zip(current_parts, latest_parts):
            if l > c:
                return True
            elif l < c:
                return False
        return False


class UpdateWindow(tk.Toplevel):
    def __init__(self, parent, updater):
        super().__init__(parent)
        self.title("软件更新")
        self.geometry("600x500")
        self.resizable(False, False)
        self.updater = updater

        # 设置窗口居中
        self.center_window()

        # 使用 grid 布局管理器
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 标题区域
        title_frame = tk.Frame(self, bg="#409eff", height=50)
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.grid_propagate(False)

        title_label = tk.Label(title_frame, text="发现新版本", bg="#409eff", fg="white",
                              font=("微软雅黑", 14, "bold"))
        title_label.pack(side="left", padx=15, pady=15)

        # 版本信息
        version_frame = tk.Frame(self, bg="#f5f5f5")
        version_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=15)

        current_label = tk.Label(version_frame, text=f"当前版本: {{CURRENT_VERSION}}", bg="#f5f5f5",
                                font=("微软雅黑", 12))
        current_label.pack(anchor="w")

        latest_label = tk.Label(version_frame, text=f"最新版本: {{updater.latest_version}}", bg="#f5f5f5",
                               font=("微软雅黑", 12, "bold"))
        latest_label.pack(anchor="w", pady=(5, 0))

        # 更新内容
        content_frame = tk.Frame(self, bg="#ffffff", relief="solid", bd=1)
        content_frame.grid(row=2, column=0, sticky="nsew", padx=25, pady=10)

        content_label = tk.Label(content_frame, text="更新内容:", bg="#ffffff",
                                font=("微软雅黑", 12, "bold"), anchor="w")
        content_label.pack(fill="x", padx=15, pady=8)

        # 使用 Text 组件并添加滚动条
        text_frame = tk.Frame(content_frame)
        text_frame.pack(fill="both", expand=True, padx=15, pady=8)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        content_text = tk.Text(text_frame, wrap="word", width=50, height=10, font=("微软雅黑", 11),
                              bd=0, yscrollcommand=scrollbar.set)
        content_text.insert("1.0", updater.update_content)
        content_text.config(state="disabled", bg="#ffffff")
        content_text.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=content_text.yview)

        # 按钮区域
        button_frame = tk.Frame(self, bg="#f5f5f5")
        button_frame.grid(row=3, column=0, sticky="ew", padx=25, pady=20)

        # 前往更新按钮
        update_btn = tk.Button(button_frame, text="前往更新", command=self.open_download,
                              bg="#409eff", fg="white", font=("微软雅黑", 12, "bold"),
                              width=20, height=2)
        update_btn.pack(side="right")

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{{width}}x{{height}}+{{x}}+{{y}}")

    def open_download(self):
        webbrowser.open(self.updater.download_url)
        self.destroy()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("{software_name}")
        self.geometry("480x400")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")

        # 设置窗口居中
        self.center_window()

        # 标题区域
        title_frame = tk.Frame(self, bg="#409eff", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="{software_name}", bg="#409eff", fg="white",
                              font=("微软雅黑", 18, "bold"))
        title_label.pack(pady=25)

        # 版本信息
        version_frame = tk.Frame(self, bg="#f5f5f5")
        version_frame.pack(fill="x", padx=30, pady=35)

        version_label = tk.Label(version_frame, text=f"当前版本: {{CURRENT_VERSION}}",
                                bg="#f5f5f5", font=("微软雅黑", 13))
        version_label.pack(anchor="w")

        # 检查更新按钮
        button_frame = tk.Frame(self, bg="#f5f5f5")
        button_frame.pack(pady=25)

        check_btn = tk.Button(button_frame, text="检查更新", command=self.check_for_update,
                             bg="#409eff", fg="white", font=("微软雅黑", 12, "bold"),
                             width=20, height=2)
        check_btn.pack(pady=10)

        # 官网链接
        official_frame = tk.Frame(self, bg="#f5f5f5")
        official_frame.pack(pady=25)

        official_btn = tk.Button(official_frame, text="访问官网", 
                               command=lambda: webbrowser.open("{self.official_website}"),
                               bg="#f5f5f5", fg="#409eff", font=("微软雅黑", 12), relief="flat",
                               width=15, height=1)
        official_btn.pack()

        # 版权信息
        copyright_frame = tk.Frame(self, bg="#f5f5f5")
        copyright_frame.pack(side="bottom", fill="x", pady=30)

        copyright_label = tk.Label(copyright_frame, text="{self.copyright_info}",
                                  bg="#f5f5f5", fg="#999999", font=("微软雅黑", 10))
        copyright_label.pack()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{{width}}x{{height}}+{{x}}+{{y}}")

    def check_for_update(self):
        updater = AppUpdater(CURRENT_VERSION, UPDATE_INFO_URL)
        if updater.check_updates():
            UpdateWindow(self, updater)
        else:
            messagebox.showinfo("检查更新", "当前已是最新版本")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
"""
        return code.strip()

if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateProgramGenerator(root)
    root.mainloop()
