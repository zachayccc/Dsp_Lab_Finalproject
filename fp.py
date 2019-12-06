import tkinter as Tk
from  tkinter  import ttk
import pyaudio
import wave
import struct
import math
from myfunctions import clip16
import vibrato
import echo
import chorus

root = Tk.Tk()

def set_sound_name(*args):   #获取音频文件名

    global sound_name
    sound_name = comboxlist_1.get() #获取歌曲名


def set_effect(*args): #选择声效
	global effect_name
	effect_name = comboxlist_2.get()



def run():
	#s1.set("you are playing" + sound_name + "with" + effect_name )
	wavfile = "music/" + sound_name 
	# wavfile = 'author.wav'
	# wavfile = 'cosine_200_hz.wav'

	print('Play the wave file: %s.' % wavfile)

	# choose sound effect
	if effect_name == "vibrato":
		vibrato.vibrato(wavfile)
		print(1)
	if effect_name == "echo":
		echo.echo(wavfile)
		print(2)
	if effect_name == "chorus":
		chorus.chorus(wavfile)
		print(3)

s1 = Tk.StringVar() 
s1.set("Please design your own sound effect") #设置歌曲名默认值


B1 = Tk.Button(root, text = 'play the sound', command = run) # 开始运行歌曲

# 创建歌曲名
L1 = Tk.Label(root, textvariable = s1)

# Define 下拉窗口
comvalue_1=Tk.StringVar()#窗体自带的文本，新建一个值
comvalue_1.set("sound")
comboxlist_1=ttk.Combobox(root,textvariable=comvalue_1) #初始化
comboxlist_1["values"]=("wood.wav","2","3","4")
comboxlist_1.bind("<<ComboboxSelected>>",set_sound_name)  #绑定事件,(下拉列表框被选中时，绑定go()函数)

comvalue_2=Tk.StringVar()
comvalue_2.set("effect")
comboxlist_2=ttk.Combobox(root,textvariable=comvalue_2) #初始化
comboxlist_2["values"]=("vibrato","echo","chorus","4")
comboxlist_2.bind("<<ComboboxSelected>>",set_effect)

#构造窗体
L1.pack() 
B1.pack()
comboxlist_1.pack()
comboxlist_2.pack()

root.mainloop() #进入消息循环

