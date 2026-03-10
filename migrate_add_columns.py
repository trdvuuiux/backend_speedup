"""
Migration script để thêm các cột mới vào bảng accounts
Chạy: python migrate_add_columns.py
"""
import pymysql

# Kết nối database - lấy từ config
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_NAME = "speed_up"

def migrate():
    try:
        # Kết nối database
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Kiểm tra và thêm từng cột
            columns_to_add = [
                ("phone_number", "VARCHAR(20)"),
                ("avatar_url", "VARCHAR(500)"),
                ("address", "VARCHAR(255)")
            ]
            
            for column_name, column_type in columns_to_add:
                # Kiểm tra xem cột đã tồn tại chưa
                cursor.execute(f"""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = '{DB_NAME}' 
                    AND TABLE_NAME = 'accounts' 
                    AND COLUMN_NAME = '{column_name}'
                """)
                
                result = cursor.fetchone()
                
                if not result:
                    # Thêm cột mới
                    cursor.execute(f"""
                        ALTER TABLE accounts 
                        ADD COLUMN {column_name} {column_type} NULL
                    """)
                    print(f"✓ Đã thêm cột: {column_name}")
                else:
                    print(f"- Cột {column_name} đã tồn tại, bỏ qua")
            
            connection.commit()
            print("\n✓ Migration hoàn tất!")
            
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    migrate()
