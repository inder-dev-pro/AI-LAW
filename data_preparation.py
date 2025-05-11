import os
import json
import pandas as pd
from typing import List, Dict
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndianLegalDataProcessor:
    def __init__(self):
        self.config = Config()
        self.create_directories()
    
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
    
    def process_supreme_court_cases(self, case_files: List[str]) -> pd.DataFrame:
        """Process Supreme Court case files"""
        cases = []
        for file in case_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    case_data = json.load(f)
                    cases.append({
                        'case_id': case_data.get('case_id'),
                        'title': case_data.get('title'),
                        'judges': case_data.get('judges'),
                        'date': case_data.get('date'),
                        'text': case_data.get('text'),
                        'category': case_data.get('category'),
                        'court': 'Supreme Court',
                        'judgment_type': case_data.get('judgment_type')
                    })
            except Exception as e:
                logger.error(f"Error processing file {file}: {str(e)}")
        
        return pd.DataFrame(cases)
    
    def process_high_court_cases(self, case_files: List[str]) -> pd.DataFrame:
        """Process High Court case files"""
        cases = []
        for file in case_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    case_data = json.load(f)
                    cases.append({
                        'case_id': case_data.get('case_id'),
                        'title': case_data.get('title'),
                        'judges': case_data.get('judges'),
                        'date': case_data.get('date'),
                        'text': case_data.get('text'),
                        'category': case_data.get('category'),
                        'court': 'High Court',
                        'judgment_type': case_data.get('judgment_type')
                    })
            except Exception as e:
                logger.error(f"Error processing file {file}: {str(e)}")
        
        return pd.DataFrame(cases)
    
    def process_statutes(self, statute_files: List[str]) -> pd.DataFrame:
        """Process Indian statutes"""
        statutes = []
        for file in statute_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    statute_data = json.load(f)
                    statutes.append({
                        'statute_id': statute_data.get('statute_id'),
                        'title': statute_data.get('title'),
                        'section': statute_data.get('section'),
                        'text': statute_data.get('text'),
                        'category': statute_data.get('category')
                    })
            except Exception as e:
                logger.error(f"Error processing file {file}: {str(e)}")
        
        return pd.DataFrame(statutes)
    
    def prepare_training_data(self) -> Dict:
        """Prepare the final training dataset"""
        # Process Supreme Court cases
        sc_files = [f for f in os.listdir(self.config.SUPREME_COURT_CASES) 
                   if f.endswith('.json')]
        sc_cases = self.process_supreme_court_cases(
            [os.path.join(self.config.SUPREME_COURT_CASES, f) for f in sc_files]
        )
        
        # Process High Court cases
        hc_files = [f for f in os.listdir(self.config.HIGH_COURT_CASES) 
                   if f.endswith('.json')]
        hc_cases = self.process_high_court_cases(
            [os.path.join(self.config.HIGH_COURT_CASES, f) for f in hc_files]
        )
        
        # Process statutes
        statute_files = [f for f in os.listdir(self.config.STATUTES_DIR) 
                        if f.endswith('.json')]
        statutes = self.process_statutes(
            [os.path.join(self.config.STATUTES_DIR, f) for f in statute_files]
        )
        
        # Combine all data
        all_cases = pd.concat([sc_cases, hc_cases], ignore_index=True)
        
        return {
            'cases': all_cases,
            'statutes': statutes
        }
    
    def save_processed_data(self, data: Dict):
        """Save processed data to disk"""
        # Save cases
        data['cases'].to_csv(
            os.path.join(self.config.CASE_LAW_DIR, 'processed_cases.csv'),
            index=False
        )
        
        # Save statutes
        data['statutes'].to_csv(
            os.path.join(self.config.STATUTES_DIR, 'processed_statutes.csv'),
            index=False
        )
        
        logger.info("Processed data saved successfully")

def main():
    processor = IndianLegalDataProcessor()
    data = processor.prepare_training_data()
    processor.save_processed_data(data)

if __name__ == "__main__":
    main() 