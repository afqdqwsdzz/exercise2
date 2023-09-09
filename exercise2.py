import sqlite3

# Copies all the content from the file to a list called stephen_king_adaptations_list
stephen_king_adaptations_list = []
with open('stephen_king_adaptations.txt', 'r') as file:
    for line in file:
        movie = line.strip().split(',')
        stephen_king_adaptations_list.append(movie)

# Establishes a connection with a new SQLite database called stephen_king_adaptations.db
conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

# Creates a table called stephen_king_adaptations_table with the column names movieID, movieName, movieYear, imdbRating
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table 
                  (movieID TEXT, movieName TEXT, movieYear INTEGER, imdbRating REAL)''')

# Takes the content from stephen_king_adaptations_list and inserts it into the table stephen_king_adaptations_table
for movie in stephen_king_adaptations_list:
    cursor.execute("INSERT INTO stephen_king_adaptations_table VALUES (?, ?, ?, ?)", movie)

# Gives the user the option to search for movies in the database
while True:
    print("Please select an option:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. STOP")

    option = input("Enter your choice: ")

    if option == '1':
        # If the user selects Option 1, ask for the name of the movie to be searched in the database
        movie_name = input("Enter the name of the movie: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
        result = cursor.fetchone()

        if result:
            # If the movie is found, display all the details of that movie
            print("Movie found:")
            print("Movie Name:", result[1])
            print("Movie Year:", result[2])
            print("IMDB Rating:", result[3])
        else:
            # If the movie is not found, display an error message
            print("No such movie exists in our database")

    elif option == '2':
        # If the user selects Option 2, ask for a year and return all the movie details from the database released in that year
        movie_year = input("Enter the year: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (movie_year,))
        results = cursor.fetchall()

        if results:
            # If movies are found for that year, display the details of those movies
            print("Movies found for the year", movie_year)
            for row in results:
                print("Movie Name:", row[1])
                print("Movie Year:", row[2])
                print("IMDB Rating:", row[3])
        else:
            # If no movie is found for that year, display an error message
            print("No movies were found for that year in our database.")

    elif option == '3':
        # If the user selects Option 3, ask for the minimum rating and return movies with rating equal to or above that
        min_rating = float(input("Enter the minimum rating: "))
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (min_rating,))
        results = cursor.fetchall()

        if results:
            # If movies fall within the rating limit, display the details of those movies
            print("Movies with rating equal to or above", min_rating)
            for row in results:
                print("Movie Name:", row[1])
                print("Movie Year:", row[2])
                print("IMDB Rating:", row[3])
        else:
            # If no movie falls within the rating limit, display an error message
            print("No movies at or above that rating were found in the database.")

    elif option == '4':
        # If the user selects Option 4, terminate the program
        break

    print()  # Add a blank line for readability

# Close the database connection
conn.close()