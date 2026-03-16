"""
Migration: Normalize roles table + Rename time_limit to duration
"""
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', password='12345678', database='speed_up')
cur = conn.cursor()

# 1. Create roles table
cur.execute("""
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")
print("Created roles table")

# 2. Insert default roles
for name, desc in [('admin', 'Quản trị viên'), ('student', 'Học sinh'), ('teacher', 'Giáo viên')]:
    cur.execute("INSERT IGNORE INTO roles (name, description) VALUES (%s, %s)", (name, desc))
print("Inserted default roles")

# 3. Add role_id column to accounts
try:
    cur.execute("ALTER TABLE accounts ADD COLUMN role_id INT NULL AFTER full_name")
    print("Added role_id column")
except Exception as e:
    print(f"role_id column: {e}")

# 4. Migrate existing role data
cur.execute("UPDATE accounts a JOIN roles r ON r.name = a.role SET a.role_id = r.id")
print(f"Migrated role data: {cur.rowcount} rows")

# 5. Add FK constraint
try:
    cur.execute("ALTER TABLE accounts ADD CONSTRAINT fk_accounts_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL")
    print("Added FK constraint")
except Exception as e:
    print(f"FK constraint: {e}")

# 6. Drop old role enum column
try:
    cur.execute("ALTER TABLE accounts DROP COLUMN role")
    print("Dropped old role column")
except Exception as e:
    print(f"Drop role: {e}")

# 7. Rename time_limit to duration in exercises
try:
    cur.execute("ALTER TABLE exercises CHANGE COLUMN time_limit duration INT DEFAULT 45")
    print("Renamed time_limit to duration")
except Exception as e:
    print(f"Rename time_limit: {e}")

conn.commit()
print("\nAll migrations completed successfully!")
conn.close()
