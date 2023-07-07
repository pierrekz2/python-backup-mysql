# Python Backup Script

This is a Python script for performing backups of MySQL databases using Docker. The script creates backups of the specified databases and compresses the files into a backup directory.

## Requirements

- Docker
- MySQL/MariaDB
- Read access to the databases you want to backup
- Write permissions to the specified backup directory
- Python 3
- requests library (`pip install requests`)

## Configuration

Before running the script, you need to make the following configurations:

1. Set the base directory to store the backups in the `DIR_BASE` variable.
2. Set the local host name in the `LOCAL_HOST` variable.
3. Specify the MariaDB container name in the `CONTAINER_NAME` variable.
4. Add the names of the databases you want to backup to the `DB` list.
5. Set the database access credentials in the `DB_USER` and `DB_USER_PASSWORD` variables.
6. Configure the desired actions for handling the backup success or failure using the provided code snippets.

## Usage

1. Save the script to a file with the `.py` extension.
2. Make sure you have the requests library installed: `pip install requests`.
3. Run the script: `python script.py`.

## Security Notice

Make sure to properly secure access to the script and the sensitive information contained within it, especially the database access credentials.

