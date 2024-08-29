import os
import sys
import json
import requests
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
from dotenv import load_dotenv


load_dotenv()

username = os.environ.get("APIUSERNAME")
password = os.environ.get("APIPASSWORD")

api_url = "https://api.imgflip.com/caption_image"

with open("memes.json", "r") as meme_db:
    data = json.load(meme_db)

meme_list = []

for meme in data:
    id_value = meme["ID"]
    meme_name = meme["Name"]
    alt_names = meme["Alternate Names"]
    meme_list.append((id_value, meme_name))


class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        # Replace "myform.ui" with the path to your .ui file
        loadUi("design.ui", self)

        for meme in data:
            id_value = meme["ID"]
            meme_name = meme["Name"]
            self.meme_box.addItem(meme_name, id_value)

        self.meme_box.currentIndexChanged.connect(self.handleComboBoxChange)

        # Load the image
        pixmap = QPixmap("demo_meme.jpg")

        # Get the aspect ratio of the image
        aspect_ratio = pixmap.width() / pixmap.height()

        # Get the QLabel object
        self.image_label = self.findChild(QLabel, "sample_image")

        # Set the pixmap and adjust the aspect ratio
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))

        # Maek Button Handler
        self.make_btn.clicked.connect(self.make_meme)

        # Initialize selected_meme_id attribute
        self.selected_meme_id = None

    def handleComboBoxChange(self, index):
        # Get the selected item's text and value
        item_text = self.meme_box.currentText()
        item_value = self.meme_box.itemData(index)
        print("Selected Item:", item_text)
        print("Selected Value:", item_value)
        self.selected_meme_id = item_value

    def make_meme(self):
        text_01 = self.text_line_01.toPlainText()
        text_02 = self.text_line_02.toPlainText()
        if self.selected_meme_id is not None:
            meme_id = self.selected_meme_id
            meme_url = self.gen_meme(meme_id, text_01, text_02)
            if meme_url is not None:
                self.display_image_from_url(meme_url)
                print("Meme URL:", meme_url)

        elif self.selected_meme_id is None:
            QMessageBox.information(
                self, "Message", "Please select a meme to edit.")

    def gen_meme(self, template_id, text1, text2):
        api_data = {
            "template_id": template_id,
            "username": username,
            "password": password,
            "text0": text1,
            "text1": text2
        }

        api_response = requests.post(url=api_url, data=api_data)

        if api_response.status_code == 200:
            # Request was successful
            api_response = api_response.json()
            if str(api_response['success']) == "True":
                generated_meme_url = api_response['data']['url']
                print("Success")
                print(f"Meme URL : {generated_meme_url}")
                return generated_meme_url

            else:
                print(api_response)

        else:
            # Request was not successful
            print("POST request failed!")
            print("Response status code:", api_response.status_code)
            return None

    def display_image_from_url(self, url):
        # Download the image from the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Convert the downloaded image data to QPixmap
            image_data = response.content
            image = QImage.fromData(image_data)

            # Set the pixmap and adjust the aspect ratio
            self.image_label.setPixmap(QPixmap.fromImage(image).scaled(
                self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        else:
            print("Failed to download image from URL:", url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(app.exec_())
