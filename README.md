# IS211_finalproject

This is a web application that gives the user the ability to run their own blog.

When first loading the application at the root URL, the user is presented with 
a list of available posts listed in reverse chronological order (newest posts first).

Each blog post has a title, published date, an author, and textual (HTML) content.

The application has a login link, that connects to '/login' and gives the user the 
ability to make changes to the blog entries.

After logging in, the user is sent to the '/dashboard' page.
The dashboard page shows a list of all the posts in a table.
The list just shows the title of the post, with buttons for 'Edit' and 'Delete'.
The edit button sends the user to the 'edit_post' page, and allows the user 
to update the post and title. 
The delete button will delete the post completely from the database.

The dashboard page also has a link that allows the user to add a new post.
The link sends the user to the 'addpost' page, where the user can submit a post
with a title and post content.  
The data will be saved, along with the date and author information, into the database.