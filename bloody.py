
import csv
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import fitz
import google.generativeai as genai
import tempfile
import os
import pandas as pd
from pathlib import Path
import PIL


GEMINI_API = "AIzaSyA2XvdbTm6DkLpDwrVhpSS0qR-rVmc23Jc"


generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,

}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel('gemini-pro-vision',safety_settings=safety_settings,generation_config=generation_config)





def get_gemini_response(pdf_path,questions):
    try :

        blood_report = pdf2img(pdf_path)
        # blood_report_1 = Image.open("images/img4.jpeg")
        # blood_report_2 = Image.open("images/img3.jpeg")
        # blood_report_3 = Image.open("images/img2.jpeg")
        # blood_report_4 = Image.open("images/img1.jpeg")
        format = Image.open("images/format.jpg")
        response = model.generate_content([f"here you have a blood report , {questions} {format}" ,blood_report])
        return response.text

    except Exception as e:
        return (f"[-]error : {e}")


def pdf2img(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        image_list = []

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            image_list.append(page.get_pixmap())

        pdf_document.close()

        images = [
            Image.frombytes("RGB", (image.width, image.height), image.samples)
            for image in image_list
        ]

        # Combine all images vertically
        combined_image = Image.new(
            "RGB", (images[0].width, sum(image.height for image in images))
        )
        offset = 0

        for image in images:
            combined_image.paste(image, (0, offset))
            offset += image.height

        # Save the combined image
        combined_image.save("combinedimage_temp.jpeg", "JPEG")
        return combined_image

    except Exception as e:
        print(f"[-]Error during image conversion detection: {str(e)}")



def dataframe_management():
    bloody_df = pd.read_csv("bloody_csv.csv")
    print (bloody_df)

    bloody_df = bloody_df.reindex(columns=['Test', 'd', 'c', 'a'])

def get_hospitalname():

    report = Image.open("combinedimage_temp.jpeg")
    
    response = model.generate_content([f"just Extract the hospitel name and northing else  ",report])
    
    return response.text

    
def get_sampleid():
    report = Image.open("combinedimage_temp.jpeg")

    response = model.generate_content(["just extract the sample id and northing else",report])

    return response.text



#***********************************************8Driver*********************************************


pdf_path = "images/PDF1.pdf"
query= "give the response in .csv ,ignore the name field, any notes and other stuffs in the report, only consider the tests and start from hematology report with the format of "
# going for snack brb

bloody_csv= (get_gemini_response(pdf_path,query)).replace(" HEMATOLOGY REPORT,","")

print(bloody_csv)

hos_name = get_hospitalname()
sample_id = get_sampleid() 

filename = (f"csv/{hos_name}--{sample_id}.csv")

file = open(filename,"w")
file.writelines(bloody_csv)
file.close()

#dataframe_management()






    

















