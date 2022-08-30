#!/usr/bin/python3

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


def main():
    prompt = input("Prompt: ")
    filepath = input("Image file path: ")

    model_id = "CompVis/stable-diffusion-v1-4"
    device = "cuda"

    #pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_token=True)
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16, revision="fp16", use_auth_token=True
    )

    pipe = pipe.to(device)

    with autocast("cuda"):
        image = pipe(prompt, guidance_scale=7.5)["sample"][0]

    image.save(filepath)


if __name__ == "__main__":
    main()
