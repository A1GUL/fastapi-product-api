from fastapi import FastAPI
import random
from pydantic import BaseModel
from typing import Union
import sqlite3

class Product(BaseModel):
    name: str
    price: float
    Stock: int
    category: Union[str, None] = None

app = FastAPI()
@app.get("/")
def read_root():
    return {"output":"Bazı insanlar, bazen insanlar.."}

@app.get("/soz/{kisi}")
def soz(kisi: str):
    sozler = {
        "Mevlana": "Ne olursan ol, yine gel.",
        "Hz. Ali": "İlim, maldan hayırlıdır.",
        "Atatürk": "Hayatta en hakiki mürşit ilimdir.",
        "Özdemir Asaf": "Aşk, bir kadının gözlerinde başlar.",
        "Cemal Süreya": "Sevda bir çiçekse, aşk onun kokusudur.",
        "Nazım Hikmet": "Yaşamak bir ağaç gibi tek ve hürdür, ve bir orman gibi kardeşçesine.",
        "Ahmet Arif": "Hasretinle yandı gönlüm, aşkınla yanarım.",
    }

    if kisi=="random":
        cikti = random.choice(list(sozler.values()))

    else:
        cikti = sozler.get(kisi, "Üzgünüm, bu kişi için bir söz bulamadım.")
    return {"output": cikti}

@app.post("/product")
def product(product: Product):
    product_dict = product.dict()
    product_dict["stock"] = "stokta var" if product.Stock > 0 else "stokta yok"
    return {"message": "Product created successfully", "product": product_dict}

def init_db():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

app = FastAPI()
init_db()



@app.post("/add_product")
def add_product(product: Product):
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, price, stock, category)
        VALUES (?, ?, ?, ?)
    ''', (product.name, product.price, product.Stock, product.category))
    conn.commit()
    conn.close()
    return {"message": "Product added to database successfully", "product": product.dict()}

