def calculate_price(weight, rate, making):
    return weight * rate + making


def get_text(lang):
    TEXT = {
        "English":{
            "title":"Jewellery Collections",
            "search":"Search",
            "filters":"Filters",
            "weight":"Weight",
            "making":"Making Charge",
            "voice":"Voice Search",
            "suggest":"AI Suggestions",
            "home":"Home",
            "products":"Products"
        },
        "Hindi":{
            "title":"आभूषण संग्रह",
            "search":"खोज",
            "filters":"फ़िल्टर",
            "weight":"वजन",
            "making":"मेकिंग चार्ज",
            "voice":"आवाज़ खोज",
            "suggest":"सुझाव",
            "home":"होम",
            "products":"उत्पाद"
        },
        "Bengali":{
            "title":"গহনার সংগ্রহ",
            "search":"অনুসন্ধান",
            "filters":"ফিল্টার",
            "weight":"ওজন",
            "making":"মেকিং চার্জ",
            "voice":"ভয়েস সার্চ",
            "suggest":"প্রস্তাবনা",
            "home":"হোম",
            "products":"পণ্য"
        }
    }
    return TEXT[lang]
