from common.database import Database

Database.initialize()
"""
Database.insert(
    'users',
    {
        'account':'mada@test.com',
        'password': '0000',
        'name':'mada'
    }
)
"""

user = Database.find_one(
    'users',
    {
        'account':'mada@test.com'
    }
)

print(user)
