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

		// 获取驱动
		WebDriver driver = getWebDriver();
		// 处理登录
		handleLogin(driver);
		// 前往搜索
		handleSearch(driver);
		// 输入车次
		String carCode = handleInputCarCode();
		WindowTriangle win = new WindowTriangle();
		win.setTitle("12306自动抢票软件");
		win.setBounds(200, 200, 450, 300);
		win.appendJTextArea("您选的车次为：" + carCode);
		win.appendJTextArea("现在开始为您抢票");
		Thread.sleep(500);
		// 处理预定
		handleReserve(driver, carCode, win);
		// 处理提交
		handleSubmit(driver, win);
		// 处理确认提交信息
		handleConfirm(driver, win);
		// 处理提醒用户
		new handleCallUser(driver);
		// 睡眠等待用户确认信息完毕
		Thread.sleep(1000000);
		// 关闭浏览器
		driver.close();
		win.appendJTextArea("结束");
	}

	// 登录12306
	private static void handleLogin(WebDriver driver) throws InterruptedException {
		driver.get(loginUrl);
		logger.info("等待用户登录"); // 登录成功
		Thread.sleep(1000);
		driver.findElement(By.linkText("登录")).click();
		Thread.sleep(1000);
		driver.findElement(By.linkText("账号登录")).click();
		driver.findElement(By.id("J-userName")).sendKeys("qdp137");
		driver.findElement(By.id("J-password")).sendKeys("qdplbwnb777");
		WebDriverWait wait = new WebDriverWait(driver, 120);
		wait.until(ExpectedConditions.urlContains(indexUrl));
		logger.info("用户登录成功~");
	}

	// 填写出发地，目的地等相关信息
	private static void handleSearch(WebDriver driver) {
		driver.get(searchUrl);
		System.out.println();
		System.err.println("请在打开的浏览器页面中填写 '出发地' '目的地' '出发日' 等相关信息, 并且点击 '查询' 按钮完成本次操作");
		// 获取搜索的条数
		WebDriverWait wait = new WebDriverWait(driver, 120);
		wait.until(ExpectedConditions
				.presenceOfElementLocated(By.cssSelector("table tbody#queryLeftTable:first-of-type tr")));
		List<WebElement> trs = driver.findElements(By.cssSelector("table tbody#queryLeftTable:first-of-type tr"));
		List<String> currentCarCodeList = new ArrayList<>(16);
		for (WebElement tr : trs) { // 获取所有车次信息
			if (tr.getAttribute("id").contains("ticket_")) {
				String currentCarCode = tr.findElements(By.cssSelector("td div.ticket-info > div.train a.number"))
						.get(0).getText();
				currentCarCodeList.add(currentCarCode);
			}
		}
		System.out.println("本次查找到车次数量为: " + currentCarCodeList.size());
		for (int i = 0; i < currentCarCodeList.size(); i++) {
			String currentCarCode = currentCarCodeList.get(i);
			System.out.print(currentCarCode + "\t||\t");
		}
		System.out.println();
	}

	// 输入要抢的车次
	private static String handleInputCarCode() {
		System.err.println("=============================请在下方输入你需要抢购的车次==================================");
		String carCode = "a";
		Scanner scanner = new Scanner(System.in);
		while ("a".equals(carCode)) {
			System.out.println("请输入你要抢的车次：");
			carCode = scanner.next();
		}
		System.out.println("您输入的车次为:" + carCode);
		return carCode;
	}

	// 抢票
	private static void handleReserve(WebDriver driver, String carCode, WindowTriangle win)
			throws InterruptedException {
		clickSearch: for (int i = 1;; i++) {
			List<WebElement> trs = driver.findElements(By.cssSelector("table tbody#queryLeftTable:first-of-type tr"));
			for (WebElement tr : trs) {
				if (tr.getAttribute("id").contains("ticket_")) {
					String currentCarCode = tr.findElements(By.cssSelector("td div.ticket-info > div.train a.number"))
							.get(0).getText();
					if (carCode.equals(currentCarCode)) {
						// 找到了车次
						WebElement purchaseTd = tr.findElement(By.cssSelector("td:last-of-type"));
						String text = purchaseTd.getText();
						logger.info("找到预定text:" + text);
						win.appendJTextArea("找到预定text:" + text);
						List<WebElement> aElementList = purchaseTd.findElements(By.tagName("a"));
						if (aElementList.size() > 0) {
							logger.info("点击预定:");
							win.appendJTextArea("点击预定:");
							purchaseTd.click();
							Thread.sleep(1000);
							if (driver.findElements(By.id("defaultwarningAlert_id")).size() > 0) {
								// 可能出现不可以预定时间
								List<WebElement> tips = driver
										.findElements(By.id("content_defaultwarningAlert_hearder"));
								if (tips.size() > 0) {
									String tip = tips.get(0).getText();
									logger.info("预定失败:" + tip);
									win.appendJTextArea("预定失败:" + tip);
								}
								// 关闭弹窗
								driver.findElement(By.id("qd_closeDefaultWarningWindowDialog_id")).click();
								continue clickSearch;
							}
							// 需要处理登录问题
							break clickSearch;
						}
					}
				}
			}
			// 没有找到车次, 或者, 点击查询按钮, 10次刷新一下页面
			if (i % 10 == 0) {
				logger.info("重新刷新页面");
				win.appendJTextArea("重新刷新页面");
				driver.navigate().refresh();
				continue;
			}
			long sleepTime = ThreadLocalRandom.current().nextLong(500, 1500);
			Thread.sleep(sleepTime);
			List<WebElement> query_ticket = driver.findElements(By.id("query_ticket"));
			if (query_ticket.size() > 0) {
				logger.info("准备点击查询更新数据第: " + i + " 次");
				win.appendJTextArea("准备点击查询更新数据第: " + i + " 次");
				query_ticket.get(0).click();
				// 等待页面数据出来
				WebDriverWait wait = new WebDriverWait(driver, 120);
				wait.until(ExpectedConditions
						.presenceOfElementLocated(By.cssSelector("table tbody#queryLeftTable:first-of-type tr")));
			} else {
				logger.info("查询按钮不可用");
				win.appendJTextArea("查询按钮不可用");
			}
		}
	}

	// 选座位，提交订单
	private static void handleSubmit(WebDriver driver, WindowTriangle win) throws InterruptedException {
		Thread.sleep(500);
		driver.findElement(By.cssSelector("#normalPassenger_0")).click();
		win.appendJTextArea("正在为您点击确认乘车人的信息");
		Thread.sleep(500);
		WebElement el = driver.findElement(By.id("ticketInfo_id"));
		WebElement sel = el.findElement(By.id("seatType_1"));
		Select downlist = new Select(sel);
		downlist.selectByValue("1"); // 选座
		win.appendJTextArea("正在为您选座");
		Thread.sleep(1000);
		do {
			if (driver.findElements(By.cssSelector("#transforNotice_id #qr_closeTranforDialog_id")).size() > 0) {
				// 这里有可能会出现网络繁忙的情况, 如果出现就点击确认, 关闭窗口, 然后再重试
				driver.findElement(By.cssSelector("#transforNotice_id #qr_closeTranforDialog_id")).click();
			}
			Thread.sleep(1000);
			driver.findElement(By.cssSelector("#submitOrder_id")).click();
			//
		} while (driver.findElements(By.cssSelector("#transforNotice_id #qr_closeTranforDialog_id")).size() > 0);
	}

	// 确认订单
	private static void handleConfirm(WebDriver driver, WindowTriangle win) throws InterruptedException {
		Thread.sleep(1000);
		if (driver.findElements(By.cssSelector("#checkticketinfo_id #qr_submit_id")).size() > 0) {
			// 点击确认订单信息
			driver.findElements(By.cssSelector("#checkticketinfo_id #qr_submit_id")).get(0).click();
			win.appendJTextArea("点击确认订单信息");
		}
		logger.info("购票成功");
		win.appendJTextArea("购票成功");
		Thread.sleep(500);
		win.appendJTextArea("成功为您抢到票，请到浏览器进行支付");

	}

	// 启动浏览器
	private static WebDriver getWebDriver() {

		// WebDriver driver = new FirefoxDriver();
		System.setProperty("webdriver.chrome.driver", "D:\\jdk1.8\\Selenium\\chromedriver.exe");
		ChromeOptions option = new ChromeOptions();
		// 通过ChromeOptions的setExperimentalOption方法，传下面两个参数来禁止掉谷歌受自动化控制的信息栏
		option.setExperimentalOption("useAutomationExtension", false);
		option.setExperimentalOption("excludeSwitches", Collections.singletonList("enable-automation"));
		WebDriver driver = new ChromeDriver(option); // 新建一个WebDriver 的对象，但是new 的是谷歌的驱动
		driver.manage().window().maximize();
		return driver;
	}

}
