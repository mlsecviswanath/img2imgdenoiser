import os 
import torch
import random
from PIL import Image
from tqdm import tqdm
import shutil 
import numpy as np
from torchvision.utils import save_image
from diffusers import StableDiffusionUpscalePipeline, FluxImg2ImgPipeline, StableDiffusion3Img2ImgPipeline, StableDiffusionXLImg2ImgPipeline, AutoPipelineForImage2Image
from diffusers.utils import make_image_grid, load_image
from openai import OpenAI
import requests
import base64
import argparse

#login()
def seed_everything(seed=0):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

def getmodel(model):
    if model == "flux":
        pipeline = FluxImg2ImgPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16).to("cuda")
        return pipeline
    if model == "sd3":
        pipeline = StableDiffusion3Img2ImgPipeline.from_pretrained("stabilityai/stable-diffusion-3-medium-diffusers", torch_dtype=torch.float16, use_safetensors=True, requires_safety_checker=False, add_watermarker=False).to("cuda") 
        return pipeline
    if model == "sdxl":
        pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0", use_safetensors=True, safety_checker=False, add_watermarker=False).to("cuda") 
        return pipeline
    if model == "sd15":
        pipeline = AutoPipelineForImage2Image.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, variant="fp16", use_safetensors=True, safety_checker=None, requires_safety_checker=False, add_watermarker=False).to("cuda") 
        return pipeline
    if model == "gpt4o":
        client = OpenAI(api_key="Insert Your Own API Key Here")
        return client
def main():

    parser = argparse.ArgumentParser(description="For Denoising")

    parser.add_argument("--model", type=str, default='flux', choices=['flux','sd3','sdxl','sd15','gpt4o'])  
    parser.add_argument("--src", type=str, default='./source/') 
    parser.add_argument("--dest", type=str, default="./destination/") 
    parser.add_argument("--seed", type=int, default=0) 

    parser.add_argument("--strength", type=float, default=0.15)
    #parser.add_argument("--num_inf_steps", type=int, default=-1) 
    parser.add_argument("--prompt", type=str, default="")
    parser.add_argument("--neg_prompt", type=str, default="")
    parser.add_argument("--img_size", type=int, default=512, choices=[256,512])

    parser.add_argument("--full_prompts", type=int, default=0, choices=[0,1])

    # Parse the arguments
    args = parser.parse_args()

    print("Setting Seed: ", args.seed)
    seed_everything(args.seed)

    print("Setting Model: ", args.model)
    model = getmodel(args.model)

    if model == "gpt4o":
        print("Model is set to GPT-4o, please ensure the API key is set.")
    elif model == "flux" and args.neg_prompt != "":
        print("Model is set to FLUX, the negative prompt will be ignored as it is not supported.")

    src = args.src
    if not src.endswith("/"):
        src = src + "/"
    dest = args.dest
    if not dest.endswith("/"):
        dest = dest + "/"
    os.makedirs(dest,exist_ok=True)
    
    print("Source Folder: ", src)
    print("Destination Folder: ", dest)

    super_res = StableDiffusionUpscalePipeline.from_pretrained("stabilityai/stable-diffusion-x4-upscaler", torch_dtype=torch.float16, variant="fp16", use_safetensors=True, requires_safety_checker=False, add_watermarker=False)
    super_res.enable_model_cpu_offload()
    super_res.enable_xformers_memory_efficient_attention()

    if args.img_size == 256:
        print("Image Size: 256")
        print("Adding Stable Diffusion Upscale to pipeline.")
    else:
        print("Image Size: 512")
    
    if args.full_prompts == 1 and args.model != "gpt4o":
        print("Running with Pleimling et al.'s prompt combinations.")
        prompts = [("Denoise the image","Add noise to the image"),("Smoothen the image","Add noise to the image"),("Denoise the image while preserving the content of the image","Add noise to the image"),("Remove adversarial perturbations","Add noise to the image"),("Denoise the image","Add adversarial perturbation to the image"),("Smoothen the image","Add adversarial perturbation to the image"),("Denoise the image while preserving the content of the image","Add adversarial perturbation to the image"),("Remove adversarial perturbations","Add adversarial perturbation to the image")]
    else:
        if args.full_prompts == 1:
            print("Ignoring full_prompts. Please do not test more than one prompt at a time with GPT-4o.")
        if args.prompt == "":
            print("No Prompt.")
        else:
            print("Prompt: ", args.prompt)
            if args.neg_prompt != "":
                print("Negative Prompt: ", args_neg_prompt)
        prompts = [(args.prompt,args.neg_prompt)]
    print("Strength: ")
    print("=====")
    print("Starting...")
    allimages = sorted(os.listdir(src))
    gpt4oimageerrors = []
    
    
    for i in tqdm(allimages):
        if not i.endswith(".png") and not i.endswith(".jpg"):
            print("Skipping " + i + ". It is not a .png or .jpg image.")
            continue
        pmt_count = 0
        for pmt in prompts:
            if args.model == "gpt4o":
                try:
                    if args.img_size == 256:
                        image_0 = super_res(pmt[0],image=image_0).images[0]
                        image_0 = image_0.resize((512,512))
                        image_0 = image_0.save(src+"512_"+i)
                        input_path = os.path.join(src+"512_"+i)
                    else:
                        input_path = os.path.join(src+i)
                    result = model.images.edit(
                        model="gpt-image-1",
                        image=open(input_path, "rb"),
                        prompt=pmt[0],
                        size="1024x1024",
                        quality="high"
                    )
                    image_base64 = result.data[0].b64_json
                    image_bytes = base64.b64decode(image_base64)
                    with open(dest+"1024_"+i, "wb") as f:
                        f.write(image_bytes)
                    image_0 = Image.open(dest+"1024_"+i)
                    image_0 = image_0.resize((args.img_size,args.img_size))
                    image_0.save(dest+i)
                except Exception as e:
                    print(f"Error processing {i}: {e}")
                    gpt4oimageerrors.append(i)
                    continue 
            else:
                image_0 = Image.open(src+i)
                image_0 = image_0.resize((256,256)) #REMOVE LINE
                imgs_path_dest = os.path.join(dest+i)
                if args.img_size == 256:
                    image_0 = super_res(pmt[0],image=image_0).images[0]
                    image_0 = image_0.resize((512,512))
                image_1 = image_0
                if args.prompt == "":
                    output = model("", image=image_1, strength=args.strength, guidance_scale=1.0).images[0] 
                elif args.model == "flux" or args.neg_prompt == "":
                    output = model(pmt[0], image=image_1, strength=args.strength).images[0]
                else:
                    output = model(pmt[0], negative_prompt=pmt[1], image=image_1, strength=args.strength).images[0]
                output = output.resize((args.img_size,args.img_size))
                if args.full_prompts == 1:
                    pmt_count = pmt_count + 1
                    output.save(imgs_path_dest[:-4]+"_C"+str(pmt_count)+".png")
                    if args.model == "flux" and pmt_count == 4:
                        break
                else:
                    output.save(imgs_path_dest)
    if len(gpt4oimageerrors) > 0:
        print("Warning: The following images passed through GPT-4o have been rejected as inputs. Please examine them again.")
        print(gpt4oimageerrors)
    print("Finished!")
main()

