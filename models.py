from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

# Xử lý kiểu dữ liệu ObjectId của MongoDB để Pydantic hiểu được
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.no_info_plain_validator_function(cls.validate)
        ])

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler):
        return {"type": "string"}

# Lược đồ dữ liệu khi Thêm/Sửa bài viết (Nhận từ ReactJS)
class ArticleSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(..., description="Tiêu đề bài viết")
    category: str = Field(..., description="Chủ đề tin tức")
    summary: str = Field(..., description="Tóm tắt ngắn")
    content: str = Field(..., description="Nội dung chi tiết")
    image_url: str = Field(default="https://placehold.co/600x400", description="Link ảnh bìa")
    keywords: List[str] = Field(default=[], description="Từ khóa để tìm kiếm")
    is_published: bool = Field(default=True, description="Trạng thái xuất bản")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Lược đồ dữ liệu khi Cập nhật (Chỉ cần gửi những trường muốn đổi)
class UpdateArticleModel(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    keywords: Optional[List[str]] = None
    is_published: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class LoginRequest(BaseModel):
    username: str
    password: str

class UserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    password: str = Field(...)
    role: str = Field(default="admin")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}