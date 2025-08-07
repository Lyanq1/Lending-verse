"""
API for credit scoring system.
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from credit_scoring import CreditScoringSystem
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LendingVerse Credit Scoring API",
    description="API for credit scoring and risk assessment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize credit scoring system
credit_system = CreditScoringSystem(model_dir='models')

# Models for request/response
class FinancialData(BaseModel):
    current_assets: Optional[float] = None
    current_liabilities: Optional[float] = None
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    total_equity: Optional[float] = None
    total_debt: Optional[float] = None
    revenue: Optional[float] = None
    previous_revenue: Optional[float] = None
    cost_of_goods_sold: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_expenses: Optional[float] = None
    operating_income: Optional[float] = None
    net_income: Optional[float] = None
    previous_net_income: Optional[float] = None
    cash: Optional[float] = None
    inventory: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    ebit: Optional[float] = None
    interest_expense: Optional[float] = None
    debt_service: Optional[float] = None

class BusinessData(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    annual_revenue: Optional[float] = None
    business_type: Optional[str] = None
    years_in_business: Optional[int] = None
    country: Optional[str] = None
    region: Optional[str] = None

class CreditHistoryData(BaseModel):
    previous_loans: Optional[int] = None
    previous_defaults: Optional[int] = None
    total_payments: Optional[int] = None
    payments_on_time: Optional[int] = None
    late_payments: Optional[int] = None
    current_debt: Optional[float] = None
    credit_limit: Optional[float] = None
    external_credit_score: Optional[float] = None

class ScoringRequest(BaseModel):
    financial_data: Optional[FinancialData] = None
    business_data: Optional[BusinessData] = None
    credit_history_data: Optional[CreditHistoryData] = None
    borrower_id: Optional[str] = None

class ScoringResponse(BaseModel):
    credit_score: Dict[str, Any]
    default_probability: float
    risk_assessment: Dict[str, str]
    explanatory_factors: Optional[List[Dict[str, Any]]] = None
    timestamp: str
    borrower_id: Optional[str] = None

# API endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "Credit Scoring API", "version": "1.0.0"}

@app.post("/score", response_model=ScoringResponse)
async def score_borrower(request: ScoringRequest, background_tasks: BackgroundTasks):
    """
    Score a borrower based on financial, business, and credit history data.
    """
    try:
        # Convert Pydantic models to DataFrames
        financial_data = None
        if request.financial_data:
            financial_data = pd.DataFrame([request.financial_data.dict()])
        
        business_data = None
        if request.business_data:
            business_data = pd.DataFrame([request.business_data.dict()])
        
        credit_history_data = None
        if request.credit_history_data:
            credit_history_data = pd.DataFrame([request.credit_history_data.dict()])
        
        # Score the borrower
        assessment = credit_system.score_borrower(
            financial_data, business_data, credit_history_data
        )
        
        # Add borrower ID if provided
        if request.borrower_id:
            assessment['borrower_id'] = request.borrower_id
        
        # Save assessment in background
        background_tasks.add_task(
            credit_system.save_assessment, assessment, output_dir='assessments'
        )
        
        # Check for errors
        if 'error' in assessment:
            raise HTTPException(status_code=400, detail=assessment['error'])
        
        return assessment
    
    except Exception as e:
        logger.error(f"Error scoring borrower: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

@app.post("/score/file")
async def score_from_file(
    background_tasks: BackgroundTasks,
    financial_file: Optional[UploadFile] = File(None),
    business_file: Optional[UploadFile] = File(None),
    credit_history_file: Optional[UploadFile] = File(None),
    borrower_id: Optional[str] = Form(None)
):
    """
    Score a borrower based on uploaded CSV or JSON files.
    """
    try:
        # Process financial data file
        financial_data = None
        if financial_file:
            if financial_file.filename.endswith('.csv'):
                financial_data = pd.read_csv(financial_file.file)
            elif financial_file.filename.endswith('.json'):
                financial_data = pd.read_json(financial_file.file)
            else:
                raise HTTPException(status_code=400, detail="Financial data file must be CSV or JSON")
        
        # Process business data file
        business_data = None
        if business_file:
            if business_file.filename.endswith('.csv'):
                business_data = pd.read_csv(business_file.file)
            elif business_file.filename.endswith('.json'):
                business_data = pd.read_json(business_file.file)
            else:
                raise HTTPException(status_code=400, detail="Business data file must be CSV or JSON")
        
        # Process credit history data file
        credit_history_data = None
        if credit_history_file:
            if credit_history_file.filename.endswith('.csv'):
                credit_history_data = pd.read_csv(credit_history_file.file)
            elif credit_history_file.filename.endswith('.json'):
                credit_history_data = pd.read_json(credit_history_file.file)
            else:
                raise HTTPException(status_code=400, detail="Credit history data file must be CSV or JSON")
        
        # Score the borrower
        assessment = credit_system.score_borrower(
            financial_data, business_data, credit_history_data
        )
        
        # Add borrower ID if provided
        if borrower_id:
            assessment['borrower_id'] = borrower_id
        
        # Save assessment in background
        background_tasks.add_task(
            credit_system.save_assessment, assessment, output_dir='assessments'
        )
        
        # Check for errors
        if 'error' in assessment:
            raise HTTPException(status_code=400, detail=assessment['error'])
        
        return assessment
    
    except Exception as e:
        logger.error(f"Error scoring borrower from files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

@app.get("/categories")
async def get_credit_categories():
    """
    Get available credit score categories and their descriptions.
    """
    return credit_system.credit_categories

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)