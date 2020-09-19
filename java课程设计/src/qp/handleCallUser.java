package qp;

import java.util.ArrayList;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;

public class handleCallUser {
	handleCallUser(WebDriver driver) throws InterruptedException {
		String windowHandle = driver.getWindowHandle();
		JavascriptExecutor executor = (JavascriptExecutor) driver;
		executor.executeScript("window.open('https://music.163.com/#/song?id=224877')");
		// ÇÐ»»µ½ÍøÒ×ÔÆ´°¿Ú
		Thread.sleep(1000);
		List<String> windowHandles = new ArrayList<>(driver.getWindowHandles());
		driver.switchTo().window(windowHandles.get(windowHandles.size() - 1));
		Thread.sleep(1000);
		driver.switchTo().frame("contentFrame");
		Thread.sleep(1000);
		driver.findElement(By.cssSelector("[id=content-operation]>a:first-child")).click();
		Thread.sleep(1000);
		driver.switchTo().window(windowHandle);
	}
}