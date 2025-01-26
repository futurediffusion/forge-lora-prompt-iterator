# 🎨 Iterador de Prompts para LoRA en Forge 🔄

Es similar al script de **"prompt from file or textbox"**, pero permite seleccionar **múltiples LoRAs** para generar imágenes con cada LoRA y cada prompt de las líneas de texto del script. 🖼️

---

## 🚀 Ejemplo
![sample](https://i.imgur.com/Zj2S7bG.jpeg)

**LoRAs seleccionados:** LoRA 1, LoRA 2  
**Prompts en el script:** Línea 1, Línea 2  

**Resultado:**  
Imágenes generadas con:  
- LoRA 1 + Línea 1  
- LoRA 1 + Línea 2  
- LoRA 2 + Línea 1  
- LoRA 2 + Línea 2  

---

## 🛠️ Cómo Usar

1. **Coloca el script** en tu carpeta de scripts en Forge (podría funcionar en A111 y REFORGE) y búscalo en tus scripts como **"apply on every lora"**.

   ![Script Placement](https://i.imgur.com/Ld5mf1O.png)

2. **En la sección de Directorio de LoRA**, elige la carpeta de LoRAs que quieres usar:

   ![Lora Directory](https://i.imgur.com/pxz4Nib.png)

3. **En la sección de Seleccionar LoRA**, elige los LoRAs que deseas usar:

   ![Select Lora](https://i.imgur.com/SdQNE0W.png)

4. **En la sección de Prompts** (uno por línea), ingresa los prompts que se usarán (además del prompt en la celda de prompt positivo original):

   ![Prompts Section](https://i.imgur.com/4B61e9B.png)

5. **Elige dónde quieres colocar las etiquetas** del script y del LoRA (el script también coloca los prompts guardados en los metadatos del LoRA):

   ![Tag Placement](https://i.imgur.com/TuC2pua.png)

6. **Elige entre semilla aleatoria o fija**:

   ![Seed Selection](https://i.imgur.com/qKo7gHD.png)

7. **También puedes subir prompts desde un archivo txt**:

   ![Upload Prompts](https://i.imgur.com/mGUTQts.png)

---

## 📝 Notas
- Este script está diseñado para facilitar la iteración a través de múltiples LoRAs y prompts, ahorrándote tiempo y esfuerzo. ⏱️
- Asegúrate de que tus archivos LoRA y prompts estén bien organizados para obtener los mejores resultados. 📂

---

¡Disfruta generando tus imágenes con facilidad! 🎉  
Si encuentras algún problema, no dudes en abrir un issue o contribuir al proyecto. 🙌