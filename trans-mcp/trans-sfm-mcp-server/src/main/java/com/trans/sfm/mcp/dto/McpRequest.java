package com.trans.sfm.mcp.dto;

import java.util.List;
import java.util.Map;

public class McpRequest {
    private String message;
    private List<Map<String, String>> messages;
    private Map<String, Object> options;

    // Getters and setters
    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public List<Map<String, String>> getMessages() {
        return messages;
    }

    public void setMessages(List<Map<String, String>> messages) {
        this.messages = messages;
    }

    public Map<String, Object> getOptions() {
        return options;
    }

    public void setOptions(Map<String, Object> options) {
        this.options = options;
    }
}