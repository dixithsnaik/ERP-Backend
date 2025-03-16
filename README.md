# Documentation for the project

To run or set-up this project, follow the steps below:

1. Clone the repository
2. Run the following command to install the dependencies:
```bash
poetry install
```

note :- before running this 
make sure you have installed mysql in your system and also
link:- https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04#step-3-creating-a-dedicated-mysql-user-and-granting-privileges

in the above artical creating user is wrong use this insted
```bash
CREATE USER 'dixith'@'%' IDENTIFIED WITH mysql_native_password BY 'your_password_here';
GRANT ALL PRIVILEGES ON *.* TO 'dixith'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```
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
