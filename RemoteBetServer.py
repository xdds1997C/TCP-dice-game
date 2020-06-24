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
import random

#根据四个参数，计算出本局的点型
#a，b是预头彩的两个点数，c，d是掷骰子的两次点数
#返回是点型和赔率
def rules(a,b,c,d):
	if(a==c and b==d):
		return 'tc',35
	elif(a+b==c+d):
		return 'dc',17
	elif(c!=d and c%2==0 and d%2==0):
		return 'kp',5
	elif(c+d==7):
		return 'qx',5
	elif(c%2==1 and d%2==1):
		return 'dd',3
	elif(c+d==3 or c+d==5 or c+d==9 or c+d==11):
		return 'sx',2
	else:
		return 'zy',0

#利用随机函数随机获得1-6的整数，产生骰子的点数
def dicing():
	dice=random.randint(1,6)
	return dice

def main():
	address=('127.0.0.1',35000)
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sock.bind(address)
	sock.listen(1)
	print('Listening at',sock.getsockname())
	while True:
		#接收来自客户端的请求
		sc,sockname=sock.accept()
		#初始的钱数为50
		monney=50
		print('recv from ',sockname)
		while True:
			msg=''
			while True:
				data=sc.recv(1024).decode('utf-8')
				msg+=data
				#接收到的字符里面有end，就代表数据接收完成
				if 'end' in data:
					break
			msg=msg[:-4]#字符串减去‘|end’
			if msg=='ks':#收到ks，开始这一局，发送pb1
				sc.sendall('pb1|庄家唱道：新开盘！预叫头彩！\n庄家将两枚玉骰往银盘中一撒。\n|end'.encode('utf-8'))
			elif msg=='ys1':#收到摇骰子的命令，调用dicing函数获得点数
				tc1=dicing()
				tc2=dicing()
				#将结果发送给客户端
				tc='tc|'+str(tc1)+'|'+str(tc2)+'|输入你压的值:|end'
				sc.sendall(tc.encode('utf-8'))
			elif msg.split(' ',1)[0]=='ya':#收到客户端压的点型和金钱
				msg_bet_list=msg.split(' ',3)
				#余额减去本局压的钱数
				monney-=int(msg_bet_list[2])
				#发送pb2
				sc.sendall('pb2|庄家将两枚玉骰扔进两个金盅，一手持一盅摇将起来。\n庄家将左手的金盅倒扣在银盘上，玉骰滚了出来。|end'.encode('utf-8'))
			elif msg=='ys2':#收到摇骰子的命令
				dice1=dicing()
				#发送骰子数
				dice='ys1|'+str(dice1)+'|end'
				sc.sendall(dice.encode('utf-8'))
			elif msg=='pb2':#收到pb2命令，发送pb
				sc.sendall('pb3|庄家将右手的金盅倒扣在银盘上，玉骰滚了出来。|end'.encode('utf-8'))
			elif msg=='ys3':#收到摇骰子命令
				dice2=dicing()
				#发送投骰子数
				dice='ys2|'+str(dice2)+'|end'
				sc.sendall(dice.encode('utf-8'))
			elif msg=='js':#收到结束命令
				dx,pl=rules(tc1,tc2,dice1,dice2)#计算本局点型
				if dx==msg_bet_list[1]:
					monney=monney+int(msg_bet_list[2])*pl#如果客户端压中，余额加上赔率乘压的钱数
				left='lt|'+str(monney)+'|end'#发送余额给客户端
				sc.sendall(left.encode('utf-8'))
		

if __name__ == '__main__':
	main()
	
