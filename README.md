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
