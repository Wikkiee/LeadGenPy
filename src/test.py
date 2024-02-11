from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing import Process

def open_new_tab():
    # Connect to the Selenium Grid server
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)
    print("Reached")

    driver.get("https://www.google.com")
    print("Done")
    # Perform other actions in the new tab
    driver.quit()

if __name__ == '__main__':
    # Spawn multiple processes, each opening a new tab using the shared driver
    processes = []
    for _ in range(4):
        process = Process(target=open_new_tab)
        process.start()
        processes.append(process)

    # Wait for all processes to finish
    for process in processes:
        process.join()
