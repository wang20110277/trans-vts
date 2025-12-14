package com.trans.sfm.mcp.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.trans.sfm.mcp.entity.SfmTaPrdDaily;
import com.trans.sfm.mcp.mapper.SfmTaPrdDailyMapper;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SfmTaPrdDailyService extends ServiceImpl<SfmTaPrdDailyMapper, SfmTaPrdDaily> {
    
    /**
     * 查询所有产品行情信息
     * @return 产品行情列表
     */
    public List<SfmTaPrdDaily> getAllPrdDailies() {
        return this.list();
    }
    
    /**
     * 根据产品代码查询产品行情信息
     * @param prdCode 产品代码
     * @return 产品行情信息
     */
    public List<SfmTaPrdDaily> getPrdDailiesByPrdCode(String prdCode) {
        return this.lambdaQuery().eq(SfmTaPrdDaily::getPrdCode, prdCode).list();
    }
    
    /**
     * 根据净值日期查询产品行情信息
     * @param issDate 净值日期
     * @return 产品行情列表
     */
    public List<SfmTaPrdDaily> getPrdDailiesByIssDate(Integer issDate) {
        return this.lambdaQuery().eq(SfmTaPrdDaily::getIssDate, issDate).list();
    }
    
    /**
     * 根据产品代码和净值日期查询产品行情信息
     * @param prdCode 产品代码
     * @param issDate 净值日期
     * @return 产品行情信息
     */
    public SfmTaPrdDaily getPrdDailyByPrdCodeAndIssDate(String prdCode, Integer issDate) {
        return this.lambdaQuery()
                .eq(SfmTaPrdDaily::getPrdCode, prdCode)
                .eq(SfmTaPrdDaily::getIssDate, issDate)
                .one();
    }
    
    /**
     * 根据TA代码查询产品行情信息
     * @param taCode TA代码
     * @return 产品行情列表
     */
    public List<SfmTaPrdDaily> getPrdDailiesByTaCode(String taCode) {
        return this.lambdaQuery().eq(SfmTaPrdDaily::getTaCode, taCode).list();
    }
}