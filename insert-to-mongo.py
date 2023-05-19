import argparse
from pymongo import MongoClient
import json
import os
import sys
from bson.json_util import loads

def parse_arguments():
    # Check if all required environment variables are set
    required_env_vars = ['CONNECTION_STRING', 'DATABASE', 'COLLECTION', 'JSON_FILES_DIRECTORY']
    for var in required_env_vars:
        if var not in os.environ:
            raise EnvironmentError(f"Environment variable '{var}' is not set")

    # Create a class to mimic the behavior of argparse.Namespace
    class Args:
        pass

    args = Args()
    args.connection_string = os.getenv('CONNECTION_STRING')
    args.database = os.getenv('DATABASE')
    args.collection = os.getenv('COLLECTION')
    args.json_files_directory = os.getenv('JSON_FILES_DIRECTORY')


    return args



def main():
    args = parse_arguments()
    
    #print connection string
    print(f"Connection string: {args.connection_string}")

    try:
        # Establish a connection to MongoDB
        client = MongoClient(args.connection_string)

        # Select the database and collection where you want to insert the JSON documents
        db = client[args.database]
        collection = db[args.collection]

        # Iterate over the JSON files and insert data into MongoDB
        directory = args.json_files_directory
        inserted_resume_counter = 0

        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                with open(os.path.join(directory, filename), 'r') as file:
                    try:
                        data = loads(file.read())
                        # Check if data is a list
                        if isinstance(data, list):
                            collection.insert_many(data)
                        else:
                            collection.insert_one(data)

                        inserted_resume_counter += 1   

                    except Exception as e:
                        print(f"Error inserting data from file {filename}: {str(e)}")


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

    finally:
        # Close the MongoDB connection
        if 'client' in locals():
            client.close()

        
    print(f"Inserted {inserted_resume_counter} resumes into MongoDB")

if __name__ == '__main__':
    main()