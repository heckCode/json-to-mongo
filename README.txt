# This program will insert all the json files in a folder into a mongodb database

# Create an env.list file with the following values

    CONNECTION_STRING=mongodb://host.docker.internal:27017
    DATABASE=Candidates
    COLLECTION=resumes
    JSON_FILES_DIRECTORY=/mapped_files

- the connection string is the connection string to your mongodb database
- the database name is the name of the database you want to use
- the collection name is the name of the collection you want to use
- dont modify the other values

#Build the image
docker build -t <IMAGE> .

#Run the container
docker run --env-file <path to env.list file> -v <path to json files>:/mapped_files <IMAGE>