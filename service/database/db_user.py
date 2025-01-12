import motor.motor_asyncio
from models.models_user import User
from service.hash_password.hash_pwd import hash_password
from service.dotenv_manage.dotenv_manage import get_env_variable
from datetime import datetime
from bson import ObjectId
import certifi
ca = certifi.where()
mongodb_url = str(get_env_variable("MONGO_URL"))
db = str(get_env_variable("DATABASE_NAME"))
col = str(get_env_variable("COLLECTION_NAME"))
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url,tlsCAFile=ca)
db = client[db]
user_collection = db[col]

# Hàm thêm user
async def add_user(user: User):
    user_data = user.model_dump()  # Sử dụng model_dump() thay cho dict()
    user_data["password"] = hash_password(user.password)
    user_data["role"] = "user"
    user_data["createdAt"] = datetime.now()
    
    result = await user_collection.insert_one(user_data)  # Đảm bảo là bất đồng bộ
    return {"message": "User added successfully", "id": str(result.inserted_id)}

# Hàm lấy danh sách user
async def get_users():
    users_cursor = user_collection.find()  # Trả về cursor bất đồng bộ
    users = await users_cursor.to_list(length=None)  # Chuyển cursor thành danh sách
    for user in users:
        user["_id"] = str(user["_id"])  # Chuyển ObjectId thành chuỗi
    return users

# Hàm lấy thông tin chi tiết user theo ID
async def get_user_by_id(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})  # Bất đồng bộ
    if user:
        user["_id"] = str(user["_id"])
        return user
    return {"error": "User not found"}

# Kiểm tra username đã tồn tại
async def check_user_exists(username: str):
    user = await user_collection.find_one({"username": username})  # Bất đồng bộ
    return True if user else False

# Kiểm tra email đã tồn tại
async def check_email_exists(email: str):
    emailCheck = await user_collection.find_one({"email": email})  # Bất đồng bộ
    return True if emailCheck else False

# Hàm tìm user theo email hoặc username
async def find_user_by_email_or_username(identifier: str):
    user = await user_collection.find_one({
        "$or": [
            {"email": identifier},  # Tìm theo email
            {"username": identifier}  # Tìm theo username
        ]
    })
    return user  # Trả về thông tin người dùng nếu tìm thấy, nếu không thì trả về None

# Cập nhật thông tin user
async def update_user(user_id: str, user: User):
    user_data = user.model_dump(exclude_unset=True)  # Sử dụng model_dump() và bỏ qua các trường không cập nhật
    result = await user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})  # Bất đồng bộ
    if result.modified_count > 0:
        return {"message": "User updated successfully"}
    return {"error": "User not found or no changes made"}

# Xóa user theo ID
async def delete_user(user_id: str):
    result = await user_collection.delete_one({"_id": ObjectId(user_id)})  # Bất đồng bộ
    if result.deleted_count > 0:
        return {"message": "User deleted successfully"}
    return {"error": "User not found"}
