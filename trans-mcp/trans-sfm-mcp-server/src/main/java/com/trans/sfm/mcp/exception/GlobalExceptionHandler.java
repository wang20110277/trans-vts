package com.trans.sfm.mcp.exception;

import com.trans.sfm.mcp.dto.McpResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<McpResponse> handleException(Exception e) {
        McpResponse response = new McpResponse(null, "error", e.getMessage());
        return ResponseEntity.status(500).body(response);
    }
}