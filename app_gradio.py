import numpy as np
import gradio as gr
import os
import random
import time
import string
from landmark_detector import detect_landmark_points
import shutil
from zipfile import ZipFile

timestr = time.strftime("%Y%m%d-%H%M%S")


input_dir_name = str(timestr) + \
    ''.join(random.choices(string.ascii_letters, k=4))
input_dir_path = os.path.join('datasets', input_dir_name)

landmark_dir_path = os.path.join(input_dir_path, 'detections')

results_dir_path = os.path.join(
    './checkpoints/demo_model/results', input_dir_name, 'epoch_20_000000')

os.makedirs(results_dir_path, exist_ok=True)
os.makedirs(input_dir_path)
os.makedirs(landmark_dir_path)


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

    return download_image_path, download_zip_path


def generate_landmark_points(path):
    if os.path.exists(path):

        img_name = path.split(os.sep)[-1]
        img_path = os.path.join(input_dir_path, img_name)

        det_name = '.'.join([img_name.split('.')[0], 'txt'])
        det_path = os.path.join(landmark_dir_path, det_name)

        shutil.move(path, img_path)

        detect_landmark_points(img_path=img_path, file_path=det_path)

        return input_dir_path, img_path, det_path


def test(path, img_out, file):
    input_dir_path, img_path, det_path = generate_landmark_points(path)

    input_image_name = img_path.split(os.sep)[-1]
    print(input_image_name)

    if img_path is not None and img_path is not None:
        test_command = "python3 test_2.py --name=demo_model --epoch=20 --img_folder={INPUT_DIR_PATH} --img_name={IMAGE_NAME}".format(
            INPUT_DIR_PATH=input_dir_path, IMAGE_NAME=input_image_name)

        os.system(test_command)
        download_image_path, download_zip_path = download_result(
            input_image_name=input_image_name)

        return download_image_path, download_zip_path


demo = gr.Blocks()


with demo:
    gr.Markdown(
        """
    <h2 style="text-align: center;">P2 E-Pro Avatar System</h3>
    <h3 style="text-align: center;">This is a sample project that takes any custom image as input and generate accurate 3D face reconstruction.</h3>
    """
    )

    img = gr.Image(type="filepath")

    btn = gr.Button(value="Generate Results")

    with gr.Column():
        gr.Markdown(
            """

            <p style="text-align: center;">Generated Results for 3D face reconstruction</p>
            
        """
        )

        with gr.Row():
            # , visible=False)
            img_out = gr.Image(type="filepath", label='Generated Image')
            file = gr.File(label='Generated Files')  # visible=False)

    btn.click(test, inputs=[img], outputs=[img_out, file])

    # img = gr.Image(echo_image, gr.Image(type="filepath", shape=(300, 200)),
    #                gr.Image(shape=(300, 200)))

    # txt_2 = gr.Textbox(label="Second Name")
    # txt_3 = gr.Textbox(value="", label="Output")


demo.launch(share=True)


title = "Ask Rick a Question"
description = """
The bot was trained to answer questions based on Rick and Morty dialogues. Ask Rick anything!
<img src="https://huggingface.co/spaces/course-demos/Rick_and_Morty_QA/resolve/main/rick.png" width=200px>
"""

article = "Check out [the original Rick and Morty Bot](https://huggingface.co/spaces/kingabzpro/Rick_and_Morty_Bot) that this demo is based off of."

gr.Interface(
    fn=predict,
    inputs="textbox",
    outputs="text",
    title=title,
    description=description,
    article=article,
    examples=[["What are you doing?"], ["Where should we time travel to?"]],
).launch()
