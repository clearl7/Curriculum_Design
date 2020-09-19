#include"migong.h"
#include <fstream>
migong::migong(int s0[][2],string s1[8],int X,int Y,string d)
{
	for(int i=0;i<8;i++)
	for(int j=0;j<2;j++)
	step[i][j]=s0[i][j];
	for(int h=0;h<8;h++)
	step1[h]=s1[h];
	head.x=X;
	head.y=Y;
	head.direction=d;
	head.pre=0;
	bushu=0;
}

void migong::getdata()
{
	//读取迷宫 
	int i=0,j=0;
	ifstream fpin;
	fpin.open("D:\migong_data.txt",ios::in);
	cout<<"读取成功。"<<endl;
	if(!fpin.good())
	{
		cout<<"cannot open file\n";
		return;
	}
	while(!fpin.eof())
	{
		if(j==10){
			i++;
			j=0;
		}
		fpin>>edge[i][j];
		j++;
	}
	fpin.close();
}

void migong::create()
{
	getdata();
	cout<<"迷宫图如下↓"<<endl;
	for(int i=0;i<8;i++){
	for(int j=0;j<10;j++)
		cout<<edge[i][j]<<" ";
	cout<<endl;
	}
	cout<<"起点：(1,1),终点：(6,8)"<<endl;
}
void migong::start()
{
	cout<<"进入迷宫，开始寻路：" <<endl;
	DF(head,0,0);
}
void migong::DF(Node &node,int top,int k)
{
	stack[top]=head;
	visit[head.x][head.y]=1;
	for(int i=k;i<8;i++)
	{
		node=stack[top];
		int x=node.x+step[i][0];
		int y=node.y+step[i][1];
		string s=step1[i];
		if(x==6&&y==8)
		{	//到达迷宫出口 
			cout<<"x:"<<head.x<<" "<<"y:"<<head.y<<" "<<s<<endl;
			int j=-1;
			Node stack1[top];	
			while(top!=-1)
			stack1[++j]=stack[top--];
			while(j!=-1)
			{	//打印正确路线 
			Node last=stack1[j--];
			road.append(last.direction);
			bushu++;
			}
		road.append(s);
		cout<<"成功走出迷宫"<<endl; 
		return;
		}
		if(edge[x][y]==0&&visit[x][y]==0)
		{	//通路可前进
			head.direction=s;
			cout<<"x:"<<head.x<<" "<<"y:"<<head.y<<" "<<head.direction<<endl;
			head.x=x;
			head.y=y;
			head.pre=i;
			return DF(head,++top,0);
			cout<<"x:"<<head.x<<" "<<"y:"<<head.y<<" "<<head.direction<<endl;
		}
		if(i==7)
		{	//死路需出栈 
			head=stack[--top];
			return DF(head,top,++node.pre);
		}
	}
}
void migong::print()
{
	cout<<"走出迷宫的结果为（箭头为行进方向）：";
	cout<<road<<endl;
	cout<<"步数为："<<bushu<<endl;
}
void migong::isave()
{
	ofstream fp;
	fp.open("stu_data.txt",ios::out);
	if(!fp.good())
	{
		cout<<"cannot open file\n";
		return;
	}
	if(road!="")
	{
		fp<<road<<endl;
		fp<<bushu<<endl;
		cout<<"写入成功。"<<endl;
	}
	fp.close();
}
void migong::iread()
{
	string s;
	int walk;
	ifstream fpin;
	fpin.open("stu_data.txt",ios::in);
	cout<<"读取成功。"<<endl;
	if(!fpin.good())
	{
		cout<<"cannot open file\n";
		return;
	}
	while(!fpin.eof())
	{
		fpin>>s;
		fpin>>walk;
	}
	cout<<"走出迷宫的结果为："<<s<<endl;
	cout<<"步数为："<<walk<<endl;
	fpin.close();
}
