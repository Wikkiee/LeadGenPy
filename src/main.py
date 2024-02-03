import asyncio
import os
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress
from rich.prompt import Prompt

from Configs.database import is_database_connected, get_database_connection
from Utils.store import get_all_data_from_json_file, insert_all_data_into_database, export_database_into_csv_dataset
from content_generator.personalized_email_sender import generatore_personalized_email_contents, send_personalized_emails
from web_scrapper.scrapper import scrape_data_from_google_map, scrape_business_email, scrape_organization_number, \
    scrape_allabolag_details


def process_input(user_input):
    console = Console(width=60)

    if user_input == 1:
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ExtractDatabase",
                      justify="center")
        console.print(Markdown("---"))

        business_name = Prompt.ask("Enter BusinessName", default="restaurants")
        location = Prompt.ask("Enter Location", default="sweden")
        limit = int(Prompt.ask("Set Limit", default="2"))

        console.print(Markdown("---"))

        with Progress() as progress:
            task_bar = progress.add_task("", total=limit)
            result = scrape_data_from_google_map(business_name, location, limit, task_bar=task_bar, progress=progress,
                                                 console=console)
            progress.stop()
            console.print(
                f"[green]🎉 Completed scrape_data_from_google_map! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")

        return True

    if user_input == 2:
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ShowDatabase", justify="center")
        console.print(Markdown("---"))
        result = get_all_data_from_json_file()
        console.print(
            f"[green]🎉 Completed get_all_data_from_json_file! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")

        console.print(Markdown("---"))
        os.system("pause")
        return True

    if user_input == 3:
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ShowDatabase", justify="center")
        console.print(Markdown("---"))
        result = insert_all_data_into_database(console=console)
        console.print(
            f"[green]🎉 Completed insert_all_data_into_database! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")

        console.print(Markdown("---"))
        os.system("pause")
        return True

    if user_input == 4:
        console.width = 100
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ScrapeEmail", justify="center")
        console.print(Markdown("---"))
        result = asyncio.run(scrape_business_email(console=console))
        console.print(f"[green]🎉 Completed scrape_business_email!\n [yellow]🔎 Time Taken:[reset]{result['time_taken']:.2f}sec | [yellow]Network Usage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if user_input == 5:
        console.width = 80
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ScrapeOrgNumber", justify="center")
        console.print(Markdown("---"))
        result = scrape_organization_number(console=console)
        console.print(f"[green]🎉 Completed scrape_organization_number! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if user_input == 6:
        console = Console()
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ScrapeAllabolag",
                      justify="center")
        console.print(Markdown("---"))
        result = scrape_allabolag_details(console=console)
        console.print(
            f"[green]🎉 Completed scrape_allabolag_details! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")

        console.print(Markdown("---"))
        os.system("pause")
        return True

    if user_input == 7:
        console.width = 60
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]GeneratePersonalizedEmail",
                      justify="center")
        console.print(Markdown("---"))
        result = generatore_personalized_email_contents(console=console)
        console.print(
            f"[green]🎉 Completed generatore_personalized_email_contents! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")

        console.print(Markdown("---"))
        os.system("pause")
        return True

    if user_input == 8:
        console = Console()
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]SendPersonalizedEmail",
                      justify="center")
        console.print(Markdown("---"))
        result = send_personalized_emails(console=console)
        console.print(
            f"[green]🎉 Completed send_personalized_emails! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")

        console.print(Markdown("---"))
        os.system("pause")
        return True

    if user_input == 9:
        console = Console()
        console.clear()
        console.print("[cyan bold]SELECT THE MODE[reset]", justify="left")
        console.print(Markdown("---"))
        console.print("1] Base Production Mode", justify="left")
        console.print("2] Pro Production Mode (Chat GPT Powered) ", justify="left")
        console.print("3] Ultra Production Mode (Outreach)\n", justify="left")
        console.print("4] Exit Production Mode", justify="left")
        console.print(Markdown("---"))
        mode = 1
        try:
            mode = int(input())
        except:
            process_input(9)
            return

        if mode not in [1,2,3,4]:
            print('invalid')
            process_input(9)
            return
        if mode == 4: return True
        console.clear()

        if mode == 1:
            console.print("[yellow]WARN:[reset]THE PRODUCTION MODE IS IN DEVELOPMENT | BASE PRODUCTION MODE!")
        elif mode == 2:
            console.print("[yellow]WARN:[reset]THE PRODUCTION MODE IS IN DEVELOPMENT | GPT POWERED MODE!")
        else:
            console.print("[yellow]WARN:[reset]THE PRODUCTION MODE IS IN DEVELOPMENT | OUTREACH MODE!")

        total_result = {"time_taken": 0, "memory_usage": 0, 'network_usage': 0}
        with console.status(
                "[bold yellow]Scrapping Data From The Google Map... [green](opening chrome driver)") as status:
            result = scrape_data_from_google_map(limit=20, status=status)
            total_result['time_taken'] += result['time_taken']
            total_result['network_usage'] += result['network_usage']
            console.print(
                f"[green]🎉 Completed scrape_data_from_google_map! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")
            status.update(f"[bold yellow]Inserting Data Into Database...")
            result = insert_all_data_into_database(status=status)
            total_result['time_taken'] += result['time_taken']
            total_result['network_usage'] += result['network_usage']
            console.print(
                f"[green]🎉 Completed insert_all_data_into_database! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")
            status.update(f"[bold yellow]Scrapping Business Email...")
            result = scrape_business_email(status=status)
            total_result['time_taken'] += result['time_taken']
            total_result['network_usage'] += result['network_usage']
            console.print(
                f"[green]🎉 Completed scrape_business_email! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")
            status.update(f"[bold yellow]Scrapping Organization Number...")
            result = scrape_organization_number(status=status)
            total_result['time_taken'] += result['time_taken']
            total_result['network_usage'] += result['network_usage']
            console.print(
                f"[green]🎉 Completed scrape_organization_number! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")
            status.update(f"[bold yellow]Scrapping Allabolag Details...")
            result = scrape_allabolag_details(status=status)
            total_result['time_taken'] += result['time_taken']
            total_result['network_usage'] += result['network_usage']
            console.print(
                f"[green]🎉 Completed scrape_allabolag_details! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")
            status.update(f"[bold yellow]Generating Personalized Email...")

            if mode == 2 or mode == 3:
                result = generatore_personalized_email_contents(status=status)
                total_result['time_taken'] += result['time_taken']
                total_result['network_usage'] += result['network_usage']
                console.print(
                    f"[green]🎉 Completed generate_personalized_email_contents! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")

            if mode == 3:
                status.update(f"[bold yellow]Sending Personalized Email...")
                result = send_personalized_emails(progress_status=status)
                total_result['time_taken'] += result['time_taken']
                total_result['network_usage'] += result['network_usage']
                console.print(
                    f"[green]🎉 Completed send_personalized_emails! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")

            status.stop()
        console.print(
            f"[green]🎉 Everything Is Completed Successfully!\n\n[bold green]Total Statistics:\n\t[reset]TimeTaken: [yellow]{total_result['time_taken']:.2f}[reset] sec\n\tNetworkUsage: [yellow]{(total_result['network_usage'] / 1000000):.3f}[reset] megabytes\n")
        console.print(Markdown("---"))
        os.system("pause")
        return True

    if user_input == 10:
        console = Console()
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow] Export CSV DATASET",
                      justify="center")
        console.print(Markdown("---"))
        result = export_database_into_csv_dataset(console=console)
        console.print(
            f"[green]🎉 Completed export_database_into_csv_dataset ! \n[yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")

        console.print(Markdown("---"))
        os.system("pause")
        return True

    if user_input == 0:
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][bold cyan]/[reset][red]Exit", justify="center")
        console.print(Markdown("---"))
        console.print("Thanks For Using Our Product", justify="center")
        console.print("For More Info Visit Our Web.\n", justify="center")
        console.print(" [bold underline green]@Wikkie[reset] [bold underline green]@ManojTGN", justify="center")
        console.print(Markdown("---"))
        return True
    return False


def main():
    console = Console(width=40)
    user_input = -1
    if not is_database_connected():
        console.print("[red]🚨 Database Is Not Connected!")
        return None
        # exit(1)
    try:
        requests.get("https://1.1.1.1").status_code
    except requests.exceptions.ConnectionError as e:
        console.print("[red]🚨 Internet Is Not Connected!")
        return  None

    while user_input != 0:

        console.print("[bold green underline]LeadGenPy[reset] [cyan bold][Automation]", justify="center")
        console.print(Markdown("---"))
        console.print("1] Extract Dataset", justify="left")
        console.print("2] Show Dataset", justify="left")
        console.print("3] Save Into Database", justify="left")
        console.print("4] Scrape Email From Site", justify="left")
        console.print("5] Scrape Organization Number", justify="left")
        console.print("6] Scrape Allabolag Number", justify="left")
        console.print("7] Generate Personalized EmailContent", justify="left")
        console.print("8] Send Personalized Email", justify="left")
        console.print("9] [bold]Production Mode", justify="left")
        console.print("10] [bold]Export Database into CSV Dataset\n", justify="left")
        console.print("0] [red]Exit💔", justify="left")
        console.print(Markdown("---"))

        user_input = -1
        while not (0 <= user_input <= 10):
            try:
                user_input = input()
                if user_input == "clear":
                    connection = get_database_connection()
                    cursor = connection.cursor()
                    cursor.execute("TRUNCATE TABLE headcounts")
                    cursor.execute("TRUNCATE TABLE revenue_track")
                    cursor.execute("SET foreign_key_checks = 0")
                    cursor.execute("TRUNCATE TABLE allabolag")
                    cursor.execute("TRUNCATE TABLE leads")
                    cursor.execute("SET foreign_key_checks = 1")
                    connection.commit()
                    cursor.close()
                    connection.close()
                    print("Tables has been cleared successfully !.")
                    user_input = -1
                    break
                user_input = int(user_input)
            except Exception:
                user_input = -1

        process_input(user_input)


if __name__ == "__main__":
    main()
