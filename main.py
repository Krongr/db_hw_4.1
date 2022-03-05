import sqlalchemy
import json


def get_password_from_file(file_name: str) -> str:
    """Возвращает пароль,
    сохраненный в отдельном файле 'file_name'.
    """
    with open(file_name, 'rt', encoding='utf-8') as file:
        return file.read().strip()


if __name__ == "__main__":
    password = get_password_from_file('db_user.txt')
    db = f'postgresql://user:{password}@localhost:5432/netology_hw_3.1'
    engine = sqlalchemy.create_engine(db)
    link = engine.connect()

    list_of_genres = [
        'pop', 'rock', 'folk', 
        'fusion', 'instrumental', 'metal'
    ]      
    for genre in list_of_genres:
        link.execute(f"""
            INSERT INTO genre_list(genre_name)
            VALUES('{genre}');
        """)

    with open('list_of_artists.json', 'r', encoding='utf-8') as file:
        list_of_artists = json.load(file)
            
    for artist in list_of_artists:
        artist_id = link.execute(f"""
            INSERT INTO singer_list(singer_name, singer_aliase)
            VALUES('{artist['name']}', ' - ');
            SELECT id FROM singer_list
                WHERE singer_name = '{artist['name']}';
        """).fetchall()
        for genre_name in artist['genre']:
            genre_id = link.execute(f"""
                SELECT id FROM genre_list
                    WHERE genre_name = '{genre_name}';
            """).fetchall()
            link.execute(f"""
                INSERT INTO singer_genre_pair(singer_id, genre_id)
                VALUES({artist_id[0][0]}, {genre_id[0][0]});
            """)
        for album in artist['albums']:
            album_id = link.execute(f"""
                INSERT INTO record_album_list(album_name, release_year)
                VALUES('{album['album_name']}', {album['year']});
                SELECT id FROM record_album_list
                    WHERE album_name = '{album['album_name']}';
            """).fetchall()
            link.execute(f"""
                INSERT INTO singer_album_pair(singer_id, album_id)
                VALUES('{artist_id[0][0]}', {album_id[0][0]});
            """)
            for song in album['songs']:
                link.execute(f"""
                    INSERT INTO track_list(
                        track_name,
                        track_length,
                        album_id
                    )
                    VALUES(
                        '{song['song_name']}',
                        {song['length']},
                        {album_id[0][0]}
                    );
                """)

    with open('list_of_collections.json', 'r', encoding='utf-8') as file:
        list_of_collections = json.load(file)

    for collection in list_of_collections:
        collection_id = link.execute(f"""
            INSERT INTO music_collection_list(collection_name, release_year)
            VALUES('{collection['name']}', {collection['year']});
            SELECT id FROM music_collection_list
                WHERE collection_name = '{collection['name']}';
        """).fetchall()
        for song in collection['songs']:
            song_id = link.execute(f"""
                SELECT id FROM track_list
                    WHERE track_name = '{song}';
            """).fetchall()
            link.execute(f"""
                INSERT INTO track_collection_pair(track_id, collection_id)
                VALUES({song_id[0][0]}, {collection_id[0][0]});
            """)