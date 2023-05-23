# import requests
from Post import Post


# URL = f"https://api.npoint.io/c790b4d5cab58020d391"
# URL = f"https://api.npoint.io/4ac9c32a945d3983ac66"


class Blog:
    all_post = []

    def __init__(self):
        # self.getAllPost()
        pass

    def getAllPost(self, Model):
        # response = requests.get(URL)
        self.all_post = Model.query.all()

    def getPost(self, BlogPost, id):
        # postData = self.all_post[int(id) - 1]
        postData = BlogPost.query.get(id)
        print(postData)
        return Post(
            post_id=int(id),
            title=postData.get("title"),
            subtitle=postData.get("subtitle"),
            body=postData.get("body"),
            image_url=postData.get("image"),
        )
