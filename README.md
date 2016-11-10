# Multi User Blog Website

Multi User Blog Website is a website that allows users to sign up,
log in/out, post/comment/like blog posts, and edit/delete posts and comments.

## Table of Contents
- Quick Start
- What's Included
- Creators
- References
- Copyright and License

## Quick Start

Here is a [demo](https://multi-user-blog-145402.appspot.com/)

To start using this repository

>  ```> $ git clone https://github.com/wernerchao/Multi-User-Blog.git```

To run the website locally, you need to have [Google App Engine SDK](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python) installed.
Go to the Multi User Blog folder and deploy by doing the following:

> ```
> $ cd Multi\ \ User\ Blog/
> $ dev_appserver.py .
> ```

## What's Included

Within the download you'll find the following directories and files. 
The main files that you can edit will be:

```
Multi User Blog/
├── static
    ├── main.css
├── templates
    ├── base.html
    ├── blog.html
    ├── comment.html
    ├── deletepost.html
    ├── editpost.html
    ├── login-form.html
    ├── newpost.html
    ├── post.html
    ├── post_page.html
    ├── signup.html
    ├── welcome.html
├── app.yaml
├── templates.py
└── README.md
```

Once you run the website, these files will be generated:

```
Multi User Blog/
├── index.yaml
└── templates.pyc
```

## Creators

**Werner Chao**

- <https://github.com/wernerchao>

## Copyright and License

Code and documentation copyright 2016 the Multi User Blog
Authors and released under the MIT license.

