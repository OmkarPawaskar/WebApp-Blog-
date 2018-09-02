from database import Database
from menu import Menu

Database.initialize()

menu = Menu()
menu.run_menu()




















#post = Post(
    #blog_id ="123",
    #title = "Another great post",
    #content = "This is some sample content",
    #author = "Jose"
#)

#post.save_to_mongo()
#posts = Post.from_blog('123')
#for post in posts:
#    print(post)
