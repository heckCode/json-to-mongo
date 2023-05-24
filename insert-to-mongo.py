from pymongo import MongoClient
from tqdm import tqdm
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
    sys.stdout.flush()
    args = parse_arguments()

    # Print message to the console
    print(f"Inserting JSON files from directory '{args.json_files_directory}' into MongoDB collection '{args.collection}'")
   
    try:
        # Establish a connection to MongoDB
        client = MongoClient(args.connection_string)

        # Select the database and collection where you want to insert the JSON documents
        db = client[args.database]
        collection = db[args.collection]

        # Iterate over the JSON files and insert data into MongoDB
        directory = args.json_files_directory
        inserted_resume_counter = 0

        # Get the total number of JSON files
        total_files = sum(1 for filename in os.listdir(directory) if filename.endswith('.json'))

        # Create a progress bar
        progress_bar = tqdm(total=total_files)

        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                with open(os.path.join(directory, filename), 'r') as file:
                    try:
                        # Load the JSON data from the file as BSON
                        data = loads(file.read())
                        # Check if data is a list
                        if isinstance(data, list):
                            collection.insert_many(data)
                        else:
                            collection.insert_one(data)

                        inserted_resume_counter += 1

                        # Update the progress bar
                        progress_bar.update(1)
                        progress_bar.set_description(f"Progress: {inserted_resume_counter}/{total_files}")
                        sys.stdout.flush()

                    except Exception as e:
                        print(f"Error inserting data from file {filename}: {str(e)}")

        # Close the progress bar
        progress_bar.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

    finally:
        # Close the MongoDB connection
        if 'client' in locals():
            client.close()


        
    print(f"Inserted {inserted_resume_counter} files into MongoDB for a total of {collection.count_documents({})} documents")

if __name__ == '__main__':
    main()