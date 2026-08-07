from fastapi import APIRouter
from app.config import settings
import httpx
import json

router = APIRouter(prefix="/planner", tags=["Destination Planner"])

CITY_DATABASE = {
    "tokyo": {
        "destination": "Tokyo, Japan",
        "must_visit": [
            {"place": "Senso-ji Temple & Nakamise Dori (Asakusa)", "est_cost": "Free admission (¥500 for street snacks)"},
            {"place": "Shibuya Crossing & Shibuya Sky Observation Deck", "est_cost": "¥2,200 (~$15 USD) for Sky Deck"},
            {"place": "Meiji Jingu Shrine & Yoyogi Park", "est_cost": "Free admission"},
            {"place": "Tokyo Skytree Tembo Deck", "est_cost": "¥2,100 (~$14 USD)"},
            {"place": "TeamLab Planets Digital Art Museum", "est_cost": "¥3,800 (~$25 USD)"}
        ],
        "estimated_budget_per_day": "$130 - $200 USD (¥20,000 - ¥30,000)",
        "best_time_to_visit": "March to May (Sakura Season) or September to November",
        "local_tips": "Purchase a Suica/Pasmo transit card for seamless subway travel, carry cash as small ramen shops use cash-only ticket vending machines, and reserve teamLab tickets online."
    },
    "hyderabad": {
        "destination": "Hyderabad, India",
        "must_visit": [
            {"place": "Charminar Monument & Laad Bazaar", "est_cost": "₹25 INR (~$0.30 USD)"},
            {"place": "Golconda Fort & Evening Sound-Light Show", "est_cost": "₹25 INR + ₹140 show (~$2 USD)"},
            {"place": "Chowmahalla Royal Nizam Palace", "est_cost": "₹100 INR (~$1.20 USD)"},
            {"place": "Salar Jung National Museum", "est_cost": "₹50 INR (~$0.60 USD)"},
            {"place": "Qutb Shahi Tombs Heritage Park", "est_cost": "₹100 INR (~$1.20 USD)"}
        ],
        "estimated_budget_per_day": "₹2,500 - ₹5,000 INR ($30 - $60 USD)",
        "best_time_to_visit": "October through March (Pleasant Winters)",
        "local_tips": "Savor authentic Hyderabadi Dum Biryani at Shadab or Paradise, use Metro auto-rickshaws for short trips, and explore pearl shopping near Charminar."
    }
}

@router.get("/recommend")
async def recommend_destinations(destination: str):
    clean_dest = destination.strip().lower()
    
    if "tok" in clean_dest:
        clean_dest = "tokyo"
    elif "hyd" in clean_dest:
        clean_dest = "hyderabad"

    for key, data in CITY_DATABASE.items():
        if key in clean_dest:
            return data

    title_dest = destination.strip().title()
    return {
        "destination": title_dest,
        "must_visit": [
            {"place": f"Historic Old Town & Heritage Center of {title_dest}", "est_cost": "Free / ~$5 USD entrance"},
            {"place": f"Central City Landmark & Historic Cathedral / Temple", "est_cost": "~$3 - $10 USD"},
            {"place": f"National Museum & Cultural Gallery of {title_dest}", "est_cost": "~$8 - $15 USD"},
            {"place": f"Scenic Riverfront Promenade & Botanical Park", "est_cost": "Free admission"},
            {"place": f"Local Craft Bazaar & Food Street Market", "est_cost": "Free entry (Pay per meal)"}
        ],
        "estimated_budget_per_day": "$80 - $150 USD",
        "best_time_to_visit": "Spring (March-May) or Autumn (September-November)",
        "local_tips": f"Explore early in the morning to beat crowds at major attractions in {title_dest}, use public transit day passes, and carry local cash for street markets."
    }
