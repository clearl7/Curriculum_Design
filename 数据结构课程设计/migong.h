const int Maxsize=50;
int visit[8][10]={0};
struct Node
{
	int x;			//����x 
	int y;			//����y 
	int pre;		//����һ��ķ��� 
	string direction;		//�н����� 
};
class migong
{
	public:
		migong(int s0[][2],string s1[8],int X,int Y,string d);
		~migong(){};
		void getdata();
		void create();			//�����Թ� 
		void start();
		void DF(Node &node,int top,int k);		//�߳��Թ��㷨 
		void print();						//������
		void isave() ;						//���� 
		void iread();      					//��ȡ 
	private:
		int edge[Maxsize][Maxsize];
		Node stack[50];
		Node head;
		string road; //ͨ���յ��·�� 
		int step[8][2]; //8����������� 
		string step1[8];  //8������ 
		int bushu;  	//���� 
};
