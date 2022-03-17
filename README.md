
<h1> Data collection	and	Storage </h1>
<h2>This is an academic project about DOE + data collection (web-scraping) + data storage </h2>
<h3>Instructions:</h3>
<p>In	order	to	answer	the	main	question,	set	up	a	proper	design	of	experiment, realize	a	
  data	collection	by <strong>web	scraping </strong> and	choose	a	suitable storage	technology  <strong>(MySql)</strong> .</p>
<h3>Set up</h3>
<ol>
  <li>execution.py</li>
  <p>In order to run this file, first you have to run an Sql server and connect whether with CLI or and UI solution (PhpMyAdmin in our case).</p>
   <p>If you use PhpMyAdmin on a Windows machine, check credentials before running .</p>
</ol>

<h3>Récupération des 10 premiers minutes:</h3>
<h2>Ordre SQL à executer:</h2>
<p>SELECT * FROM `Match` WHERE _id = `_id` ORDER BY `_id` ASC LIMIT 10</p>
