import request from "@/utils/request";

export function convert_text(payload) {
  return request.post(`/tool/convert_text`, payload);
}
