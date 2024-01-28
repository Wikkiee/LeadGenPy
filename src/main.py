
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress

import os
from Utils.store import get_all_data_from_json_file, insert_all_data_into_database
from web_scrapper.scrapper import getDataFromGoogleMap,get_business_email,get_organization_number,get_allabolag_details
from content_generator.personalized_email_sender import generatore_personalized_email_contents, send_personalized_emails
from Configs.database import is_database_connected

def processInput(userInput):
    console = Console(width=60)

    if(userInput == 1):
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ExtractDatabase",justify="center")
        console.print(Markdown("---"))

        business_name = Prompt.ask("Enter BusinessName", default="restaurants")
        location = Prompt.ask("Enter Location", default="sweden")
        limit = int( Prompt.ask("Set Limit", default="2") )

        console.print(Markdown("---"))

        with Progress() as progress:
            taskBar = progress.add_task("",total=limit)
            result = getDataFromGoogleMap(business_name,location,limit, taskBar=taskBar,progress=progress)
            progress.stop()

        console.print(f"[green]Scraped [cyan bold]{len(result)}[reset] [green]{business_name} Data Successfully!\n")
        return True

    if(userInput == 2):
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ShowDatabase",justify="center")
        console.print(Markdown("---"))
        get_all_data_from_json_file()
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if(userInput == 3):
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ShowDatabase", justify="center")
        console.print(Markdown("---"))
        insert_all_data_into_database( console=console )
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if(userInput == 4):
        console.width = 100
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ScrapeEmail", justify="center")
        console.print(Markdown("---"))
        get_business_email(console=console)
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if (userInput == 5):
        console.width = 80
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ScrapeOrgNumber", justify="center")
        console.print(Markdown("---"))
        get_organization_number(console=console)
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if (userInput == 6):
        console = Console()
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ScrapeAllabolag",justify="center")
        console.print(Markdown("---"))
        get_allabolag_details(console=console)
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if (userInput == 7):
        console.width = 60
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]GeneratePersonalizedEmail",justify="center")
        console.print(Markdown("---"))
        generatore_personalized_email_contents(console=console)
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if (userInput == 8):
        console = Console()
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]SendPersonalizedEmail",justify="center")
        console.print(Markdown("---"))
        send_personalized_emails(console=console)
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if (userInput == 9):
        console.print("[yellow]warning:[reset]THE PRODUCTION MODE IS IN DEVELOPMENT!")
        # getDataFromGoogleMap()
        # get_all_data_from_json_file()
        # insert_all_data_into_database()
        # get_business_email()
        # get_organization_number()
        # get_allabolag_details()
        return True

    if(userInput == 0):
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
    console = Console(width=40)
    userInput = -1
    if not is_database_connected():
        console.print("[red]❌ Database Is Not Connected!")
        return

    while(userInput != 0):
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset] [cyan bold][Automation]",justify="center")
        console.print(Markdown("---"))
        console.print("1] Extract Dataset",justify="left")
        console.print("2] Show Dataset",justify="left")
        console.print("3] Save Into Database",justify="left")
        console.print("4] Scrape Email From Site",justify="left")
        console.print("5] Scrape Organization Number",justify="left")
        console.print("6] Scrape Allabolag Number",justify="left")
        console.print("7] Generate Personalized EmailContent",justify="left")
        console.print("8] Send Personalized Email",justify="left")
        console.print("9] [bold]Production Mode\n",justify="left")
        console.print("0] [red]Exit💔",justify="left")
        console.print(Markdown("---"))

        userInput = -1
        while( not (userInput >= 0 and userInput <= 9) ):
            try:userInput = int( input() )
            except Exception as err:userInput = -1
        
        processInput(userInput)

if __name__ == "__main__":
    main()
