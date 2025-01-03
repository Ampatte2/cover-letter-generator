from fpdf import FPDF
from PIL import Image, ImageOps
import yaml

with open("config.yaml") as stream:
    try:
        yamlObj = yaml.safe_load(stream)
        global body
        body = yamlObj.get("body")
        global photo_path 
        photo_path = yamlObj.get("photo_path")
        global first
        first = yamlObj.get("first")
        global last
        last = yamlObj.get("last")
        global email
        email = yamlObj.get("email ")
        global phone_number
        phone_number = yamlObj.get("phone_number")
        global applicant_name
        applicant_name=f'{first} {last}'
        for value in (body, photo_path): 
            if value == None:
                raise KeyError("Config missing keys")

    except yaml.YAMLError as exc:
        print("config.yaml does not exist or is invalid")

company_name = input("Company Name \n") 
hiring_manager = input("Hiring Manager \n") 
job_title= input("Job Title \n")
company_mission = f"I am drawn to {company_name.title()}'s mission and would welcome the opportunity to contribute and build a outstanding product."

class PDF(FPDF):
    def create_cover_letter(self):
        self.set_font("Times", "", 12)
        self.add_page()
        self.set_title(job_title)
        self.set_author(applicant_name)

        self.letter_header()
        self.letter_title()
        self.letter_body()
        self.letter_footer()
        self.output(f'{first}_{last}_{company_name.replace(" ", "_")}_cover_letter.pdf')

    def letter_header(self):
        self.set_fill_color(30, 58, 138)  
        self.rect(0, 0, self.w * 0.2, self.h, 'F')
        self.set_line_width(1)
        self.set_draw_color(251, 191, 36)
        self.ellipse(self.w * 0.1 - 15, 15, 30, 30)
        halfHeaderOffset = self.w * 0.1 - 15
        mask = Image.open('mask.webp').convert('L')
        im = Image.open(photo_path)
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        output.save('output.png')
        self.image("output.png", halfHeaderOffset, 15, 30, 30)

    def letter_title(self):
        self.set_font("Times", "B", 14)
        titleOffset = self.w * 0.2 + 5
        self.set_xy(titleOffset, 10)
        self.cell(0, 10, f'Dear {hiring_manager.title()},', ln=True)
        self.ln(5)
        self.set_x(titleOffset)
        self.set_margins(titleOffset,0, 5)
        self.set_font("Arial", "", 12)
        self.write(10, "My name is ")
        self.set_font("Arial", "B")
        self.write(10, applicant_name)
        self.set_font("Arial", "")
        self.write(10, f' and I\'m looking to discuss joining {company_name} as a {job_title}.')
        self.ln(15)

    def letter_body(self):
        titleOffset = self.w * 0.2 + 5
        self.set_x(titleOffset)
        self.set_margins(titleOffset,0, 5)
        sections = body + [company_mission]
        for section in sections:
            self.write(10, section)
            self.ln(15)

    def letter_footer(self):
        self.set_font("Arial", "I")
        self.write(10, "Best Regards,")
        self.ln(10)
        self.set_font("Arial", "")
        self.write(10, "Andrew Patterson")
        self.ln(10)
        self.set_text_color(30, 58, 138)
        self.write(10, f'Phone: {phone_number}', link=f'tel:{phone_number}')
        self.ln(10)
        self.write(10, f'Email: {email}', link=f'mailto:{email}')
        self.ln(10)
        self.set_font("Arial", "I")
        self.cell(0, 10, "LinkedIn: https://www.linkedin.com/in/andrewmpatterson", link="https://www.linkedin.com/in/andrewmpatterson", ln=1)
        self.cell(0, 10, "GitHub: https://github.com/ampatte2", link="https://github.com/ampatte2", ln=1)

pdf = PDF()

pdf.create_cover_letter()
