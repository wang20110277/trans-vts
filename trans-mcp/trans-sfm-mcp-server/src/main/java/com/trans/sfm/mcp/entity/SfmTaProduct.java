package com.trans.sfm.mcp.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("sfm_ta_product")
public class SfmTaProduct {
    
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
    
    private String prdId;
    
    private String prdCode;
    
    private String modelFlag;
    
    private String prdCyclicalType;
    
    private String taCode;
    
    private String prdName;
    
    private String prdShortName;
    
    private String interestWay;
    
    private BigDecimal nav;
    
    private BigDecimal totNav;
    
    private Integer navDate;
    
    private BigDecimal faceValue;
    
    private BigDecimal issPrice;
    
    private String prdBenchmark;
    
    private String prdSponsor;
    
    private String prdTrustee;
    
    private String prdManager;
    
    private String branchNo;
    
    private String depId;
    
    private Integer ipoStartDate;
    
    private Integer ipoEndDate;
    
    private Integer estabDate;
    
    private Integer lockUpDays;
    
    private String beginOfLock;
    
    private Integer incomeStartDate;
    
    private Integer incomeEndDate;
    
    private Integer endDate;
    
    private Integer alimitEndDate;
    
    private Integer ipoTime;
    
    private Integer realEstabDate;
    
    private BigDecimal prdMinBala;
    
    private BigDecimal prdMaxBala;
    
    private BigDecimal pMinBala;
    
    private BigDecimal pMaxBala;
    
    private BigDecimal prdIssueRealBala;
    
    private String divModes;
    
    private String divMode;
    
    private String recPerLiquiMode;
    
    private String openPerLiquiMode;
    
    private String buyAccountingType;
    
    private String withdrawMode;
    
    private String channels;
    
    private String clientGroups;
    
    private String controlFlag;
    
    private String subExp;
    
    private String riskLevel;
    
    private String prdStatus;
    
    private String convFlag;
    
    private BigDecimal prdTotal;
    
    private String currType;
    
    private String cashFlag;
    
    private Integer openTime;
    
    private Integer closeTime;
    
    private BigDecimal firstAmt;
    
    private BigDecimal pappAmt;
    
    private BigDecimal pminimumHoldingVol;
    
    private BigDecimal pmaximumHoldingAmt;
    
    private Integer holdingLimitType;
    
    private BigDecimal ofirstAmt;
    
    private BigDecimal oappAmt;
    
    private BigDecimal ominimumHoldingVol;
    
    private BigDecimal omaximumHoldingAmt;
    
    private BigDecimal buyUnitAmt;
    
    private BigDecimal withdrawUnitAmt;
    
    private BigDecimal prdCurrentQuota;
    
    private String debitAccount;
    
    private Long crebitCustId;
    
    private String crebitAccountName;
    
    private String advAccount;
    
    private Long advCustId;
    
    private String advAccountName;
    
    private String chargeAccount;
    
    private String shareClass;
    
    private String isNeedCharge;
    
    private String isNightMarket;
    
    private String jsonParam;
    
    private String createdBy;
    
    private LocalDateTime createTime;
    
    private String updatedBy;
    
    private LocalDateTime updateTime;
}