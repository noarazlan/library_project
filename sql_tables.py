import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

print("Creating tables...")


cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id_user INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, 
    full_name TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    summary TEXT,
    category TEXT,
    price REAL,
    rating REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Loans (
    id INTEGER PRIMARY KEY,
    id_user INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date TEXT NOT NULL,       
    return_due_date TEXT NOT NULL,   
    actual_return_date TEXT,         
    FOREIGN KEY (id_user) REFERENCES Users(id_user),
    FOREIGN KEY (book_id) REFERENCES Books(id)
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS Waitlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    joined_date TEXT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES Books(id),
    FOREIGN KEY (id_user) REFERENCES Users(id_user)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    rating_value INTEGER NOT NULL,
    review_text TEXT,
    FOREIGN KEY (id_user) REFERENCES Users(id_user),
    FOREIGN KEY (book_id) REFERENCES Books(id)
);
""")

users_data = [
    (1, 'john_doe', 'john.doe@example.com', 'JohnD123', 'John Doe'),
    (2, 'jane_smith', 'jane.smith@example.com', 'JaneS99', 'Jane Smith'),
    (3, 'michael_b', 'michael.brown@example.com', 'BrownM44', 'Michael Brown'),
    (4, 'emily_d', 'emily.davis@example.com', 'EmDavis7', 'Emily Davis'),
    (5, 'david_w', 'david.wilson@example.com', 'WilsonD5', 'David Wilson'),
    (6, 'olivia_m', 'olivia.martin@example.com', 'OliviaM1', 'Olivia Martin'),
    (7, 'james_t', 'james.taylor@example.com', 'JamesT22', 'James Taylor'),
    (8, 'sophia_a', 'sophia.anderson@example.com', 'SophA88', 'Sophia Anderson'),
    (9, 'robert_t', 'robert.thomas@example.com', 'RobT999', 'Robert Thomas'),
    (10, 'isabella_j', 'isabella.jackson@example.com', 'IsaJack10', 'Isabella Jackson'),
    (11, 'william_w', 'william.white@example.com', 'WillW111', 'William White'),
    (12, 'mia_h', 'mia.harris@example.com', 'MiaH222', 'Mia Harris'),
    (13, 'lucas_m', 'lucas.martin@example.com', 'LucasM33', 'Lucas Martin'),
    (14, 'charlotte_g', 'charlotte.garcia@example.com', 'CharG44', 'Charlotte Garcia'),
    (15, 'henry_m', 'henry.martinez@example.com', 'HenryM55', 'Henry Martinez'),
    (16, 'amelia_r', 'amelia.robinson@example.com', 'AmeliaR6', 'Amelia Robinson'),
    (17, 'alex_clark', 'alex.clark@example.com', 'AlexC777', 'Alex Clark'),
    (18, 'harper_r', 'harper.rodriguez@example.com', 'HarperR8', 'Harper Rodriguez'),
    (19, 'daniel_l', 'daniel.lewis@example.com', 'DanL999', 'Daniel Lewis'),
    (20, 'evelyn_l', 'evelyn.lee@example.com', 'EvelynL2', 'Evelyn Lee'),
    (21, 'matthew_w', 'matthew.walker@example.com', 'MattW21', 'Matthew Walker'),
    (22, 'abigail_h', 'abigail.hall@example.com', 'AbbyH22', 'Abigail Hall'),
    (23, 'joseph_a', 'joseph.allen@example.com', 'JoeAllen3', 'Joseph Allen'),
    (24, 'elizabeth_y', 'elizabeth.young@example.com', 'LizY242', 'Elizabeth Young'),
    (25, 'david_k', 'david.king@example.com', 'DavidK25', 'David King'),
    (26, 'sofia_w', 'sofia.wright@example.com', 'SofiaW26', 'Sofia Wright'),
    (27, 'jackson_s', 'jackson.scott@example.com', 'JackS27', 'Jackson Scott'),
    (28, 'avery_g', 'avery.green@example.com', 'AveryG28', 'Avery Green'),
    (29, 'sebastian_b', 'sebastian.baker@example.com', 'BastianB', 'Sebastian Baker'),
    (30, 'chloe_a', 'chloe.adams@example.com', 'ChloeA30', 'Chloe Adams'),
    (31, 'jack_hill', 'jack.hill@example.com', 'JackH31', 'Jack Hill'),
    (32, 'eleanor_n', 'eleanor.nelson@example.com', 'EleanorN', 'Eleanor Nelson'),
    (33, 'owen_c', 'owen.carter@example.com', 'OwenC33', 'Owen Carter'),
    (34, 'hazel_m', 'hazel.mitchell@example.com', 'HazelM34', 'Hazel Mitchell'),
    (35, 'alexander_p', 'alexander.perez@example.com', 'AlexP35', 'Alexander Perez'),
    (36, 'lily_r', 'lily.roberts@example.com', 'LilyR36', 'Lily Roberts'),
    (37, 'luke_t', 'luke.turner@example.com', 'LukeT37', 'Luke Turner'),
    (38, 'zoey_p', 'zoey.phillips@example.com', 'ZoeyP38', 'Zoey Phillips'),
    (39, 'gabriel_c', 'gabriel.campbell@example.com', 'GabeC39', 'Gabriel Campbell'),
    (40, 'stella_p', 'stella.parker@example.com', 'StellaP4', 'Stella Parker'),
    (41, 'anthony_e', 'anthony.evans@example.com', 'TonyE41', 'Anthony Evans'),
    (42, 'natalie_e', 'natalie.edwards@example.com', 'NatE42', 'Natalie Edwards'),
    (43, 'isaac_c', 'isaac.collins@example.com', 'IsaacC43', 'Isaac Collins'),
    (44, 'victoria_s', 'victoria.stewart@example.com', 'VicS44', 'Victoria Stewart'),
    (45, 'samuel_m', 'samuel.morris@example.com', 'SamM45', 'Samuel Morris'),
    (46, 'madison_r', 'madison.rogers@example.com', 'MadiR46', 'Madison Rogers'),
    (47, 'christopher_m', 'christopher.morgan@example.com', 'ChrisM47', 'Christopher Morgan'),
    (48, 'emma_cook', 'emma.cook@example.com', 'EmmaC48', 'Emma Cook'),
    (49, 'joshua_r', 'joshua.rogers@example.com', 'JoshR49', 'Joshua Rogers'),
    (50, 'salome_s', 'salome.shalom@example.com', 'Salome50', 'Salome Shalom')
]

books_data = [
    (1, 'The Hobbit', 'J.R.R. Tolkien', 'The adventure of Bilbo Baggins in Middle-earth.', 'Fantasy', 45.0, 0),
    (2, 'The Fellowship of the Ring', 'J.R.R. Tolkien', 'The epic journey to destroy the One Ring begins.', 'Fantasy', 60.0, 0),
    (3, 'Harry Potter and the Sorcerers Stone', 'J.K. Rowling', 'A young boy discovers he is a wizard and attends Hogwarts.', 'Fantasy', 50.0, 0),
    (4, '1984', 'George Orwell', 'A dystopian novel about totalitarianism and Big Brother.', 'Science Fiction', 40.0, 0),
    (5, 'Animal Farm', 'George Orwell', 'A satirical allegory about the Russian Revolution using farm animals.', 'Classics', 35.0, 0),
    (6, 'The Little Prince', 'Antoine de Saint-Exupery', 'A philosophical story about a young prince visiting planets.', 'Children', 30.0, 0),
    (7, 'Crime and Punishment', 'Fyodor Dostoevsky', 'The mental anguish and moral dilemmas of Rodion Raskolnikov.', 'Classics', 55.0, 0),
    (8, 'The Catcher in the Rye', 'J.D. Salinger', 'The experiences of teenager Holden Caulfield in New York City.', 'Fiction', 42.0, 0),
    (9, 'The Alchemist', 'Paulo Coelho', 'An Andalusian shepherd boy travels to Egypt in search of a treasure.', 'Philosophy', 38.0, 0),
    (10, 'Sapiens', 'Yuval Noah Harari', 'A brief history of humankind from the Stone Age to the modern era.', 'History', 65.0, 0),
    (11, 'Dune', 'Frank Herbert', 'A complex sci-fi story about politics and survival on a desert planet.', 'Science Fiction', 48.0, 0),
    (12, 'The Hitchhikers Guide to the Galaxy', 'Douglas Adams', 'A comedy sci-fi adventure following the last surviving human.', 'Comedy Sci-Fi', 39.0, 0),
    (13, 'The Kite Runner', 'Khaled Hosseini', 'A story of friendship, betrayal, and redemption in Afghanistan.', 'Drama', 45.0, 0),
    (14, 'Wuthering Heights', 'Emily Bronte', 'A classic tale of love, passion, and revenge on the Yorkshire moors.', 'Classics', 42.0, 0),
    (15, 'Pride and Prejudice', 'Jane Austen', 'The romantic clash between Elizabeth Bennet and Mr. Darcy.', 'Romance', 40.0, 0),
    (16, 'Frankenstein', 'Mary Shelley', 'A scientist creates a creature and must face the consequences.', 'Horror', 35.0, 0),
    (17, 'Dracula', 'Bram Stoker', 'The legendary vampire attempts to move from Transylvania to England.', 'Horror', 38.0, 0),
    (18, 'The Trial', 'Franz Kafka', 'A man is arrested and prosecuted by a remote, inaccessible authority.', 'Philosophy', 44.0, 0),
    (19, 'Moby-Dick', 'Herman Melville', 'Captain Ahab obsession with revenge on the white whale.', 'Adventure', 52.0, 0),
    (20, 'Alices Adventures in Wonderland', 'Lewis Carroll', 'A girl named Alice falls through a rabbit hole into a fantasy world.', 'Children', 32.0, 0),
    (21, 'Watership Down', 'Richard Adams', 'A survival story about a small group of wild rabbits.', 'Adventure', 46.0, 0),
    (22, 'The Adventures of Sherlock Holmes', 'Arthur Conan Doyle', 'A collection of detective stories featuring Sherlock Holmes.', 'Mystery', 58.0, 0),
    (23, 'The Old Man and the Sea', 'Ernest Hemingway', 'An aging Cuban fisherman struggles with a giant marlin.', 'Classics', 34.0, 0),
    (24, 'I, Robot', 'Isaac Asimov', 'A collection of sci-fi stories that explore the Three Laws of Robotics.', 'Science Fiction', 42.0, 0),
    (25, 'The Island of Doctor Moreau', 'H.G. Wells', 'A shipwrecked man discovers an island populated by beast-people.', 'Science Fiction', 36.0, 0),
    (26, 'Cell', 'Stephen King', 'A mysterious cell phone signal turns humans into zombies.', 'Horror', 45.0, 0),
    (27, 'The Stand', 'Stephen King', 'An apocalyptic vision of a world decimated by a plague.', 'Thriller', 65.0, 0),
    (28, 'The Da Vinci Code', 'Dan Brown', 'A murder mystery involving symbols, history, and secret societies.', 'Thriller', 48.0,0),
    (29, 'Angels & Demons', 'Dan Brown', 'Robert Langdon tries to stop a secret society from destroying the Vatican.', 'Thriller', 48.0, 0),
    (30, 'Gone Girl', 'Gillian Flynn', 'A suspenseful thriller about a woman who suddenly disappears.', 'Thriller', 44.0, 0),
    (31, 'The Girl with the Dragon Tattoo', 'Stieg Larsson', 'A mystery involving a financial journalist and a tattooed hacker.', 'Mystery', 50.0,0),
    (32, 'The Secret History', 'Donna Tartt', 'A group of clever misfits discover a completely new way of thinking.', 'Drama', 52.0, 0),
    (33, 'The Slave', 'Isaac Bashevis Singer', 'A historical novel about a Jewish man enslaved in Poland.', 'Historical Fiction', 40.0, 0),
    (34, 'Black Box', 'Amos Oz', 'An epistolary novel exploring family relations in Israel.', 'Fiction', 42.0, 0),
    (35, 'Someone to Run With', 'David Grossman', 'A gripping tale of teenagers and a dog on the streets of Jerusalem.', 'Fiction', 46.0, 0),
    (36, 'A Trumpet in the Wadi', 'Sami Michael', 'A love story between a Jewish man and an Arab woman in Haifa.', 'Fiction', 38.0, 0),
    (37, 'Gai Oni', 'Shulamit Lapid', 'A historical novel about early Zionist settlement in Rosh Pinna.', 'Historical Fiction', 44.0, 0),
    (38, 'Catching Fire', 'Suzanne Collins', 'The second installment in the dystopian Hunger Games trilogy.', 'YA Dystopian', 45.0, 0),
    (39, 'The Hunger Games', 'Suzanne Collins', 'Katniss Everdeen must fight for survival in a televised game.', 'YA Dystopian', 45.0, 0),
    (40, 'City of Bones', 'Cassandra Clare', 'A girl discovers she belongs to a secret race of shadowhunters.', 'YA Fantasy', 43.0, 0),
    (41, 'The Fault in Our Stars', 'John Green', 'Two teenage cancer patients embark on a life-changing journey.', 'YA Romance', 39.0, 0),
    (42, 'The Book Thief', 'Markus Zusak', 'A young girl in Nazi Germany finds comfort in stealing books.', 'Historical Fiction', 48.0, 0),
    (43, 'The Lightning Thief', 'Rick Riordan', 'A boy discovers he is a demigod and son of Poseidon.', 'YA Fantasy', 42.0, 0),
    (44, 'Foundation', 'Isaac Asimov', 'A mathematician predicts the fall of a galactic empire.', 'Science Fiction', 46.0, 0),
    (45, 'Fifty Shades of Grey', 'E.L. James', 'A romantic relationship between a college graduate and a businessman.', 'Romance', 40.0, 0),
    (46, 'Nemesis', 'Agatha Christie', 'Miss Marple is hired to investigate a crime from the past.', 'Mystery', 35.0, 0),
    (47, 'Murder on the Orient Express', 'Agatha Christie', 'Hercule Poirot investigates a murder on a snowbound train.', 'Mystery', 38.0, 0),
    (48, 'Influence', 'Robert Cialdini', 'The classic book on the psychology of persuasion.', 'Psychology', 55.0, 0),
    (49, 'Thinking, Fast and Slow', 'Daniel Kahneman', 'An analysis of the two systems that drive the way we think.', 'Psychology', 60.0, 0),
    (50, 'Atomic Habits', 'James Clear', 'An easy and proven way to build good habits and break bad ones.', 'Self-Help', 50.0, 0)
]

loans_data = [
    (1, 1, 1, '2026-06-01', '2026-06-15', None),
    (2, 2, 2, '2026-06-02', '2026-06-16', None),
    (3, 3, 3, '2026-06-03', '2026-06-17', None),
    (4, 4, 4, '2026-06-04', '2026-06-18', None),
    (5, 5, 5, '2026-06-05', '2026-06-19', None),
    (6, 6, 6, '2026-06-05', '2026-06-19', None),
    (7, 7, 7, '2026-06-06', '2026-06-20', None),
    (8, 8, 8, '2026-06-06', '2026-06-20', None),
    (9, 9, 9, '2026-06-07', '2026-06-21', None),
    (10, 10, 10, '2026-06-07', '2026-06-21', None),
    (11, 11, 11, '2026-06-08', '2026-06-22', None),
    (12, 12, 12, '2026-06-08', '2026-06-22', None),
    (13, 13, 13, '2026-06-08', '2026-06-22', None),
    (14, 14, 14, '2026-06-08', '2026-06-22', None),
    (15, 15, 15, '2026-06-08', '2026-06-22', None),
    (16, 16, 16, '2026-06-08', '2026-06-22', None),
    (17, 17, 17, '2026-06-08', '2026-06-22', None),
    (18, 18, 18, '2026-06-08', '2026-06-22', None),
    (19, 19, 19, '2026-06-08', '2026-06-22', None),
    (20, 20, 20, '2026-05-01', '2026-05-15', '2026-05-12'),
    (21, 21, 21, '2026-05-01', '2026-05-15', '2026-05-14'),
    (22, 22, 22, '2026-05-02', '2026-05-16', '2026-05-10'),
    (23, 23, 23, '2026-05-02', '2026-05-16', '2026-05-15'),
    (24, 24, 24, '2026-05-03', '2026-05-17', '2026-05-12'),
    (25, 25, 25, '2026-05-04', '2026-05-18', '2026-05-16'),
    (26, 26, 26, '2026-05-05', '2026-05-19', '2026-05-18'),
    (27, 27, 27, '2026-05-05', '2026-05-19', '2026-05-19'),
    (28, 28, 28, '2026-05-06', '2026-05-20', '2026-05-15'),
    (29, 29, 29, '2026-05-07', '2026-05-21', '2026-05-20'),
    (30, 30, 30, '2026-05-08', '2026-05-22', '2026-05-21'),
    (31, 31, 31, '2026-05-10', '2026-05-24', '2026-05-22'),
    (32, 32, 32, '2026-05-11', '2026-05-25', '2026-05-24'),
    (33, 33, 33, '2026-05-12', '2026-05-26', '2026-05-25'),
    (34, 34, 34, '2026-05-12', '2026-05-26', '2026-05-26'),
    (35, 35, 35, '2026-05-13', '2026-05-27', '2026-05-27'),
    (36, 36, 36, '2026-05-14', '2026-05-28', '2026-05-25'),
    (37, 37, 37, '2026-05-15', '2026-05-29', '2026-05-28'),
    (38, 38, 38, '2026-05-15', '2026-05-29', '2026-05-29'),
    (39, 39, 39, '2026-05-16', '2026-05-30', '2026-05-28'),
    (40, 40, 40, '2026-05-17', '2026-05-31', '2026-05-30'),
    (41, 41, 41, '2026-05-18', '2026-06-01', '2026-06-01'),
    (42, 42, 42, '2026-05-19', '2026-06-02', '2026-06-01'),
    (43, 43, 43, '2026-05-20', '2026-06-03', '2026-06-03'),
    (44, 44, 44, '2026-05-21', '2026-06-04', '2026-06-02'),
    (45, 45, 45, '2026-05-22', '2026-06-05', '2026-06-05'),
    (46, 46, 46, '2026-05-22', '2026-06-05', '2026-06-04'),
    (47, 47, 47, '2026-05-23', '2026-06-06', '2026-06-06'),
    (48, 48, 48, '2026-05-24', '2026-06-07', '2026-06-06'),
    (49, 49, 49, '2026-05-25', '2026-06-08', '2026-06-07'),
    (50, 50, 50, '2026-05-26', '2026-06-09', '2026-06-08')
]

waitlist_data = [
    # (book_id, id_user, joined_date)
    (1, 5, '2026-06-02'),
    (1, 6, '2026-06-03')
]


print("Inserting Users...")
cursor.executemany("INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?, ?)", users_data)

print("Inserting Books...")
cursor.executemany("INSERT OR IGNORE INTO Books VALUES (?, ?, ?, ?, ?, ?, ?)", books_data)

print("Inserting Loans...")
cursor.executemany("INSERT OR IGNORE INTO Loans VALUES (?, ?, ?, ?, ?, ?)", loans_data)


print("Inserting Waitlist...")
cursor.executemany("INSERT INTO Waitlist (book_id, id_user, joined_date) VALUES (?, ?, ?)", waitlist_data)

conn.commit()
conn.close()

print("\nSuccess! 'library.db' has been created and populated with 50 rows each.")