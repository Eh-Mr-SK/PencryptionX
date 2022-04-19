"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from Module import app
from flask import request
import random
import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from flask import send_file


def encrypt(file):
    fo = open(file, "rb")
    image=fo.read()
    fo.close()
    image=bytearray(image)
    key=random.randint(0,256)
    for index , value in enumerate(image):
	    image[index] = value^key
    fo=open("enc.jpg","wb")
    imageRes="enc.jpg"
    fo.write(image)
    fo.close()
    return (key,imageRes)

def decrypt(key,file):
    fo = open(file, "rb")
    image=fo.read()
    fo.close()
    image=bytearray(image)
    for index , value in enumerate(image):
	    image[index] = value^key
    fo=open("dec.jpg","wb")
    imageRes="dec.jpg"
    fo.write(image)
    fo.close()
    return imageRes


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/decryption')
def decryption():
    """Renders the decryption page."""
    return render_template(
        'decryption.html',
        title='Decrypt',
        year=datetime.now().year,
        message='Upload your encrypted image along with the key'
    )

@app.route('/encryption')
def encryption():
    """Renders the encryption page."""
    return render_template(
        'encryption.html',
        title='Encrypt',
        year=datetime.now().year,
        message='Upload the image here'
    )

@app.route('/decryption1', methods = ['POST'])  
def decryption1():  
    if request.method == 'POST':  
        global f
        f = request.files['file']  
        f.save(f.filename)  
        text = request.form['key']
        key=int(text)
        image=decrypt(key,f.filename)
        return render_template('decryption1.html',
        title='Decrypted',
        year=datetime.now().year,
        message='This is your Decrypted image', name = f.filename) 

@app.route('/encryption1', methods = ['POST'])  
def encryption1():  
    if request.method == 'POST':  
        global f
        f = request.files['file']  
        f.save(f.filename)  
        key,image=encrypt(f.filename)
        return render_template('encryption1.html',
        title='Encrypted',
        year=datetime.now().year,
        message='This is your encrypted image', name = f.filename,keys=key,images=image)

@app.route('/return-file')
def return_file():
    return send_file("../enc.jpg",attachment_filename="enc.jpg")

@app.route('/return-file1')
def return_file1():
    return send_file("../dec.jpg",attachment_filename="dec.jpg")