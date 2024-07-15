import os
import sys
import cv2
import json
import random
import time
import requests
import func_timeout
import numpy as np
import gradio as gr


ApiUrl = os.environ['ApiUrl']
OpenId = os.environ['OpenId']
ApiKey = os.environ['ApiKey']
OssUrl = os.environ['OssUrl']
Regions = os.environ['Regions']


proj_dir = os.path.dirname(os.path.abspath(_file_))
data_dir = os.path.join(proj_dir, 'Datas')
# data_dir = "Datas"
tmpFolder = "tmp"
os.makedirs(tmpFolder, exist_ok=True)


def get_cloth_examples():
    cloth_dir = os.path.join(data_dir, 'ClothImgs')
    examples = []
    files = sorted(os.listdir(cloth_dir))
    # files = sorted(os.listdir(cloth_dir))[::-1]
    for f in files:
        cloth_id = f
        cloth_path = os.path.join(cloth_dir, f)
        examples.append([cloth_id, cloth_path])
    examples = examples[::-1]
    return examples

def get_pose_examples():
    pose_dir = os.path.join(data_dir, 'PoseImgs')
    examples = []
    for f in os.listdir(pose_dir):
        pose_id = f
        pose_path = os.path.join(pose_dir, f)
        examples.append([pose_id, pose_path])
    return examples

def get_result_example(cloth_id, pose_id):
    result_dir = os.path.join(data_dir, 'ResultImgs')
    res_path = os.path.join(result_dir, f"{cloth_id}_{pose_id}")
    return res_path

def getAllFastInfs(apiUrl, openId, apiKey, clientIp):
    params = {'openId':openId, 'apiKey':apiKey, 'ipId':clientIp, 'page':0}
    session = requests.session()
    ret = requests.post(f"{apiUrl}/api/inf/get_batch_fast_results", data=json.dumps(params))
    res = []
    if ret.status_code==200:
        if 'data' in ret.json():
            records = ret.json()['data']['records']
            for record in records:
                res.append({'pose':OssUrl+record['bodyUrl']+"?thumbnail/768x768>", 
                    'res':OssUrl+record['showUrl']+"?thumbnail/768x768>",
                    'state':int(record['state']), 
                    'position':int(record['position'])})
    return res

def upload_imgs(apiUrl, openId, apiKey, clientIp, cloth_image, pose_image):
    folder = os.path.join(tmpFolder, clientIp.replace(".", ""))
    os.makedirs(folder, exist_ok=True)
    pose_path = os.path.join(folder, 'pose.jpg')
    cloth_path = os.path.join(folder, 'cloth.jpg')
    cv2.imwrite(pose_path, pose_image[:,:,::-1])
    cv2.imwrite(cloth_path, cloth_image[:,:,::-1])

    params = {'openId':openId, 'apiKey':apiKey, 'ipId':clientIp, 
        'poseFileName':os.path.basename(pose_path), 
        'clothFileName':os.path.basename(cloth_path), 
        'maskFileName':''}
    session = requests.session()
    ret = requests.post(f"{apiUrl}/api/inf/fastinf_upload", data=json.dumps(params))
    res = 0
    if ret.status_code==200:
        if 'data' in ret.json():
            data = ret.json()['data']
            if data['cod'] in [2, 3]: return data['cod']
            with open(cloth_path, 'rb') as file:
                response = requests.put(data['clothUrl'], data=file)
            with open(pose_path, 'rb') as file:
                response = requests.put(data['poseUrl'], data=file)
            if os.path.exists(pose_path): os.remove(pose_path)
            if os.path.exists(cloth_path): os.remove(cloth_path)
            return data['infId']
    return res

def publicFastSwap(apiUrl, openId, apiKey, infId, category, caption, denoise_steps):
    if category=="upper_cloth":
        category = 1
    elif category=="lower_cloth":
        category = 2
    elif category=="dresses":
        category = 3
    elif category=="full_body":
        category = 4
    params = {'openId':OpenId, 'apiKey':ApiKey, 'infId':infId, 
        'denoise_steps':int(denoise_steps), 'auto_mask':1, 'auto_crop':1, 
        'category':category, 'caption':caption, 'notifyUrl':''}
    session = requests.session()
    ret = requests.post(f"{ApiUrl}/api/inf/public_fastinf", data=json.dumps(params))
    if ret.status_code==200:
        if 'data' in ret.json():
            """
                [Success] An example returns the result
                {'code': 200, 'msg': 'ok', 'data': True}
            """
            print('public task successfully!')
            return ret.json()['data']

def getFastInfRes(apiUrl, openId, apiKey, infId):
    params = {'openId':openId, 'apiKey':apiKey, 'infId':infId}
    session = requests.session()
    ret = requests.get(f"{apiUrl}/api/inf/get_fast_result", params=params)
    if ret.status_code==200:
        if 'data' not in ret.json():
            return 0
        return ret.json()['data']
    else:
        return 0

@func_timeout.func_set_timeout(10)
def check_func(ip):
    session = requests.session()
    ret = requests.get(f"https://webapi-pc.meitu.com/common/ip_location?ip={ip}")
    for k in ret.json()['data']:
        nat = ret.json()['data'][k]['nation']
        if nat.lower() in Regions.lower():
            print(nat, 'invalid')
            return False
        else:
            print(nat, 'valid')
    return True
def check_warp(ip):
    try:
        return check_func(ip)
    except Exception as e:
        print(e)
        return True