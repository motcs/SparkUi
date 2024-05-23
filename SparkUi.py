from io import BytesIO

import wx
import os
import SparkApi  # 假设SparkApi是一个已经定义好的模块
import base64

# 以下密钥信息从控制台获取   https://console.xfyun.cn/services/bm35
appid = os.getenv("XH_APPID")  # 填写控制台中获取的 APPID 信息
api_secret = os.getenv("XH_API_SECRET")  # 填写控制台中获取的 APISecret 信息
api_key = os.getenv("XH_API_KEY")  # 填写控制台中获取的 APIKey 信息



# domain = "generalv3.5"      # Max版本
# domain = "generalv3"       # Pro版本
domain = "general"  # Lite版本
# domain = os.getenv("XH_DOMAIN")

# Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"   # Max服务地址
# Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # Pro服务地址
Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址


# Spark_url = os.getenv("XH_SPARK_URL")

class PyEmbeddedImage(object):
    def __init__(self, isBase64=True):
        self.data = ("AAABAAEAgIAAAAEAGAAZDwAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAC"
                     "AAAAAgAgGAAAAwz5hywAAAAFzUkdCAK7OHOkAAAAEZ0FNQQAAsY8L/GEF"
                     "AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAOrklEQVR4Xu2dd8zV1B/G+ZM"
                     "/TAgJMRICIUqUMMIwEtlT9goOMDEomBCmgIQRgUiYkSUruAegyHAAKhsBlS"
                     "3KVJEXkA0vS0AZQTi/fJoW+yvn9rS9vbfnpedJnoTwtr29PU/P+a7zvc"
                     "WEQaphBJByGAGkHEYAKYcRQMphBJByGAGkHEYAKYcRQMphBJByGAGkHEYAK"
                     "YcRQMphBJByGAGkHEYAKYcRQMphBJByaC+A27dvi19//VWsWrVKbNiwQ"
                     "RQWFtp/MYgDWgvgxo0bYtasWeKhhx4SxYoVs8i/e/fuLX744Qfx77//2kcaR"
                     "IXWAvjjjz9E48aN7w6+l88//7z48ccfrVnCIBq0FsC+ffvEk08+KR18hy"
                     "VKlBB9+/YVBQUF9lkGYaC1AI4cOSJatGghHXgvq1evLj7//HNx69Yt+2y"
                     "DINBaAP/8848YPHiwdMBlLF26tHj77bfFzZs37SsYqKC1AO7cuSPmz59v"
                     "DaxswGWsUaOG2Lx5s30FAxW0FgDYtGmTqFq1qnSwZXzggQfE5MmTzVIQENoL"
                     "gBhA/fr1pYOdia+99pq4fv26fQUDP2gvgD///FO0atVKOtAy4hUQOzAxgm"
                     "DQXgAnTpwQ7du3lw62jHXq1BE7d+60zzZQQXsBnDx5UnTo0EE62F4WL1"
                     "5cjB071kz/IXBfLQHYCnv27LHPNAgC7QVw6NAh8dRTT0kH3MuhQ4dasQMd"
                     "gHC//vpryyOZOHGiWLZsmZaJLO0FsH//flG3bl3pgLv58MMPi2+++cY+KxkQgF"
                     "q6dGlGwZLI6tmzp1i7dq02wSrtBbB161YrzCt7oG6yTPDWJQECViSlnn76"
                     "aem9ydioUSMrdE3GM0loLwDqACpUqCB9iG6OHDkyEeOPOMWAAQNEqVKlpP"
                     "el4gsvvGB5LYgoCWgtAB7KwoULlaHgMmXKiMWLF+ftITJ9r1mzRrz88suiZ"
                     "MmS0nsKQ5avjz76KJFlQWsBEMwhqENwR/bgHDZo0MCyFXIJZhcqkogyVqlS"
                     "RXof2ZBrIqp8zwRaC4CHzgOXPTA3e/ToIS5dumSfFQ8YiN9//128++67ol"
                     "u3bqJs2bLSz46Tw4cPF9euXbPvID/QWgCXL1+2Blf2sBzGFfpl+t2+fbuYO"
                     "XOmeOmllwLZHXFz0KBB4u+//7bvKD/QWgDHjh0Tbdq0kT4sh48++qjlVoWB"
                     "U2iKfYHx2K5du1jW8mzI58+ePTvvOQytBbBr1y5lSRg+N8EiFXbv3m1Z67Vq"
                     "1ZJeJ2kS7g7yPeKG1gJYuXKlZSHLHphDKoSvXLlinyEH8YHWrVtLz9eBGLFb"
                     "tmyx7za/0FYATNNz5swRDz74oPShwaDr/08//SQef/xx6TWSJoO/bds2+07z"
                     "D20FgFFGZk/20ByWL1/eirGrXKcLFy4ojckorFixohXaxYc/ePCgZbS+8sor"
                     "0mNlxPVbsWJF3l0/N7QVAA+Thyt7cA7D+P8sA1j3susEJbNRly5drMLT33777"
                     "Z79CJShqUTrEKMPjyPp0jVtBXD69GnRqVMn6cNziH9+8eJF+ww1rl69Kt5//31"
                     "Rs2ZN6fVkJBE1YsQIy9NQZRrx4clIyq7jJUbf0aNH7TOTg7YCYFOIKgv4+uuv"
                     "W8EiptC9e/da9gADzLl+u4UIGr3zzjuiefPmVhGJ+5pUFPXr10988sknlhsaBk"
                     "HiFpCg0meffabFjiZtBfDdd99Za6zsAUJSq85DXL58uahUqdL//b1Zs2Zi7ty5"
                     "1lvvB2yNn3/+WezYsSPrZFKQuAV88cUXxblz5+yzkoWWAuCN5g10bwr1klJxSsYZNII5smMgVUJfffVVXtbaIN4Gb"
                     "/+iRYsSNfzc0FIAvJUTJky4Z3p208n/k08fPXq09BiHuIuszefPn7c/IX4woHgkeCaye3BIzQB1jr"
                     "pASwEE8QCcABAPfsGCBYF2DxFr59q5ALEIQrl+IWVqBvAg8h3u9YOWAlCtpcwM1Nk5"
                     "+fOgu4eIKgaJG0RBkMxl06ZNrQyjTtBSAKq1lAIQyqmcgQxaNwhZLnJRhsXyQnWP7D"
                     "OhU7KedAmYF9oJgEFdsmSJKFeunPRBQjaAkrp1wFvVsGFD6bFe5qp0THUPeCkUlOgG7QTA+jh9"
                     "+nTfKiBcPGYA1tNevXoFjvPnsnSMQNFjjz0m/Vyok+vnhnYCCNsTIAzbtm2bk+gboiWwlMkAJIT84YcfahH48UILARCZo"
                     "+nTvHnzrOjeE088IX2Q2ZAZhZklF/EAlWjzUbMYFXkRAFMuDZ/WrVtnvQljxoyx4vi0f/EL9sRJQrwUmMSNs"
                     "2fPig8++EDUrl1b+rmQ7zhjxgztDEAQSQAMKEYPX3z8+PFi3Lhxd4mRRcaMMiuqdfzy+fkktsJff"
                     "/1l3T9TcVQ7gHPJOzCgzzzzjK+t4iYRQELTOsUAQGgBkPGaOnWqNgMbhLyBH3/8sVVwOWXKlLv3jk3A/6syijSrIjTdv3"
                     "//UN1KvLwv4gBUr4RJp+aS+Na4hKq3EJuC3TfEF2Q1gVQAk/JlnUYkBJbILJLZq1y58j3HR6WTwMqFFxIVoQUQdK9eLshAd"
                     "+3a1Ur5ksHDoAsSBeQcXLAgNYa5JKFg7l0nbyC0ALDYWU9lXzDXxGhkOnbAm6TKA7jDxmEbTsXNevXqiV9++cW"
                     "+ez0QyQik4CJoA8egZKBUdgWxdvfOGSJ6uI2yYx269w2EbTcTJ6lKJhKo0"
                     "/QPIgkAYAkHbd0iI6HR7t27W3VxvJm4U2T4ZMdCQsPu+D/gnM6dO0uPd+ieNXIZZHIT0XXs2NFKQb/33nuW"
                     "+6mb9e8gsgAACRD2swXZGs1++GHDhlnFEMePH7ev8B+IExDilZ0L+RvHuEEtPUag7HiHDLhTy8cgBNlsGpRE"
                     "/igrGzhwoBWW3rhxY87SzblCVgIAGDR05sRidk/heAoM+LfffqvcuMlbrSqm8LZ/4XMJKvktG1jdRBcdo4vP"
                     "+eKLLyJt9CSPwFuNt4DdwdYynYy5qMhaAG7wQA4cOGCttWGAgYahhh2Q6eF7kzjU"
                     "+qlq8B33zw1VrSFEOCxvzmDzne6HwZYhVgFEBUsJ2TLZYMAmTZpYg+AG66qqBgD3z1sGpnJjmR2YJXQz1nIFLQTAW"
                     "+qXAJJN//jTftM/PYPffPPNe5I/xA"
                     "/8PkvXvH2ukLgAeNP8OoLLrP8zZ84orf9MA6n6EQpmFV0zd7lA4gJQ1dIRPHFn8RAC7eBUET12FZ06dco"
                     "+6z9QSeTnOSTZbSwJJC6AILtp8KunTZtmJW3wKFTH+7WMVwmA3yHSsXInV0hcAET2gvQBgtTccayq9r5atWpW3z4ZVAII0m"
                     "/gfoIWRiCuWZwxeopN2BIuA5VHfl2+MDjz3agpCNi6xvLEvX/66aexVTZpIQAidKRJ/YoqgxJjksKLTH47hqF3H6GblI07"
                     "+w10Actknz597t6jNymWDbQQgAM6ffvV1gdhy5YtxeHDh+0r3gsSQ9gUsnMzuY5JA6"
                     "+EukLnPlnC3GXx2UArAQDWXzZQRGm9ygC+8cYbvm+wX01AUp26/IDX4w2TR+mMlgnaCQDgGmL1q9LDXuLDq"
                     "/LtKgFQ3q2TAGRhcqKVdCWPA1oKAGCITZo0KdRMQBs4VaPFoiYA2UbZOEvLtBUAwOfnZ2HdX96PGHf8SIPfg"
                     "6FXAMkl2fk6CoCglPcXU+K8T20FgBX/5ZdfhvYMiBz6GUhFTQCy5JVT5haHsaqlABh8DJ+oXbmfe+65jFvA/A"
                     "SgmxfATJap5tFd6JINtBMAg0+sP+rgOySgI4vo"
                     "+QkAUmOoyw4ev5pHfqvA2eiSDbQSAFMvJWOqgo0gZJBlO3Gwnv0qgjC4dCnr8qt5JNlFK71soY0AcHcooIxSrp"
                     "WJsjJsv0AQ1CkbSD6DvIbsPhs3bnxPjWQUaCEAXDcCOGH9/iBkO5d7qlTtDWD2Wb9+vX10cnD8f+wS2X2yRJLXy"
                     "BaJC4BpjEHKVA8oYxjPgG1f9BF0XMMg3USS+OUOL2Tun5sYhhiI2cYCEhMAN05ZN2XVsi+Yia+++qq1J0FVEeSme"
                     "2cwNQVkC2XHOcTtSrIsDCOUIJiqfN3plJoNEhEAN83Wcr+12EsigmTqHAMtTArZXR3Mw1X1FYTsHPYWouYDvBj8"
                     "VF6QTan0HJRVPYVB3gXA28uOoDBTPoYhGy/cauffNJPMtEa6yfkElZzpkl/nCrKMkFsgspivuAB+/VtvvSUeeeQR"
                     "6f14yXG0m88GeRMAZVYYeqpqHi+xdlevXi3N7xPsCbI9zRvh417CpJ1pdEGA6Pvvv4+1WghBMstQFEu+P+jAu5m"
                     "tvZJzAXBzJC5wyWRfIBMZtCFDhlgVwJnAA6Ri2K+lHPQKgPP4waioLifJGIoy8MW5R3eHFNLJTOEsUZCdUWQ2nb"
                     "9T0vbss89aW924L9n1w5AOaYSLoyJnAuBh8+b6WbKZyMNlagsy9ZIwclfLyCizmIOcV1RIW56os0BOBMDUTM/9I"
                     "Ouzmxhr7OUL+9t5+O1+oWOMRfx/L6izc1faFFXSq8hvpvRD7AJgoygt2mU3mol08CIKqNpEmgkYT6yFsmvDTE0am"
                     "RFkvzVQ1JhNKXusAqASV+Vju4kBxz68OIIu7NaVbS9XFYmyVGFHFFUR4B5n04E8VgHQB19llTMd44dT6Ohek7MFA4"
                     "xh5zUIaRGvyppxHxhsfr3+dGWQ7+eHWAWAChkEd4CGYA/5eXbqEIyJqtQgQAQke4guEtMnUhbmxxkIv1KBFNZ2SYIEi"
                     "gimZTt75sQILMrA88CNI9QcJliVL9JpBVeTVHEcMALIAGYTZqxRo0Yl6ikQOMPIo7VNLrqSGAEERGFhoRWbIElDco"
                     "lfNIkSuctElh3ebppasC8Cw7SgoCBWO0kGI4AYgPtKbh77A9LOhjwFTbG9ZHB5mylPp3l2HD9Xlw2MAFIOI4CUw"
                     "wgg5TACSDmMAFIOI4CUwwgg5TACSDmMAFIOI4CUwwgg5TACSDmMAFIOI4CUwwgg5TACSDmMAFIOI4CUwwgg5TACSD"
                     "mMAFIOI4CUwwgg5TACSDmMAFINIf4HURWeUR6bgQ4AAAAASUVORK5CYII=")
        self.isBase64 = isBase64

    def GetBitmap(self):
        return wx.Bitmap(self.GetImage())

    def GetData(self):
        data = self.data
        if self.isBase64:
            data = base64.b64decode(self.data)
        return data

    def GetIcon(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(self.GetBitmap())
        return icon

    def GetImage(self):
        stream = BytesIO(self.GetData())
        return wx.Image(stream)


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 600))
        # 设置窗口的图标
        a = PyEmbeddedImage()
        self.SetIcon(a.GetIcon())
        self.send_button = None
        self.input_ctrl = None
        self.sizer = None
        self.text_ctrl = None
        self.panel = wx.Panel(self)
        self.init_ui()
        self.text = [
            {"role": "system", "content": "你现在叫妃妃，是一个全能型的AI，你非常的喜欢帮助人们处理日常事务。"}
        ]

    # 假设getText是一个处理文本的函数
    def getText(self, role, content):
        jsoncon = {}
        jsoncon["role"] = role
        jsoncon["content"] = content
        self.text.append(jsoncon)
        return self.text

    def getlength(self):
        length = 0
        for content in self.text:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length

    def checklen(self):
        while (self.getlength() > 8000):
            del self.text[0]

    def init_ui(self):
        # 创建一个垂直的BoxSizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # 创建文本显示区域
        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 1)
        # 绑定键盘事件
        self.text_ctrl.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        # 创建一个水平的BoxSizer用于放置输入框和按钮
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # 创建文本输入框，并设置最小高度
        self.input_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        # 设置输入框的最小尺寸
        hbox.SetMinSize((-1, 100))  # -1 表示宽度自动调整，50 表示最小高度为50像素
        hbox.Add(self.input_ctrl, 1, wx.EXPAND | wx.LEFT, 0)  # 将输入框添加到水平sizer中

        # 创建发送按钮
        self.send_button = wx.Button(self.panel, label="发送")
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send)
        # wx.EXPAND 使得按钮高度与输入框一致
        hbox.Add(self.send_button, 0, wx.EXPAND | wx.ALL, 5)

        # 将水平sizer添加到垂直sizer中
        self.sizer.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 0)
        self.panel.SetSizer(self.sizer)
        # 显示窗口后，设置焦点到输入框
        self.Bind(wx.EVT_SHOW, self.on_show)

    def on_show(self, event):
        self.input_ctrl.SetFocus()
        event.Skip()

    def on_key_down(self, event):
        # 检查按下的键是否是删除键
        if event.GetKeyCode() == wx.WXK_DELETE:
            event.Skip()  # 忽略删除事件
        else:
            event.Skip()  # 其他事件正常处理

    def on_send(self, event):
        user_input = self.input_ctrl.GetValue()
        # 清空输入框
        self.input_ctrl.SetValue("")
        self.input_ctrl.SetFocus()
        if len(user_input) > 0:
            question = self.getText("user", user_input)
            print(question)
            # 对内容进行检查
            self.checklen()
            self.text_ctrl.AppendText(f"我: {user_input}\n")
            SparkApi.answer = ""
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question, self)


# 运行程序
if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, '妃妃Chat')
    frame.Show()
    app.MainLoop()
