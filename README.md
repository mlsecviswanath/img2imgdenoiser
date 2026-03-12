# Off-The-Shelf Image-to-Image Models Are All You Need To Defeat Image Protection Schemes [IEEE SaTML '26]

**Official repository for the paper "Off-The-Shelf Image-to-Image Models Are All You Need To Defeat Image Protection Schemes". Accepted to IEEE SaTML 2026.**

## Abstract

Advances in Generative AI (GenAI) have led to the development of various protection strategies to prevent the unauthorized use of images. These methods rely on adding imperceptible protective perturbations to images to thwart misuse such as style mimicry or deepfake manipulations. Although previous attacks on these protections required specialized, purpose-built methods, we demonstrate that this is no longer necessary. We show that off-the-shelf image-to-image GenAI models can be repurposed as generic ``denoisers" using a simple text prompt, effectively removing a wide range of protective perturbations. Across 8 case studies spanning 6 diverse protection schemes, our general-purpose attack not only circumvents these defenses but also outperforms existing specialized attacks while preserving the image's utility for the adversary. Our findings reveal a critical and widespread vulnerability in the current landscape of image protection, indicating that many schemes provide a false sense of security. We stress the urgent need to develop robust defenses and establish that any future protection mechanism must be benchmarked against attacks from off-the-shelf GenAI models.

## Installation

The code in this repository is set up with a conda environment with **Python 3.8.19**.

Please run the following sequence of commands to fully install the environment:

```
conda env create -n denoise python=3.8.19
conda activate denoise
pip install -r requirements.txt
```

At least 1 GPU core is required and we recommend using an NVIDIA A100 or H200 GPU core.

## Denoising

Our denoising code can be run with the following command:

```
accelerate launch --num_processes=1 denoise_code.py
```

We also provide the following arguments:
**model** - The choice of model to load and denoise with. Must be one of **flux**, **sd3**, **sdxl**, **sd15**, and **gpt4o**. The **gpt4o** option requires an API key to OpenAI. A HuggingFace account is required to access and use some models. If you wish to integrate a custom model, internal code modification is needed. The default option is **flux**.

**src** - The source folder containing your input images. These images **MUST** be **256x256** or **512x512**.

**dest** - The destination folder to contain your denoised images.

**seed** - The random seed to freeze model randomness on. This is necessary to ensure reproducibility. The default value is **0**.

**strength** - The strength hyperparameter where higher strength modifies more of the image in the denoising process, yielding better performance but weaker utility. The default value is **0.15**.

**prompt** - The prompt to condition the denoising on. Not defining the prompt will perform non-prompt denoising where the guidance scale is also reduced to 1. The default prompt is an empty string.

**neg_prompt** - The prompt to condition the denoising against. This field is ignored if the model is **flux**, since FLUX does not support negative prompts. The default prompt is an empty string.

**img_size** - The image size of the images in your source folder. Must be one of **256** or **512**. The output images will match the dimensions of the input images. If the size is 256, Stable Diffusion Upscaling is performed to resize the image to **512** before denoising.

**full_prompts** - A binary flag indicating whether or not to run our prompts (C1-C8 in Table 1 in paper) all at once.  Must be either **0** (use single prompt) or **1** (run our prompts). The default value is **0**.

An example command where we use SD3 with strength 0.05 to denoise 512x512 images with our C5 combination is provided below:

```
accelerate launch --num_processes=1 denoise_code.py \
    --model sd3 \
    --src ./path_to_imgs/ \
    --dest ./denoised_imgs/ \
    --seed 0 \
    --strength 0.05 \
    --prompt "Denoise the image" \
    --neg_prompt "Add adversarial perturbation to the image" \
    --img_size 512
```

## Defenses

Note: For each defense, we plan to provide image datasets as well as setup and evaluation instructions so our main tables and figures can be reproduced.  This will be provided in a future update.

### UnGANable (USENIX Security 2023)
Paper: [UnGANable: Defending Against GAN-based Face Manipulation](https://www.usenix.org/conference/usenixsecurity23/presentation/li-zheng)
[GitHub](https://github.com/zhenglisec/UnGANable)

**Setup:**
Instructions Coming Soon...
**Denoising:**
Set **strength** to 0.025 and **img_size** to 256. Our best performing prompt combination is C6.
**Evaluation:**
Instructions Coming Soon...
**Image Dataset:**
Dataset Coming Soon...

### PRC Watermark (ICLR 2025)
Paper: [An Undetectable Watermark for Generative Image Models](https://arxiv.org/pdf/2410.07369)
[GitHub](https://github.com/XuandongZhao/PRC-Watermark)

**Setup:**
Instructions Coming Soon...
**Denoising:**
Set **strength** to 0.15 and **img_size** to 512. Our best performing prompt combination is C8.
**Evaluation:**
Instructions Coming Soon...
**Image Dataset:**
Dataset Coming Soon...

### VINE (ICLR 2025)
Paper: [Robust Watermarking Using Generative Priors Against Image Editing: From Benchmarking to Advances](https://arxiv.org/pdf/2410.18775)
[GitHub](https://github.com/Shilin-LU/VINE)

**Setup:**
Instructions Coming Soon...
**Denoising:**
Set **strength** to 0.25 and **img_size** to 512. Our best performing prompt combination is C6.
**Evaluation:**
Instructions Coming Soon...
**Image Dataset:**
Dataset Coming Soon...

### SIREN (IEEE S&P 2025)
Paper: [Towards Reliable Verification of Unauthorized Data Usage in Personalized Text-to-Image Diffusion Models](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=11023473)
[GitHub](https://github.com/AntigoneRandy/SIREN)

**Setup:**
Instructions Coming Soon...
**Denoising:**
Set **strength** to 0.35 and **img_size** to 512. Our best performing prompt combination is C6.
**Evaluation:**
Instructions Coming Soon...
**Image Dataset:**
Dataset Coming Soon...

### Mist
Paper: [Adversarial Example Does Good: Preventing Painting Imitation from Diffusion Models via Adversarial Examples](https://arxiv.org/pdf/2302.04578)
[GitHub](https://github.com/psyker-team/mist)

**Setup:**
Instructions Coming Soon...
**Denoising:**
Set **strength** to 0.15 and **img_size** to 512. We use prompt combination C8 and model **flux**.
**Evaluation:**
Instructions Coming Soon...
**Image Dataset:**
Dataset Coming Soon...

### Tree-Ring Watermark (NeurIPS 2025)
Paper: [Tree-Ring Watermarks: Fingerprints for Diffusion Images that are Invisible and Robust](https://proceedings.neurips.cc/paper_files/paper/2023/file/b54d1757c190ba20dbc4f9e4a2f54149-Paper-Conference.pdf)
[GitHub](https://github.com/YuxinWenRick/tree-ring-watermark)

**Setup:**
Instructions Coming Soon...
**Denoising:**
Set **strength** to 0.45 and **img_size** to 256. We use prompt combination C8 and model **flux**.  We also used model **gpt4o**.
**Evaluation:**
Instructions Coming Soon...
**Image Dataset:**
Dataset Coming Soon...

## Links

**Paper:** [Off-The-Shelf Image-to-Image Models Are All You Need To Defeat Image Protection Schemes](https://arxiv.org/abs/2602.22197)

**Website:** Coming Soon

**Authors:** [Xavier Pleimling](https://people.cs.vt.edu/xavierp7/), [Sifat Muhammad Abdullah](https://sifatmd.github.io), [Gunjan Balde](https://sites.google.com/view/baldegunjan/home), [Peng Gao](https://people.cs.vt.edu/penggao/), [Mainack Mondal](https://cse.iitkgp.ac.in/~mainack/), [Murtuza Jadliwala](https://sprite.utsa.edu/people/mjadliwala/), [Bimal Viswanath](https://people.cs.vt.edu/vbimal/)

## Changelog

This repository will receive updates over time to add instructions, data, etc.

March 12, 2026 - v0.1 - Released main denoising pipeline and used hyperparameters for each defense.

## Citation

```bibtex
@inproceedings{pleimling2026off,
author = {Xavier Pleimling and Sifat Muhammad Abdullah and Gunjan Balde and Peng Gao and Mainack Mondal and Murtuza Jadliwala and Bimal Viswanath},
title = {{Off-The-Shelf Image-to-Image Models Are All You Need To Defeat Image Protection Schemes}},
booktitle = {{USENIX Security Symposium (USENIX Security)}},
publisher = {IEEE},
year = {2026}
}
```