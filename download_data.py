import os
import requests
import json
from typing import List, Dict
import logging
from config import Config
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndianLegalDataDownloader:
    def __init__(self):
        self.config = Config()
        self.create_directories()
        
        # API endpoints for Indian legal data
        self.SUPREME_COURT_API = "https://api.indiankanoon.org/supreme_court"
        self.HIGH_COURT_API = "https://api.indiankanoon.org/high_court"
        self.INDIA_CODE_API = "https://api.indiankanoon.org/statutes"
    
    def create_directories(self):
        """Create necessary directories for data storage"""
        directories = [
            self.config.CASE_LAW_DIR,
            self.config.STATUTES_DIR,
            self.config.SUPREME_COURT_CASES,
            self.config.HIGH_COURT_CASES,
            self.config.INDIAN_PENAL_CODE,
            self.config.CONSTITUTION
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def download_supreme_court_cases(self, year_range: List[int]):
        """Download Supreme Court cases for given year range"""
        logger.info(f"Downloading Supreme Court cases for years {year_range}")
        
        for year in tqdm(year_range, desc="Downloading Supreme Court cases"):
            try:
                # API call to get case list for the year
                response = requests.get(
                    f"{self.SUPREME_COURT_API}/year/{year}",
                    headers={"Authorization": f"Bearer {os.getenv('INDIAN_KANOON_API_KEY')}"}
                )
                cases = response.json()
                
                # Download each case
                for case in cases:
                    case_id = case['case_id']
                    case_response = requests.get(
                        f"{self.SUPREME_COURT_API}/case/{case_id}",
                        headers={"Authorization": f"Bearer {os.getenv('INDIAN_KANOON_API_KEY')}"}
                    )
                    case_data = case_response.json()
                    
                    # Save case data
                    with open(
                        os.path.join(self.config.SUPREME_COURT_CASES, f"{case_id}.json"),
                        'w',
                        encoding='utf-8'
                    ) as f:
                        json.dump(case_data, f, ensure_ascii=False, indent=2)
                
            except Exception as e:
                logger.error(f"Error downloading Supreme Court cases for year {year}: {str(e)}")
    
    def download_high_court_cases(self, court: str, year_range: List[int]):
        """Download High Court cases for given court and year range"""
        logger.info(f"Downloading {court} High Court cases for years {year_range}")
        
        for year in tqdm(year_range, desc=f"Downloading {court} High Court cases"):
            try:
                # API call to get case list for the year
                response = requests.get(
                    f"{self.HIGH_COURT_API}/{court}/year/{year}",
                    headers={"Authorization": f"Bearer {os.getenv('INDIAN_KANOON_API_KEY')}"}
                )
                cases = response.json()
                
                # Download each case
                for case in cases:
                    case_id = case['case_id']
                    case_response = requests.get(
                        f"{self.HIGH_COURT_API}/{court}/case/{case_id}",
                        headers={"Authorization": f"Bearer {os.getenv('INDIAN_KANOON_API_KEY')}"}
                    )
                    case_data = case_response.json()
                    
                    # Save case data
                    with open(
                        os.path.join(self.config.HIGH_COURT_CASES, f"{court}_{case_id}.json"),
                        'w',
                        encoding='utf-8'
                    ) as f:
                        json.dump(case_data, f, ensure_ascii=False, indent=2)
                
            except Exception as e:
                logger.error(f"Error downloading {court} High Court cases for year {year}: {str(e)}")
    
    def download_statutes(self):
        """Download Indian statutes"""
        logger.info("Downloading Indian statutes")
        
        try:
            # Download Indian Penal Code
            ipc_response = requests.get(
                f"{self.INDIA_CODE_API}/ipc",
                headers={"Authorization": f"Bearer {os.getenv('INDIAN_KANOON_API_KEY')}"}
            )
            ipc_data = ipc_response.json()
            
            with open(
                os.path.join(self.config.INDIAN_PENAL_CODE, "ipc.json"),
                'w',
                encoding='utf-8'
            ) as f:
                json.dump(ipc_data, f, ensure_ascii=False, indent=2)
            
            # Download Constitution
            constitution_response = requests.get(
                f"{self.INDIA_CODE_API}/constitution",
                headers={"Authorization": f"Bearer {os.getenv('INDIAN_KANOON_API_KEY')}"}
            )
            constitution_data = constitution_response.json()
            
            with open(
                os.path.join(self.config.CONSTITUTION, "constitution.json"),
                'w',
                encoding='utf-8'
            ) as f:
                json.dump(constitution_data, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.error(f"Error downloading statutes: {str(e)}")

def main():
    downloader = IndianLegalDataDownloader()
    
    # Download Supreme Court cases for last 5 years
    current_year = 2024
    year_range = list(range(current_year - 5, current_year + 1))
    downloader.download_supreme_court_cases(year_range)
    
    # Download High Court cases for major courts
    high_courts = ["delhi", "bombay", "madras", "calcutta", "karnataka"]
    for court in high_courts:
        downloader.download_high_court_cases(court, year_range)
    
    # Download statutes
    downloader.download_statutes()

if __name__ == "__main__":
    main() 