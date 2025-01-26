# 🎨 Forge LoRA Prompt Iterator 🔄

It's like the script for **"prompt from file or textbox"**, but it allows selecting **multiple LoRAs** to generate images with each LoRA and each prompt from the script's text lines. 🖼️

---

## 🚀 Example
![sample](https://i.imgur.com/Zj2S7bG.jpeg)

**Selected LoRAs:** LoRA 1, LoRA 2  
**Prompts in the script:** Line 1, Line 2  

**Result:**  
Images generated with:  
- LoRA 1 + Line 1  
- LoRA 1 + Line 2  
- LoRA 2 + Line 1  
- LoRA 2 + Line 2  

---

## 🛠️ How to Use

1. **Place the script** in your script folder in Forge (it might work in A111 and REFORGE) and look for it in your scripts as **"apply on every lora"**.

   ![Script Placement](https://i.imgur.com/Ld5mf1O.png)

2. **In the Lora Directory section**, choose the folder of LoRAs you want to use:

   ![Lora Directory](https://i.imgur.com/pxz4Nib.png)

3. **In the Select Lora section**, choose the LoRAs you want to use:

   ![Select Lora](https://i.imgur.com/SdQNE0W.png)

4. **In the Prompts section** (one per line), enter the prompts to be used (in addition to the prompt in the original positive prompt cell):

   ![Prompts Section](https://i.imgur.com/4B61e9B.png)

5. **Choose where you want to place the tags** from the script and the LoRA (the script also places prompts saved in the LoRA's metadata):

   ![Tag Placement](https://i.imgur.com/TuC2pua.png)

6. **Choose between random or fixed seed**:

   ![Seed Selection](https://i.imgur.com/qKo7gHD.png)

7. **You can also upload prompts from a txt file**:

   ![Upload Prompts](https://i.imgur.com/mGUTQts.png)

---

## 📝 Notes
- This script is designed to make it easy to iterate through multiple LoRAs and prompts, saving you time and effort. ⏱️
- Make sure your LoRA files and prompts are properly organized for the best results. 📂

---

Enjoy generating your images with ease! 🎉  
If you encounter any issues, feel free to open an issue or contribute to the project. 🙌
