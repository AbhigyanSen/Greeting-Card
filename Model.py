'''
REQUIREMENTS
pip install diffusers torch accelerate
'''

# IMPORTING LIBRARIES AND MODEL
import pandas as pd
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from PIL import Image
from PIL import ImageDraw, ImageFont, ImageChops
import cv2

# Loading Stable Diffusion Model
# model_id = "stabilityai/stable-diffusion-2"
# scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
# pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
# pipe = pipe.to("cuda")