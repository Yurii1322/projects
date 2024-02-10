from minio_f import check_minio_bucket, upload_to_minio
from database_f import check_database_access, backup_databases

def main():
    print("Step 1. Check access to database host:")
    check_database_access()

    print("\n")
    print("Step 2. Check access to minio bucket:")
    check_minio_bucket()

    print("\n")
    print("Step 3. Download backups to local machine:")
    backup_databases()

    print("\n")
    print("Step 4. Upload backups to minio:")
    upload_to_minio()

if __name__ == "__main__":
    main()