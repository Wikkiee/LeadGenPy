import openai
import json
import re
import traceback
from beaupy.spinners import *

class EmailContentGenerator:

    def generate(self,client_data):
        try:
            messages =[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Hey, can you help me generate lead content with the following details?"},
                        {"role": "assistant", "content": """Sure, I can help! Please provide the details in JSON format like this:
                                            {
                                            "My details": {
                                                "Name": "Vicky",
                                                "Title": "Developer",
                                                "Email Address": "contact@wikkie.com",
                                                "Contact Number ": "9876543210"
                                            },
                                            "My company": {
                                                "Company Name": "Wikkie Pvt Limited",
                                                "Website": "Wikkie.me"
                                            },
                                            "Targeted business details": {
                                                "business_name": "Kafe Himlavalvet",
                                                "business_address": "Drottninggatan 120, 113 60 Stockholm, Sweden",
                                                "business_email": "camilla@kafehimlavalvet.com",
                                                "mobile_number": "+46 8 31 40 41",
                                                "website_url": "kafehimlavalvet.se",
                                                "business_category": "Cafe",
                                                "ratings": "4.2",
                                                "review_counts": "296",
                                                "top_review_1": "null",
                                                "top_review_2": "null",
                                                "top_review_3": "null",
                                                "google_map_url": "https://www.google.com/maps/place/Kafe+Himlavalvet/data=!4m7!3m6!1s0x465f9d6f6a6fcddf:0xadca5aae3c412aa3!8m2!3d59.3418851!4d18.0547933!16s%2Fg%2F1tls1gfn!19sChIJ381vam-dX0YRoypBPK5ayq0?authuser=0&hl=en&rclk=1",
                                                "personalized_email_content": "null",
                                                "status": "null"
                                            }
                                            }"""},

                            {"role": "user", "content": """
                                Here are the details in JSON format:
                                                {
                                                "My details": {
                                                    "Name": "Vicky",
                                                    "Title": "Developer",
                                                    "Email Address": "contact@wikkie.com",
                                                    "Contact Number ": "9876543210"
                                                },
                                                "My company": {
                                                    "Company Name": "Wikkie Pvt Limited",
                                                    "Website": "Wikkie.me"
                                                },
                                                "Targeted business details": {
                                                    "business_name": "Kafe Himlavalvet",
                                                    "business_address": "Drottninggatan 120, 113 60 Stockholm, Sweden",
                                                    "business_email": "camilla@kafehimlavalvet.com",
                                                    "mobile_number": "+46 8 31 40 41",
                                                    "website_url": "kafehimlavalvet.se",
                                                    "business_category": "Cafe",
                                                    "ratings": "4.2",
                                                    "review_counts": "296",
                                                    "top_review_1": "null",
                                                    "top_review_2": "null",
                                                    "top_review_3": "null",
                                                    "google_map_url": "https://www.google.com/maps/place/Kafe+Himlavalvet/data=!4m7!3m6!1s0x465f9d6f6a6fcddf:0xadca5aae3c412aa3!8m2!3d59.3418851!4d18.0547933!16s%2Fg%2F1tls1gfn!19sChIJ381vam-dX0YRoypBPK5ayq0?authuser=0&hl=en&rclk=1",
                                                    "personalized_email_content": "null",
                                                    "status": "null"
                                                }
                                                
                                                }"""},

                        {"role": "assistant", "content": "Thanks for providing the details! Now, let me generate personalized email content for you. Give me a moment."},
                        {"role": "assistant", "content": """
                                            Certainly! Here's the lead content generated from the given details:

                                            ```json
                                            {
                                                "subject": "Exploring Exciting Opportunities for Collaboration Between Wikkie Pvt Limited and Kafe Himlavalvet",
                                                "content": "Dear Kafe Himlavalvet,\n\nI hope this email finds you well. My name is Vicky, and I am reaching out to you on behalf of Wikkie Pvt Limited. As a Developer at Wikkie, I am always on the lookout for innovative collaborations, and your company, Kafe Himlavalvet, has caught our attention.\n\nI recently came across Kafe Himlavalvet and was impressed by the outstanding reviews and ratings your cafe has garnered. The exceptional feedback, especially the reviews by Edwin Rijkaart, Cécile J, and Ulf Aspeqvist, highlights the unique experience and quality offerings at Kafe Himlavalvet. It's evident that your commitment to providing a delightful experience for customers aligns with the values we hold at Wikkie.\n\nHere are some key points that stood out to us\n\t-> Business Category - Cafe\n\t-> Ratings - 4.2\n\t-> Review Counts - 296\nTop Reviews\n\t-> Review By Edwin Rijkaart - What a great place for eating traditional Swedish waffles...\n\t-> Review By Cécile J - We loved it! It was a pleasant discovery after arriving on the hilltop...\n\t-> Review By Ulf Aspeqvist - What a view! You can see 360 around the horizon.\n\nYour dedication to creating a positive environment for customers is truly commendable. At Wikkie, we believe that collaboration is key to achieving mutual success. We have a range of innovative solutions that could potentially enhance the digital presence and overall experience for Kafe Himlavalvet.\n\nI would love to schedule a brief call at your convenience to discuss how Wikkie Pvt Limited can contribute to the continued success of Kafe Himlavalvet. Whether it's optimizing your website, implementing a mobile app, or exploring other digital solutions, we are eager to explore the possibilities together.\n\nPlease let me know a time that suits you, and I will make the necessary arrangements. Additionally, if you have any specific areas of interest or challenges you'd like us to address, feel free to share them so that our discussion can be more tailored to your needs.\n\nThank you for considering this collaboration, and I look forward to the opportunity to connect with you.\n\nBest regards,\n\nVicky\nDeveloper at Wikkie Pvt Limited\nwikkiedev@gmail.com\n9876543210"
                                            }
                                            ```
                                            Please note that this generated content is based on the given details. Feel free to customize it according to your preferences.   

                                            """},

                        {"role": "user", "content": """Looks, Great. Thanks for giving in json format 
                                            ,Now i want  you to help me generate lead content with the following details, 
                                            
                                            Here are the details in JSON format:
                                                                        {
                                                                        "My details": {
                                                                            "Name": "Vicky",
                                                                            "Title": "Developer",
                                                                            "Email Address": "contact@wikkie.com",
                                                                            "Contact Number ": "9876543210"
                                                                        },
                                                                        "My company": {
                                                                            "Company Name": "Wikkie Pvt Limited",
                                                                            "Website": "Wikkie.me"
                                                                        },
                                                                        "Targeted business details": """+ f"{client_data}"+"""
                                                                        
                                    }"""},]


            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            result = response["choices"][0]["message"]["content"]
        
            match_subject = re.search(r'"subject":\s*"([^"]+)"', result)
            subject = match_subject.group(1) if match_subject else None

            match_content = re.search(r'"content":\s*"([^}]+)"', result)
            content = match_content.group(1) if match_content else None

            return [subject,content]
        except Exception as error:
            traceback.print_exc()
            print(error)
            return []
            



