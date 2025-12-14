package com.trans.sfm.mcp.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;

@Data
@TableName("sfm_ta_prd_daily")
public class SfmTaPrdDaily {
    
    /**
     * 物理主键
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
    
    /**
     * 净值日期
     */
    private Integer issDate;
    
    /**
     * 确认日期
     */
    private Integer cfmDate;
    
    /**
     * TA代码
     */
    private String taCode;
    
    /**
     * 产品代码
     */
    private String prdCode;
    
    /**
     * 产品净值
     */
    private BigDecimal nav;
    
    /**
     * 七日年化收益率
     */
    private BigDecimal sevenRate;
    
    /**
     * 万份单位收益
     */
    private BigDecimal tenthIncome;
    
    /**
     * 产品状态
     */
    private String prdStatus;
    
    /**
     * 产品累计净值
     */
    private BigDecimal totNav;
}