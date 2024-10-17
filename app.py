from flask import Flask,render_template,request
import pickle
import numpy as np
app = Flask(__name__)

popular_df = pickle.load(open('popular.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html', 
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           ratings = list(popular_df['avg_ratings'].values),
                           )
    
@app.route('/recommend')
def recommend_ui():
    return render_template('recos.html',
                           )
   
@app.route('/recommend_books',methods = ['post'])
def recommend():
    user_input = request.form.get('user_input')
    x = np.where(pt.index == user_input)[0][0]
    distances = list(enumerate(similarity_score[x]))
    z = sorted(distances, key = lambda x:x[1])
    z= z[::-1]
    similar_items= z[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
        
    print (data)  
    return render_template("recos.html",data= data)
    
if __name__ == "__main__":
    app.run(debug =True)