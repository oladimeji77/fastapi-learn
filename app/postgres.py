from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional

app = FastAPI()

class Blog(BaseModel):
    id: int
    name: str
    price: int
    is_sale: bool = False
    inventory: int
    created_at: Optional[str]
    
while True:     #while is used so that it can continue to attempt to connect to the db when the db is up
    try:        #try and except are used when there are chances that a code might fail
        conn = psycopg2.connect(host='localhost', database='Zendb', 
                                user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Conecting to database Failed")
        print("Error: ", error)
        time.sleep(2)   #wait 2 secs before attempting to connect again



@app.get("/posts")
def get_all():
    cursor.execute(""" SELECT * FROM products """)
    getPost = cursor.fetchall()
    return getPost


@app.post("/posts")
def push_post(post: Blog):
    cursor.execute(""" INSERT INTO products (id, name, price, is_sale, inventory, created_at) VALUES 
                   (%s,%s,%s,%s,%s,%s) RETURNING * """,
                  (post.id, post.name, post.price, post.is_sale, post.inventory, post.created_at))
    newPost = cursor.fetchone()
    conn.commit()
    return {"DATA": newPost }



@app.get("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def get_one(id: int):
    cursor.execute(""" SELECT * FROM products WHERE id=%s """, (str(id),)) #Note that this comma is important
    getOnePost = cursor.fetchone()
    if not getOnePost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return {"data":getOnePost}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    cursor.execute(""" DELETE FROM products WHERE id=%s returning * """, (str(id),)) #Note that this comma is important
    deletedPost = cursor.fetchone()
    if not deletedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    conn.commit()
    return {"data":deletedPost}

        
@app.put("/posts/{id}")
def update_post(id: int, post: Blog):
    cursor.execute(""" UPDATE products SET id=%s, name=%s, price=%s, is_sale=%s, inventory=%s, created_at=%s WHERE id=%s returning * """,
                   (post.id, post.name, post.price, post.is_sale, post.inventory, post.created_at, str(id))) 
    updatedPost = cursor.fetchone()
    if not updatedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    conn.commit()
    return {"data":updatedPost}



    
        
        
