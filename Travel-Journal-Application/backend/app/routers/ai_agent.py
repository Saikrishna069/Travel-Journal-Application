from fastapi import APIRouter
from app.models import ChatMessage
from app.config import settings
import httpx
import sys

router = APIRouter(prefix="/ai", tags=["AI Agent"])

SYSTEM_PROMPT = (
    "You are a global AI Travel Assistant & Knowledge Engine. "
    "Analyze the user's question, identify the exact city/region and intent, "
    "and provide a direct, highly accurate, and structured answer for any city in India or worldwide."
)

DESTINATIONS_DB = {
    "hyderabad": {
        "title": "Hyderabad, Telangana, India",
        "day1": "Morning: Charminar & Chowmahalla Palace. Afternoon: Salar Jung Museum. Evening: Laad Bazaar pearl shopping & Irani Chai at Nimrah Café.",
        "day2": "Morning: Golconda Fort & Qutb Shahi Tombs. Evening: Durgam Cheruvu Cable Bridge & Hitech City.",
        "day3": "Morning: Birla Mandir. Afternoon: Hussain Sagar Lake Boat Ride & Buddha Statue. Evening: Shilparamam Crafts Village.",
        "hotels": "Luxury: Taj Falaknuma Palace (~₹35,000), ITC Kohenur. Mid-Range: Mercure KCP. Budget: FabHotel Abids (~₹1,800).",
        "food": "Hyderabadi Dum Biryani (Paradise/Shadab/Bawarchi), Haleem, Mirchi Ka Salan, Osmania Biscuits."
    },
    "tokyo": {
        "title": "Tokyo, Japan",
        "day1": "Morning: Senso-ji Temple Asakusa. Afternoon: Tokyo Skytree & Ueno Park. Evening: Akihabara Electric Town.",
        "day2": "Morning: Meiji Shrine & Harajuku. Afternoon: Shibuya Crossing & Shibuya Sky. Evening: Shinjuku Golden Gai.",
        "day3": "Morning: Tsukiji Outer Seafood Market. Afternoon: TeamLab Planets Digital Art Toyosu. Evening: Odaiba waterfront.",
        "hotels": "Luxury: Park Hyatt Tokyo, Aman Tokyo. Mid-Range: Hotel Gracery Shinjuku. Budget: Nine Hours Capsule.",
        "food": "Fresh Tsukiji Sushi, Tonkotsu Ramen, Tempura, Wagyu Beef, Matcha Desserts."
    },
    "paris": {
        "title": "Paris, France",
        "day1": "Morning: Eiffel Tower & Champ de Mars. Afternoon: Arc de Triomphe & Champs-Élysées. Evening: Seine River Cruise.",
        "day2": "Morning: Louvre Museum. Afternoon: Notre-Dame & Sainte-Chapelle. Evening: Le Marais bistros.",
        "day3": "Morning: Palace of Versailles day trip. Evening: Montmartre & Sacré-Cœur Basilica.",
        "hotels": "Luxury: The Ritz Paris, Four Seasons George V. Mid-Range: Hotel Malte. Budget: MIJE Marais Hostel.",
        "food": "Croissants, Crepes, Duck Confit, Escargots, Macarons (Ladurée), French Cheese."
    }
}

@router.post("/chat")
async def chat_assistant(msg: ChatMessage):
    user_prompt = msg.message.strip()
    q_lower = user_prompt.lower()
    
    if settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY.strip()) > 0:
        try:
            print(f"DEBUG: Attempting OpenAI API call", file=sys.stderr)
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.2,
                        "max_tokens": 500
                    }
                )
                
                print(f"DEBUG: OpenAI Response Status: {res.status_code}", file=sys.stderr)
                data = res.json()
                
                if "choices" in data and len(data["choices"]) > 0:
                    return {"reply": data["choices"][0]["message"]["content"]}
                    
        except Exception as e:
            print(f"DEBUG: OpenAI Error: {str(e)}", file=sys.stderr)

    for key, data in DESTINATIONS_DB.items():
        if key in q_lower:
            return {"reply": f"🎯 Travel Analysis for {data['title']}...\n\n{data['day1']}\n{data['day2']}\n{data['day3']}"}

    return {"reply": "Ask me about travel destinations!"}
    # Fallback to template if OpenAI fails
    for key, data in DESTINATIONS_DB.items():
        if key in q_lower:
            return {
                "reply": f"🎯 **Travel Analysis for {data['title']}:**\n\n"
                         f"🗓️ **Itinerary:** Day 1: {data['day1']}\nDay 2: {data['day2']}\nDay 3: {data['day3']}\n\n"
                         f"🏨 **Hotels:** {data['hotels']}\n\n"
                         f"🍲 **Famous Food:** {data['food']}"
            }

    return {
        "reply": f"🤖 **AI Travel Assistant Analysis for '{user_prompt}':**\n"
                 f"When planning your journey, prioritize historical landmarks early in the morning, use local public transport cards, and sample signature regional dishes!"
    }    # Fallback to template if OpenAI fails
    for key, data in DESTINATIONS_DB.items():
        if key in q_lower:
            return {
                "reply": f"🎯 **Travel Analysis for {data['title']}:**\n\n"
                         f"🗓️ **Itinerary:** Day 1: {data['day1']}\nDay 2: {data['day2']}\nDay 3: {data['day3']}\n\n"
                         f"🏨 **Hotels:** {data['hotels']}\n\n"
                         f"🍲 **Famous Food:** {data['food']}"
            }

    return {
        "reply": f"🤖 **AI Travel Assistant Analysis for '{user_prompt}':**\n"
                 f"When planning your journey, prioritize historical landmarks early in the morning, use local public transport cards, and sample signature regional dishes!"
    }
