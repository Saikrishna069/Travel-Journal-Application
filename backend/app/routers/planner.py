from fastapi import APIRouter, Depends
from app.utils import get_current_user
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
    "kyoto": {
        "destination": "Kyoto, Japan",
        "must_visit": [
            {"place": "Fushimi Inari Taisha (10,000 Torii Gates)", "est_cost": "Free admission"},
            {"place": "Kiyomizu-dera Historic Wooden Temple", "est_cost": "¥400 (~$3 USD)"},
            {"place": "Kinkaku-ji (Golden Pavilion)", "est_cost": "¥500 (~$3.50 USD)"},
            {"place": "Arashiyama Bamboo Grove & Monkey Park", "est_cost": "¥600 (~$4 USD)"},
            {"place": "Gion Historic Geisha District Walking Tour", "est_cost": "Free (Guided tours ~$25 USD)"}
        ],
        "estimated_budget_per_day": "$120 - $180 USD (¥18,000 - ¥27,000)",
        "best_time_to_visit": "March-May or October-November",
        "local_tips": "Use local city bus day passes, arrive at Fushimi Inari before 7:00 AM to beat crowds, and wear shoes that are easy to slip off for temple entry."
    },
    "paris": {
        "destination": "Paris, France",
        "must_visit": [
            {"place": "Eiffel Tower Summit Access", "est_cost": "€28 EUR (~$30 USD)"},
            {"place": "Louvre Museum (Mona Lisa & Antiquities)", "est_cost": "€22 EUR (~$24 USD)"},
            {"place": "Palace of Versailles & Gardens", "est_cost": "€21 EUR (~$23 USD)"},
            {"place": "Sainte-Chapelle Stained Glass Chapel", "est_cost": "€13 EUR (~$14 USD)"},
            {"place": "Montmartre & Sacré-Cœur Basilica", "est_cost": "Free admission (Basilica dome €8 EUR)"}
        ],
        "estimated_budget_per_day": "€130 - €210 EUR ($140 - $230 USD)",
        "best_time_to_visit": "April to June or September to November",
        "local_tips": "Book Louvre and Eiffel Tower tickets weeks in advance, get a Paris Museum Pass if visiting 3+ museums, and use the Metro Navigo Easy pass."
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
    },
    "rome": {
        "destination": "Rome, Italy",
        "must_visit": [
            {"place": "Colosseum, Roman Forum & Palatine Hill", "est_cost": "€18 EUR (~$20 USD)"},
            {"place": "Vatican Museums & Sistine Chapel", "est_cost": "€20 EUR (~$22 USD)"},
            {"place": "Pantheon Ancient Monument", "est_cost": "€5 EUR (~$5.50 USD)"},
            {"place": "Trevi Fountain & Spanish Steps", "est_cost": "Free admission"},
            {"place": "Borghese Gallery & Gardens", "est_cost": "€13 EUR (~$14 USD)"}
        ],
        "estimated_budget_per_day": "€120 - €190 EUR ($130 - $200 USD)",
        "best_time_to_visit": "April-May or September-October",
        "local_tips": "Carry a refillable water bottle for free street nasoni fountains, buy skip-the-line Vatican tickets, and avoid eating at restaurants right on main squares."
    }
}

@router.get("/recommend")
async def recommend_destinations(destination: str, user_id: str = Depends(get_current_user)):
    clean_dest = destination.strip().lower()
    
    # Handle typos / aliases (e.g. tokya -> tokyo)
    if "tok" in clean_dest:
        clean_dest = "tokyo"
    elif "kyo" in clean_dest:
        clean_dest = "kyoto"
    elif "par" in clean_dest:
        clean_dest = "paris"
    elif "hyd" in clean_dest or "secun" in clean_dest:
        clean_dest = "hyderabad"
    elif "rom" in clean_dest:
        clean_dest = "rome"

    for key, data in CITY_DATABASE.items():
        if key in clean_dest:
            return data

    # Default Dynamic Response for any city
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
