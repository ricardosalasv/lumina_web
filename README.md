<h1>LUMINA</h1>

<h2>Video Demo: <a href=https://youtu.be/DHrjlLXTYMQ>https://youtu.be/DHrjlLXTYMQ</a></h2>
<br>
<h2>Lumina is a project which is intended to calculate how many lighting fixtures are needed in a room based on its physical characteristics, its use or the activities that will be performed there, and also based on the characteristics of the chosen type of light.</h2>
<br>
<h2>This tool is intended to help the architectural or lighting designer, therefore, a lot of the terms are to be understood by an architectural professional that is able to judge the design problem and determine the best parameters based on the design's requirements.</h2>
<br>
<h2>The user will be able of specifying the dimensions of the space, the characteristics of the materials and finishes on the floor, wall, and ceiling/roof, and then choose a lighting fixture from the app database with its real specifications.</h2>
<br>
<h2>I tried to expand my knowledge a bit more further the Flask lesson, that is the reason I used SQLAlchemy in this project, which is a library that allows to interact with the SQL database with an Object Oriented Programming approach. This helped me a lot, as I needed to spend some time to take the Database to the Third Normal Form, and once that done, SQLAlchemy made it pretty easy to make queries and updates to the Database itself in all the places of the code where it was referenced.</h2>
<br>
<h2>Also, this project was a great exercise to practice AJAX and jQuery in order to connect functionalities between the front-end and the back-end, as I wanted to make the Project Page as dynamic and reactive as possible inside of the knowledge I have in the moment. For the next project I expect to explore and learn more about Django and React.</h2>
<br>
<h2>In matter of the front-end, this was a great opportunity to practice Bootstrap in order to get the page to look exactly as I wanted. Combining it with some JS scripts allowed me to give the front-end with the aspect and interactivity that I exactly wanted.</h2>
<br>
<h2>This was a very iterative process, I used some reinforcement knowledge that I learnt from other courses which helped me to understand even more how a lot of web processes work, and also test different ideas and implementations of those ideas, it was definitely a sandbox for me. Also, I have to remark that before finishing this course I was able of finding a great job as a developer for the AEC industry, which allowed me to see with a new perspective this final project as I started it about 10 months ago and that I was able of finishing it now.</h2>
<br>
<h1>Files descriptions</h1>
<ul>
    <h2>
        <li>
            <strong>run.py:</strong> Is the file from where everything is run. To start the server just execute "python run.py" from your command line and the Flask server will be started. It will run in Debug mode
        </li>
        <li>
            <strong>databaseManipulation.py:</strong> This is an utility script I created to populate the database with default data in order to save time each time I needed to recreate the database when testing.
        </li>
        <li>
            <strong>DBPopulationData.py:</strong> This file contains the data that is read by databaseManipulation.py and then written to the database
        </li>
        <li>
            <strong>Lumina package (__init__.py):</strong> Contains the initialization of the Flask app, the SQLAlchemy database object, login managers, and Bcrypt
        </li>
        <li>
            <strong>forms.py:</strong> Contains the classes of all the forms used in the project, created with WTForms
        </li>
        <li>
            <strong>routes.py:</strong> Contains all the routes and relevant backend procedures.
        </li>
        <li>
            <strong>helpers.py:</strong> Contains helper functions used throughout the project.
        </li>
        <li>
            <strong>models.py:</strong> Contains the SQLAlchemy models representing each table in the SQL Database.
        </li>
        <li>
            <strong>utilizationFactorTables.py:</strong> It is part of the lighting calculation, it is a table used to get a value which is relevant on this calculation based on the room's and lighting specifications.
        </li>
        <li>
            <strong>lumina_db.db:</strong> The SQL database.
        </li>
        <li>
            <strong>project.js:</strong> Front-end procedures for the /project page.
        </li>
        <li>
            <strong>loadProject.js:</strong> Front-end procedures for the /loadProject page.
        </li>
        <li>
            <strong>heightFiller.js and heightFiller_ProjectPage:</strong> Helper jQuery scripts to assist the styling of the pages.
        </li>
        <li>
            <strong>Branding, Color Palette, and icons folders:</strong> Folders containing relevant graphics for the project.
        </li>
        <li>
            <strong>Bootstrap folder:</strong> Bootstrap library.
        </li>
    </h2>
</ul>
<hr>
<br>
<h2>In summary, this was a great exercise to practice everything, DB creation and manipulation, UI/UX Design, folder structure, Python, JS, AJAX, jQuery, Bootstrap. Definitely it has been a great experience.</h2>
<br>
<h2>Now, I intend to continue learning and taking the CS50w course, learn about Django, React.js, three.js (in order to complement my knowledge in 3D and Rendering), and Tailwind is in my sight as well, I would like to start experimenting with it.</h2>

<hr>
<span>This app is the final project of <a href=https://cs50.harvard.edu/x/2021> CS50x </a> from <a href=ricardosalasv.com>Ricardo Salas</a></span>