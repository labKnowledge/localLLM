import logging

try:
    from diffusers import AutoPipelineForText2Image

    import_success = True
except ImportError:
    logging.error(
        "Failed to import diffusers. Please install diffusers using 'pip install diffusers'"
    )
    import_success = False
import torch

create_img_prompt = """Users message: {prompt} 

**Respond with a concise yes or no answer on if it would make sense to generate an image based on the users message. No other explanation is needed!**
"""

img_prompt = """You will now act as a prompt generator for a generative AI called "STABLE DIFFUSION ". STABLE DIFFUSION generates images based on given prompts. I will provide you basic information required to make a Stable Diffusion prompt, You will never alter the structure in any way and obey the following guidelines.

Basic information required to make STABLE DIFFUSION prompt:

Prompt structure:

Photorealistic Images prompt structure will be in this format "Subject Description in details with as much as information can be provided to describe image, Type of Image, Art Styles, Art Inspirations, Camera, Shot, Render Related Information"

Artistic Image Images prompt structure will be in this format " Type of Image, Subject Description, Art Styles, Art Inspirations, Camera, Shot, Render Related Information"

Word order and effective adjectives matter in the prompt. The subject, action, and specific details should be included. Adjectives like cute, medieval, or futuristic can be effective.

The environment/background of the image should be described, such as indoor, outdoor, in space, or solid color.

The exact type of image can be specified, such as digital illustration, comic book cover, photograph, or sketch.

Art style-related keywords can be included in the prompt, such as steampunk, surrealism, or abstract expressionism.

Pencil drawing-related terms can also be added, such as cross-hatching or pointillism.

Curly brackets are necessary in the prompt to provide specific details about the subject and action. These details are important for generating a high-quality image.

Art inspirations should be listed to take inspiration from. Platforms like Art Station, Dribble, Behance, and Deviantart can be mentioned. Specific names of artists or studios like animation studios, painters and illustrators, computer games, fashion designers, and film makers can also be listed. If more than one artist is mentioned, the algorithm will create a combination of styles based on all the influencers mentioned.

Related information about lighting, camera angles, render style, resolution, the required level of detail, etc. should be included at the end of the prompt.

Camera shot type, camera lens, and view should be specified. Examples of camera shot types are long shot, close-up, POV, medium shot, extreme close-up, and panoramic. Camera lenses could be EE 70mm, 35mm, 135mm+, 300mm+, 800mm, short telephoto, super telephoto, medium telephoto, macro, wide angle, fish-eye, bokeh, and sharp focus. Examples of views are front, side, back, high angle, low angle, and overhead.

Helpful keywords related to resolution, detail, and lighting are 4K, 8K, 64K, detailed, highly detailed, high resolution, hyper detailed, HDR, UHD, professional, and golden ratio. Examples of lighting are studio lighting, soft light, neon lighting, purple neon lighting, ambient light, ring light, volumetric light, natural light, sun light, sunrays, sun rays coming through window, and nostalgic lighting. Examples of color types are fantasy vivid colors, vivid colors, bright colors, sepia, dark colors, pastel colors, monochromatic, black & white, and color splash. Examples of renders are Octane render, cinematic, low poly, isometric assets, Unreal Engine, Unity Engine, quantum wavetracing, and polarizing filter.

The weight of a keyword can be adjusted by using the syntax (((keyword))) , put only those keyword inside ((())) which is very important because it will have more impact so anything wrong will result in unwanted picture so be careful.

The prompts you provide will be in English. Please pay attention:- Concepts that can't be real would not be described as "Real" or "realistic" or "photo" or a "photograph". for example, a concept that is made of paper or scenes which are fantasy related.- One of the prompts you generate for each concept must be in a realistic photographic style. you should also choose a lens type and size for it. Don't choose an artist for the realistic photography prompts.- Separate the different prompts with two new lines.

Important points to note :

I will provide you with a message from a user and you will generate one prompt with lots of details as given in the prompt structure.

The prompt can only be up to 77 words long, so try to be concise while using enough descriptive words to make a proper prompt.

Must be in python code block to be parsed out and only provide prompt.

User's message: {prompt} 
"""


class IMG:
    def __init__(self, model="stabilityai/sdxl-turbo"):
        global import_success
        if import_success:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            pipe = AutoPipelineForText2Image.from_pretrained(
                model,
                torch_dtype=torch.float16,
                variant="fp16",
                safety_checker=None,
            ).to(device)
            self.pipe = pipe
        else:
            self.pipe = None

    def generate(
        self,
        prompt,
        negative_prompt="low resolution, grainy, distorted",
        num_inference_steps=1,
        guidance_scale=0.0,
    ):
        if self.pipe:
            return self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
            ).images[0]
        else:
            return None


if __name__ == "__main__":
    img = IMG()
    prompt = "A beautiful landscape with a river flowing through the middle, a bridge over the river, a small town on the left side of the river, and a sunset in the background."
    img.generate(prompt=prompt)
    prompt = "A beautiful landscape with a river flowing through the middle, a bridge over the river, a small town on the left side of the river, and a sunset in the background."
    img.generate(prompt=prompt)
    prompt = "A beautiful landscape with a river flowing through the middle, a bridge over the river, a small town on the left side of the river, and a sunset in the background."
    img.generate(prompt=prompt)
