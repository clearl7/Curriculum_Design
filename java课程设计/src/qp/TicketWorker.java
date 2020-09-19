package qp;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;
import java.util.concurrent.ThreadLocalRandom;
import java.util.logging.Logger;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

public class TicketWorker {

	private static final Logger logger = Logger.getLogger("TicketWorker2.class");
	private static final String loginUrl = "https://www.12306.cn/index/";
	private static final String indexUrl = "https://kyfw.12306.cn/otn/view/index.html";
	private static final String searchUrl = "https://kyfw.12306.cn/otn/leftTicket/init";
	private static final String confirmUrl = "https://kyfw.12306.cn/otn/confirmPassenger/initDc";

	public static void main(String[] args) throws InterruptedException {

		// ��ȡ����
		WebDriver driver = getWebDriver();
		// �����¼
		handleLogin(driver);
		// ǰ������
		handleSearch(driver);
		// ���복��
		String carCode = handleInputCarCode();
		WindowTriangle win = new WindowTriangle();
		win.setTitle("12306�Զ���Ʊ���");
		win.setBounds(200, 200, 450, 300);
		win.appendJTextArea("��ѡ�ĳ���Ϊ��" + carCode);
		win.appendJTextArea("���ڿ�ʼΪ����Ʊ");
		Thread.sleep(500);
		// ����Ԥ��
		handleReserve(driver, carCode, win);
		// �����ύ
		handleSubmit(driver, win);
		// ����ȷ���ύ��Ϣ
		handleConfirm(driver, win);
		// ���������û�
		new handleCallUser(driver);
		// ˯�ߵȴ��û�ȷ����Ϣ���
		Thread.sleep(1000000);
		// �ر������
		driver.close();
		win.appendJTextArea("����");
	}

	// ��¼12306
	private static void handleLogin(WebDriver driver) throws InterruptedException {
		driver.get(loginUrl);
		logger.info("�ȴ��û���¼"); // ��¼�ɹ�
		Thread.sleep(1000);
		driver.findElement(By.linkText("��¼")).click();
		Thread.sleep(1000);
		driver.findElement(By.linkText("�˺ŵ�¼")).click();
		driver.findElement(By.id("J-userName")).sendKeys("qdp137");
		driver.findElement(By.id("J-password")).sendKeys("qdplbwnb777");
		WebDriverWait wait = new WebDriverWait(driver, 120);
		wait.until(ExpectedConditions.urlContains(indexUrl));
		logger.info("�û���¼�ɹ�~");
	}

	// ��д�����أ�Ŀ�ĵص������Ϣ
	private static void handleSearch(WebDriver driver) {
		driver.get(searchUrl);
		System.out.println();
		System.err.println("���ڴ򿪵������ҳ������д '������' 'Ŀ�ĵ�' '������' �������Ϣ, ���ҵ�� '��ѯ' ��ť��ɱ��β���");
		// ��ȡ����������
		WebDriverWait wait = new WebDriverWait(driver, 120);
		wait.until(ExpectedConditions
				.presenceOfElementLocated(By.cssSelector("table tbody#queryLeftTable:first-of-type tr")));
		List<WebElement> trs = driver.findElements(By.cssSelector("table tbody#queryLeftTable:first-of-type tr"));
		List<String> currentCarCodeList = new ArrayList<>(16);
		for (WebElement tr : trs) { // ��ȡ���г�����Ϣ
			if (tr.getAttribute("id").contains("ticket_")) {
				String currentCarCode = tr.findElements(By.cssSelector("td div.ticket-info > div.train a.number"))
						.get(0).getText();
				currentCarCodeList.add(currentCarCode);
			}
		}
		System.out.println("���β��ҵ���������Ϊ: " + currentCarCodeList.size());
		for (int i = 0; i < currentCarCodeList.size(); i++) {
			String currentCarCode = currentCarCodeList.get(i);
			System.out.print(currentCarCode + "\t||\t");
		}
		System.out.println();
	}

	// ����Ҫ���ĳ���
	private static String handleInputCarCode() {
		System.err.println("=============================�����·���������Ҫ�����ĳ���==================================");
		String carCode = "a";
		Scanner scanner = new Scanner(System.in);
		while ("a".equals(carCode)) {
			System.out.println("��������Ҫ���ĳ��Σ�");
			carCode = scanner.next();
		}
		System.out.println("������ĳ���Ϊ:" + carCode);
		return carCode;
	}

	// ��Ʊ
	private static void handleReserve(WebDriver driver, String carCode, WindowTriangle win)
			throws InterruptedException {
		clickSearch: for (int i = 1;; i++) {
			List<WebElement> trs = driver.findElements(By.cssSelector("table tbody#queryLeftTable:first-of-type tr"));
			for (WebElement tr : trs) {
				if (tr.getAttribute("id").contains("ticket_")) {
					String currentCarCode = tr.findElements(By.cssSelector("td div.ticket-info > div.train a.number"))
							.get(0).getText();
					if (carCode.equals(currentCarCode)) {
						// �ҵ��˳���
						WebElement purchaseTd = tr.findElement(By.cssSelector("td:last-of-type"));
						String text = purchaseTd.getText();
						logger.info("�ҵ�Ԥ��text:" + text);
						win.appendJTextArea("�ҵ�Ԥ��text:" + text);
						List<WebElement> aElementList = purchaseTd.findElements(By.tagName("a"));
						if (aElementList.size() > 0) {
							logger.info("���Ԥ��:");
							win.appendJTextArea("���Ԥ��:");
							purchaseTd.click();
							Thread.sleep(1000);
							if (driver.findElements(By.id("defaultwarningAlert_id")).size() > 0) {
								// ���ܳ��ֲ�����Ԥ��ʱ��
								List<WebElement> tips = driver
										.findElements(By.id("content_defaultwarningAlert_hearder"));
								if (tips.size() > 0) {
									String tip = tips.get(0).getText();
									logger.info("Ԥ��ʧ��:" + tip);
									win.appendJTextArea("Ԥ��ʧ��:" + tip);
								}
								// �رյ���
								driver.findElement(By.id("qd_closeDefaultWarningWindowDialog_id")).click();
								continue clickSearch;
							}
							// ��Ҫ�����¼����
							break clickSearch;
						}
					}
				}
			}
			// û���ҵ�����, ����, �����ѯ��ť, 10��ˢ��һ��ҳ��
			if (i % 10 == 0) {
				logger.info("����ˢ��ҳ��");
				win.appendJTextArea("����ˢ��ҳ��");
				driver.navigate().refresh();
				continue;
			}
			long sleepTime = ThreadLocalRandom.current().nextLong(500, 1500);
			Thread.sleep(sleepTime);
			List<WebElement> query_ticket = driver.findElements(By.id("query_ticket"));
			if (query_ticket.size() > 0) {
				logger.info("׼�������ѯ�������ݵ�: " + i + " ��");
				win.appendJTextArea("׼�������ѯ�������ݵ�: " + i + " ��");
				query_ticket.get(0).click();
				// �ȴ�ҳ�����ݳ���
				WebDriverWait wait = new WebDriverWait(driver, 120);
				wait.until(ExpectedConditions
						.presenceOfElementLocated(By.cssSelector("table tbody#queryLeftTable:first-of-type tr")));
			} else {
				logger.info("��ѯ��ť������");
				win.appendJTextArea("��ѯ��ť������");
			}
		}
	}

	// ѡ��λ���ύ����
	private static void handleSubmit(WebDriver driver, WindowTriangle win) throws InterruptedException {
		Thread.sleep(500);
		driver.findElement(By.cssSelector("#normalPassenger_0")).click();
		win.appendJTextArea("����Ϊ�����ȷ�ϳ˳��˵���Ϣ");
		Thread.sleep(500);
		WebElement el = driver.findElement(By.id("ticketInfo_id"));
		WebElement sel = el.findElement(By.id("seatType_1"));
		Select downlist = new Select(sel);
		downlist.selectByValue("1"); // ѡ��
		win.appendJTextArea("����Ϊ��ѡ��");
		Thread.sleep(1000);
		do {
			if (driver.findElements(By.cssSelector("#transforNotice_id #qr_closeTranforDialog_id")).size() > 0) {
				// �����п��ܻ�������緱æ�����, ������־͵��ȷ��, �رմ���, Ȼ��������
				driver.findElement(By.cssSelector("#transforNotice_id #qr_closeTranforDialog_id")).click();
			}
			Thread.sleep(1000);
			driver.findElement(By.cssSelector("#submitOrder_id")).click();
			//
		} while (driver.findElements(By.cssSelector("#transforNotice_id #qr_closeTranforDialog_id")).size() > 0);
	}

	// ȷ�϶���
	private static void handleConfirm(WebDriver driver, WindowTriangle win) throws InterruptedException {
		Thread.sleep(1000);
		if (driver.findElements(By.cssSelector("#checkticketinfo_id #qr_submit_id")).size() > 0) {
			// ���ȷ�϶�����Ϣ
			driver.findElements(By.cssSelector("#checkticketinfo_id #qr_submit_id")).get(0).click();
			win.appendJTextArea("���ȷ�϶�����Ϣ");
		}
		logger.info("��Ʊ�ɹ�");
		win.appendJTextArea("��Ʊ�ɹ�");
		Thread.sleep(500);
		win.appendJTextArea("�ɹ�Ϊ������Ʊ���뵽���������֧��");

	}

	// ���������
	private static WebDriver getWebDriver() {

		// WebDriver driver = new FirefoxDriver();
		System.setProperty("webdriver.chrome.driver", "D:\\jdk1.8\\Selenium\\chromedriver.exe");
		ChromeOptions option = new ChromeOptions();
		// ͨ��ChromeOptions��setExperimentalOption������������������������ֹ���ȸ����Զ������Ƶ���Ϣ��
		option.setExperimentalOption("useAutomationExtension", false);
		option.setExperimentalOption("excludeSwitches", Collections.singletonList("enable-automation"));
		WebDriver driver = new ChromeDriver(option); // �½�һ��WebDriver �Ķ��󣬵���new ���ǹȸ������
		driver.manage().window().maximize();
		return driver;
	}

}
