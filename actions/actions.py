from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

API_KEY = "54e9405bead3399cb9e097867394011c"

DESTINATIONS = {
    'beach': [
        {'name': 'Goa, India', 'budget': '₹₹', 'season': 'Nov-Feb', 'highlights': 'Beaches, Nightlife, Churches', 'days': '4-6'},
        {'name': 'Kerala, India', 'budget': '₹₹', 'season': 'Sep-Mar', 'highlights': 'Backwaters, Ayurveda, Houseboats', 'days': '5-7'}
    ],
    'mountain': [
        {'name': 'Manali, Himachal Pradesh', 'budget': '₹₹', 'season': 'Mar-Jun, Oct-Feb', 'highlights': 'Snow, Trekking, Solang Valley', 'days': '4-6'},
        {'name': 'Darjeeling, West Bengal', 'budget': '₹₹', 'season': 'Mar-Jun, Sep-Nov', 'highlights': 'Tea Gardens, Toy Train, Kanchenjunga Views', 'days': '3-5'}
    ],
    'cultural': [
        {'name': 'Jaipur, Rajasthan', 'budget': '₹₹', 'season': 'Oct-Mar', 'highlights': 'Forts, Palaces, Local Bazaars', 'days': '3-5'},
        {'name': 'Varanasi, Uttar Pradesh', 'budget': '₹', 'season': 'Oct-Mar', 'highlights': 'Ghats, Temples, Ganga Aarti', 'days': '2-4'}
    ],
    'city': [
        {'name': 'Delhi, India', 'budget': '₹₹', 'season': 'Oct-Mar', 'highlights': 'Heritage, Street Food, Markets', 'days': '3-5'},
        {'name': 'Mumbai, India', 'budget': '₹₹₹', 'season': 'Nov-Feb', 'highlights': 'Beaches, Nightlife, Bollywood', 'days': '3-5'}
    ]
}

HOTELS = {
    'goa': [
        {'name': 'Taj Exotica Resort & Spa', 'rating': 4.9, 'price': '₹18,000/night', 'type': 'luxury'},
        {'name': 'The Leela Goa', 'rating': 4.8, 'price': '₹21,000/night', 'type': 'luxury'},
        {'name': 'Marina Bay Beach Resort', 'rating': 4.2, 'price': '₹5,500/night', 'type': 'budget'}
    ],
    'manali': [
        {'name': 'Span Resort & Spa', 'rating': 4.6, 'price': '₹9,000/night', 'type': 'midrange'},
        {'name': 'Snow Valley Resorts', 'rating': 4.4, 'price': '₹6,500/night', 'type': 'budget'}
    ],
    'jaipur': [
        {'name': 'The Oberoi Rajvilas', 'rating': 4.9, 'price': '₹25,000/night', 'type': 'luxury'},
        {'name': 'Umaid Bhawan Heritage Hotel', 'rating': 4.5, 'price': '₹7,500/night', 'type': 'midrange'}
    ]
}

RESTAURANTS = {
    'goa': [
        {'name': 'Vinayak Family Restaurant', 'cuisine': 'Goan Seafood', 'rating': 4.6, 'price': '₹₹', 'specialty': 'Fish Thali'},
        {'name': 'Thalassa', 'cuisine': 'Greek', 'rating': 4.7, 'price': '₹₹₹', 'specialty': 'Sunset Dining'}
    ],
    'jaipur': [
        {'name': 'Laxmi Misthan Bhandar', 'cuisine': 'Rajasthani', 'rating': 4.5, 'price': '₹', 'specialty': 'Ghewar, Thali'},
        {'name': 'Peacock Rooftop Restaurant', 'cuisine': 'Indian', 'rating': 4.6, 'price': '₹₹', 'specialty': 'Rooftop Dining'}
    ]
}

class ActionRecommendDestinations(Action):
    def name(self) -> Text:
        return "action_recommend_destinations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        destination_type = tracker.get_slot('destination_type') or 'beach'
        if destination_type not in DESTINATIONS:
            dispatcher.utter_message(text="Sorry, I couldn't find destinations for that type.")
            return []
        destinations = DESTINATIONS[destination_type]
        message = f"🌍 Here are some {destination_type} destinations you might love:\n\n"
        for dest in destinations:
            message += f"**{dest['name']}**\n💰 Budget: {dest['budget']} | 📅 Best: {dest['season']}\n✨ Highlights: {dest['highlights']}\n⏱️ Recommended: {dest['days']} days\n\n"
        dispatcher.utter_message(text=message)
        dispatcher.utter_message(text="Would you like to explore hotels or restaurants?", buttons=[
            {"title": "🏨 Hotels", "payload": "/search_hotels"},
            {"title": "🍽️ Restaurants", "payload": "/find_restaurants"}
        ])
        return []

class ActionRecommendHotels(Action):
    def name(self) -> Text:
        return "action_recommend_hotels"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = (tracker.get_slot('location') or 'goa').lower()
        if location not in HOTELS:
            dispatcher.utter_message(text="Sorry, I couldn't find hotels for that location.")
            return []
        hotels = HOTELS[location]
        message = f"🏨 Top hotels in {location.title()}:\n\n"
        for h in hotels:
            message += f"{h['name']} - ⭐ {h['rating']}/5 - {h['price']} ({h['type'].title()})\n"
        dispatcher.utter_message(text=message)
        return []

class ActionRecommendRestaurants(Action):
    def name(self) -> Text:
        return "action_recommend_restaurants"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = (tracker.get_slot('location') or 'jaipur').lower()
        if location not in RESTAURANTS:
            dispatcher.utter_message(text="Sorry, I couldn't find restaurants for that location.")
            return []
        restaurants = RESTAURANTS[location]
        message = f"🍴 Best restaurants in {location.title()}:\n\n"
        for r in restaurants:
            message += f"{r['name']} - {r['cuisine']} ({r['price']}) - ⭐ {r['rating']}\n🌟 Specialty: {r['specialty']}\n\n"
        dispatcher.utter_message(text=message)
        return []

class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot('location') or 'Goa'
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get('cod') != 200:
            dispatcher.utter_message(text=f"Sorry, I couldn't fetch weather data for {location}.")
            return []
        weather = response['weather'][0]['description'].capitalize()
        temp = response['main']['temp']
        dispatcher.utter_message(text=f"🌤️ It's currently {temp}°C in {location.title()} with {weather}.")
        return []
