# Dự án Technews - Lộ trình Thực tập Cloud Engineer

## Day 1: GCP Setup & IAM Basics

### 1. Thông tin Google Cloud Project
* **Tên Project:** technews
* **Project ID:** technews-500407
* **Khu vực (Region) mặc định:** asia-southeast1 (Singapore)
* **Budget & Alerts:** Đã thiết lập ngân sách [$40/tháng] và cảnh báo ở mức 50%, 90%, 100%.

### 2. Các APIs đã kích hoạt (Enabled APIs)
Dự án đã bật các API cần thiết để phục vụ cho ứng dụng và CI/CD:
* Cloud Run API
* Artifact Registry API
* Compute Engine API

### 3. Thiết lập IAM & Service Account
Để chuẩn bị cho việc tự động hóa triển khai (deployment), đã tạo một Service Account với nguyên tắc cấp quyền:
* **Tên Service Account:** tech-news-deployer
* **Các quyền (Roles) được cấp:**
  * Cloud Run Admin
  * Artifact Registry Writer
  * Service Account User
* **Xác thực:** Đã tạo file JSON key (đã được lưu trữ bảo mật cục bộ, không commit lên git).

### 4. GCP CLI Setup
* Đã cài đặt thành công Google Cloud CLI trên máy cá nhân.
* Đã đăng nhập và xác thực thành công bằng lệnh `gcloud auth login`.

---

## Day 2: Docker Fundamentals

---

## 1. Kiến thức lý thuyết cốt lõi

### Docker Image (Khuôn đúc)
Là một gói tĩnh (Read-only), chứa toàn bộ mã nguồn, môi trường thực thi (Python 3.13), các thư viện phụ thuộc và cấu hình hệ thống cần thiết để ứng dụng **TechNews API** có thể chạy.

### Docker Container (Thực thể sống)
Là một tiến trình cô lập được khởi tạo từ Docker Image. Container sử dụng tài nguyên thật của hệ thống và có vòng đời riêng.

### Docker Layers (Cấu trúc xếp lớp)
Mỗi chỉ thị trong `Dockerfile` sẽ tạo ra một **layer** riêng biệt. Docker sử dụng các layer này để tối ưu việc lưu trữ và tái sử dụng dữ liệu.

### Docker Cache (Bộ nhớ đệm)
Docker tự động lưu lại các layer đã build. Khi build lại Image, nếu một layer không thay đổi thì Docker sẽ sử dụng cache thay vì thực hiện lại toàn bộ bước đó, giúp giảm đáng kể thời gian build.

---

## 2. Cấu trúc `Dockerfile` và `.dockerignore`

Dockerfile được thiết kế nhằm tối ưu hiệu năng build, tận dụng Docker Cache và tăng cường bảo mật bằng cách sử dụng **Non-root User**.

### Dockerfile

```dockerfile
FROM python:3.13

WORKDIR /usr/local/app

# Cài đặt dependencies trước để tận dụng Docker Cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn
COPY . .

EXPOSE 8080

# Tăng cường bảo mật bằng Non-root User
RUN useradd app
USER app

# Khởi chạy API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### `.dockerignore`

```text
.git
.gitignore
venv/
.venv/
__pycache__/
*.pyc
.env
dockerfile
.dockerignore
```

---

## 3. Hướng dẫn chạy ứng dụng

### Bước 1: Build Docker Image

```bash
docker build -t technews-api:v1 .
```

### Bước 2: Chạy Docker Container

```bash
docker run -p 8080:8080 technews-api:v1
```

Sau khi container khởi chạy thành công, API sẽ có thể truy cập tại:

```text
http://localhost:8080
```

---

## 4. Kết quả

- Xây dựng Docker Image thành công.
- Khởi chạy thành công Docker Container.
- Ứng dụng TechNews API hoạt động bình thường trong môi trường Docker cục bộ.
- API có thể truy cập tại:

```text
http://localhost:8080
```
![alt text](image.png)