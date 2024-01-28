from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress
from web_scrapper.scrapper import Scrapper
from selenium import webdriver


def processInput(userInput, scrapper:Scrapper):
    console = Console(width=55)

    if(userInput == 1):
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ExtractDatabase",justify="center")
        console.print(Markdown("---"))

        business_name = Prompt.ask("Enter BusinessName", default="restaurants")
        location = Prompt.ask("Enter Location", default="sweden")
        limit = int( Prompt.ask("Set Limit", default="2") )

        console.print(Markdown("---"))
            
        driver:webdriver.Chrome = scrapper.getDriver()
        driver:webdriver.Chrome = scrapper.createDriver() if driver==None else driver

        with Progress() as progress:
            taskBar = progress.add_task("",total=limit)
            result = scrapper.getDataFromGoogleMap(business_name,location,limit, taskBar=taskBar,progress=progress)
            console.print(result)
            driver.close()
        
        return True

    if(userInput == 2):
        return True

    if(userInput == 3):
        return True

    if(userInput == 4):
        return True

    if(userInput == 5):
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][bold cyan]/[reset][red]Exit",justify="center")
        console.print(Markdown("---"))
        console.print("Thanks For Using Our Product",justify="center")
        console.print("For More Info Visit Our Web.\n",justify="center")
        console.print(" [bold underline green]@Wikkie[reset] [bold underline green]@ManojTGN",justify="center")
        console.print(Markdown("---"))
        return True

    return False


def main():
    console = Console(width=35)
    scrapper = Scrapper()
    userInput = -1

    while(userInput != 5):
        # console.clear()
        console.print("[bold green underline]LeadGenPy[reset] [cyan bold][Automation]",justify="center")
        console.print(Markdown("---"))
        console.print("1] Extract Dataset",justify="left")
        console.print("2] Show Dataset",justify="left")
        console.print("3] Personalized Email",justify="left")
        console.print("4] [bold]Production Mode\n",justify="left")
        console.print("5] [red]Exit💔",justify="left")
        console.print(Markdown("---"))

        userInput = -1
        while( not (userInput >= 1 and userInput <= 5) ):
            try:userInput = int( input() )
            except Exception as err:userInput = -1
        
        processInput(userInput, scrapper)

if __name__ == "__main__":
    main()
