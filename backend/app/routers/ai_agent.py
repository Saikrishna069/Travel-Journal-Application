from fastapi import APIRouter, Depends
from app.models import ChatMessage
from app.utils import get_current_user
from app.config import settings
import httpx
import re

router = APIRouter(prefix="/ai", tags=["AI Agent"])

SYSTEM_PROMPT = (
    "You are a global AI Travel Assistant & Knowledge Engine. "
    "Analyze the user's question, identify the exact city/region and intent, "
    "and provide a direct, highly accurate, and structured answer for any city in India or worldwide."
)

# Comprehensive Global & Indian Regional Destinations Knowledge Base
DESTINATIONS_DB = {
    # INDIAN CITIES & REGIONS
    "hyderabad": {
        "title": "Hyderabad, Telangana, India",
        "day1": "Morning: Charminar & Chowmahalla Palace. Afternoon: Salar Jung Museum. Evening: Laad Bazaar pearl shopping & Irani Chai at Nimrah Café.",
        "day2": "Morning: Golconda Fort & Qutb Shahi Tombs. Evening: Durgam Cheruvu Cable Bridge & Hitech City.",
        "day3": "Morning: Birla Mandir. Afternoon: Hussain Sagar Lake Boat Ride & Buddha Statue. Evening: Shilparamam Crafts Village.",
        "hotels": "Luxury: Taj Falaknuma Palace (~₹35,000), ITC Kohenur. Mid-Range: Mercure KCP. Budget: FabHotel Abids (~₹1,800).",
        "food": "Hyderabadi Dum Biryani (Paradise/Shadab/Bawarchi), Haleem, Mirchi Ka Salan, Osmania Biscuits."
    },
    "mumbai": {
        "title": "Mumbai, Maharashtra, India",
        "day1": "Morning: Gateway of India & Taj Mahal Palace Hotel. Afternoon: Elephanta Caves ferry ride. Evening: Marine Drive (Queen's Necklace) sunset.",
        "day2": "Morning: Chhatrapati Shivaji Maharaj Terminus (UNESCO) & Crawford Market. Evening: Juhu Beach & Bandra Bandstand.",
        "day3": "Morning: Siddhivinayak Temple & Haji Ali Dargah. Afternoon: Prince of Wales Museum (CSMVS).",
        "hotels": "Luxury: The Taj Mahal Palace, The St. Regis. Mid-Range: Suba Palace. Budget: Zostel Mumbai / FabHotel.",
        "food": "Vada Pav (Ashok Vada Pav), Pav Bhaji (Cannon), Bhelpuri at Girgaon Chowpatty, Bombil Fry."
    },
    "delhi": {
        "title": "Delhi (NCR), India",
        "day1": "Morning: Red Fort (Lal Qila) & Chandni Chowk rickshaw ride. Afternoon: Jama Masjid & Paranthe Wali Gali. Evening: India Gate & Kartavya Path.",
        "day2": "Morning: Qutub Minar (1192 AD). Afternoon: Humayun's Tomb (Precursor to Taj Mahal) & Lotus Temple. Evening: Connaught Place.",
        "day3": "Morning: Swaminarayan Akshardham Temple. Afternoon: National Museum & Hauz Khas Village.",
        "hotels": "Luxury: The Imperial, The Leela Palace. Mid-Range: Bloomrooms Janpath. Budget: City Park CP.",
        "food": "Chole Bhature (Sitaram Diwan Chand), Butter Chicken (Moti Mahal), Old Delhi Kebabs, Dahi Bhalla."
    },
    "bengaluru": {
        "title": "Bengaluru (Bangalore), Karnataka, India",
        "day1": "Morning: Bengaluru Palace & Tipu Sultan's Summer Palace. Afternoon: Lalbagh Botanical Garden. Evening: Church Street & MG Road breweries.",
        "day2": "Morning: Cubbon Park & Vidhana Soudha. Afternoon: Visvesvaraya Industrial Museum. Evening: Indiranagar cafes.",
        "day3": "Morning: ISKCON Temple. Afternoon: Bannerghatta National Park Safari.",
        "hotels": "Luxury: The Leela Palace, Taj West End. Mid-Range: The Paul Bangalore. Budget: Treebo Trend.",
        "food": "Masala Dosa (MTR / Vidyarthi Bhavan), Filter Coffee, Benne Dosa, Mysore Pak."
    },
    "jaipur": {
        "title": "Jaipur (Pink City), Rajasthan, India",
        "day1": "Morning: Amber Fort elephant/jeep ride & Sheesh Mahal. Afternoon: Jal Mahal (Water Palace) view & Hawa Mahal (Palace of Winds). Evening: Johari Bazaar.",
        "day2": "Morning: City Palace & Jantar Mantar (UNESCO Observatory). Afternoon: Nahargarh Fort sunset view over Pink City.",
        "day3": "Morning: Jaigarh Fort (world's largest cannon). Afternoon: Albert Hall Museum.",
        "hotels": "Luxury: Rambagh Palace, Samode Palace. Mid-Range: Shahpura House. Budget: Zostel Jaipur.",
        "food": "Dal Baati Churma, Pyaaz Kachori (Rawat), Laal Maas, Ghewar sweets."
    },
    "varanasi": {
        "title": "Varanasi (Benares), Uttar Pradesh, India",
        "day1": "Morning: Sunrise boat ride on Ganges River (Dashashwamedh to Manikarnika Ghat). Afternoon: Kashi Vishwanath Temple. Evening: Ganga Aarti ceremony.",
        "day2": "Morning: Excursion to Sarnath (where Lord Buddha gave first sermon). Evening: Assi Ghat cultural music.",
        "day3": "Morning: Banaras Hindu University (BHU) & Bharat Kala Bhavan. Evening: Shopping for Banarasi Silk Sarees.",
        "hotels": "Luxury: BrijRama Palace, Taj Nadesar Palace. Mid-Range: Hotel Surya. Budget: Stops Hostel Varanasi.",
        "food": "Banarasi Paan, Kachori Jalebi, Tamatar Chaat (Deena), Blue Lassi."
    },
    "goa": {
        "title": "Goa, India",
        "day1": "Morning: Basilica of Bom Jesus & Se Cathedral (Old Goa). Afternoon: Fontainhas Latin Quarter Panaji. Evening: Mandovi River Cruise.",
        "day2": "Morning: Fort Aguada & Calangute/Baga beaches. Evening: Anjuna/Vagator beach shacks & sunset.",
        "day3": "Morning: Dudhsagar Waterfalls jeep safari & Spice Plantation lunch. Evening: Palolem Beach South Goa.",
        "hotels": "Luxury: Taj Exotica, The Leela. Mid-Range: Lemon Tree Candolim. Budget: Zostel Anjuna.",
        "food": "Goan Fish Curry Rice, Pork Vindaloo, Bebinca, Prawn Balchão, Fresh Grilled Lobster."
    },

    # GLOBAL WORLD CITIES
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
    "london": {
        "title": "London, United Kingdom",
        "day1": "Morning: Tower of London & Tower Bridge. Afternoon: St Paul's Cathedral & Millennium Bridge. Evening: West End Theatre show.",
        "day2": "Morning: British Museum. Afternoon: Big Ben, Parliament & Westminster Abbey. Evening: London Eye wheel.",
        "day3": "Morning: Buckingham Palace Guard Change & Hyde Park. Afternoon: Victoria and Albert Museum & Harrods.",
        "hotels": "Luxury: The Ritz London, The Savoy. Mid-Range: CitizenM Tower Bridge. Budget: YHA London Central.",
        "food": "Fish and Chips, Traditional Sunday Roast, Afternoon Tea, Chicken Tikka Masala."
    },
    "dubai": {
        "title": "Dubai, United Arab Emirates",
        "day1": "Morning: Burj Khalifa At the Top (124th floor) & Dubai Mall. Afternoon: Dubai Aquarium. Evening: Dubai Fountain Show.",
        "day2": "Morning: Old Dubai Gold & Spice Souks. Afternoon: Abra boat ride across Dubai Creek. Evening: Desert Safari & BBQ.",
        "day3": "Morning: Palm Jumeirah & Atlantis Aquaventure. Evening: Dubai Marina walk & yacht cruise.",
        "hotels": "Luxury: Burj Al Arab, Atlantis The Palm. Mid-Range: Rove Downtown. Budget: Premier Inn Dubai.",
        "food": "Shawarma, Al Machboos, Luqaimat, Camel Milk Chocolate, Arabian Grills."
    },
    "singapore": {
        "title": "Singapore",
        "day1": "Morning: Marina Bay Sands Observation Deck. Afternoon: Gardens by the Bay (Supertree Grove). Evening: Marina Bay Light Show.",
        "day2": "Morning: Singapore Botanic Gardens & Orchid Garden. Afternoon: Chinatown & Sri Mariamman Temple. Evening: Clarke Quay.",
        "day3": "Morning: Sentosa Island & Universal Studios. Evening: Night Safari at Singapore Zoo.",
        "hotels": "Luxury: Marina Bay Sands, Raffles Singapore. Mid-Range: YOTEL Singapore. Budget: Pod Boutique Capsule.",
        "food": "Hainanese Chicken Rice, Chili Crab, Laksa, Kaya Toast, Satay at Lau Pa Sat."
    }
}

def analyze_user_prompt(query: str) -> str:
    q_clean = query.strip()
    q_lower = q_clean.lower()

    # Identify matching city/region key
    matched_key = None
    for key in DESTINATIONS_DB:
        if key in q_lower:
            matched_key = key
            break

    # 1. DAY PLAN / ITINERARY QUERY
    if any(k in q_lower for k in ["day", "itinerary", "plan", "tour", "visit", "trip", "schedule"]):
        if matched_key:
            data = DESTINATIONS_DB[matched_key]
            return (
                f"🗓️ **3-Day Detailed Itinerary for {data['title']}:**\n\n"
                f"🏛️ **Day 1:** {data['day1']}\n\n"
                f"🏰 **Day 2:** {data['day2']}\n\n"
                f"🌅 **Day 3:** {data['day3']}\n\n"
                f"💡 **Travel Advice:** Arrive at primary attractions by 8:00 AM to avoid lines and use day transit passes."
            )
        else:
            # Dynamic Plan for any city name not in preset database
            city_title = q_clean.replace("3 day plan in", "").replace("plan", "").replace("itinerary", "").strip().title()
            if not city_title: city_title = "Selected Destination"
            return (
                f"🗓️ **3-Day Detailed Itinerary for {city_title}:**\n\n"
                f"🏛️ **Day 1 (Historical Heritage & Cultural Core):**\n"
                f"• Morning (8:30 AM): Visit the primary historic monument and central heritage landmark of {city_title}.\n"
                f"• Afternoon (1:00 PM): Sample traditional regional dishes at iconic local eateries.\n"
                f"• Evening (5:30 PM): Stroll through central cultural squares and old town night markets.\n\n"
                f"🏰 **Day 2 (Fortresses, Palaces & Museum Tours):**\n"
                f"• Morning (9:00 AM): Guided tour of national architectural palaces, forts, or cathedrals/temples.\n"
                f"• Afternoon (2:00 PM): Visit top art galleries and historical museums.\n"
                f"• Evening (6:30 PM): Enjoy panoramic views from scenic waterfront or hilltop viewpoints.\n\n"
                f"🌅 **Day 3 (Nature Parks & Local Handicraft Markets):**\n"
                f"• Morning (9:00 AM): Explore botanical gardens and scenic nature parks.\n"
                f"• Afternoon (1:30 PM): Visit handicraft markets for regional souvenirs.\n"
                f"• Evening (6:00 PM): Relaxing evening cafe experience and farewell dinner."
            )

    # 2. HOTEL / ACCOMMODATION QUERY
    if any(k in q_lower for k in ["hotel", "stay", "resort", "accommodation", "where to stay", "lodge"]):
        if matched_key:
            data = DESTINATIONS_DB[matched_key]
            return f"🏨 **Best Hotels & Accommodations to Stay in {data['title']}:**\n\n{data['hotels']}"
        else:
            city_title = q_clean.replace("best hotel in", "").replace("hotel", "").replace("stay in", "").strip().title()
            return f"🏨 **Hotel Guidance for {city_title}:**\n• **Luxury:** Book 5-star heritage hotels or international chains in central district.\n• **Mid-Range:** Select 3/4-star business hotels near major metro subway lines.\n• **Budget:** Book verified hostels (e.g. Zostel/FabHotel) with 4.5+ star guest reviews."

    # 3. FOOD / RESTAURANT QUERY
    if any(k in q_lower for k in ["food", "eat", "restaurant", "cuisine", "dish", "biryani", "breakfast"]):
        if matched_key:
            data = DESTINATIONS_DB[matched_key]
            return f"🍽️ **Famous Foods & Top Dining Spots in {data['title']}:**\n\n{data['food']}"
        else:
            city_title = q_clean.replace("best food in", "").replace("food in", "").strip().title()
            return f"🍲 **Famous Local Dishes in {city_title}:**\nExplore heritage food lanes, regional night markets, and iconic local breakfast spots to sample signature traditional dishes of {city_title}."

    # DEFAULT DIRECT ANSWER
    if matched_key:
        data = DESTINATIONS_DB[matched_key]
        return (
            f"📍 **Complete Guide for {data['title']}:**\n\n"
            f"🗓️ **Itinerary:** Day 1: {data['day1']} | Day 2: {data['day2']}\n\n"
            f"🏨 **Hotels:** {data['hotels']}\n\n"
            f"🍲 **Famous Foods:** {data['food']}"
        )

    return (
        f"🎯 **Analysis & Direct Answer for '{q_clean}':**\n"
        f"For any destination in India or globally, ensure you research top historic landmarks, "
        f"book museum entry tickets in advance, use city transit passes, and sample regional street foods. "
        f"Ask specifically for '3 day plan in [city]', 'hotels in [city]', or 'famous food in [city]' for immediate details!"
    )

@router.post("/chat")
async def chat_assistant(msg: ChatMessage, user_id: str = Depends(get_current_user)):
    user_prompt = msg.message.strip()
    
    # If OpenAI API key exists, call GPT model for direct dynamic responses
    if settings.OPENAI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.2
                    }
                )
                data = res.json()
                if "choices" in data and len(data["choices"]) > 0:
                    reply = data["choices"][0]["message"]["content"]
                    return {"reply": reply}
        except Exception:
            pass

    reply_text = analyze_user_prompt(user_prompt)
    return {"reply": reply_text}
