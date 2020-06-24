#  我真诚地保证：
#  我自己独立地完成了整个程序从分析、设计到编码的所有工作。
#  如果在上述过程中，我遇到了什么困难而求教于人，那么，我将在程序实习报告中
#  详细地列举我所遇到的问题，以及别人给我的提示。
#  我的程序里中凡是引用到其他程序或文档之处，
#  例如教材、课堂笔记、网上的源代码以及其他参考书上的代码段,
#  我都已经在程序的注释里很清楚地注明了引用的出处。

#  我从未没抄袭过别人的程序，也没有盗用别人的程序，
#  不管是修改式的抄袭还是原封不动的抄袭。
#  我编写这个程序，从来没有想过要去破坏或妨碍其他计算机系统的正常运转。 
#  <刘子亮> 

import socket
import time
#根据骰子数显示骰子形状
def draw(dice):
	dice_list=[
	'┌─────┐\n│     │\n│  ●  │\n│     │\n└─────┘\n',
	'┌─────┐\n│     │\n│●   ●│\n│     │\n└─────┘\n',
	'┌─────┐\n│●    │\n│  ●  │\n│    ●│\n└─────┘\n',
	'┌─────┐\n│●   ●│\n│     │\n│●   ●│\n└─────┘\n',
	'┌─────┐\n│●   ●│\n│  ●  │\n│●   ●│\n└─────┘\n',
	'┌─────┐\n│●   ●│\n│●   ●│\n│●   ●│\n└─────┘\n']
	print(dice_list[dice-1])
def main():
	serveraddr=('127.0.0.1',35000)
	clientaddr=('127.0.0.1',34999)
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind(clientaddr)
	sock.connect(serveraddr)
	#发送开始命令给服务端
	ks='ks'+'|end'
	sock.sendall(ks.encode('utf-8'))
	while True:
		msg=''
		while True:
			data=sock.recv(2048).decode('utf-8')
			msg+=data
			#使用end作为结束符，如果接收到end字符，就停止接收数据
			if 'end' in data:
				break
		msg=msg[:-4]#把‘|end’字符除去
		if msg.split('|',1)[0]=='pb1':#接收到pb1命令，把旁白打印出来
			print(msg.split('|',1)[1])
			ys1='ys1'+'|end'#发送摇骰子的命令
			sock.sendall(ys1.encode('utf-8'))
		elif msg.split('|',1)[0]=='tc':#接收到预头彩的点数
			tc1=msg.split('|',3)[1]
			tc2=msg.split('|',3)[2]
			draw(int(tc1))#画出骰子
			draw(int(tc2))
			print(msg.split('|',3)[3])
			msg_bet=input()#输入压的命令，例如ya tc 10 gold
			msg_bet=msg_bet+'|end'
			sock.sendall(msg_bet.encode('utf-8'))
		elif msg.split('|',1)[0]=='pb2':#收到pb2，打印旁白到屏幕
			print(msg.split('|',1)[1])
			time.sleep(1)#暂停一秒钟，增强游戏的感觉
			ys2='ys2'+'|end'#发送摇骰子的命令
			sock.sendall(ys2.encode('utf-8'))
		elif msg.split('|',1)[0]=='ys1':#收到骰子数
			dice1=msg.split('|',1)[1]
			time.sleep(1)#暂停一秒钟，增强游戏的感觉
			draw(int(dice1))#画出骰子
			pb2='pb2'+'|end'#发送旁白命令，从服务端获取旁白
			sock.sendall(pb2.encode('utf-8'))
		elif msg.split('|',1)[0]=='pb3':#收到pb3，打印到屏幕
			print(msg.split('|',1)[1])
			time.sleep(1)#暂停一秒钟，增强游戏感觉
			ys3='ys3'+'|end'#发送摇骰子的命令
			sock.sendall(ys3.encode('utf-8'))
		elif msg.split('|',1)[0]=='ys2':#接收到骰子数
			dice2=msg.split('|',1)[1]
			time.sleep(1)
			draw(int(dice2))#画出骰子
			js='js'+'|end'#发送结束命令
			sock.sendall(js.encode('utf-8'))
		elif msg.split('|',1)[0]=='lt':#接受到余额，打印出余额
			print('余额为：',msg.split('|',1)[1])
			time.sleep(3)
			ks='ks'+'|end'
			sock.sendall(ks.encode('utf-8'))
	



if __name__ == '__main__':
	main()