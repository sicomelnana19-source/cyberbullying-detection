import re

# ============================================
# CYBERBULLYING LEXICON
# ============================================

CYBERBULLYING_LEXICON = {
    # Direct Insults
    'idiot': 'Insult',
    'idiots': 'Insult',
    'stupid': 'Insult',
    'dumb': 'Insult',
    'loser': 'Insult',
    'worthless': 'Insult',
    'useless': 'Insult',
    'pathetic': 'Insult',
    'fool': 'Insult',
    'moron': 'Insult',
    'retard': 'Insult',
    'dummy': 'Insult',
    'dumbass': 'Insult',
    'horrible': 'Insult',
    'shitty': 'Insult',
    'bullshit': 'Insult',
    'nut': 'Insult',
    'stfu': 'Insult',
    'basterd': 'Insult',
    'ass': 'Insult',
    'hate': 'Insult',
    'hatred': 'Insult',
    'disgustingly': 'Insult',  # Betulkan ejaan
    'mfs': 'Insult',
    'shittiest': 'Insult',
    'fucked': 'Insult',
    'asshole': 'Insult',
    'dumbest': 'Insult',
    
    # Derogatory
    'ugly': 'Derogatory',
    'fat': 'Derogatory',
    'disgusting': 'Derogatory',
    'nasty': 'Derogatory',
    'gawky': 'Derogatory',
    'deformed': 'Derogatory',
    'broken': 'Derogatory',
    'ill': 'Derogatory',
    'poor': 'Derogatory',
    'filthy': 'Derogatory',
    'sexist': 'Derogatory',
    'pussy hoe': 'Derogatory',
    'son of a bitch': 'Derogatory',  # Betulkan
    'pussy': 'Derogatory',  # Hanya dalam Derogatory
    'sexism': 'Derogatory',
    'pig': 'Derogatory',
    'btch': 'Derogatory',
    'racist': 'Derogatory',
    'bitches': 'Derogatory',  # Betulkan
    'nigger': 'Derogatory',
    'mother fuckerd': 'Derogatory',
    
    # Exclusion
    'ignore': 'Exclusion',
    'reject': 'Exclusion',
    'exclude': 'Exclusion',
    'alone': 'Exclusion',
    'leave': 'Exclusion',
    'abandon': 'Exclusion',
    'lost': 'Exclusion',  # Hanya dalam Exclusion
    
    # Threats
    'kill': 'Threat',
    'hurt': 'Threat',
    'harm': 'Threat',
    'threat': 'Threat',
    'danger': 'Threat',
    'murder': 'Threat',
    'attack': 'Threat',
    'destroy': 'Threat',
    'die': 'Threat',
    'burn': 'Threat',
    'shoot': 'Threat',
    'hang': 'Threat',
    'f..k up': 'Threat',  # Hanya dalam Threat
    
    # Harassment
    'harass': 'Harassment',
    'annoy': 'Harassment',
    'bully': 'Harassment',
    'bullied': 'Harassment',
    'bullying': 'Harassment',
    'bullies': 'Harassment',
    'abuse': 'Harassment',
    'torture': 'Harassment',
    'disturb': 'Harassment',
    'stalk': 'Harassment',
    'intimidate': 'Harassment',
    'punks': 'Harassment',
    'punk': 'Harassment',
    'wtf': 'Harassment',
    'bullshitting': 'Harassment',
    
    # Profanity
    'fuck': 'Profanity',
    'fucking': 'Profanity',
    'asshole': 'Profanity',
    'bitch': 'Profanity',
    'bastard': 'Profanity',
    'shit': 'Profanity',
    'damn': 'Profanity',
    'hell': 'Profanity',
    'crap': 'Profanity',
    'f*uck': 'Profanity',
    'fag': 'Profanity',
    'shitty': 'Profanity',
    'bullshit': 'Profanity',
    'fucken': 'Profanity',
    'dammit': 'Profanity',  # Betulkan
    'son of a bitch': 'Profanity',
    'ass': 'Profanity',
    'holy shit': 'Profanity',
    'hoooooooly shit': 'Profanity',  # Betulkan
    'fuckin': 'Profanity',
    'shittiest': 'Profanity',
    'fucked': 'Profanity',
    'wtf': 'Profanity',
    'bullshitting': 'Profanity',
    'asshole': 'Profanity',
    'bitches': 'Profanity',
}

# ============================================
# PREPROCESSING
# ============================================

def preprocess_text(text):
    """Clean and preprocess text data"""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ============================================
# LEXICON FEATURE EXTRACTION
# ============================================

def extract_lexicon_features(text):
    """Extract features based on lexicon"""
    words = text.split()
    
    features = {
        'keyword_count': 0,
        'insult_count': 0,
        'threat_count': 0,
        'harassment_count': 0,
        'derogatory_count': 0,
        'exclusion_count': 0,
        'profanity_count': 0,
        'has_cyberbullying': False
    }
    
    for word in words:
        if word in CYBERBULLYING_LEXICON:
            category = CYBERBULLYING_LEXICON[word]
            features['keyword_count'] += 1
            features['has_cyberbullying'] = True
            
            if category == "Insult":
                features['insult_count'] += 1
            elif category == "Threat":
                features['threat_count'] += 1
            elif category == "Harassment":
                features['harassment_count'] += 1
            elif category == "Derogatory":
                features['derogatory_count'] += 1
            elif category == "Exclusion":
                features['exclusion_count'] += 1
            elif category == "Profanity":
                features['profanity_count'] += 1
    
    return features

# ============================================
# HIGHLIGHT KEYWORDS
# ============================================

def highlight_keywords(text, lexicon=CYBERBULLYING_LEXICON):
    """Find and return keywords found in text"""
    words = preprocess_text(text).split()
    found_keywords = []
    
    for word in words:
        if word in lexicon:
            if word not in found_keywords:
                found_keywords.append(word)
    
    return found_keywords

# ============================================
# GET KEYWORD CATEGORIES
# ============================================

def get_keyword_categories(keywords):
    """Return category for every detected keyword"""
    categories = []
    
    for word in keywords:
        if word in CYBERBULLYING_LEXICON:
            categories.append(CYBERBULLYING_LEXICON[word])
    
    return list(dict.fromkeys(categories))