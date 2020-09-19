const int Maxsize=50;
int visit[8][10]={0};
struct Node
{
	int x;			//坐标x 
	int y;			//坐标y 
	int pre;		//记上一点的方向 
	string direction;		//行进方向 
};
class migong
{
	public:
		migong(int s0[][2],string s1[8],int X,int Y,string d);
		~migong(){};
		void getdata();
		void create();			//输入迷宫 
		void start();
		void DF(Node &node,int top,int k);		//走出迷宫算法 
		void print();						//输出结果
		void isave() ;						//保存 
		void iread();      					//读取 
	private:
		int edge[Maxsize][Maxsize];
		Node stack[50];
		Node head;
		string road; //通往终点的路径 
		int step[8][2]; //8个方向的坐标 
		string step1[8];  //8个方向 
		int bushu;  	//步数 
};
