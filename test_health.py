"""
Unit tests for core functions
"""
import pytest
import sys
sys.path.insert(0, '/workspaces/projekt')

from utils import (
    calculate_bmi, validate_date, validate_blood_group, validate_sex,
    validate_age, validate_vaccination_status, is_due_for_booster
)
from datetime import datetime, timedelta

class TestBMICalculation:
    """Test BMI calculation"""
    
    def test_bmi_normal(self):
        """Test normal BMI"""
        bmi, status = calculate_bmi(170, 65)
        assert 22 <= bmi <= 23
        assert status == "Normal"
    
    def test_bmi_underweight(self):
        """Test underweight BMI"""
        bmi, status = calculate_bmi(170, 45)
        assert bmi < 18.5
        assert status == "Underweight"
    
    def test_bmi_overweight(self):
        """Test overweight BMI"""
        bmi, status = calculate_bmi(170, 90)
        assert 25 <= bmi < 30
        assert status == "Overweight"
    
    def test_bmi_obese(self):
        """Test obese BMI"""
        bmi, status = calculate_bmi(170, 110)
        assert bmi >= 30
        assert status == "Obese"
    
    def test_bmi_invalid_input(self):
        """Test invalid BMI input"""
        bmi, status = calculate_bmi(0, 65)
        assert bmi is None
        assert status == "Invalid measurements"

class TestValidation:
    """Test validation functions"""
    
    def test_validate_date_valid(self):
        """Test valid date"""
        assert validate_date("2024-12-10") == True
    
    def test_validate_date_invalid(self):
        """Test invalid date"""
        assert validate_date("12-10-2024") == False
        assert validate_date("2024-13-01") == False
    
    def test_validate_blood_group_valid(self):
        """Test valid blood groups"""
        for bg in ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']:
            assert validate_blood_group(bg) == True
    
    def test_validate_blood_group_invalid(self):
        """Test invalid blood group"""
        assert validate_blood_group("C+") == False
        assert validate_blood_group("ABC") == False
    
    def test_validate_sex_valid(self):
        """Test valid sex"""
        assert validate_sex("M") == True
        assert validate_sex("F") == True
        assert validate_sex("Other") == True
    
    def test_validate_sex_invalid(self):
        """Test invalid sex"""
        assert validate_sex("X") == False
    
    def test_validate_age_valid(self):
        """Test valid age"""
        assert validate_age(10) == True
        assert validate_age(25) == True
    
    def test_validate_age_invalid(self):
        """Test invalid age"""
        assert validate_age(3) == False
        assert validate_age(30) == False
    
    def test_validate_vaccination_status(self):
        """Test vaccination status"""
        assert validate_vaccination_status("Y") == True
        assert validate_vaccination_status("N") == True
        assert validate_vaccination_status("X") == False

class TestVaccinationBooster:
    """Test vaccination booster logic"""
    
    def test_booster_due(self):
        """Test booster is due"""
        past_date = (datetime.now() - timedelta(days=6*365)).strftime('%Y-%m-%d')
        assert is_due_for_booster(past_date, 5) == True
    
    def test_booster_not_due(self):
        """Test booster is not due"""
        recent_date = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m-%d')
        assert is_due_for_booster(recent_date, 5) == False
    
    def test_booster_no_date(self):
        """Test with no vaccination date"""
        assert is_due_for_booster(None) == False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
