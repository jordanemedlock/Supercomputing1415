from PIL import Image

for z in range(1,190):
	name = "Math6-%03d"%(z) # Find picture name
	print name

	picture = Image.open("../Ipython/whiteMath6/"+name+".png") 
	width, height = picture.size					# Create variables with picture information
	rgb_picture = picture.convert('RGB')

	outputImg = Image.new("RGB", (width,height)) # Create a picture to make

	for x in range(width):		# Search every pixel
		for y in range(height):
			current_color = rgb_picture.getpixel((x,y)) # Find pixel's color

			if current_color == (255,255,255):				
				outputImg.putpixel((x,y), (221,221,221))    # Change pixel color
			else:
				outputImg.putpixel((x,y), current_color)

	outputImg.save("../Ipython/greyMath6/"+name+".png", "png") # Create the new image
