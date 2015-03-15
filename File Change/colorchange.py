from PIL import Image
def changeColor():
	for z in range(1,190):
		name = "Math6-%03d"%(z) # Find picture name
		print name

		picture = Image.open("../Ipython/whiteMath6/"+name+".png") 
		picture = picture.convert("RGBA")					
		pixels = picture.getdata()

		newPixels = []
		for pixel in pixels:
		    if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
		        newPixels.append((255, 255, 255, 0))
		    else:
		        newPixels.append(pixel)

		picture.putdata(newPixels)
		picture.save("../Ipython/tranMath6/"+name+".png", "png")

changeColor()