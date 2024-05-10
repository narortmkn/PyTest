#generate a app to combine png photo from PIL import Image
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from tempfile import NamedTemporaryFile
import shutil
import os 
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/upload_image/")
async def upload_image(image: UploadFile = File(...)):
	print(image.filename)
	return {"filename": image.filename}

@app.get('/')
async def Home():
      return HTMLResponse("<form enctype=\"multipart/form-data\"  action=\"/\" method=\"post\">Select a image:<input type=\"file\" name=\"file\"><button>Process</button></form>")

@app.post('/')
async def genpicture(file: UploadFile = File(...)):
    # Save the uploaded Excel file temporarily
    with NamedTemporaryFile(delete=False) as tmp_file:
        # Copy the contents of the uploaded file to the temporary file
        shutil.copyfileobj(file.file, tmp_file)

        # Example usage
        image1_path = tmp_file.name
        image2_path = "resource/frame_name.png"
        output_path = "resource/combined_image3.png"
        combine_and_resize_images(image1_path, image2_path, output_path)
         
    return FileResponse("resource/combined_image3.png")

   # return Response(content=image_bytes, media_type="image/png")
    #return {"message": "SUCCESS " + output_path}

def combine_and_resize_images(image1_path, image2_path, output_path, output_size=(512, 512)):
    """
    Combines two PNG images and resizes them to a fixed size.
    
    Args:
        image1_path (str): Path to the first PNG image.
        image2_path (str): Path to the second PNG image.
        output_path (str): Path to save the combined and resized image.
        output_size (tuple): Desired size of the output image (width, height).
    """
    # Open the two images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    
    # Resize the images to the same size
    image1 = image1.resize((440, 440), resample=Image.BICUBIC)
    image2 = image2.resize(output_size, resample=Image.BICUBIC)
    
    # Create a new image with transparent background
    combined_image = Image.new("RGBA", output_size, (0, 0, 0, 0))
    
    # Paste the two images onto the combined image
    combined_image.paste(image1, (30, 100))
    combined_image.paste(image2, (0, 0), mask=image2)
    
    # Save the combined and resized image
    combined_image.save(output_path)
    return combined_image