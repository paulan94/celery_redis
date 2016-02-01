from mongoengine import *
import tasks

#mongoclient, localhost
connect('tumblelog')

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    
class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    #allowing inheritence here for child classes
    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    image_path = StringField()

class LinkPost(Post):
    link_url = StringField()

def delete_posts():
    try:
        for post in Post.objects:
            post.delete()
    except:
        print("Posts do not exist")

if __name__ == '__main__':
                      
    num_posts = Post.objects(tags='mongodb').count()
    print 'Found %d posts with tag "mongodb"' % num_posts
    
    
    
    """too many instances of posts with mongodb"""
    #     #creating a user here with required/nonrequired attributes.
#     paul = User(email='paul@technorides.com')
#     paul.first_name = 'Paul'
#     paul.last_name = 'An'
#     paul.save()
# 
#     #first post
#     post1 = TextPost(title='Fun with MongoEngine', author=paul)
#     post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
#     post1.tags = ['mongodb', 'mongoengine']
#     post1.save()
# 
#     #second post, different child class than first
#     post2 = LinkPost(title='MongoEngine Documentation', author=paul)
#     post2.link_url = 'http://docs.mongoengine.com/'
#     post2.tags = ['mongoengine']
#     post2.save()
