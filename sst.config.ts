/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "technews-backend", // Tên ứng dụng của bạn
      removal: input?.stage === "prod" ? "retain" : "remove",
      protect: ["prod"].includes(input?.stage),
      home: "local", // Sử dụng local state để đơn giản hóa quá trình thực tập, không cần AWS credentials
      providers: {
        gcp: "9.29.0", // Phiên bản GCP provider
      }
    };
  },
  async run() {
    // Dynamic import theo yêu cầu của SST v3
    const gcp = await import("@pulumi/gcp");

    // 1. Cấu hình GCP
    const project = "technews-500407";
    const region = "asia-southeast1";

    // Sử dụng Image đã push lên Artifact Registry từ Day 3
    const imageUrl = `asia-southeast1-docker.pkg.dev/${project}/technews-repo/technews-api:v1`;

    // 2. Định nghĩa Cloud Run Service thông qua mã (IaC)
    const service = new gcp.cloudrunv2.Service("technews-api-service", {
      project: project,
      location: region,
      name: "technews-api-sst", // Tên service trên Cloud Run sẽ được tạo
      template: {
        containers: [{
          image: imageUrl
        }]
      }
    });

    // Bỏ return Outputs vì đang gặp lỗi serialization trong SST v3 + GCP
  },
});