
from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import Recipe, User,Comment,Upvote,Downvote
from .forms import RecipeForm, CommentForm, UpvoteForm
from flask.views import View,MethodView
from .. import db 



@main.route('/', methods = ['GET','POST'])
def index():

    '''
    Root page functions that return the home page and its data
    '''
    recipe = Recipe.query.filter_by().first()
    title = 'Recipe'
    mains = Recipe.query.filter_by(category="mains")
    dessert = Recipe.query.filter_by(category ="dessert")
    soups = Recipe.query.filter_by(category ="soups")
    general = Recipe.query.filter_by(category ="general")

    upvotes = Upvote.get_all_upvotes(recipe_id=Recipe.id)
    

    return render_template('home.html', title = title, recipe = recipe, dessert=dessert, mains=mains, soups=soups, general=general, upvotes=upvotes)
    

@main.route('/recipe/new/', methods = ['GET','POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    my_upvotes = Upvote.query.filter_by(recipe_id = Recipe.id)
    if form.validate_on_submit():
        description = form.description.data
        title = form.title.data
        owner_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)
        new_recipe = Recipe(owner_id =current_user._get_current_object().id, title = title,description=description,category=category)
        db.session.add(new_recipe)
        db.session.commit()
        
        
        return redirect(url_for('main.index'))
    return render_template('recipe.html',form=form)



@main.route('/comment/new/<int:recipe_id>', methods = ['GET','POST'])
@login_required
def new_comment(recipe_id):
    form = CommentForm()
    recipe=Recipe.query.get(recipe_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, recipe_id = recipe_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for('.new_comment', recipe_id= recipe_id))

    all_comments = Comment.query.filter_by(recipe_id = recipe_id).all()
    return render_template('comments.html', form = form, comment = all_comments, recipe= recipe )

   
@main.route('/recipe/upvote/<int:recipe_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    user = current_user
    recipe_upvotes = Upvote.query.filter_by(recipe_id= recipe_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.recipe_id==recipe_id).first():
        return  redirect(url_for('main.index'))


    new_upvote = Upvote(recipe_id=recipe_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))


@main.route('/recipe/downvote/<int:recipe_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    user = current_user
    recipe_downvotes = Downvote.query.filter_by(recipe_id= recipe_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.recipe_id==recipe_id).first():
        return  redirect(url_for('main.index'))


    new_downvote = Downvote(recipe_id=recipe_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))