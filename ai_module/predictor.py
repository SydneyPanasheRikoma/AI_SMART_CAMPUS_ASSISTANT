"""
Predictor for estimating complaint resolution time
Uses historical data and simple ML to predict resolution time
"""
from typing import Dict, List
import random


class ResolutionTimePredictor:
    """
    Predicts complaint resolution time based on:
    - Category
    - Priority
    - Historical data patterns
    """
    
    def __init__(self):
        # Average resolution times by category (in hours)
        # Based on typical campus complaint resolution patterns
        self.category_avg_times = {
            'IT Issues': 24,  # 1 day
            'Hostel Management': 48,  # 2 days
            'Academics': 72,  # 3 days
            'Administration': 96,  # 4 days
            'Library': 48,  # 2 days
            'Sports & Recreation': 72,  # 3 days
            'Other': 120  # 5 days
        }
        
        # Priority multipliers
        self.priority_multipliers = {
            'High': 0.5,  # Resolve faster
            'Medium': 1.0,  # Normal time
            'Low': 1.5  # May take longer
        }
        
        # Workload factor (simulated)
        # In a real system, this would be based on current pending complaints
        self.workload_factor = 1.0
    
    def predict_resolution_time(
        self,
        category: str,
        priority: str,
        description: str = None
    ) -> Dict:
        """
        Predict resolution time for a complaint
        
        Args:
            category: Complaint category
            priority: Priority level
            description: Optional complaint description
        
        Returns:
            Dictionary with predicted time in hours and days
        """
        # Get base time for category
        base_time = self.category_avg_times.get(category, 72)
        
        # Apply priority multiplier
        priority_mult = self.priority_multipliers.get(priority, 1.0)
        
        # Calculate predicted time
        predicted_hours = base_time * priority_mult * self.workload_factor
        
        # Add some variance (±20%)
        variance = random.uniform(0.8, 1.2)
        predicted_hours = int(predicted_hours * variance)
        
        # Ensure minimum of 1 hour
        predicted_hours = max(predicted_hours, 1)
        
        # Calculate days
        predicted_days = predicted_hours / 24
        
        return {
            'hours': predicted_hours,
            'days': round(predicted_days, 1),
            'category_avg': base_time,
            'priority_factor': priority_mult,
            'confidence': 0.75  # Confidence in prediction
        }
    
    def get_resolution_estimate(
        self,
        category: str,
        priority: str,
        description: str = None
    ) -> str:
        """
        Get human-readable resolution time estimate
        """
        prediction = self.predict_resolution_time(category, priority, description)
        
        hours = prediction['hours']
        
        if hours < 24:
            return f"Within {hours} hours"
        elif hours < 48:
            return "1-2 days"
        elif hours < 72:
            return "2-3 days"
        elif hours < 120:
            return "3-5 days"
        else:
            return f"{int(hours/24)} days"
    
    def update_workload_factor(self, pending_count: int):
        """
        Update workload factor based on pending complaints
        
        Args:
            pending_count: Number of pending complaints
        """
        # Increase resolution time if many pending complaints
        if pending_count < 10:
            self.workload_factor = 0.9
        elif pending_count < 20:
            self.workload_factor = 1.0
        elif pending_count < 50:
            self.workload_factor = 1.2
        else:
            self.workload_factor = 1.5
    
    def get_category_statistics(self, complaints_data: List[Dict]) -> Dict:
        """
        Analyze historical data to get category-wise statistics
        
        Args:
            complaints_data: List of complaint dictionaries
        
        Returns:
            Statistics by category
        """
        stats = {}
        
        for category in self.category_avg_times.keys():
            category_complaints = [
                c for c in complaints_data 
                if c.get('category') == category
            ]
            
            if category_complaints:
                # Calculate actual average resolution time
                resolved = [
                    c for c in category_complaints 
                    if c.get('status') == 'Resolved' and c.get('resolution_time')
                ]
                
                if resolved:
                    avg_time = sum(c['resolution_time'] for c in resolved) / len(resolved)
                else:
                    avg_time = self.category_avg_times[category]
                
                stats[category] = {
                    'total_complaints': len(category_complaints),
                    'resolved': len(resolved),
                    'avg_resolution_hours': round(avg_time, 1),
                    'avg_resolution_days': round(avg_time / 24, 1)
                }
            else:
                stats[category] = {
                    'total_complaints': 0,
                    'resolved': 0,
                    'avg_resolution_hours': self.category_avg_times[category],
                    'avg_resolution_days': round(self.category_avg_times[category] / 24, 1)
                }
        
        return stats


# Global predictor instance
predictor = ResolutionTimePredictor()


def predict_resolution_time(category: str, priority: str, description: str = None) -> Dict:
    """
    Convenience function to predict resolution time
    """
    return predictor.predict_resolution_time(category, priority, description)


def get_resolution_estimate(category: str, priority: str) -> str:
    """
    Convenience function to get resolution estimate
    """
    return predictor.get_resolution_estimate(category, priority)
