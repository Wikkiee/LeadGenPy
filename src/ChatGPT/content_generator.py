import Configs.chatgpt_config
import openai
import json

class EmailContentGenerator:
    __data = {
        "user": {
            "Name": "Vicky",
            "Title": "Developer",
            "Email Address": "contact@wikkie.com",
            "Contact Number ": "9876543210"
        },
        "company": {
            "Company Name": "Axe",
            "Website": "Wikkieeee.com"
        }
    }

    def generate(self,client_data):
        print("\n[LOG] - GENERATING CONTENT USING CHATGPT\n")
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"""
                            Create a personalized lead email content to reach out to the client company and return the response as JSON Formatted [
                                "subject":"  ",
                                "content": " " ]
                            Use the below details to build
                            My company data: [
                                {self.__data["company"]}
                            ]
                            The Client data:  [{client_data}]
                            My Data: [
                                {self.__data["user"]}
                            ]

                            *Use less \n\n in between the para and the 3-5 length paragraph is perferable*
        """}])
            content = json.loads(response["choices"][0]["message"]["content"]) 
            print("\n[LOG] - CONTENT READY\n")
            return list(content.values())
        except Exception as error:
            print(error)



