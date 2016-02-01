from celery import Celery
from celery_config import BROKER_URL
import moneng_test


app = Celery('celery_config', broker=BROKER_URL)

@app.task(ignore_result=True)
def print_hello():
    print 'hello there'

@app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return results

@app.task()
def create_user():
    moneng_test.connect('tumblelog')
    user = moneng_test.User('paul@technorides.com')
    user.save()
    
    post1 = moneng_test.TextPost(title='Fun with MongoEngine', author=user)
    post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
    post1.tags = ['mongodb', 'mongoengine']
    post1.save()

    #second post, different child class than first
    post2 = moneng_test.LinkPost(title='MongoEngine Documentation', author=user)
    post2.link_url = 'http://docs.mongoengine.com/'
    post2.tags = ['mongoengine']
    post2.save()
    
@app.task()
def delete_posts():
    moneng_test.delete_posts()

# @app.task()
# def print_info():
#     for post in moneng_test.Post.objects:
#         print post.title
#         print '=' * len(post.title)
#         if isinstance(post, moneng_test.TextPost):
#                         print post.content
#         if isinstance(post,moneng_test.LinkPost):
#                         print 'Link:', post.link_url
#         print
#                      
#     num_posts = moneng_test.Post.objects(tags='mongodb').count()
#     print 'Found %d posts with tag "mongodb"' % num_posts
