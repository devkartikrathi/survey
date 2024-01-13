import os
from pymongo import MongoClient
from gridfs import GridFS

# Establish a connection to the MongoDB instance
client = MongoClient('mongodb+srv://<username>:<password>@cluster0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

# Select the database
db = client['database_name']

# Create a GridFS object
fs = GridFS(db)

# Function to insert an image into the database
def insert_image(folder_path):
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".png") or filepath.endswith(".jpg"):  # add more conditions if there are other image types
                with open(filepath, 'rb') as f:
                    fs.put(f, filename=filepath)

# Function to retrieve an image from the database
def retrieve_image(filename):
    outfilename = "output_" + filename
    with open(outfilename, 'wb') as f:
        filedata = fs.get_last_version(filename=filename)
        f.write(filedata.read())
