package com.trans.sfm.mcp;

import org.noear.solon.ai.mcp.client.McpClientProvider;

import java.util.Collections;
import java.util.Map;

public class McpClientTest {
    public static void main(String[] args) throws Exception {
        McpClientProvider toolProvider = McpClientProvider.builder()
                .apiUrl("http://localhost:8080/mcp/sse")
                .build();

        //工具调用
        Map<String, Object> map = Collections.singletonMap("location", "杭州");
        String rst = toolProvider.callToolAsText("getWeather", map).getContent();
        System.out.println(rst);
        assert "晴，14度".equals(rst);


        //资源读取
        String resourceContent = toolProvider.readResourceAsText("config://app-version").getContent();
        System.out.println(resourceContent);
    }
}
