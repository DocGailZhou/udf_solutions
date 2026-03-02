"""
Business Growth & Market Event Logic
===================================

This module contains the logic for business growth patterns and market event simulation
to make sample data generation more realistic and representative of growing businesses.

Implements a three-phase continuous growth model:
- Phase 1 (0-33%): Strong Growing Baseline (1.4x → 2.2x avg 1.8x)
- Phase 2 (33-67%): Sustained Growth (0.8x → 1.4x avg 1.1x)  
- Phase 3 (67-100%): Explosive Growth (2.0x → 4.0x avg 3.0x)

Market events include Black Friday, Christmas, Memorial Day, etc.
Customer tier amplification makes VIP/Partner customers more responsive to trends.
"""

from datetime import datetime, timedelta
from typing import Tuple
import calendar

def calculate_business_phase(current_date: datetime, start_date: datetime, end_date: datetime) -> Tuple[int, float]:
    """
    Calculate which business growth phase we're in and the growth multiplier.
    Uses the entire period as a scale of 100%, with each phase getting proportional days.
    
    Returns:
        Tuple[int, float]: (phase_number, growth_multiplier)
    """
    total_days = (end_date - start_date).days
    days_elapsed = (current_date - start_date).days
    
    # Calculate progress as percentage of total period (0.0 to 1.0)
    progress_percent = days_elapsed / total_days if total_days > 0 else 0.0
    
    # Define phase boundaries as percentages
    phase_1_end = 0.33  # 0% to 33%
    phase_2_end = 0.67  # 33% to 67%
    # phase_3_end = 1.0  # 67% to 100%
    
    if progress_percent <= phase_1_end:
        # Phase 1: Strong Growing Baseline (0% → 33%)
        phase = 1
        phase_progress = progress_percent / phase_1_end  # 0.0 to 1.0 within this phase
        # Growth from 1.4 to 2.2 (average 1.8x - very strong growing baseline)
        multiplier = 1.4 + (phase_progress * 0.8)
        
    elif progress_percent <= phase_2_end:
        # Phase 2: Continued Growth (33% → 67%) 
        phase = 2
        phase_progress = (progress_percent - phase_1_end) / (phase_2_end - phase_1_end)  # 0.0 to 1.0 within this phase
        # Slower growth from 0.8 to 1.4 (average 1.1x - sustained growth)
        multiplier = 0.8 + (phase_progress * 0.6)
        
    else:
        # Phase 3: Explosive Growth (67% → 100%)
        phase = 3
        phase_progress = (progress_percent - phase_2_end) / (1.0 - phase_2_end)  # 0.0 to 1.0 within this phase
        # Growth from 2.0 to 4.0 (average 3.0x - explosive growth & expansion)
        multiplier = 2.0 + (phase_progress * 2.0)
    
    return phase, multiplier

def get_market_event_multiplier(current_date: datetime) -> Tuple[str, float, float]:
    """
    Determine if current date falls on a market event and return multipliers.
    
    Returns:
        Tuple[str, float, float]: (event_name, order_frequency_multiplier, order_size_multiplier)
    """
    month = current_date.month
    day = current_date.day
    
    # Black Friday (last Friday of November)
    if month == 11:
        # Find the last Friday of November
        last_day = calendar.monthrange(current_date.year, 11)[1]
        last_friday = None
        for d in range(last_day, 0, -1):
            test_date = datetime(current_date.year, 11, d)
            if test_date.weekday() == 4:  # Friday is 4
                last_friday = d
                break
        
        if last_friday and day >= last_friday and day <= last_friday + 3:  # 4-day weekend
            return "Black Friday Weekend", 4.0, 1.4
    
    # Christmas Shopping Season (December 1-25)
    if month == 12 and 1 <= day <= 25:
        # Gradual ramp-up throughout December
        week = (day - 1) // 7 + 1  # Week 1-4
        multipliers = {1: 1.2, 2: 1.5, 3: 1.8, 4: 2.0}
        week_mult = multipliers.get(min(week, 4), 2.0)
        return "Christmas Shopping", week_mult, 1.2
    
    # Memorial Day Weekend (last Monday of May)
    if month == 5:
        # Find the last Monday of May
        last_day = calendar.monthrange(current_date.year, 5)[1]
        last_monday = None
        for d in range(last_day, 0, -1):
            test_date = datetime(current_date.year, 5, d)
            if test_date.weekday() == 0:  # Monday is 0
                last_monday = d
                break
        
        if last_monday and day >= last_monday - 2 and day <= last_monday:  # 3-day weekend
            return "Memorial Day Weekend", 1.5, 1.3  # Especially good for camping
    
    # Back-to-School (August 15-31)
    if month == 8 and day >= 15:
        return "Back-to-School", 1.3, 1.2  # Good for kitchen equipment
    
    # New Year Resolution (January 2-15)
    if month == 1 and 2 <= day <= 15:
        return "New Year Resolutions", 1.4, 1.1  # Fitness/outdoor goals
    
    # Post-Holiday Lull (January 16-31)
    if month == 1 and 16 <= day <= 31:
        return "Post-Holiday Lull", 0.7, 0.9
    
    return "Normal", 1.0, 1.0

def get_customer_tier_multiplier(customer_relationship_type: str, base_multiplier: float) -> float:
    """
    Apply tier-based multipliers to the base growth multiplier.
    Higher tiers benefit more from growth and suffer more from decline.
    
    Args:
        customer_relationship_type: The customer's relationship type
        base_multiplier: The base phase multiplier
        
    Returns:
        float: Adjusted multiplier for this customer tier
    """
    tier_amplifiers = {
        # Individual customers
        "standard": 1.0,    # Base tier, no amplification
        "premium": 1.3,     # 30% more responsive to changes
        "vip": 1.6,         # 60% more responsive
        
        # Business customers  
        "smb": 1.2,         # 20% more responsive
        "premier": 1.5,     # 50% more responsive
        "partner": 1.6,     # 60% more responsive (highest tier)
        
        # Government customers (less responsive)
        "federal": 0.8,     # 20% less responsive
        "state": 0.7,       # 30% less responsive  
        "local": 0.6        # 40% less responsive
    }
    
    tier_key = customer_relationship_type.lower()
    amplifier = tier_amplifiers.get(tier_key, 1.0)
    
    # Calculate the deviation from 1.0 and amplify it
    deviation = base_multiplier - 1.0
    amplified_deviation = deviation * amplifier
    
    # Ensure we don't go below 0.1 (minimum activity level)
    final_multiplier = max(1.0 + amplified_deviation, 0.1)
    
    return final_multiplier

def calculate_order_adjustments(current_date: datetime, start_date: datetime, end_date: datetime, 
                              customer_relationship_type: str) -> Tuple[float, float, str]:
    """
    Calculate the complete order frequency and size adjustments for a given date and customer.
    
    Returns:
        Tuple[float, float, str]: (frequency_multiplier, size_multiplier, debug_info)
    """
    # Get business phase
    phase, phase_multiplier = calculate_business_phase(current_date, start_date, end_date)
    
    # Get market event
    event_name, event_freq_mult, event_size_mult = get_market_event_multiplier(current_date)
    
    # Apply customer tier amplification
    tier_adjusted_multiplier = get_customer_tier_multiplier(customer_relationship_type, phase_multiplier)
    
    # Combine all multipliers
    final_freq_multiplier = tier_adjusted_multiplier * event_freq_mult
    final_size_multiplier = event_size_mult
    
    # Debug information
    debug_info = f"Phase{phase}({phase_multiplier:.2f}) × Tier({tier_adjusted_multiplier:.2f}) × {event_name}({event_freq_mult:.1f}×{event_size_mult:.1f})"
    
    return final_freq_multiplier, final_size_multiplier, debug_info