package com.trans.sfm.mcp.dto;

public class McpResponse {
    private String response;
    private String status;
    private Object data;

    public McpResponse() {}

    public McpResponse(String response, String status, Object data) {
        this.response = response;
        this.status = status;
        this.data = data;
    }

    // Getters and setters
    public String getResponse() {
        return response;
    }

    public void setResponse(String response) {
        this.response = response;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }
}