import psycopg2
import yaml
import subprocess
import os
from datetime import datetime

def check_database_access():
    timeout = 10
    try:
        with open('db_config.yaml', 'r') as file:
            yaml_data = yaml.safe_load(file)

        server_info = yaml_data['servers'][0]
        user = server_info['user']
        password = server_info['password']
        host = server_info['host']
        port = server_info['port']
        databases = server_info.get('databases', [])

        connection_string = f"dbname={databases[0]} user={user} password={password} host={host} port={port} connect_timeout={timeout}"

        with psycopg2.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT datname FROM pg_database")
                existing_databases = [row[0] for row in cursor.fetchall()]

                print(f"Connection is ok to {host}. Available databases:")
                for db in existing_databases:
                    print(f"- {db}")

                # Check if the specified databases exist
                for db in databases:
                    if db not in existing_databases:
                        print(f"Warning: Database '{db}' does not exist.")

        return True
    except psycopg2.Error as e:
        print(f"Connection is NOT ok: {e}")
        return False


def backup_databases():
    with open('db_config.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)

    backup_directory = '/home/user/Desktop/DevOps/tasks/task2/backup'

    backup_file_names = []

    for server in yaml_data['servers']:
        host = server.get('host')
        user = server.get('user')
        password = server.get('password')
        port = server.get('port', 5432)

        for database in server.get('databases', []):
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            backup_file_name = f"test_{database}_{timestamp}_backup.sql"
            backup_file_path = os.path.join(backup_directory, backup_file_name)

            command = f"PGPASSWORD={password} pg_dump -h {host} -p {port} -U {user} -d {database} -f {backup_file_path}"

            try:
                subprocess.run(command, shell=True, check=True)
                print(f"Backup for {database} on {host}:{port} completed successfully. Location&File: {backup_file_path}")
                backup_file_names.append(backup_file_name)
            except subprocess.CalledProcessError as e:
                print(f"Error creating backup for {database} on {host}:{port}: {e}")

    with open('backup_file_names.txt', 'w') as file:
        for name in backup_file_names:
            file.write(name + '\n')

