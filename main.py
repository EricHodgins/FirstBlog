#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2

from google.appengine.ext import db 

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
							   autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))




class MainPage(Handler):
	def render_blog_entries(self):
		blogs = db.GqlQuery("SELECT * from Blog")
		self.render("front.html", blogs=blogs)


	def get(self):
		self.render_blog_entries()


class Newpost(Handler):
	def render_newpost(self, title="", blog_entry="", error=""):
		self.render("newpost.html", title=title, blog_entry=blog_entry, error=error)

	def render_permalink(self, title="", blog_entry=""):
		self.redirect

	def get(self):
		self.render_newpost()

	def post(self):
		title = self.request.get("subject")
		blog_entry = self.request.get("content")
		print title
		print blog_entry

		if title and blog_entry:
			b = Blog(title=title, blog=blog_entry)
			b.put()

			self.redirect("/blog/%s" % b.key().id())
		else:
			error = "Oops, we need both a title and Blog entry."
			self.render_newpost(title=title, blog_entry=blog_entry, error=error)


class Permalink(Handler):
	def get(self, blog_id):
		blogs = db.GqlQuery("SELECT * FROM Blog")
		b = Blog.get_by_id(int(blog_id))


		self.render("permalink.html", title=b.title, blog=b.blog, created=b.created)



class Blog(db.Model):
	title = db.StringProperty(required=True)
	blog = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)

	def render(self):
		input_text = self.blog.replace('\n', '<br>')
		return input_text


app = webapp2.WSGIApplication([
	('/blog', MainPage),
	('/blog/newpost', Newpost),
	('/blog/(\d+)', Permalink)
], debug=True)












