
import warnings
warnings.filterwarnings('ignore')

import os, json
from IPython.display import JSON
from fastembed import TextEmbedding

import weaviate
from weaviate.classes.data import DataObject

from helper import suppress_output

COLLECTION_NAME = "Movie_rec"
MOVIE_DESCRIPTION_MOT_FOLDER = "include/movie_filesc_rec"
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

with suppress_output():
    client = weaviate.connect_to_embedded(
        persistence_data_path= "tmp/weaviate_rec"
    )

print("Starting new Weaviate instance")
print(f"Client is set: {client.is_ready()}")

import time
existing_collections = client.collections.list_all()
existing_collection_name = existing_collections.keys()

if COLLECTION_NAME not in existing_collection:
    print(f"Collection name: '{COLLECTION_NAME}' not found, creating..")
    collection = client.collections.create(name=COLLECTION_NAME)
    print(f"Collection name '{COLLECTION_NAME}' created successfully✅")

else:
    print("Checking for '{COLLECTION_NAME}'....")
    time.sleep(2)
    print(f"Collection name '{COLLECTION_NAME}' exists")
    collection = client.collections.get(COLLECTION_NAME)

movie_summary = """0 ::: Children of Men ::: Alfonso Cuarón ::: In a dystopian future where humans have become infertile, a disillusioned bureaucrat must escort a miraculously pregnant woman to safety. ::: 2006 ::: Sci-Fi, Thriller
1 ::: Arrival ::: Denis Villeneuve ::: A linguist is recruited to communicate with aliens who have arrived on Earth, revealing a new perception of time and humanity. ::: 2016 ::: Sci-Fi, Drama
2 ::: The Fall ::: Tarsem Singh ::: In a 1920s hospital, a stuntman tells a fantastical story to a little girl, blending fiction and reality in visually stunning ways. ::: 2006 ::: Fantasy, Drama
3 ::: The Handmaiden ::: Park Chan-wook ::: In Japanese-occupied Korea, a conman and a pickpocket plan to defraud a rich heiress, but betrayal and love complicate everything. ::: 2016 ::: Psychological Thriller, Romance
4 ::: Coherence ::: James Ward Byrkit ::: A group of friends experience a reality-bending night when a comet passes overhead, leading to parallel timelines. ::: 2013 ::: Sci-Fi, Mystery
5 ::: The Man from Earth ::: Richard Schenkman ::: A retiring professor reveals to his colleagues that he’s a 14,000-year-old immortal, sparking philosophical debates. ::: 2007 ::: Sci-Fi, Drama
6 ::: Stalker ::: Andrei Tarkovsky ::: A guide leads two men through a forbidden zone that supposedly grants one’s innermost desires. ::: 1979 ::: Sci-Fi, Art House
7 ::: Perfect Blue ::: Satoshi Kon ::: A retired pop singer’s identity unravels when she pursues an acting career, blurring the line between fiction and madness. ::: 1997 ::: Psychological Thriller, Anime
8 ::: A Ghost Story ::: David Lowery ::: A recently deceased ghost silently observes the passage of time and human life from the house he once occupied. ::: 2017 ::: Drama, Fantasy
9 ::: Moon ::: Duncan Jones ::: A man nearing the end of his 3-year lunar mining contract begins to unravel the truth about his mission and identity. ::: 2009 ::: Sci-Fi, Mystery"""

with open(f"{MOVIE_DESCRIPTION_MOT_FOLDER}/recommended_movie.txt", 'w') as f:
    f.write(movie_summary)

movie_summary_2 = """10 ::: Predestination ::: Michael Spierig, Peter Spierig ::: A temporal agent embarks on his final mission to stop a mysterious terrorist, encountering shocking truths about identity and time. ::: 2014 ::: Sci-Fi, Thriller
11 ::: Enemy ::: Denis Villeneuve ::: A man discovers his exact double in a film and becomes obsessed, leading to a psychological unraveling. ::: 2013 ::: Psychological Thriller, Mystery
12 ::: Timecrimes ::: Nacho Vigalondo ::: A man accidentally travels back in time and must deal with the unintended and increasingly complex consequences. ::: 2007 ::: Sci-Fi, Thriller
13 ::: The Man Who Fell to Earth ::: Nicolas Roeg ::: An alien arrives on Earth to find water for his dying planet but is corrupted by human greed and desire. ::: 1976 ::: Sci-Fi, Drama
14 ::: Synecdoche, New York ::: Charlie Kaufman ::: A theater director creates a life-sized replica of New York inside a warehouse, blurring reality and art. ::: 2008 ::: Drama, Experimental
15 ::: Paprika ::: Satoshi Kon ::: A therapist uses a device that allows people to enter dreams, but chaos erupts when the machine is stolen. ::: 2006 ::: Sci-Fi, Anime
16 ::: Burning ::: Lee Chang-dong ::: A young man becomes obsessed with a woman and her mysterious new friend, leading to a slow-burning psychological mystery. ::: 2018 ::: Mystery, Drama
17 ::: Upstream Color ::: Shane Carruth ::: Two people entangled in a life cycle of organisms struggle to rebuild their identities and connection. ::: 2013 ::: Sci-Fi, Experimental
18 ::: Sound of My Voice ::: Zal Batmanglij ::: A couple infiltrates a cult led by a woman who claims to be from the future, testing their beliefs and trust. ::: 2011 ::: Thriller, Drama
19 ::: Solaris ::: Andrei Tarkovsky ::: A psychologist is sent to a space station orbiting a mysterious planet that materializes people from his memories. ::: 1972 ::: Sci-Fi, Philosophical Drama"""

with open(f"{MOVIE_DESCRIPTION_MOT_FOLDER}/second_recommended_movie.txt", 'w') as f:
    f.write(movie_summary_2)

movie_description_files = [
    f for f in os.listdir(MOVIE_DESCRIPTION_MOT_FOLDER)
    if f.endswith('.txt')
]

list_of_movie_data = []

for movie_file in movie_description_files:
    with open(
        os.path.join(MOVIE_DESCRIPTION_MOT_FOLDER, movie_file), 'r') as f:
        movie_lines = f.readlines()

    titles = [line.split(':::')[1].strip() for line in movie_lines]
    directors = [line.split(':::')[2].strip() for line in movie_lines]
    descriptions = [line.split(':::')[3].strip() for line in movie_lines]
    years = [int(line.split(':::')[4].strip()) for line in movie_lines]
    genres = [line.split(':::')[5].strip() for line in movie_lines]

    movie_data = [
        {
            "title": title,
            "director": director,
            "description": description,
            "year": year,
            "genre": genre,
        }
        for title, director, description, year, genre in zip(
           titles, directors, descriptions, years, genres
        )
    ]
    list_of_movie_data.append(movie_data)


embedding_model = TextEmbedding(EMBEDDING_MODEL_NAME)

list_of_embeddings = []

for movie_data in list_of_movie_data:
    descriptions = [movie["description"] for movie in movie_data]
    embeddings = [list(embedding_model.embed([desc]))[0] for desc in descriptions]
    list_of_embeddings.append(embeddings)

for movie_data_list, emb_list in zip(list_of_movie_data, list_of_embeddings):
    items = []
    for movie_data, emb in zip(movie_data_list, emb_list):
        item = DataObject(
            properties={
                "title": movie_data["title"],
                "director": movie_data["director"],
                "description": movie_data["description"],
                "year": movie_data["year"],
                "genre": movie_data["genre"],
            },
            vector=emb,
        )
        items.append(item)
            
    collection.data.insert_many(items)

query_str = "Can you recommend any drama movie to me?"
query_embedding = list(embedding_model.embed([query_str]))[0]

results = collection.query.near_vector(
    near_vector=query_embedding,
    limit=2,
)

for result in results.objects:
    print("="*50)
    print("Recommended movies for you:")
    print(f"🎬 Title: {result.properties['title']}")
    print(f"🎥 Director: {result.properties['director']}")
    print(f"📜 Description: {result.properties['description']}")
    print(f"📅 Year: {result.properties.get('year', 'N/A')}")
    print(f"🎭 Genre: {', '.join(result.properties.get('genre', []))}")
    print("="*50 + "\n")
