from mtcnn.mtcnn import MTCNN
from utils import *


cloth_examples = get_cloth_examples()
pose_examples = get_pose_examples()
face_detector = MTCNN()

# Description
title = r"""
<h1 align="center">TAO: Try Any Outfit</h1>
"""
css = """
.gradio-container {width: 85% !important}
"""

def onUpload():
    return ""


def onClick(cloth_image, cloth_id, pose_image, pose_id, category, 
        denoise_steps, caption, request: gr.Request):
    if pose_image is None:
        return None, "no pose image found !", ""
    if isinstance(cloth_id, dict):
        cloth_id = cloth_id['label']
    if isinstance(pose_id, dict):
        pose_id = pose_id['label']
    if len(pose_id)>0 and len(cloth_id)>0:
        res = get_result_example(cloth_id, pose_id)
        assert os.path.exists(res), res
        return res, "Done! Use the pre-run results directly, the cloth size does not take effect ", ""
    else:
        try:
            client_ip = request.client.host
            x_forwarded_for = dict(request.headers).get('x-forwarded-for')
            if x_forwarded_for:
                client_ip = x_forwarded_for
                
            faces = face_detector.detect_faces(pose_image[:,:,::-1])
            if len(faces)==0:
                print(client_ip, 'faces num is 0! ', flush=True)
                return None, "Fatal Error !!! No face detected in pose image !!! ", ""
            else:
                x, y, w, h = faces[0]["box"]
                H, W = pose_image.shape[:2]
                max_face_ratio = 1/3.3
                if w/W>max_face_ratio or h/H>max_face_ratio:
                    return None, "Fatal Error !!! Headshot is not allowed in pose image!!!", ""
            if not check_warp(client_ip):
                return None, "Failed !!! Our server is under maintenance, please try again tomorrow", ""
            
            infId = upload_imgs(ApiUrl, OpenId, ApiKey, client_ip, cloth_image, pose_image)
            if infId==0:
                return None, "fail to upload", ""
            elif infId==2:
                return None, "There is a running task already, please wait and check the history tab. Please remember to give us a star on github, thx~", ""

            isPub = publicFastSwap(ApiUrl, OpenId, ApiKey, infId, category, 
                caption, denoise_steps)
            if not isPub:
                return None, "fail to public you task", ""
            info =  "task has been created successfully, you can refresh the page 1~3 mins latter, and check the following history tab"
            return None, info, ""
        except Exception as e:
            print(e)
            return None, "fail to create task", ""

def onLoad(request: gr.Request):
    client_ip = request.client.host
    x_forwarded_for = dict(request.headers).get('x-forwarded-for')
    if x_forwarded_for:
        client_ip = x_forwarded_for
    his_datas = [None for _ in range(10)]
    info = ''
    try:
        infs = getAllFastInfs(ApiUrl, OpenId, ApiKey, client_ip)
        print(client_ip, 'history infs: ', len(infs))
        cnt = 0
        finish_n, fail_n, queue_n = 0, 0, 0
        for i, inf in enumerate(infs):
            if inf['state']==2:
                if cnt>4: continue
                pose, res = inf['pose'], inf['res']
                his_datas[cnt*2] = f"<img src=\"{pose}\" >"
                his_datas[cnt*2+1] = f"<img src=\"{res}\" >"
                finish_n += 1
                cnt += 1
            elif inf['state'] in [-1, -2, 0]:
                fail_n += 1
            elif inf['state'] in [1]:
                queue_n += 1
        info = f"{client_ip}, you have {finish_n} successed tasks, {queue_n} running tasks, {fail_n} failed tasks."
        if fail_n>0:
            info = info+" Please upload a half/full-body human image, not just a clothing image!!!"
        if queue_n>0:
            position = inf['position']
            info = info+" Wait for 3~10 mins and refresh this page, successed results will display in the history tab at the bottom. "
            info = info+f" your task position in queue is {position}. "
        time.sleep(3)
    except Exception as e:
        print(e)
    his_datas = his_datas + [info]
    return his_datas

with gr.Blocks(css=css) as demo:
    # description
    gr.Markdown(title)
    gr.Markdown(description)
                    
    with gr.Row():
        with gr.Column():
            with gr.Column():
                cloth_image = gr.Image(value=None, type="numpy", label="")
                cloth_id = gr.Label(value=cloth_examples[0][0], label="Clothing Image", visible=False)
                example = gr.Examples(inputs=[cloth_id, cloth_image],
                                      examples_per_page=3,
                                      examples = cloth_examples)
        with gr.Column():
            with gr.Column():
                pose_image = gr.Image(value=None, type="numpy", label="")
                pose_id = gr.Label(value=pose_examples[0][0], label="Pose Image", visible=False)
                example_pose = gr.Examples(inputs=[pose_id, pose_image],
                                          examples_per_page=3,
                                          examples=pose_examples)
        with gr.Column():
            with gr.Column():
                category = gr.Dropdown(value="upper_cloth", choices=["upper_cloth", 
                    "lower_cloth", "full_body", "dresses"], interactive=True)
                denoise_steps = gr.Slider(20, 30, value=20, interactive=True, label="denoise_steps")
                caption = gr.Textbox(value="", interactive=True, label='cloth caption')
                
                info_text = gr.Textbox(value="", interactive=False, label='runtime information')
                run_button = gr.Button(value="Run")
                init_res = get_result_example(cloth_examples[0][0], pose_examples[0][0])
                res_image = gr.Image(label="result image", value=None, type="filepath")
                MK01 = gr.Markdown()

    with gr.Tab('history'):

        with gr.Row():
            MK02 = gr.Markdown()

        with gr.Row():
            his_pose_image1 = gr.HTML()
            his_res_image1 = gr.HTML()

        with gr.Row():
            his_pose_image2 = gr.HTML()
            his_res_image2 = gr.HTML()

        with gr.Row():
            his_pose_image3 = gr.HTML()
            his_res_image3 = gr.HTML()            

        with gr.Row():
            his_pose_image4 = gr.HTML()
            his_res_image4 = gr.HTML()            

        with gr.Row():
            his_pose_image5 = gr.HTML()
            his_res_image5 = gr.HTML()            

    run_button.click(fn=onClick, inputs=[cloth_image, cloth_id, pose_image, 
        pose_id, category, denoise_steps, caption, ], 
        outputs=[res_image, info_text, MK01])

    pose_image.upload(fn=onUpload, inputs=[], outputs=[pose_id],)
    cloth_image.upload(fn=onUpload, inputs=[], outputs=[cloth_id],)
    demo.load(onLoad, inputs=[], outputs=[his_pose_image1, his_res_image1,
        his_pose_image2, his_res_image2, his_pose_image3, his_res_image3,
        his_pose_image4, his_res_image4, his_pose_image5, his_res_image5,
        MK02])

if _name_ == "_main_":

    demo.queue(max_size=50)
    demo.launch(server_name='0.0.0.0')