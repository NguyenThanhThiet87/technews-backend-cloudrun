import os
import certifi
import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URL")

mock_data = [
    {
        "title": "OpenAI chính thức ra mắt GPT-5 với khả năng suy luận vượt trội",
        "summary": "Phiên bản AI mới nhất từ OpenAI đánh dấu một bước tiến lớn trong khả năng suy luận logic và giải quyết vấn đề phức tạp.",
        "content": "Theo thông báo mới nhất từ OpenAI, GPT-5 không chỉ nhanh hơn mà còn có khả năng hiểu ngữ cảnh dài hơn gấp 10 lần. Đặc biệt, hệ thống này đã vượt qua các bài kiểm tra logic ở mức độ chuyên gia trong nhiều lĩnh vực như y tế và luật. Các nhà phát triển có thể tận dụng API mới với chi phí rẻ hơn đáng kể.",
        "category": "AI",
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=800",
        "keywords": ["OpenAI", "GPT-5", "Trí tuệ nhân tạo"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=1)
    },
    {
        "title": "Apple ra mắt iPhone 17 Pro Max: Thiết kế viền siêu mỏng, chip A19 Bionic",
        "summary": "Chiếc flagship mới nhất của Apple mang đến thiết kế hoàn toàn không viền, camera 100MP và sức mạnh xử lý chưa từng có.",
        "content": "iPhone 17 Pro Max đánh dấu sự thay đổi lớn nhất về thiết kế trong 3 năm qua. Viền màn hình gần như không tồn tại, kết hợp cùng chip A19 Bionic tiến trình 2nm giúp tối ưu thời lượng pin lên đến 30% so với thế hệ tiền nhiệm. Camera tiềm vọng mới hỗ trợ zoom quang học 10x mà không làm giảm chất lượng ảnh.",
        "category": "Mobile",
        "image_url": "https://images.unsplash.com/photo-1512054502232-10a0a035d672?auto=format&fit=crop&q=80&w=800",
        "keywords": ["Apple", "iPhone 17", "Smartphone"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=2)
    },
    {
        "title": "NVIDIA giới thiệu dòng card đồ họa RTX 5090",
        "summary": "Quái vật đồ họa mới của NVIDIA hứa hẹn mang lại hiệu năng gấp đôi thế hệ trước, hỗ trợ chơi game 8K mượt mà.",
        "content": "RTX 5090 sử dụng kiến trúc Blackwell mới nhất, sở hữu 32GB VRAM chuẩn GDDR7. Card đồ họa này không chỉ dành cho game thủ mà còn là công cụ đắc lực cho các chuyên gia sáng tạo nội dung và kỹ sư AI. Tuy nhiên, mức tiêu thụ điện năng lên đến 500W yêu cầu người dùng phải trang bị nguồn máy tính chuẩn ATX 3.0 mới.",
        "category": "PC",
        "image_url": "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&q=80&w=800",
        "keywords": ["NVIDIA", "RTX 5090", "GPU", "PC Gaming"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=3)
    },
    {
        "title": "Google phát hành Gemini 2.0 tích hợp sâu vào hệ sinh thái Android",
        "summary": "Bản cập nhật AI mới từ Google giúp trợ lý ảo trên điện thoại thông minh hơn, phản hồi nhanh và tự nhiên như con người.",
        "content": "Gemini 2.0 sẽ được tích hợp mặc định trên các dòng máy Pixel mới và dần mở rộng cho toàn bộ thiết bị Android. Tính năng đáng chú ý nhất là khả năng tương tác trực tiếp với các ứng dụng bên thứ ba để thực hiện các tác vụ phức tạp chỉ bằng giọng nói, ví dụ như đặt lịch hẹn, phân tích tin nhắn và soạn thảo email chi tiết.",
        "category": "AI",
        "image_url": "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&q=80&w=800",
        "keywords": ["Google", "Gemini", "Android"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=4)
    },
    {
        "title": "Samsung Galaxy Z Fold 7: Bản lề mới không nếp gấp, màn hình siêu sáng",
        "summary": "Thế hệ điện thoại gập mới của Samsung tập trung vào việc cải thiện độ bền và tối ưu trải nghiệm hiển thị ngoài trời.",
        "content": "Với bản lề 'Flex Hinge 3.0', Samsung đã hoàn toàn loại bỏ được khe hở khi gập máy và làm mờ gần như 100% nếp gấp giữa màn hình. Độ sáng màn hình trong cũng được nâng lên 3000 nits, cho phép sử dụng thoải mái dưới ánh nắng mặt trời gắt. Máy còn tích hợp khe cắm bút S-Pen ngay trong thân máy thay vì dùng ốp lưng như trước.",
        "category": "Mobile",
        "image_url": "https://images.unsplash.com/photo-1585060544812-6b45742d762f?auto=format&fit=crop&q=80&w=800",
        "keywords": ["Samsung", "Z Fold", "Smartphone gập"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=5)
    },
    {
        "title": "AMD Ryzen 9000 Series ra mắt, đe dọa ngôi vương của Intel",
        "summary": "Dòng vi xử lý mới của AMD mang lại hiệu năng đa nhân khủng khiếp với mức tiêu thụ điện năng cực thấp.",
        "content": "Dựa trên tiến trình 3nm, Ryzen 9000 Series mang lại mức IPC (lệnh trên mỗi xung nhịp) tăng 15%. Điều này giúp các game thủ có số khung hình cao hơn và các nhà làm phim xuất video nhanh hơn tới 25% so với thế hệ cũ. Nền tảng AM5 tiếp tục được hỗ trợ, giúp người dùng tiết kiệm chi phí nâng cấp mainboard.",
        "category": "PC",
        "image_url": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&q=80&w=800",
        "keywords": ["AMD", "Ryzen", "CPU"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=6)
    },
    {
        "title": "Mạng 6G dự kiến sẽ được thương mại hóa vào năm 2030",
        "summary": "Tốc độ kết nối nhanh gấp 100 lần 5G hứa hẹn mở ra kỷ nguyên mới cho vạn vật kết nối và vũ trụ ảo (Metaverse).",
        "content": "Các chuyên gia viễn thông cho biết, 6G sẽ không chỉ giải quyết vấn đề tốc độ mà còn tích hợp cảm biến từ xa và trí tuệ nhân tạo vào hạ tầng mạng. Điều này sẽ biến xe tự lái và phẫu thuật từ xa trở nên phổ biến và an toàn tuyệt đối. Hàn Quốc và Nhật Bản hiện đang là những quốc gia tiên phong thử nghiệm hạ tầng 6G.",
        "category": "Mobile",
        "image_url": "https://images.unsplash.com/photo-1616423640778-28d1b53229bd?auto=format&fit=crop&q=80&w=800",
        "keywords": ["6G", "Mạng viễn thông", "Tương lai"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=7)
    },
    {
        "title": "Microsoft Copilot Plus PC: Định nghĩa lại máy tính xách tay với AI tích hợp",
        "summary": "Những chiếc laptop mới được trang bị NPU siêu mạnh để chạy trực tiếp các mô hình AI ngôn ngữ mà không cần internet.",
        "content": "Dòng máy tính Copilot Plus đánh dấu sự khởi đầu của kỷ nguyên 'AI PC'. Chức năng 'Recall' giúp người dùng tìm lại bất kỳ thứ gì từng xem trên màn hình bằng ngôn ngữ tự nhiên. Chip Snapdragon X Elite đi kèm hứa hẹn thời lượng pin lên đến 20 giờ và hiệu năng vượt mặt nhiều dòng chip Intel cùng phân khúc.",
        "category": "PC",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&q=80&w=800",
        "keywords": ["Microsoft", "Copilot", "AI PC"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=8)
    },
    {
        "title": "Phát hiện đột phá: AI học cách tự viết code tối ưu hơn con người",
        "summary": "Một hệ thống AI mới đã có thể tự động phân tích và tối ưu hóa hàng triệu dòng code phức tạp chỉ trong vài phút.",
        "content": "Hệ thống có tên gọi 'AutoCoder-X' không chỉ phát hiện lỗi (bug) mà còn có thể tái cấu trúc (refactor) lại toàn bộ hệ thống phần mềm, giảm thiểu dung lượng và tăng tốc độ xử lý lên 40%. Điều này làm dấy lên nhiều tranh luận về tương lai của nghề lập trình viên cũng như khả năng tự tiến hóa của trí tuệ nhân tạo.",
        "category": "AI",
        "image_url": "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?auto=format&fit=crop&q=80&w=800",
        "keywords": ["Lập trình", "AI Code", "Công nghệ phần mềm"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=9)
    },
    {
        "title": "Màn hình OLED 240Hz 4K đầu tiên trên thế giới chính thức lên kệ",
        "summary": "Trải nghiệm hình ảnh hoàn hảo với độ phân giải siêu nét và tần số quét cực cao, đáp ứng mọi nhu cầu từ giải trí đến eSports chuyên nghiệp.",
        "content": "Nhà sản xuất ASUS vừa trình làng mẫu màn hình OLED đỉnh cao nhất từ trước đến nay. Với thời gian phản hồi chỉ 0.03ms, độ tương phản vô cực và màu đen sâu thẳm, đây được đánh giá là 'chén thánh' của thế giới màn hình gaming hiện tại. Các công nghệ chống cháy hình (burn-in) độc quyền cũng được tích hợp sâu vào phần cứng.",
        "category": "PC",
        "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&q=80&w=800",
        "keywords": ["Monitor", "OLED", "Gaming", "ASUS"],
        "is_published": True,
        "created_at": datetime.utcnow() - timedelta(days=10)
    }
]

async def seed():
    print("Connecting to MongoDB...")
    # Thêm tlsAllowInvalidCertificates=True để vượt qua lỗi tường lửa chặn SSL 
    client = AsyncIOMotorClient(MONGO_DETAILS, tlsCAFile=certifi.where(), tlsAllowInvalidCertificates=True)
    db = client.news_database
    collection = db.get_collection("articles")
    
    await collection.delete_many({})
    print("Cleared existing articles.")
    
    result = await collection.insert_many(mock_data)
    print(f"Successfully inserted {len(result.inserted_ids)} articles!")

if __name__ == "__main__":
    asyncio.run(seed())
