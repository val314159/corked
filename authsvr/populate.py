import os
from cork.backends import SQLiteBackend

def populate_backend():
    b = SQLiteBackend(os.environ['DBNAME'], initialize=True)
    b.connection.executescript("""
        INSERT INTO users (username, email_addr, desc, role, hash, creation_date) VALUES
        (
            'admin',
            'admin@ccl.io',
            '{"key1": "f64ef282-4410-47bb-9ebf-b8719d2a8a19", "key0": "4504dd6b-50ba-11e4-be6f-3c15c2e8aac8", "id": "45033d33-50ba-11e4-8e60-3c15c2e8aac8"}',
            'admin',
            'cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=',
            '2012-10-28 20:50:26.286723'
        );
        INSERT INTO roles (role, level) VALUES ('special', 200);
        INSERT INTO roles (role, level) VALUES ('admin', 100);
        INSERT INTO roles (role, level) VALUES ('editor', 60);
        INSERT INTO roles (role, level) VALUES ('user', 50);
    """)
    return b

if __name__ == "__main__":
    b = populate_backend()
