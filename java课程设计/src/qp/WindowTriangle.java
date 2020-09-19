package qp;

import java.awt.BorderLayout;
import java.awt.FlowLayout;

import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;

@SuppressWarnings("serial")
public class WindowTriangle extends JFrame {
	static JTextArea textShow;

	public WindowTriangle() {
		init();
		setVisible(true);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	void init() {
		setLayout(new FlowLayout());
		textShow = new JTextArea(10, 28);
		add(new JScrollPane(textShow), BorderLayout.CENTER);
	}

	public void appendJTextArea(String info) {
		SwingUtilities.invokeLater(new Runnable() {

			@Override
			public void run() {

				if (info != null) {
					textShow.append(info + "\n");
				}
				try {
					Thread.currentThread();
					Thread.sleep(100); // �õ�ǰ�Ľ���˯�����ɺ��룬������ʾ����̬����Ч������Ȼ�⽫��ʱ

				} catch (InterruptedException ex) { // �����ж��쳣}

				}
			}
		});
	}
}