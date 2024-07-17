from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip

#登录信息
email=""#账号/邮件
password=""#密码
fourmurl="http://nationarea.wikidot.com/forum/t-16519797/"#发布删除公告论坛链接
deltagpageurl="http://nationarea.wikidot.com/system:page-tags/tag/%E5%BE%85%E5%88%A0%E9%99%A4"#待删除tag的列表页面

def login(driver, wait):
    driver.get(deltagpageurl)
    login_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "login-status-sign-in"))
    )
    login_button.click()
    
    driver.switch_to.window(driver.window_handles[-1])
    login_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "login"))
    )
    login_input.send_keys(email)
    
    password_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys(password)
    
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    
    driver.switch_to.window(driver.window_handles[0])

def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    
    login(driver, wait)
    
    driver.get(deltagpageurl)
    
    tagged_pages_list = wait.until(
        EC.presence_of_element_located((By.ID, "tagged-pages-list"))
    )
    pages = tagged_pages_list.find_elements(By.CLASS_NAME, "pages-list-item")
    
    for page in pages:
        link = page.find_element(By.TAG_NAME, "a").get_attribute("href")
        pagename = link.split("/")[-1]
        full_link = f"http://nationarea.wikidot.com/{pagename}"
        
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(full_link)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        rate_span = wait.until(
            EC.presence_of_element_located((By.ID, "prw54355"))
        )
        rate = rate_span.text
        print(f"Rate: {rate}")
        
        #获取neirong
        edit_button = wait.until(
            EC.element_to_be_clickable((By.ID, "edit-button"))
        )
        edit_button.click()
        edit_textarea = wait.until(
            EC.visibility_of_element_located((By.ID, "edit-page-textarea"))
        )
        neirong = edit_textarea.get_attribute("value")
        cancel_button = wait.until(
            EC.element_to_be_clickable((By.ID, "edit-cancel-button"))
        )
        cancel_button.click()
        
        pagename = pagename[0].upper() + pagename[1:] if pagename and pagename[0].isalpha() else pagename

        reply_content = (f"{pagename}的等待周期已到，分数仍未>0 ({rate})，因此它被删除\n"
                 '[[collapsible show="+ 查看源代码" hide="- 隐藏源代码"]]\n'
                 '[[code]]\n'
                 f"{neirong}\n"
                 '[[/code]]\n'
                 '[[/collapsible]]')
        print(f"Reply content:\n{reply_content}")
        
        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 删除页面
        
        more_button = wait.until(
            EC.element_to_be_clickable((By.ID, "more-options-button"))
        )
        more_button.click()

        delete_button = wait.until(
            EC.element_to_be_clickable((By.ID, "delete-button"))
        )
        delete_button.click()
        
        confirm_delete_radio = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='how'][value='delete']"))
        )
        confirm_delete_radio.click()
        
        confirm_delete_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn-primary[value='删除']"))
        )
        confirm_delete_button.click()
        
        # 处理弹出的网页弹窗
        alert = wait.until(EC.alert_is_present())
        alert.accept()
        
        time.sleep(3)

        # 在论坛发表新回复
        driver.get(fourmurl)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        new_post_button = wait.until(
            EC.element_to_be_clickable((By.ID, "new-post-button"))
        )
        new_post_button.click()
        
        reply_textarea = wait.until(
            EC.visibility_of_element_located((By.ID, "np-text"))
        )
        
        pyperclip.copy(reply_content)
        reply_textarea = wait.until(
            EC.visibility_of_element_located((By.ID, "np-text"))
        )
        reply_textarea.click()
        reply_textarea.send_keys(webdriver.Keys.CONTROL, 'v')
        
        submit_reply_button = driver.find_element(By.ID, "np-post")
        submit_reply_button.click()
        time.sleep(2)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        
    driver.quit()

if __name__ == "__main__":
    main()
