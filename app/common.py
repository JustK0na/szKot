from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import  random



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:16] 

