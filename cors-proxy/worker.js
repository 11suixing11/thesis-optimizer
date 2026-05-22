// Cloudflare Worker — Anthropic API CORS 代理
// 部署到 Cloudflare Workers（免费）

export default {
  async fetch(request) {
    // 处理 CORS 预检
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders() });
    }

    const url = new URL(request.url);

    // 只代理 /v1/messages 路径
    if (url.pathname !== "/v1/messages") {
      return new Response("Not Found", { status: 404 });
    }

    // 从请求头获取 API Key
    const apiKey = request.headers.get("x-api-key");
    if (!apiKey) {
      return jsonResponse({ error: "Missing x-api-key header" }, 401);
    }

    // 构建转发请求
    const body = await request.text();
    const apiResponse = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body,
    });

    // 返回响应（加上 CORS 头）
    const responseBody = await apiResponse.text();
    return new Response(responseBody, {
      status: apiResponse.status,
      headers: {
        ...corsHeaders(),
        "Content-Type": "application/json",
      },
    });
  },
};

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, x-api-key",
    "Access-Control-Max-Age": "86400",
  };
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...corsHeaders(), "Content-Type": "application/json" },
  });
}
