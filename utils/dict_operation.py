nautiljon_mapping = {
    "Titre alternatif": "alternative_titles",
    "Titre original": "original_title",
    "Origine": "origin",
    "Année VF": "year_fv",
    "Type": "anime_type",
    "Thèmes": "themes",
    "Auteur": "author",
    "Traducteur": "translator",
    "Éditeur VO": "ov_editor",
    "Éditeur VF": "fv_editor",
    "Prépublié dans": "pre_published_magazine",
    "Nb volumes VO": "nb_of_volumes_ov",
    "Nb volumes VF": "nb_of_volumes_fv",
    "Synopsis": "synopsis",
    "Note moyenne": "average_rating",
    "Nombre de membres": "member_count",
    "Début de diffusion en simulcast/streaming": "streaming_start_date"
}
def dict_map_field_names(dictionary, new_mapping):
    mapped_dict = {}

    for key, value in dictionary.items():
        new_key = new_mapping.get(key) # use new mapping to get the new key
        if new_key: mapped_dict[new_key] = value

    return mapped_dict

genre_translation = {
    "Comédie": "Comedy",
    "Romance": "Romance",
    "School Life": "School Life",
    "Slice of Life": "Slice of Life",
    "Action": "Action",
    "Aventure": "Adventure",
    "Fantastique": "Fantasy",
    "Science-Fiction": "Science Fiction",
    "Horreur": "Horror",
    "Drame": "Drama",
    "Historique": "Historical",
    "Mystère": "Mystery",
}

def translate_genres(genres):
    genre_list = genres.split(' - ')
    translated_genres = [genre_translation.get(genre.strip(), genre.strip()) for genre in genre_list]
    return ' - '.join(translated_genres)