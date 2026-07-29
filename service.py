import os
from pathlib import Path
from typing import List

import bentoml
import pandas as pd
import spacy
from dotenv import load_dotenv

my_image = bentoml.images.Image(python_version="3.12") \
    .python_packages("spacy", "pandas")


@bentoml.service(
    image=my_image,
)
class SpacyCSVService:
    def __init__(self):
        load_dotenv() 
        self.nlp = spacy.load("./model-best")
    
    @bentoml.api
    def upload(self, csv_files: List[Path]):
        # Read and concatenate all CSVs
        dfs = [pd.read_csv(f) for f in csv_files]
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df = combined_df.fillna("None")


        brands = [
            "Dove", "Rexona", "LUX", "Axe", "Lifebuoy", "Pepsodent", "Closeup", "Vaseline", "Wild",
            "Pampers", "Luvs", "Charlie Banana", "Ninjamas",
            "Tide", "Ariel", "Gain", "Downy", "Bounce", "Cheer", "Dreft", "Era","L'Oreal",
            "Bounty", "Charmin", "Puffs",
            "Always", "Tampax", "Always Discreet", "Just", "This is L",
            "Head & Shoulders", "Herbal Essences", "Pantene", "Aussie", "Hair Recipe", "WaterLess",
            "Crest", "Oral-B", "Braun",
            "Vicks", "Align", "Clearblue", "Meta", "VÖOST",
            "Olay", "Old Spice", "SK-II", "Native",
            "Gillette", "Venus", "Braun"
        ]

        brands_set = set(brands)
        
        # Run spaCy inference on a specific column, e.g., 'text'
        for i, doc in enumerate(self.nlp.pipe(combined_df["offer"].astype(str))):
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            entity_text = str(entities[0][0] if entities else "None")
            combined_df.loc[i, "normalized_offer"] = combined_df.loc[i, "normalized_offer"] + " [BRAND] " + entity_text
        
        # Alternative approach using to_dict() on the entire DataFrame
        data = []
        records = combined_df.to_dict('records')
        for record in records:
            if record.get("brand", "None") != "None" and record.get("brand", "") in brands_set:
                metadata={
                    'offer': record.get("offer", ""), 
                    'offer_url': record.get("offer_url", ""),
                    'offer_type': record.get("offer_type", ""),
                    'brand': record.get("brand", ""),
                    'category': record.get("category", ""),
                    'expires_date': record.get("expires_date", ""),
                    'source': record.get("source", "")
                }
                data.append(metadata)
        
        return data