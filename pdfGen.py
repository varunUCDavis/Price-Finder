from fpdf import FPDF
import tempfile
from PIL import Image

class GenPDF:

    HEADERFONTSZ = 30
    LINKFONTSZ = 16
    REGFONTSZ = 10
    PRICEFONTSZ = 20

    LOTX = 70 
    LOTWIDTH = 70
    INDWIDTH = 30

    BOXWIDTH = 80
    BOXHEIGHT = 42

    TEXTHEIGHT = 3

    ITEMMARGIN = 90

    x_pos = 99
    y_pos = 25


    pdf = FPDF()
    pdf.add_page()

    # header text
    pdf.set_font('Arial', 'B', HEADERFONTSZ)
    pdf.cell(0, 10, 'Price Breakdown', 0, 1, 'C')


    @classmethod
    def add_image_from_bytes(cls,img, x, y, w):
        # Create a temporary file to save the image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpeg') as tmp:
            # Write the bytes data to a temporary file
            img.save(tmp.name)
            # Add the image to the PDF using the path of the temporary file
            cls.pdf.image(tmp.name, x=x, y=y, w=w)


    @classmethod
    def generatePDF(cls, data):
        
        for lot in data:
            lot_image = lot[0]
            lot_size = lot[1]
            lot_link = lot[2]
            cropped_hat_data = lot[3]
            if cls.y_pos + cls.LOTWIDTH + 15 > 255:
                cls.pdf.add_page()
                cls.y_pos = 25

            # lot image and link
            cls.add_image_from_bytes(lot_image,x=cls.LOTX,y=cls.y_pos,w=cls.LOTWIDTH)
            cls.y_pos += cls.LOTWIDTH
            cls.x_pos = 99
            cls.pdf.set_xy(cls.x_pos,cls.y_pos)
            cls.pdf.set_font('Arial', 'B', cls.LINKFONTSZ)
            cls.pdf.cell(0,10, "Visit", ln=True, link=lot_link)
            cls.x_pos = 25
            cls.y_pos += 15

            for img_price_data in cropped_hat_data:
                img = img_price_data[0]
                price = img_price_data[1]
                if cls.x_pos > 140:
                    cls.x_pos = 25
                    cls.y_pos += 55
                if cls.y_pos > 255:  # Approximate limit for image bottom margin
                    cls.pdf.add_page()
                    cls.y_pos = 20  # Reset y position at the top of the new page

                # place individual hat image
                cls.add_image_from_bytes(img, x=cls.x_pos, y=cls.y_pos, w=cls.INDWIDTH)
                cls.pdf.set_font('Arial', 'B', cls.REGFONTSZ)
                cls.pdf.set_xy(cls.x_pos + cls.INDWIDTH ,cls.y_pos + 2)

                cls.pdf.cell(cls.BOXWIDTH/2,3, "Average Selling Price:") 
                cls.pdf.set_font('Arial', '', cls.PRICEFONTSZ)
                cls.pdf.set_xy(cls.x_pos + cls.BOXWIDTH/2 ,cls.y_pos + 10)
                cls.pdf.cell(cls.BOXWIDTH/2,cls.TEXTHEIGHT, f"${round(price, 2)}")
                cls.pdf.set_font('Arial', 'B', 10)
                cls.pdf.set_xy(cls.x_pos + cls.INDWIDTH ,cls.y_pos + 18)
                cls.pdf.cell(cls.BOXWIDTH/2,cls.TEXTHEIGHT, "Expected Profit: ")

                cls.pdf.set_font('Arial', '', cls.PRICEFONTSZ)
                cls.pdf.set_xy(cls.x_pos + cls.BOXWIDTH/2 ,cls.y_pos + 28)
                cls.pdf.cell(cls.BOXWIDTH/2,cls.TEXTHEIGHT, f"${round(price/lot_size, 2)}")

                cls.pdf.rect(cls.x_pos-5, cls.y_pos-5, cls.BOXWIDTH, cls.BOXHEIGHT)
                cls.x_pos += cls.ITEMMARGIN
            cls.y_pos += 55
            

        cls.pdf.output("Price_Breakdown.pdf")
