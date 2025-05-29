import mysql.connector
from Demos.EvtSubscribe_pull import query_text
from prettytable import PrettyTable

# Настройки подключения к базе данных
dbconfig = {
    'host': 'localhost',
    'user': 'root',
    'password': 'aliik0555@#$',
    'database': 'sakila'
}


# Функция для подключения к базе данных
def connect_to_db():
    return mysql.connector.connect(**dbconfig)


# Функция для поиска фильмов по ключевому слову
def search_movies_by_keyword(keyword):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT title FROM film WHERE title LIKE %s LIMIT 10"
    cursor.execute(query, (f"%{keyword}%",))
    results = cursor.fetchall()
    db.close()
    return results


# Функция для поиска фильмов по жанру и году
def search_movies_by_genre_and_year(genre, year):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT title
    FROM film
    JOIN film_category fc ON film.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = %s AND film.release_year = %s
    LIMIT 10
    """
    cursor.execute(query, (genre, year))
    results = cursor.fetchall()
    db.close()
    return results


# Функция для записи запросов в базу данных
def log_search_query(query):
    db = connect_to_db()
    cursor = db.cursor()
    check_query = "SELECT id FROM search_queries WHERE query = %s"
    cursor.execute(check_query, (query,))
    result = cursor.fetchone()
    if result:
        update_query = "UPDATE search_queries SET search_count = search_count + 1 WHERE id = %s"
        cursor.execute(update_query, (result['id'],))
    else:
        insert_query = "INSERT INTO search_queries (query) VALUES (%s)"
        cursor.execute(insert_query, (query,))
    db.commit()
    db.close()


# Функция для получения популярных запросов
def get_popular_searches():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """ 
    SELECT query_text, COUNT(*) AS count
    FROM search_query WHERE query_text != ''
    GROUP BY query_text ORDER BY
    count DESC LIMIT 10 
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


# Функция для поиска фильмов по актерам
def search_movies_by_actor(actor_name):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT f.title
    FROM film f
    JOIN film_actor fa ON f.film_id = fa.film_id
    JOIN actor a ON fa.actor_id = a.actor_id
    WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
    LIMIT 10
    """
    cursor.execute(query, (f"%{actor_name}%",))
    results = cursor.fetchall()
    db.close()
    return results


# Функция для поиска фильмов по рейтингу
def search_top_rated_movies():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT title, rating
    FROM film
    ORDER BY rating DESC
    LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


# Функция для поиска самых длинных фильмов
def search_longest_movies():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT title, length
    FROM film
    ORDER BY length DESC
    LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def search_comedy_movies():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT f.title, f.description, f.release_year
    FROM film f
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE c.name = 'Comedy'
    LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


# Функция для поиска фильма по id
def search_movie_by_id(movie_id):
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT title FROM film WHERE film_id = %s"
    cursor.execute(query, (movie_id,))
    result = cursor.fetchone()
    db.close()
    return result


# Функция для отображения меню
def display_menu():
    print("""
    1: Поиск фильма по ключевому слову
    2: Поиск фильмов по жанру и году
    3: Посмотреть популярные 10 запросов
    4: Поиск фильмов по актёрам
    5: Поиск фильма по id
    6: Поиск фильмов по рейтингу (топ 10)
    7: Поиск фильмов жанра Comedy
    8: Поиск самых длинных 10 фильмов
    9: Выход
    """)


# Основная функция для работы с пользователем
def main():
    while True:
        display_menu()
        choice = input("Введите номер действия: ")

        if choice == '1':
            keyword = input("Введите ключевое слово для поиска: ")
            results = search_movies_by_keyword(keyword)
            if results:
                table = PrettyTable(['Title'])
                for row in results:
                    table.add_row([row['title']])
                print(table)
            else:
                print("Фильмы не найдены.")

        elif choice == '2':
            genre = input("Введите жанр: ")
            year = input("Введите год: ")
            results = search_movies_by_genre_and_year(genre, year)
            if results:
                table = PrettyTable(['Title'])
                for row in results:
                    table.add_row([row['title']])
                print(table)
            else:
                print("Фильмы не найдены.")

        elif choice == '3':
            results = get_popular_searches()
            if results:
                table = PrettyTable(['Запрос', 'Количество запросов'])
                for row in results:
                    table.add_row([row['query'], row['search_count']])
                print(table)
            else:
                print("Популярных запросов пока нет.")

        elif choice == '4':
            actor_name = input("Введите имя актёра: ")
            results = search_movies_by_actor(actor_name)
            if results:
                table = PrettyTable(['Title'])
                for row in results:
                    table.add_row([row['title']])
                print(table)
            else:
                print("Фильмы с указанным актёром не найдены.")

        elif choice == '5':
            movie_id = input("Введите ID фильма: ")
            result = search_movie_by_id(movie_id)
            if result:
                print(f"Название фильма: {result['title']}")
            else:
                print("Фильм не найден.")

        elif choice == '6':
            results = search_top_rated_movies()
            if results:
                table = PrettyTable(['Title', 'Rating'])
                for row in results:
                    table.add_row([row['title'], row['rating']])
                print(table)
            else:
                print("Фильмы не найдены.")

        elif choice == '7':
            results = search_comedy_movies()
            if results:
                table = PrettyTable(['Title'])
                for row in results:
                    table.add_row([row['title']])
                print(table)
            else:
                print("Комедийные фильмы не найдены.")

        elif choice == '8':
            results = search_longest_movies()
            if results:
                table = PrettyTable(['Title', 'Length'])
                for row in results:
                    table.add_row([row['title'], row['length']])
                print(table)
            else:
                print("Длинные фильмы не найдены.")

        elif choice == '9':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите действие от 1 до 9.")


if __name__ == '__main__':
    main()
