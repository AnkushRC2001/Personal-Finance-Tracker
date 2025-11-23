def categorize_transaction(description: str) -> str:
    description = description.lower()
    
    # Food & Dining
    if any(keyword in description for keyword in ["swiggy", "zomato", "restaurant", "cafe", "starbucks", "kfc", "mcdonalds", "burger", "pizza", "dining", "lunch", "dinner", "breakfast", "food"]):
        return "Food"
    
    # Travel & Commute
    elif any(keyword in description for keyword in ["uber", "ola", "rapido", "train", "metro", "flight", "airline", "bus", "ticket", "fuel", "petrol", "diesel", "parking", "toll", "travel", "cab"]):
        return "Travel"
    
    # Shopping & Groceries
    elif any(keyword in description for keyword in ["amazon", "flipkart", "myntra", "ajio", "zara", "h&m", "nike", "adidas", "mall", "store", "mart", "supermarket", "grocery", "blinkit", "zepto", "instamart", "shop"]):
        return "Shopping"
    
    # Utilities & Bills
    elif any(keyword in description for keyword in ["electricity", "bill", "water", "gas", "internet", "wifi", "broadband", "mobile", "recharge", "dth", "subscription", "postpaid", "prepaid"]):
        return "Utilities"
        
    # Entertainment
    elif any(keyword in description for keyword in ["netflix", "spotify", "prime", "movie", "cinema", "bookmyshow", "game", "steam", "playstation", "xbox", "entertainment"]):
        return "Entertainment"
        
    # Health & Fitness
    elif any(keyword in description for keyword in ["pharmacy", "doctor", "hospital", "med", "clinic", "gym", "fitness", "health", "medicine"]):
        return "Health"
    
    # Housing
    elif "rent" in description or "housing" in description or "maintenance" in description:
        return "Rent"
        
    else:
        return "Other"
