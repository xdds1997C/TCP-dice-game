# TCP-dice-game
1.交互式游戏设计（RemoteBet）基于TCP协议。<br>
结构为C/S模型，客户端主要负责将客户的所压的点型和压的金额发送给服务端和接受来自服务端的游戏情况，服务端主要负责产生随机点数，模拟摇塞子的过程，并且负责计算生成的点型，根据用户所压的点型，计算客户赔多少钱或者得到多少钱，并把结果发送给客户端<br>

2.应用层协议设计<br>
客户端到服务端：<br>
	“ks|end”:  发送开始的命令<br>
	“ys1|end”: 发送第一次摇骰子命令<br>
	“ya tc 10 gold|end”:发送本局压的情况<br>
	“ys2|end”: 发送第二次摇骰子的命令<br>
	“pb2|end”: 发送旁白2的命令<br>
	“ys3|end”: 发送第三次摇骰子命令<br>
	“js|end”:结束这一句<br>
服务端到客户端:<br>
	“pb1xxx|end”:发送旁白1给客户端<br>
	“tc|xx|xx|xxx|end”:发送一次预彩情况给客户端<br>
	“pb2|xxx|end”:发送旁白2给客户端<br>
	“ys1|xx|end”:发送第一次摇骰子的点数给客户端<br>
	“pb3|xxx|end”:发送旁白3给客户端<br>
	“ys2|xx|end”:发送第二次摇骰子点数给客户端<br>
	“lt|xx|end”:发送余额给客户端<br>


end是封帧的方式，end是每次发送数据的结束标志。封帧代码如下：<br>
while True:<br>
			data=sock.recv(2048).decode('utf-8')<br>
			msg+=data<br>
			if 'end' in data:<br>
				break<br>
3.运行方式  <br>      
a运行服务端<br>
![](https://github.com/xdds1997C/TCP-dice-game/blob/master/1.png)<br>
b在另一个命令行窗口运行客户端：<br>
 ![](https://github.com/xdds1997C/TCP-dice-game/blob/master/2.png)<br>
如图所示，客户端接受到服务端的旁白和预头彩的点数并使用骰子的样式展示出来，然后需要用户输入本次所压的点型和金额。<br>
3，用户输入压的典型和金额（ya tc 10 gold）<br>
 ![](https://github.com/xdds1997C/TCP-dice-game/blob/master/3.png)<br>
如图，服务端接受到客户端的压的情况后，模拟两次摇骰子的过程，并计算本局点型，将结果发送给客户端，客户端输了10gold。<br>


