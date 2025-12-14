package com.trans.sfm.mcp.service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.trans.sfm.mcp.entity.SfmTaProduct;
import com.trans.sfm.mcp.mapper.SfmTaProductMapper;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SfmTaProductService extends ServiceImpl<SfmTaProductMapper, SfmTaProduct> {
    
    /**
     * 查询所有产品信息
     * @return 产品列表
     */
    public List<SfmTaProduct> getAllProducts() {
        return this.list();
    }
    
    /**
     * 根据产品代码查询产品信息
     * @param prdCode 产品代码
     * @return 产品信息
     */
    public SfmTaProduct getProductByPrdCode(String prdCode) {
        return this.lambdaQuery().eq(SfmTaProduct::getPrdCode, prdCode).one();
    }
    
    /**
     * 根据产品名称模糊查询产品信息
     * @param prdName 产品名称
     * @return 产品列表
     */
    public List<SfmTaProduct> getProductsByPrdName(String prdName) {
        return this.lambdaQuery().like(SfmTaProduct::getPrdName, prdName).list();
    }
}