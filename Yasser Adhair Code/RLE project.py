import random
#   vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#-> REPORT IS AT THE BOTTOM OF CODE <-
#-> REPORT IS AT THE BOTTOM OF CODE <-
#-> REPORT IS AT THE BOTTOM OF CODE <-
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#Function name: compress_image
#Description: compresses an image using RLE
#Inputs: image which is [[s1,s1,s2,s1],[s3,s3,s1, s4]....] where all s are integers from 0 to 255
#Expected output: [[(s1,2),(s2,1),(s1,1)],[(s3,2),(s1,1),(s4,1)] where () are tuples
def compress_image(image):
    compressed = [] #Initialises array for output
    rows = len(image) #Calculates number of rows early for efficiency
    len_row = len(image[0]) #Also calculates row length
    count = 1 #Count is set to 1 since there will never be 0 occurences of a pixel in RLE
    for i in range(rows): #Iterates through the rows
        temp = [] #Temp array used to simulate a row
        for j in range(len_row): #Iterates through a row
            if j == len_row-1: #Prevents an error occuring where j+1 does not exist
                temp.append((image[i][j],count)) #Appends the tuple of the pixel and the number of itentical pixels
                count = 1 #Resets the count
                break #Makes sure program does not run the next line since it would produce an error
            elif image[i][j] == image[i][j+1]: #Checks if there are two of the same pixel in a row
                count += 1 #Adds 1 to the count
            else: #For when two pixels in a row are not the same
                temp.append((image[i][j],count)) #Appends the tuple of the pixel and the number of identical pixels
                count = 1 #Resets the count
        compressed.append(temp) #Append the row to the array to create a 2D array.
    return compressed #Returns the compressed 2D array

#Function name: generate_Image
#Description: Generates a random image of a set resolution
#Inputs: width and height which are both integers
#Expected output: [[s1,s1,s2,s1],[s3,s3,s1, s4]....] where all s are integers from 0 to 255
def generate_Image(width, height):
    image = [] #Initialises output array
    for i in range(height): #Iterates through height and width
        image.append([]) #Appends empty row
        for j in range(width): 
            randomNumber = random.randint(0,255) #Generates random number from 0 to 255 inclusive
            image[i].append(randomNumber) #Joins random number onto row
    return image #Returns image

#Function name: decompress_image
#Description: decompresses an image using RLE
#Inputs:  compressed which is [[(s1,2),(s2,1),(s1,1)],[(s3,2),(s1,1),(s4,1)] where () are tuples 
#Expected output: [[s1,s1,s2,s1],[s3,s3,s1, s4]....] where all s are integers from 0 to 255
def decompress_image(compressed):
    image = [] #intialises output array
    for row in compressed: #Iterates through rows
        temp = [] #Initialises empty row
        for data in row: #Iterates through compressed row
            for i in range(data[1]): #appends the pixel n times where n is the count (the second value in the tuple)
                temp.append(data[0])
        image.append(temp) #Appends row
    return image #Returns decompressed image
        


#Initialising images
randomImage = [
    [255, 0, 0, 0, 0, 255],
    [120, 120, 0, 0, 255, 1],
    [50, 50, 20, 20, 20, 10]
]
boxImage = [
    [0, 255, 255, 255, 255, 0],
    [0, 255, 0, 0, 255, 0],
    [0, 255, 0, 0, 255, 0],
    [0, 255, 255, 255, 255, 0]
]
blockImage = [
    [0, 255, 255, 255, 255, 0],
    [0, 255, 255, 255, 255, 0],
    [0, 255, 255, 255, 255, 0],
    [0, 255, 255, 255, 255, 0]
]

print('Would you like to compress or decompress: (1 = compress, 2 = decompress)') #Giving player choice
choice = int(input())
if choice  == 1: #Branching depending on choice
    print('Choose one of the following to compress:')
    print('1 = Random Image (not randomly generated)')
    print('2 = An image of a box')
    print('3 = An image of a block')
    print('4 = Randomly Generated Image')
    choice = int(input())
    if choice == 1: #Compresses 'random' image
        print('Here is the original data:')
        print(randomImage)
        print('Here is the compressed data:')
        compressed = compress_image(randomImage)
        print(compressed)
    elif choice == 2: #Compresses box image
        print('Here is the original data:')
        print(boxImage)
        print('Here is the compressed data:')
        compressed = compress_image(boxImage)
        print(compressed)
    elif choice == 3: #Compresses block image
        print('Here is the original data:')
        print(blockImage)
        print('Here is the compressed data:')
        compressed = compress_image(blockImage)
        print(compressed)
    elif choice == 4: #Compresses randomly generated image
        print('Beware, at smaller resolutions or higher colour depths RLE will take more space than the original data')
        width = int(input('Please input the width of the image: '))
        height = int(input('Please input the height of the image: '))
        generatedImage = generate_Image(width, height)
        print('Here is the original data:')
        print(generatedImage)
        print('Here is the compressed data:')
        compressed = compress_image(generatedImage)
        print(compressed)
    else:
        print('Invalid choice')

elif choice  == 2: #Branching depending on choice
    print('Choose one of the following to decompress:')
    print('1 = Random Image (not randomly generated)')
    print('2 = An image of a box')
    print('3 = An image of a block')
    choice = int(input())
    if choice == 1: #Decompresses 'random' image
        print('Here is the compressed data:')
        compressed = compress_image(randomImage) #Too complicated to generate specific compressed data so this will be reused
        print(compressed)
        print('Here is the original data:')
        decompressed = decompress_image(compressed)
        print(decompressed)
    elif choice == 2: #Decompresses box image
        print('Here is the compressed data:')
        compressed = compress_image(boxImage) 
        print(compressed)
        print('Here is the original data:')
        decompressed = decompress_image(compressed)
        print(decompressed)
    elif choice == 3: #Decompresses block image
        print('Here is the compressed data:')
        compressed = compress_image(blockImage) 
        print(compressed)
        print('Here is the original data:')
        decompressed = decompress_image(compressed)
        print(decompressed)
    else:
        print('Invalid choice')

else:
    print('Invalid choice')

#Report
    #The logic I used is clear throughout the code comments. The code produced the expected output for all test cases.
    #Not many challenges were encountered apart from simple syntax errors. The hardest thing was trying to generate compressed data, 
    #which I decided to scrap since it would be too complicated so I settled for reusing the same data for compressed and decompressed data. 