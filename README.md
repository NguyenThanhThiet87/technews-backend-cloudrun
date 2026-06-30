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

---

## Day 3: Advanced Docker & Artifact Registry

---

# 1. Tối ưu hóa Docker Image bằng Multi-stage Build

Tiến hành nâng cấp `Dockerfile` sang kiến trúc **Multi-stage Build** nhằm tối ưu dung lượng Image và tăng tính bảo mật.

## Stage 1 - Builder

- Sử dụng môi trường ảo Python (`venv`) để cô lập các thư viện phụ thuộc.
- Cài đặt toàn bộ dependencies cần thiết cho quá trình build.
- Chuẩn bị các thành phần (artifacts) phục vụ cho Runtime Stage.

## Stage 2 - Runtime

- Sử dụng image `python:3.13-slim` nhằm giảm kích thước Docker Image.
- Chỉ sao chép các thành phần cần thiết từ Builder sang Runtime.
- Loại bỏ compiler, cache và các file tạm không cần thiết.

> **Kết quả:** Docker Image có kích thước nhỏ hơn, bảo mật hơn và thời gian triển khai nhanh hơn.

---

# 2. Thiết lập Google Artifact Registry

Đã tạo thành công Docker Repository trên Google Cloud.

| Thuộc tính | Giá trị |
|------------|----------|
| Repository Name | `technews-repo` |
| Repository Format | Docker |
| Region | `asia-southeast1` (Singapore) |

Khu vực lưu trữ được lựa chọn đồng bộ với hạ tầng mạng đã thiết lập từ **Day 1**, giúp giảm độ trễ khi triển khai.

---

# 3. Xác thực Docker với Google Cloud

Để Docker trên máy cục bộ có thể truy cập Artifact Registry, tiến hành cấu hình thông qua **Google Cloud CLI**.

## Cấu hình

```bash
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
```

## Kết quả

Sau khi thực hiện lệnh, hệ thống hiển thị thông báo:

```text
gcloud credential helpers already registered correctly
```

Thông báo trên xác nhận Docker đã được cấu hình xác thực thành công với Google Cloud.

---

# 4. Chiến lược quản lý phiên bản Docker Image

Dự án áp dụng quy chuẩn đặt tên Image theo chuẩn của Google Artifact Registry.

## Quy ước đặt tên

```text
[REGION]-docker.pkg.dev/technews-500407/[REPOSITORY]/[IMAGE_NAME]:[TAG]
```

### Ví dụ

```text
asia-southeast1-docker.pkg.dev/my-project/technews-repo/technews-api:v1
```

## Chiến lược phát hành

- `v1`
- `v2`
- `v3`
- ...

Mỗi phiên bản phát hành đều được gắn tag riêng nhằm:

- Quản lý lịch sử phiên bản.
- Dễ dàng rollback khi cần.
- Hỗ trợ triển khai CI/CD.

## Gắn tag Image

```bash
docker tag technews-api:v1 \
asia-southeast1-docker.pkg.dev/technews-500407/technews-repo/technews-api:v1
```

---

# 5. Đẩy Docker Image lên Artifact Registry

Sau khi gắn tag, tiến hành đẩy Docker Image lên Google Cloud.

## Push Image

```bash
docker push asia-southeast1-docker.pkg.dev/technews-500407/technews-repo/technews-api:v1
```

## Kết quả

Docker Image được upload thành công lên Artifact Registry.

Artifact Registry hiển thị đầy đủ các thông tin:

- Repository
- Image Name
- Tag
- Digest
- Dung lượng Image
- Thời gian upload

Image đã sẵn sàng để sử dụng trong các bước triển khai Cloud tiếp theo.

---

# ✅ Kết quả đạt được

- Hoàn thành tối ưu Docker Image bằng **Multi-stage Build**.
- Thiết lập thành công **Google Artifact Registry**.
- Docker được xác thực với Google Cloud.
- Áp dụng chiến lược quản lý phiên bản Docker Image.
- Push thành công Docker Image lên Artifact Registry.
- Sẵn sàng phục vụ cho các bước triển khai **Kubernetes** và **CI/CD** ở các giai đoạn tiếp theo.

![alt text](image-1.png)

---

# Day 4: Deploying Containers to Cloud Run

## 🎯 Mục tiêu

- Triển khai thành công Docker Container từ **Google Artifact Registry** lên **Google Cloud Run**.
- Cho phép ứng dụng truy cập công khai thông qua Internet.
- Hiểu cơ chế hoạt động của dịch vụ Serverless trên Google Cloud.

> **Public Service URL:**  
> `https://<your-cloud-run-service-url>`

---

# 1. Tìm hiểu Google Cloud Run

Cloud Run là dịch vụ **Serverless Container Platform** của Google Cloud, cho phép triển khai trực tiếp Docker Container mà không cần quản lý máy chủ.

## Mô hình thực thi (Execution Model)

- Không cần quản lý máy chủ hoặc hạ tầng.
- Chỉ cần triển khai Docker Image, Cloud Run sẽ tự động vận hành ứng dụng.

## Tự động mở rộng (Auto Scaling)

Cloud Run tự động:

- Tăng số lượng instance khi lưu lượng truy cập tăng.
- Giảm số lượng instance khi lưu lượng giảm.
- **Scale to Zero** khi không có request nhằm tối ưu chi phí.

## Quản lý phiên bản (Revisions)

Mỗi lần triển khai một Docker Image mới:

- Cloud Run tự động tạo một **Revision** mới.
- Cho phép chuyển đổi hoặc rollback về phiên bản cũ nếu cần.

---

# 2. Triển khai Docker Image lên Cloud Run

## Bước 1 - Khởi tạo Service

- Truy cập **Google Cloud Console**.
- Chọn **Cloud Run**.
- Nhấn **Create Service**.

---

## Bước 2 - Chọn Container Image

Tại mục **Container Image URL**:

- Chọn **SELECT**.
- Truy cập **Artifact Registry**.
- Chọn repository `technews-repo`.
- Chọn image:

```text
technews-api:v1
```

---

## Bước 3 - Cấu hình Service

Thiết lập các thông tin cơ bản:

| Thuộc tính | Giá trị |
|------------|----------|
| Service Name | `technews-api` |
| Region | `asia-southeast1` (Singapore) |

---

## Bước 4 - Cấu hình Authentication

Trong phần **Authentication**, chọn:

```text
Allow unauthenticated invocations
```

Cấu hình này cho phép:

- API được truy cập công khai.
- Không yêu cầu xác thực người dùng.
- Phù hợp với REST API phục vụ các ứng dụng bên ngoài.

---

## Bước 5 - Cấu hình Container

Mở mục:

```text
Containers, Networking, Security
```

### Container Port

Thiết lập:

```text
8080
```

Port phải trùng với cổng mà ứng dụng khai báo trong Dockerfile.

### Environment Variables & Secrets

Trong tab **Variables & Secrets**:

- Thiết lập các biến môi trường (Environment Variables).
- Lưu trữ thông tin nhạy cảm (Secrets) như:
  - Database URL
  - API Key
  - Access Token
  - Secret Key

Không nên hard-code các thông tin này trong mã nguồn.

---

## Bước 6 - Hoàn tất triển khai

- Nhấn **CREATE**.
- Chờ Cloud Run tạo Service.
- Sau khi hoàn tất, hệ thống sẽ cung cấp một **Public Service URL**.

Ví dụ:

```text
https://technews-api-xxxxx-uc.a.run.app
```

Người dùng có thể truy cập trực tiếp API thông qua đường dẫn này.

---

# ✅ Kết quả đạt được

- Hiểu nguyên lý hoạt động của Google Cloud Run.
- Triển khai thành công Docker Image từ Artifact Registry.
- Cấu hình Service với Authentication phù hợp.
- Thiết lập Container Port và Environment Variables.
- Ứng dụng hoạt động ổn định trên môi trường Serverless.
- Nhận được Public Service URL để phục vụ truy cập và tích hợp với các hệ thống khác.


- Tài liệu Swagger API có thể truy cập qua:

```text
https://technews-api-234032679535.asia-southeast1.run.app/docs
```
![alt text](image-2.png)

---

# Day 5: Infrastructure as a Service (IaaS) - Networking & Compute Engine

## 🎯 Mục tiêu

- Hiểu mô hình **Infrastructure as a Service (IaaS)** trên Google Cloud.
- Xây dựng hệ thống mạng riêng bằng **Virtual Private Cloud (VPC)**.
- Cấu hình **Firewall Rules** theo nguyên tắc **Least Privilege**.
- Triển khai máy ảo trên **Compute Engine**.
- Thiết lập môi trường hạ tầng Cloud an toàn và tối ưu chi phí.

---

# 1. Tổng quan kiến thức

## Virtual Private Cloud (VPC)

**Virtual Private Cloud (VPC)** là mạng riêng ảo trên Google Cloud, cho phép cô lập các tài nguyên trong một hệ thống mạng độc lập.

Lợi ích:

- Chủ động quản lý dải địa chỉ IP.
- Kiểm soát định tuyến mạng.
- Tăng tính bảo mật so với mạng mặc định (`default`).
- Dễ dàng mở rộng hạ tầng trong tương lai.

---

## Firewall Rules

Firewall Rules hoạt động theo nguyên tắc **Least Privilege** (Đặc quyền tối thiểu), chỉ cho phép các kết nối thực sự cần thiết.

Kết hợp với **Network Tags** giúp:

- Quản lý nhiều máy ảo dễ dàng.
- Áp dụng chính sách bảo mật theo từng nhóm tài nguyên.
- Hạn chế truy cập trái phép.

---

## Compute Engine

Compute Engine là dịch vụ **Infrastructure as a Service (IaaS)** của Google Cloud.

Người dùng có toàn quyền:

- Quản lý hệ điều hành.
- Cài đặt phần mềm.
- Cấu hình CPU, RAM và Storage.
- Kiểm soát toàn bộ máy chủ.

---

# 2. Thiết lập Virtual Private Cloud

Tạo một mạng riêng phục vụ cho dự án Technews.

| Thuộc tính | Giá trị |
|------------|----------|
| Network Name | `technews-vpc` |
| Mode | Custom |
| Subnet | `technews-subnet-asia` |
| Region | `asia-southeast1` |
| CIDR Range | `10.0.0.0/24` |

Mục đích:

- Tách biệt hoàn toàn với mạng mặc định của Google Cloud.
- Chủ động quản lý địa chỉ IP.
- Tạo nền tảng cho việc mở rộng hệ thống.

---

# 3. Cấu hình Firewall Rules

Tạo Firewall Rule:

```text
technews-allow-web-ssh
```

Firewall được áp dụng thông qua **Network Tags**.

## Network Tag

```text
technews-web-tag
```

Chỉ các máy ảo được gắn tag này mới chịu tác động của Firewall Rule.

## Ingress Rules

| Protocol | Port | Mục đích |
|-----------|------|----------|
| TCP | 22 | SSH |
| TCP | 80 | HTTP |
| TCP | 443 | HTTPS |

Nguồn truy cập:

```text
0.0.0.0/0
```

Firewall chỉ mở các cổng cần thiết nhằm đảm bảo nguyên tắc **Least Privilege**.

---

# 4. Triển khai Compute Engine VM

Tạo máy ảo phục vụ thực hành.

| Thuộc tính | Giá trị |
|------------|----------|
| VM Name | `technews-vm` |
| Machine Type | `e2-micro` |
| Operating System | Debian GNU/Linux |

## Network

Máy ảo được kết nối với:

- VPC: `technews-vpc`
- Subnet: `technews-subnet-asia`

## Network Tag

```text
technews-web-tag
```

Tag này giúp Firewall tự động áp dụng đúng chính sách bảo mật.

---

# 5. Kiểm tra kết nối

Sau khi triển khai, tiến hành kiểm tra:

- Máy ảo truy cập Internet thành công.
- Kiểm tra kết nối bằng lệnh:

```bash
ping google.com
```

- Kết nối SSH thành công đến máy ảo.
- Xác nhận các Firewall Rules hoạt động đúng như cấu hình.

---

# 6. Quản lý chi phí

Sau khi hoàn thành thực hành:

- Chuyển máy ảo `technews-vm` sang trạng thái:

```text
STOP
```

Việc dừng VM giúp:

- Tránh phát sinh chi phí Compute Engine.
- Tối ưu ngân sách trong quá trình học tập và thử nghiệm.

---

# ✅ Kết quả đạt được

- Hiểu mô hình Infrastructure as a Service (IaaS).
- Thiết lập thành công Virtual Private Cloud (VPC).
- Cấu hình Firewall Rules theo nguyên tắc Least Privilege.
- Triển khai thành công máy ảo Compute Engine.
- Kiểm tra thành công khả năng kết nối mạng và SSH.
- Quản lý tài nguyên hiệu quả bằng cách dừng máy ảo sau khi sử dụng.
![alt text](image-3.png)