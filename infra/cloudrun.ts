// File: infra/cloudrun.ts
import * as gcp from "@pulumi/gcp";

export const CloudRunService = new gcp.cloudrunv2.Service("TechnewsApi", {
  location: "asia-southeast1",
  template: {
    containers: [{
      image: "asia-southeast1-docker.pkg.dev/technews-500407/technews-repo/technews-api:v1",
    }],
  },
});