
import os
import queue
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from markupsafe import Markup
from models import Posts
from flask_security import login_required
from werkzeug.utils import secure_filename
from forms import PostForm, SearchForm
from app import db

post = Blueprint('post', __name__)

@post.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
	form = PostForm()
	
	if form.validate_on_submit():
		img = request.files['img']
		if img:
			img_name = secure_filename(img.filename)
			img.save(os.path.join('./static/posts', img_name))
		else:
			img_name = None
		post = Posts(title=form.title.data,
		content=form.content.data, 
		img=img_name,
		poster_id=current_user.id)

		db.session.add(post)
		db.session.commit()
		title = form.title.data
		form = PostForm(formdata=None)
		flash(Markup(f"'{title}' Posted!!"))
		return redirect(url_for('post.view_post', id=post.id))
	return render_template("add_post.html", form=form)

@post.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	update_post = Posts.query.get_or_404(id)
	if update_post.poster_id == current_user.id or current_user.has_role('admin'):
		
		form = PostForm()
		form.content.data = update_post.content
		if request.method == 'POST':
			update_post.title = request.form['title']
			update_post.content = request.form['content']
			img = request.files['img']
			check = request.form.get('clear')
			if img.filename != '':
				update_post.img = img_name = secure_filename(img.filename)
				img.save(os.path.join('./static/posts', img_name))
			elif check == 'on':
				update_post.img = None
			try:
				db.session.commit()
				flash("Updated Successfully!")
				return redirect(url_for('post.posts'))
			except Exception as e:
				flash("Error!  Looks like there was a problem...try again!")
				# flash(e)

				return render_template("edit_post.html", 
					form=form,
					post = update_post)
		else:
			return render_template("edit_post.html", 
					form=form,
					post = update_post)
	else:
		return redirect(url_for('post.update_post', id=update_post.id))

		
@post.route('/posts', methods=['GET', 'POST'])
def posts():
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template('posts.html', posts=posts)

@post.route('/posts/<int:id>')
def view_post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)


@post.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)
	id = current_user.id
	if id == post_to_delete.poster.id:
		try:
			db.session.delete(post_to_delete)
			db.session.commit()

			# Return a message
			flash("Blog Post Was Deleted!")

			# Grab all the posts from the database
			return redirect(url_for('post.posts'))


		except:
			# Return an error message
			flash("Whoops! There was a problem deleting post, try again...")

			# Grab all the posts from the database
			return redirect(url_for('post.posts'))
	else:
		# Return a message
		flash("You Aren't Authorized To Delete That Post!")

		# Grab all the posts from the database
		return redirect(url_for('post.posts'))