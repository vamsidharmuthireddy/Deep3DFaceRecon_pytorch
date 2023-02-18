from PIL import Image
import pandas as pd
import streamlit as st
import streamlit.components as stc
import os
from os.path import basename
# Utils
import base64
import time
import string
import random
from zipfile import ZipFile

timestr = time.strftime("%Y%m%d-%H%M%S")
# from test_2 import load_model, test_image
# from .options.base_options import BaseOptions


# input_dir_path = 'datasets/' + \
#     str(timestr) + ''.join(random.choices(string.ascii_letters, k=4))
input_dir_path = './datasets/examples'

results_dir_path = './checkpoints/demo_model/results/examples/epoch_20_000000'
os.makedirs(results_dir_path, exist_ok=True)
# results_dir_path = 'results'


def load_image(image_file):
    img = Image.open(image_file)
    return img


# class FileDownloader(object):
#     def __init__(self, data, filename="myfile", file_ext="txt"):
#         super(FileDownloader, self).__init__()
#         self.data = data
#         self.filename = filename
#         self.file_ext = file_ext

#     def download(self):
#         b64 = base64.b64encode(self.data.encode()).decode()
#         new_filename = "{}_{}_.{}".format(self.filename, timestr, self.file_ext)
#         st.markdown("#### Download File ###")
#         href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click Here!!</a>'
#         st.markdown(href, unsafe_allow_html=True)


def result_image_display(input_image_name):
    download_image_name = '.'.join([input_image_name.split('.')[0], 'png'])
    download_image_path = os.path.join(results_dir_path, download_image_name)

    if os.path.exists(download_image_path):

        st.image(load_image(download_image_path))


def download_result(input_image_name):

    download_image_name = '.'.join([input_image_name.split('.')[0], 'png'])
    download_image_path = os.path.join(results_dir_path, download_image_name)

    download_mat_name = '.'.join([input_image_name.split('.')[0], 'mat'])
    download_mat_path = os.path.join(results_dir_path, download_mat_name)

    download_obj_name = '.'.join([input_image_name.split('.')[0], 'obj'])
    download_obj_path = os.path.join(results_dir_path, download_obj_name)

    download_zip_name = '.'.join([input_image_name.split('.')[0], 'zip'])
    download_zip_path = os.path.join(results_dir_path, download_zip_name)

    with ZipFile(download_zip_path, 'w') as zipObj2:
       # Add multiple files to the zip
        zipObj2.write(download_image_path, download_image_name)
        zipObj2.write(download_mat_path, download_mat_name)
        zipObj2.write(download_obj_path, download_obj_name)

    st.download_button(label='Download Results',
                       data=open(download_zip_path, 'rb').read(),
                       file_name=download_zip_name,
                       mime='application/zip')


def image_uploader():
    st.subheader("Image")
    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
    input_image_path = None
    input_image_name = None

    if image_file is not None:
        # os.makedirs(input_dir_path, exist_ok=True)

        input_image_name = image_file.name
        # TO See details
        file_details = {
            "filename": input_image_name,
            "filetype": image_file.type,
            "filesize": image_file.size,
        }
        st.write(file_details)
        st.image(load_image(image_file), width=250)

        # Saving upload
        input_image_path = os.path.join(input_dir_path, input_image_name)
        with open(input_image_path, "wb") as f:
            f.write((image_file).getbuffer())

        st.success("File Saved")

    return input_image_path, input_image_name


def main():
    input_image_path, input_image_name = image_uploader()
    menu = ["Image"]

    # if st.button(label="Test"):
    #     os.system(
    #         "python test_2.py --name=demo_model --epoch=20 --img_folder=./datasets/examples")

    if input_image_path is not None and input_image_name is not None:
        if st.button(label="Test"):
            test_command = "python test_2.py --name=demo_model --epoch=20 --img_folder={INPUT_DIR_PATH} --img_name={IMAGE_NAME}".format(
                INPUT_DIR_PATH=input_dir_path, IMAGE_NAME=input_image_name)

            os.system(test_command)
            download_result(input_image_name=input_image_name)

            result_image_display(input_image_name=input_image_name)

        # image_downloader(input_image_name=input_image_name)
        # mat_downloader(input_image_name=input_image_name)
        # obj_downloader(input_image_name=input_image_name)

        # os.remove(input_image_path)

    # choice = st.sidebar.selectbox("Menu", menu)


#     if choice == "Text":
#         st.subheader("Text")
#         my_text = st.text_area("Your Message")
#         if st.button("Save"):
#             st.write(my_text)
#             download = FileDownloader(my_text).download()
#
#     elif choice == "CSV":
#         df = pd.read_csv("iris.csv")
#         st.dataframe(df)
#         download = FileDownloader(df.to_csv(),file_ext='csv').download()
if __name__ == "__main__":
    main()
