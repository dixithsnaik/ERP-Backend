# Documentation for the project

To run or set-up this project, follow the steps below:

1. Clone the repository
2. Run the following command to install the dependencies:
```bash
poetry install
```

note :- before running this 
make sure you have installed mysql in your system and also
then
```bash
sudo mysql -u root -p
```

then you need to create a db with name ` ERPDB `
```bash
CREATE DATABASE ERPDB;
```

3. Run the following command to run the project:
```bash
poetry run python run.py
```

4. To get dummy data to test the server
```bash
poetry run python scripts/fake_data_generation.py
```

5. GCP setup
- Create a bucket and service account
- make sure the bucket is fine grained control
- add the service account to the bucket permission
- Download the key.json file from the service account
- In the local download google cloud CLI and login to gcloud
    -https://cloud.google.com/sdk/docs/install
    - gcloud auth login --cred-file=erp_key.json
    - gcloud config set project "id_of_the_projet"
- In ~/.bashrc export GOOGLE_APPLICATION_CREDENTIALS="path to key.json"
- run the command source ~/.bashrc
