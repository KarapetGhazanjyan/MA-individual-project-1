# This class builds train and test models
import os

slash = "/"
if os.name == 'nt':
    slash = "\\"


class Recommending_Movies:

    def __init__(self, data):
        self.fullTrainSet = data.build_full_trainset()

    # Full Train set of model
    def Train_Full(self):
        return self.fullTrainSet

    # Anti test set for the userId you have passed in argument
    # Then this testset is used tofind recommendations
    def Anti_Test(self, user_id):
        train_set = self.fullTrainSet
        fill = train_set.global_mean
        anti_test_set = []
        user_items = set([j for (j, _) in train_set.ur[user_id]])
        anti_test_set += [(str(user_id), str(i), fill) for
                          i in train_set.all_items() if
                          i not in user_items]
        return anti_test_set


from surprise import SVD


class Recom:

    def __init__(self, dataset):
        rd = Recommending_Movies(dataset)
        self.dataset = rd

    # This function calculates Top N recommendations mentioned by the user in the MainScreen
    def Top_N(self, ml, user_id, n):
        # Using recommender SVD
        Top_n = SVD(n_factors=100, random_state=10)

        # Building recommendation model...
        train__set = self.dataset.Train_Full()
        Top_n.fit(train__set)

        # Computing recommendations...
        test__set = self.dataset.Anti_Test(user_id)

        predictions = Top_n.test(test__set)

        recommendations = []

        for userID, movieID, actualRating, estimatedRating, _ in predictions:
            intMovieID = int(movieID)
            recommendations.append((intMovieID, estimatedRating))

        recommendations.sort(key=lambda x: x[1], reverse=True)
        recommendations = recommendations[:n]

        return recommendations


from surprise import Dataset
from surprise import Reader
import pandas as pd


# Class which loads data and pick a movie name
class Movie:
    ID_to_name = {}
    ratings = f"data{slash}ratings.csv"
    movies = f"data{slash}movies.csv"

    # Function loads data and show ratings for each movie
    def Load_Movie_Data(self):

        self.ID_to_name = {}
        self.name_to_movieID = {}

        reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
        # Loading ratings dataset
        ratings_data = Dataset.load_from_file(self.ratings, reader=reader)

        ds = pd.read_csv(self.movies)
        ids = list(ds['movieId'])
        mname = list(ds['title'])
        for i in range(len(ids)):
            self.ID_to_name[ids[i]] = mname[i]
            self.name_to_movieID[mname[i]] = ids[i]

        return ratings_data

    def Get_Movie_Name(self, movieID):
        if movieID in self.ID_to_name:
            return self.ID_to_name[movieID]
        else:
            return ""


from tkinter import *
from tkinter import messagebox

# This interface has been downloaded from public to show the results to the users


root = Tk()


# Function loads ratings and returning moviename and rating
def Movie_len_data():
    ml = Movie()
    data = ml.Load_Movie_Data()
    return (ml, data)


(ml, recommendingData) = Movie_len_data()

recommender = Recom(recommendingData)


def button():
    if e3.get() == "" or e4.get() == "":
        listbox.delete(1, END)
        messagebox.showerror("ERROR", 'Please fill UserID and No.of Recommendation first')
    else:
        listbox.delete(1, END)

        recommendations = recommender.Top_N(ml, int(e3.get()), int(e4.get()))

        for i in range(len(recommendations)):
            b = str(ml.Get_Movie_Name(recommendations[i][0])) + "  |  " + str(round(recommendations[i][1], 2))
            listbox.insert((i + 2), str(i + 1) + "  |  " + b)


root.iconbitmap('movie.ico')

root.configure(background='skyblue')

root.minsize(650, 650)

root.title("Movie Recommender System")

T = Text(root, height=1, width=30, font=("bold", 24), bg="skyblue", bd=0, fg="black")
T.pack()
T.insert(END, 'Welcome to Recommendation System')

# this is the first label
l = Label(root, text='Ratings and Movies dataset are here', font=('bold', 16), fg="green", bg="skyblue")
l.place(x=80, y=50, width=450, height=25)

# this is the label for entry1
l1 = Label(root, text='ratings.csv', font=16, fg="black", bg="skyblue")
l1.place(x=80, y=80, width=95, height=25)

# Entry field for ratings.csv label
e1 = Entry(root)
e1.place(x=80, y=105, width=500, height=25)
# inserted default value in this entry field
e1.insert(0, Movie.ratings)

l2 = Label(root, text='movies.csv', font=16, fg="black", bg="skyblue")
l2.place(x=80, y=140, width=95, height=25)

e2 = Entry(root)
e2.place(x=80, y=165, width=500, height=25)
e2.insert(0, Movie.movies)

l3 = Label(root, text='User Id:-', font=16, fg="black", bg="skyblue")
l3.place(x=80, y=210, width=80, height=25)

e3 = Entry(root)
e3.place(x=170, y=210, width=30, height=25)

l4 = Label(root, text='No. of recommendations:-', font=16, fg="black", bg="skyblue")
l4.place(x=80, y=245, width=230, height=25)

e4 = Entry(root)
e4.place(x=320, y=245, width=30, height=25)

# this is creating a button Recommend on clicking that button() runs
b = Button(root, text="Recommend", fg="white", bg="blue", padx=2, pady=4, command=button)
b.place(x=250, y=285, width=80, height=25)

lb = Label(root, text="We Recommend:-", font=("bold", 16), fg="gray40", bg="skyblue")
lb.place(x=80, y=335, width=180, height=25)

# This is the List Box for displaying recommendations
listbox = Listbox(root, borderwidth=0, highlightthickness=0)
listbox.insert(1, "Sno.  |  Movie Name               |                  Ratings")
listbox.place(x=80, y=385, width=500, height=200)

# This function is responsible for window that comes
# If this is not written then there is no window
root.mainloop()
