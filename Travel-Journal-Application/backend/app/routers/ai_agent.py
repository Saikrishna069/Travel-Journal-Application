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
    },
    "goa": {
        "title": "Goa, India",
        "day1": "Morning: Baga Beach & water sports. Afternoon: Fort Aguada & lighthouse. Evening: Sunset at Anjuna Beach.",
        "day2": "Morning: Dudhsagar Waterfall trek. Afternoon: Spice plantation tour. Evening: Beach shack dinner.",
        "day3": "Morning: Old Goa churches & architecture. Afternoon: Calangute Beach. Evening: Casino cruise.",
        "hotels": "Luxury: Taj Exotica (~₹25,000). Mid-Range: Novotel Goa (~₹8,000). Budget: Backpackers (~₹1,500).",
        "food": "Fish Curry Rice, Prawn Koliwada, Bebinca, Feni, Tandoori Fish."
    }
}

@router.post("/chat")
async def chat_assistant(msg: ChatMessage):
    """AI Chat endpoint with OpenAI integration and fallback templates"""
    user_prompt = msg.message.strip()
    q_lower = user_prompt.lower()
    
    # Try to use OpenAI API if key is available
    if settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY.strip()) > 0:
        try:
            print(f"DEBUG: Attempting OpenAI API call with key length: {len(settings.OPENAI_API_KEY)}", file=sys.stderr)
            
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
                        "temperature": 0.7,
                        "max_tokens": 500
                    }
                )
                
                print(f"DEBUG: OpenAI API Response Status: {res.status_code}", file=sys.stderr)
                
                if res.status_code == 200:
                    data = res.json()
                    
                    if "choices" in data and len(data["choices"]) > 0:
                        reply = data["choices"][0]["message"]["content"]
                        print(f"DEBUG: Got OpenAI response: {len(reply)} characters", file=sys.stderr)
                        return {"reply": reply}
                    else:
                        print(f"DEBUG: Unexpected response format: {data}", file=sys.stderr)
                else:
                    error_msg = res.text if res.text else "Unknown error"
                    print(f"DEBUG: OpenAI API failed with status {res.status_code}: {error_msg}", file=sys.stderr)
                    
        except Exception as e:
            print(f"DEBUG: OpenAI API Exception: {str(e)}", file=sys.stderr)
            pass  # Fall back to template responses
    else:
        print(f"DEBUG: OPENAI_API_KEY not set or empty. Key status: {bool(settings.OPENAI_API_KEY)}", file=sys.stderr)

    # Fallback: Use template responses if OpenAI is not available
    for key, data in DESTINATIONS_DB.items():
        if key in q_lower:
            return {
                "reply": f"🎯 **Travel Analysis for {data['title']}:**\n\n"
                         f"🗓️ **Itinerary:**\n"
                         f"**Day 1:** {data['day1']}\n"
                         f"**Day 2:** {data['day2']}\n"
                         f"**Day 3:** {data['day3']}\n\n"
                         f"🏨 **Hotels:** {data['hotels']}\n\n"
                         f"🍲 **Famous Food:** {data['food']}"
            }

    # Generic fallback response
    return {
        "reply": f"🤖 **AI Travel Assistant Response:**\n\n"
                 f"I'm here to help you plan your travel! Ask me about:\n"
                 f"• Destination recommendations\n"
                 f"• Travel itineraries\n"
                 f"• Hotel suggestions\n"
                 f"• Local food and dining\n"
                 f"• Transportation tips\n"
                 f"• Packing advice\n\n"
                 f"For best results, mention a specific city or destination!"
    }
