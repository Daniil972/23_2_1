from bs4 import BeautifulSoup
import requests
import openpyxl


class Rating:
    def __init__(self, movie_title, rating, user_rating, date):
        self.movie_title = movie_title
        self.rating = rating
        self.user_rating = user_rating
        self.date = date


def get_user_ratings(user_id):
    ratings = []
    page = 1

    while True:
        user_url = f'https://www.kinopoisk.ru/user/{user_id}/votes/page/{page}/'
        response = requests.get(user_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('div', class_='profileFilmsList')

        if not table:
            break

        entries = table.find_all('div', class_='item')

        if not entries:
            break

        for entry in entries:
            movie_title = entry.find('div', class_='nameRus').text.strip() if entry.find('div',
                                                                                         class_='nameRus') else 'Нет названия'
            rating_elements = entry.find('div', class_='rating').find_all()
            rating = rating_elements[0].text.strip() if rating_elements else 'Нет оценки'
            user_rating = entry.find('div', class_='vote').text.strip() if entry.find('div', 'vote') else 'Нет оценки'
            date = entry.find('div', class_='date').text.strip() if entry.find('div', class_='date') else 'Нет даты'

            ratings.append(Rating(movie_title, rating, user_rating, date))

        page += 1

    return ratings

def save_data_to_excel(data, filename):
    """Сохраняет данные в Excel-формат."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Название фильма', 'Рейтинг', 'Оценка', 'Дата оценки'])
    for rating in data:
        ws.append([rating.movie_title, rating.rating, rating.user_rating, rating.date])
    wb.save(filename)

def main():
    """Основная функция для запуска парсера."""
    user_id = input("Введите ID пользователя Кинопоиска: ")
    user_ratings = get_user_ratings(user_id)

    if user_ratings:
        save_data_to_excel(user_ratings, f'user_ratings_{user_id}.xlsx')
        print("Данные сохранены в файл Excel.")
    else:
        print("Не удалось получить данные.")

if __name__ == "__main__":
    main()