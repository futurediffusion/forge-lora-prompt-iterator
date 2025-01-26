import os
import json
import copy
import random
import math

import gradio as gr
from PIL import Image, ImageDraw, ImageFont

from modules import sd_samplers, errors, scripts, images, sd_models
from modules.paths_internal import roboto_ttf_file
from modules.processing import Processed, process_images
from modules.shared import state, cmd_opts, opts
from pathlib import Path

lora_dir = Path(cmd_opts.lora_dir).resolve()


def allowed_path(path):
    return Path(path).resolve().is_relative_to(lora_dir)


def get_base_path(is_use_custom_path, custom_path):
    return lora_dir.joinpath(custom_path) if is_use_custom_path else lora_dir


def is_directory_contain_lora(path):
    try:
        if allowed_path(path):
            safetensor_files = [f for f in os.listdir(
                path) if f.endswith('.safetensors')]
            return len(safetensor_files) > 0
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)
    return False


def get_directories(base_path, include_root=True):
    directories = ["/"] if include_root else []
    try:
        if allowed_path(base_path):
            for entry in os.listdir(base_path):
                full_path = os.path.join(base_path, entry)
                if os.path.isdir(full_path):
                    if is_directory_contain_lora(full_path):
                        directories.append(entry)
                    nested_directories = get_directories(
                        full_path, include_root=False)
                    directories.extend([os.path.join(entry, d)
                                       for d in nested_directories])
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)
    return directories


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def get_lora_name(lora_path):
    if opts.lora_preferred_name == "Filename":
        lora_name = lora_path.stem
    else:
        metadata = sd_models.read_metadata_from_safetensors(lora_path)
        lora_name = metadata.get('ss_output_name', lora_path.stem)
    return lora_name


def get_lora_prompt(lora_path, json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    preferred_weight = data.get("preferred weight", 1)
    activation_text = data.get("activation text", "")
    try:
        if float(preferred_weight) == 0:
            preferred_weight = 1
    except:
        preferred_weight = 1
    lora_name = get_lora_name(lora_path)
    return f"<lora:{lora_name}:{preferred_weight}>, {activation_text},"


def image_grid_with_text(imgs, texts, rows=None, cols=None, font_path=None, font_size=20, text_color="#FFFFFF", stroke_color="#000000", stroke_width=2, add_text=True):
    if rows is None:
        rows = round(math.sqrt(len(imgs)))
    cols = math.ceil(len(imgs) / rows) if cols is None else cols
    w, h = imgs[0].size
    grid = Image.new('RGB', (cols * w, rows * h), 'black')
    for i, img in enumerate(imgs):
        grid.paste(img, (i % cols * w, i // cols * h))
    if add_text:
        draw = ImageDraw.Draw(grid)
        try:
            font = ImageFont.truetype(font_path, font_size) if font_path and os.path.exists(
                font_path) else ImageFont.truetype(roboto_ttf_file, font_size)
        except:
            font = ImageFont.truetype(roboto_ttf_file, font_size)
        for i, text in enumerate(texts):
            x = (i % cols) * w
            y = (i // cols) * h
            for dx, dy in [(j, k) for j in range(-stroke_width, stroke_width+1) for k in range(-stroke_width, stroke_width+1)]:
                draw.text((x+5+dx, y+5+dy), text, font=font, fill=stroke_color)
            draw.text((x+5, y+5), text, font=font, fill=text_color)
    return grid


class Script(scripts.Script):
    def title(self):
        return "Apply on every Lora"

    def ui(self, is_img2img):
        def build_lora_tree(base_path):
            tree = {"__root__": {"name": base_path.name, "children": {}}}
            for root, dirs, files in os.walk(base_path):
                rel_path = os.path.relpath(root, base_path)
                current_node = tree["__root__"]
                if rel_path != ".":
                    for part in rel_path.split(os.sep):
                        current_node = current_node["children"].setdefault(
                            part, {"name": part, "children": {}, "loras": []})

                loras = [f[:-12] for f in files if f.endswith(".safetensors")]
                current_node["loras"] = loras
            return tree["__root__"]

        def update_tree(is_use_custom, custom_path):
            base_path = get_base_path(is_use_custom, custom_path)
            return gr.Tree.update(value=build_lora_tree(base_path))

        with gr.Column():
            base_dir_checkbox = gr.Checkbox(
                label="Use Custom Lora path", value=False)
            base_dir_textbox = gr.Textbox(
                label="Lora directory", visible=False)
            with gr.Row():
                lora_dir_dropdown = gr.Dropdown(
                    label="LORA Directory",
                    choices=["/"] + get_directories(lora_dir),
                    value="/",
                    interactive=True
                )
                refresh_btn = gr.Button("🔄", variant="tool")

            lora_checkboxes = gr.CheckboxGroup(
                label="Select LoRAs",
                interactive=True
            )

            def update_directory(current_dir):
                base_path = lora_dir.joinpath(current_dir.lstrip('/'))
                loras = []
                if allowed_path(base_path):
                    for root, _, files in os.walk(base_path):
                        for file in files:
                            if file.endswith(('.safetensors', '.pt')):
                                rel_path = os.path.relpath(root, lora_dir)
                                loras.append(
                                    f"{rel_path}/{file}" if rel_path != '.' else file)
                return gr.CheckboxGroup.update(choices=loras)

            def scan_loras(current_dir):
                return update_directory(current_dir)

            lora_dir_dropdown.change(
                fn=scan_loras,
                inputs=[lora_dir_dropdown],
                outputs=lora_checkboxes
            )
            refresh_btn.click(
                fn=lambda: scan_loras(lora_dir_dropdown.value),
                outputs=lora_checkboxes
            )
            prompt_lines = gr.Textbox(label="Prompts (one per line)", lines=5)
            lora_tags_position_radio = gr.Radio(
                ["Prepend", "Append"], value="Prepend", label="LoRA Tags Position")
            checkbox_save_grid = gr.Checkbox(
                label="Save grid image", value=True)
            font_path = gr.Textbox(label="Custom Font Path")

            with gr.Row():
                use_random_seed = gr.Checkbox(
                    label="Random seed", value=True)
                use_fixed_seed = gr.Checkbox(label="Fixed seed", value=False)

            file_upload = gr.File(
                label="Load prompts from file", file_types=[".txt"], type='binary')

            def load_prompt_file(file, current_prompts):
                if file is None:
                    return None, current_prompts, gr.update()
                lines = [x.strip() for x in file.decode(
                    'utf8', errors='ignore').split("\n")]
                return None, "\n".join(lines), gr.update(lines=max(7, len(lines)))

            file_upload.change(
                fn=load_prompt_file,
                inputs=[file_upload, prompt_lines],
                outputs=[file_upload, prompt_lines, prompt_lines],
                show_progress=False
            )

        base_dir_checkbox.change(
            fn=lambda is_use, path: get_base_path(is_use, path),
            inputs=[base_dir_checkbox, base_dir_textbox],
            outputs=lora_dir_dropdown
        )

        return [base_dir_checkbox, base_dir_textbox, lora_checkboxes, prompt_lines, lora_tags_position_radio, checkbox_save_grid, font_path]

    def run(self, p, is_use_custom_path, custom_path, lora_checkboxes, prompt_lines, lora_tags_position, is_save_grid, font_path):
        selected_loras = [
            str(lora_dir.joinpath(lora))
            for lora in lora_checkboxes
            if lora.endswith(('.safetensors', '.pt'))
        ]

        if not selected_loras or not prompt_lines:
            return Processed(p, [], p.seed, "No LoRAs or prompts selected")

        prompts = [line.strip()
                   for line in prompt_lines.splitlines() if line.strip()]
        combinations = [(lora, prompt)
                        for lora in selected_loras for prompt in prompts]

        state.job_count = len(combinations)
        result_images = []
        all_prompts = []
        infotexts = []
        grid_texts = []

        for lora_path, prompt in combinations:
            if state.interrupted:
                break

            current_p = copy.copy(p)
            lora_file = Path(lora_path)
            json_file = lora_file.with_suffix('.json')

            try:
                lora_tags = get_lora_prompt(
                    lora_file, json_file) if json_file.exists() else f"<lora:{lora_file.stem}:1>,"
            except Exception as e:
                print(f"Error loading Lora {lora_file}: {str(e)}")
                continue

            final_prompt = f"{lora_tags} {prompt}" if lora_tags_position == "Prepend" else f"{prompt} {lora_tags}"
            current_p.prompt = final_prompt

            proc = process_images(current_p)
            result_images.extend(proc.images)
            all_prompts.extend(proc.all_prompts)
            infotexts.extend(proc.infotexts)
            grid_texts.extend(
                [f"{lora_file.stem}\n{prompt}"] * len(proc.images))

        if is_save_grid and len(result_images) > 1:
            rows = round(math.sqrt(len(result_images)))
            grid_image = image_grid_with_text(
                result_images, grid_texts,
                rows=rows,
                font_path=font_path,
                text_color="#FFFFFF",
                stroke_color="#000000",
                stroke_width=2
            )
            images.save_image(grid_image, p.outpath_grids,
                              "grid", grid=True, p=p)
            result_images.insert(0, grid_image)

        return Processed(p, result_images, p.seed, "", all_prompts=all_prompts, infotexts=infotexts)
