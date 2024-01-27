from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress

import time


def processInput(userInput):
    console = Console(width=55)

    if(userInput == 1):
        from web_scrapper.scrapper import get_data_from_google_map

        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ExtractDatabase",justify="center")
        console.print(Markdown("---"))

        business_name = Prompt.ask("Enter BusinessName", default="restaurants")
        location = Prompt.ask("Enter Location", default="sweden")
        limit = int( Prompt.ask("Set Limit", default="2") )

        console.print(Markdown("---"))
        with Progress() as progress:
            taskBar = progress.add_task("",total=limit)
            result = get_data_from_google_map(business_name,location,limit, taskBar=taskBar,progress=progress)

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
    userInput = -1

    while(userInput != 5):
        console.clear()
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
        
        processInput(userInput)

if __name__ == "__main__":
    main()
