import tkinter as Tk
from  tkinter  import ttk
import pyaudio
import wave
import struct
import math
from myfunctions import clip16
import vibrato

root = Tk.Tk()

def set_sound_name(*args):   #处理事件，*args表示可变参数
    s1.set(comboxlist.get())
    global sound_name
    sound_name = comboxlist.get() #获取歌曲名
    print(sound_name)
def run():

	wavfile = sound_name 
	# wavfile = 'author.wav'
	# wavfile = 'cosine_200_hz.wav'

	print('Play the wave file: %s.' % wavfile)

	# Open wave file

	vibrato.vibrato(wavfile)
		#print(output_bytes)
		#stream.write(output_bytes)


s1 = Tk.StringVar() 
s1.set("sound_name") #设置歌曲名默认值


B1 = Tk.Button(root, text = 'play the sound', command = run) # 开始运行歌曲

# 创建歌曲名
L1 = Tk.Label(root, textvariable = s1)

# Define 下拉窗口
comvalue=Tk.StringVar()#窗体自带的文本，新建一个值
comvalue.set("sound")
comboxlist=ttk.Combobox(root,textvariable=comvalue) #初始化
comboxlist["values"]=("wood.wav","2","3","4")
comboxlist.bind("<<ComboboxSelected>>",set_sound_name)  #绑定事件,(下拉列表框被选中时，绑定go()函数)

#构造窗体
L1.pack() 
B1.pack()
comboxlist.pack()
 

root.mainloop() #进入消息循环

